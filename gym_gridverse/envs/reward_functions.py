from collections import deque
from functools import lru_cache, partial
from typing import Callable, Iterator, List, Sequence, Tuple, Type

import more_itertools as mitt
import numpy as np

from gym_gridverse.action import Action
from gym_gridverse.envs.utils import updated_agent_position_if_unobstructed
from gym_gridverse.geometry import DistanceFunction, Position
from gym_gridverse.grid_object import (
    Beacon,
    Door,
    Exit,
    GridObject,
    MovingObstacle,
    Wall,
)
from gym_gridverse.state import State
from gym_gridverse.utils.functions import (
    checkraise_kwargs,
    get_custom_function,
    is_custom_function,
    select_kwargs,
)

RewardFunction = Callable[[State, Action, State], float]
"""Signature that all reward functions must follow"""

RewardReductionFunction = Callable[[Iterator[float]], float]
"""Signature for a float reduction function"""


def reduce(
    state: State,
    action: Action,
    next_state: State,
    *,
    reward_functions: Sequence[RewardFunction],
    reduction: RewardReductionFunction,
) -> float:
    """reduction of multiple reward functions into a single boolean value

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        reward_functions (`Sequence[RewardFunction]`):
        reduction (`RewardReductionFunction`):

    Returns:
        bool: reduction operator over the input reward functions
    """
    # TODO: test

    return reduction(
        reward_function(state, action, next_state)
        for reward_function in reward_functions
    )


def reduce_sum(
    state: State,
    action: Action,
    next_state: State,
    *,
    reward_functions: Sequence[RewardFunction],
) -> float:
    """utility reward function which sums other reward functions

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        reward_functions (`Sequence[RewardFunction]`):

    Returns:
        float: sum of the evaluated input reward functions
    """
    # TODO: test
    return reduce(
        state,
        action,
        next_state,
        reward_functions=reward_functions,
        reduction=sum,
    )


def overlap(
    state: State,  # pylint: disable=unused-argument
    action: Action,  # pylint: disable=unused-argument
    next_state: State,
    *,
    object_type: Type[GridObject],
    reward_on: float = 1.0,
    reward_off: float = 0.0,
) -> float:
    """reward for the agent occupying the same position as another object

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        object_type (`Type[GridObject]`):
        reward_on (`float`): reward for when agent is on the object
        reward_off (`float`): reward for when agent is not on the object

    Returns:
        float: one of the two input rewards
    """
    return (
        reward_on
        if isinstance(next_state.grid[next_state.agent.position], object_type)
        else reward_off
    )


def living_reward(
    state: State,  # pylint: disable=unused-argument
    action: Action,  # pylint: disable=unused-argument
    next_state: State,  # pylint: disable=unused-argument
    *,
    reward: float = -1.0,
) -> float:
    """a living reward which does not depend on states or actions

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        reward (`float`): reward for when agent is on exit

    Returns:
        float: the input reward
    """
    return reward


def reach_exit(
    state: State,
    action: Action,
    next_state: State,
    *,
    reward_on: float = 1.0,
    reward_off: float = 0.0,
) -> float:
    """reward for the Agent being on a Exit

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        reward_on (`float`): reward for when agent is on exit
        reward_off (`float`): reward for when agent is not on exit

    Returns:
        float: one of the two input rewards
    """
    return overlap(
        state,
        action,
        next_state,
        object_type=Exit,
        reward_on=reward_on,
        reward_off=reward_off,
    )


def bump_moving_obstacle(
    state: State, action: Action, next_state: State, *, reward: float = -1.0
) -> float:
    """reward for the Agent bumping into on a MovingObstacle

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        reward (`float`): reward for when Agent bumps a MovingObstacle

    Returns:
        float: the input reward or 0.0
    """
    return overlap(
        state,
        action,
        next_state,
        object_type=MovingObstacle,
        reward_on=reward,
        reward_off=0.0,
    )


def proportional_to_distance(
    state: State,  # pylint: disable=unused-argument
    action: Action,  # pylint: disable=unused-argument
    next_state: State,
    *,
    distance_function: DistanceFunction = Position.manhattan_distance,
    object_type: Type[GridObject],
    reward_per_unit_distance: float = -1.0,
) -> float:
    """reward proportional to distance to object

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        distance_function (`DistanceFunction`):
        object_type: (`Type[GridObject]`): type of unique object in grid
        reward (`float`): reward per unit distance

    Returns:
        float: input reward times distance to object
    """

    object_position = mitt.one(
        position
        for position in next_state.grid.positions()
        if isinstance(next_state.grid[position], object_type)
    )
    distance = distance_function(next_state.agent.position, object_position)
    return reward_per_unit_distance * distance


def getting_closer(
    state: State,
    action: Action,  # pylint: disable=unused-argument
    next_state: State,
    *,
    distance_function: DistanceFunction = Position.manhattan_distance,
    object_type: Type[GridObject],
    reward_closer: float = 1.0,
    reward_further: float = -1.0,
) -> float:
    """reward for getting closer or further to object

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        distance_function (`DistanceFunction`):
        object_type: (`Type[GridObject]`): type of unique object in grid
        reward_closer (`float`): reward for when agent gets closer to object
        reward_further (`float`): reward for when agent gets further to object

    Returns:
        float: one of the input rewards, or 0.0 if distance has not changed
    """

    def _distance_agent_object(state):
        object_position = mitt.one(
            position
            for position in state.grid.positions()
            if isinstance(state.grid[position], object_type)
        )
        return distance_function(state.agent.position, object_position)

    distance_prev = _distance_agent_object(state)
    distance_next = _distance_agent_object(next_state)

    return (
        reward_closer
        if distance_next < distance_prev
        else reward_further
        if distance_next > distance_prev
        else 0.0
    )


@lru_cache(maxsize=10)
def dijkstra(
    layout: Tuple[Tuple[bool]], source_position: Tuple[int, int]
) -> np.ndarray:
    layout_array = np.array(layout)

    visited = np.zeros(layout_array.shape, dtype=bool)
    visited[source_position] = True
    distances = np.full(layout_array.shape, float('inf'))
    distances[source_position] = 0.0

    frontier = deque([source_position])
    while frontier:
        y_old, x_old = frontier.popleft()

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            y_new = y_old + dy
            x_new = x_old + dx

            if (
                0 <= y_new < layout_array.shape[0]
                and 0 <= x_new < layout_array.shape[1]
                and layout_array[y_new, x_new]
                and not visited[y_new, x_new]
            ):
                distances[y_new, x_new] = distances[y_old, x_old] + 1
                visited[y_new, x_new] = True
                frontier.append((y_new, x_new))

    return distances


def getting_closer_shortest_path(
    state: State,
    action: Action,  # pylint: disable=unused-argument
    next_state: State,
    *,
    object_type: Type[GridObject],
    reward_closer: float = 1.0,
    reward_further: float = -1.0,
) -> float:
    """reward for getting closer or further to object, *assuming normal navigation dynamics*

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        object_type: (`Type[GridObject]`): type of unique object in grid
        reward_closer (`float`): reward for when agent gets closer to object
        reward_further (`float`): reward for when agent gets further to object

    Returns:
        float: one of the input rewards, or 0.0 if distance has not changed
    """

    def _distance_agent_object(state):
        object_position = mitt.one(
            position
            for position in state.grid.positions()
            if isinstance(state.grid[position], object_type)
        )

        layout = tuple(
            tuple(not state.grid[y, x].blocks for x in range(state.grid.width))
            for y in range(state.grid.height)
        )
        distance_array = dijkstra(layout, object_position.astuple())
        return distance_array[state.agent.position.astuple()]

    distance_prev = _distance_agent_object(state)
    distance_next = _distance_agent_object(next_state)

    return (
        reward_closer
        if distance_next < distance_prev
        else reward_further
        if distance_next > distance_prev
        else 0.0
    )


def bump_into_wall(
    state: State,
    action: Action,
    next_state: State,  # pylint: disable=unused-argument
    *,
    reward: float = -1.0,
):
    """Returns `reward` when bumping into wall, otherwise 0

    Bumping is tested by seeing whether the intended move would end up with the
    agent on a wall.

    Args:
        state (State):
        action (Action):
        next_state (State):
        reward (float): (optional) The reward to provide if bumping into wall
    """

    attempted_next_position = updated_agent_position_if_unobstructed(
        state.agent.position, state.agent.orientation, action
    )

    return (
        reward
        if attempted_next_position in state.grid
        and isinstance(state.grid[attempted_next_position], Wall)
        else 0.0
    )


def actuate_door(
    state: State,
    action: Action,
    next_state: State,
    *,
    reward_open: float = 1.0,
    reward_close: float = -1.0,
):
    """Returns `reward_open` when opening and `reward_close` when closing door.

    Opening/closing is checked by making sure the actuate action is performed,
    and checking the status of the door in front of the agent.

    Args:
        state (State):
        action (Action):
        next_state (State):
        reward_open (float): (optional) The reward to provide if opening a door
        reward_close (float): (optional) The reward to provide if closing a door
    """

    if action is not Action.ACTUATE:
        return 0.0

    position = state.agent.position_in_front()

    door = state.grid[position]
    if not isinstance(door, Door):
        return 0.0

    # assumes same door
    next_door = next_state.grid[position]
    if not isinstance(next_door, Door):
        return 0.0

    return (
        reward_open
        if not door.is_open and next_door.is_open
        else reward_close
        if door.is_open and not next_door.is_open
        else 0.0
    )


def pickndrop(
    state: State,
    action: Action,  # pylint: disable=unused-argument
    next_state: State,
    *,
    object_type: Type[GridObject],
    reward_pick: float = 1.0,
    reward_drop: float = -1.0,
):
    """Returns `reward_pick` / `reward_drop` when an object is picked / dropped.

    Picking/dropping is checked by the agent's object, and not the action.

    Args:
        state (State):
        action (Action):
        next_state (State):
        reward_pick (float): (optional) The reward to provide if picking a key
        reward_drop (float): (optional) The reward to provide if dropping a key
    """

    has_key = isinstance(state.agent.obj, object_type)
    next_has_key = isinstance(next_state.agent.obj, object_type)

    return (
        reward_pick
        if not has_key and next_has_key
        else reward_drop
        if has_key and not next_has_key
        else 0.0
    )


def reach_exit_memory(
    state: State,  # pylint: disable=unused-argument
    action: Action,  # pylint: disable=unused-argument
    next_state: State,
    *,
    reward_good: float = 1.0,
    reward_bad: float = -1.0,
) -> float:
    """reward for the Agent being on a Exit

    Args:
        state (`State`):
        action (`Action`):
        next_state (`State`):
        reward_good (`float`): reward for when agent is on the good exit
        reward_bad (`float`): reward for when agent is on the bad exit

    Returns:
        float: one of the two input rewards
    """
    # TODO: test

    agent_grid_object = next_state.grid[next_state.agent.position]
    grid_objects = (
        next_state.grid[position] for position in next_state.grid.positions()
    )
    beacon_color = next(
        grid_object.color
        for grid_object in grid_objects
        if isinstance(grid_object, Beacon)
    )

    return (
        (reward_good if agent_grid_object.color is beacon_color else reward_bad)
        if isinstance(agent_grid_object, Exit)
        else 0.0
    )


def factory(name: str, **kwargs) -> RewardFunction:

    required_keys: List[str]
    optional_keys: List[str]

    if name == 'reduce':
        required_keys = ['reward_functions', 'reduction']
        optional_keys = []
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(reduce, **kwargs)

    if name == 'reduce_sum':
        required_keys = ['reward_functions']
        optional_keys = []
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(reduce_sum, **kwargs)

    if name == 'overlap':
        required_keys = ['object_type']
        optional_keys = ['reward_on', 'reward_off']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(overlap, **kwargs)

    if name == 'living_reward':
        required_keys = []
        optional_keys = ['reward']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(living_reward, **kwargs)

    if name == 'reach_exit':
        required_keys = []
        optional_keys = ['reward_on', 'reward_off']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(reach_exit, **kwargs)

    if name == 'bump_moving_obstacle':
        required_keys = []
        optional_keys = ['reward']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(bump_moving_obstacle, **kwargs)

    if name == 'proportional_to_distance':
        required_keys = ['object_type']
        optional_keys = ['distance_function', 'reward_per_unit_distance']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(proportional_to_distance, **kwargs)

    if name == 'getting_closer':
        required_keys = ['object_type']
        optional_keys = ['distance_function', 'reward_closer', 'reward_further']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(getting_closer, **kwargs)

    if name == 'getting_closer_shortest_path':
        required_keys = ['object_type']
        optional_keys = ['reward_closer', 'reward_further']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(getting_closer_shortest_path, **kwargs)

    if name == 'bump_into_wall':
        required_keys = []
        optional_keys = ['reward']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(bump_into_wall, **kwargs)

    if name == 'actuate_door':
        required_keys = []
        optional_keys = ['reward_open', 'reward_close']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(actuate_door, **kwargs)

    if name == 'pickndrop':
        required_keys = ['object_type']
        optional_keys = ['reward_pick', 'reward_drop']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(pickndrop, **kwargs)

    if name == 'reach_exit_memory':
        required_keys = []
        optional_keys = ['reward_good', 'reward_bad']
        checkraise_kwargs(kwargs, required_keys)
        kwargs = select_kwargs(kwargs, required_keys + optional_keys)
        return partial(reach_exit_memory, **kwargs)

    if is_custom_function(name):
        function = get_custom_function(name)
        return partial(function, **kwargs)

    raise ValueError(f'invalid reward function name {name}')
