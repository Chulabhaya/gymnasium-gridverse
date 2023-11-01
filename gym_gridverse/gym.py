from __future__ import annotations

import time
from functools import partial
from typing import Callable, Dict, List, Optional

import gymnasium as gym
import numpy as np
import pkg_resources

from gym_gridverse.envs.yaml.factory import factory_env_from_yaml
from gym_gridverse.outer_env import OuterEnv
from gym_gridverse.representations.observation_representations import (
    make_observation_representation,
)
from gym_gridverse.representations.spaces import Space, SpaceType
from gym_gridverse.representations.state_representations import (
    make_state_representation,
)

import pygame
from gym_gridverse.rendering_gv_objects import *
from gym_gridverse.grid_object import (
    Beacon,
    Color,
    Door,
    Exit,
    Floor,
    GridObject,
    Hidden,
    Key,
    MovingObstacle,
    Telepod,
    Wall,
)
from gym_gridverse.geometry import Orientation

orientation_as_degrees = {
    Orientation.F: 0,
    Orientation.L: 270,
    Orientation.B: 180,
    Orientation.R: 90,
}


NONE = (191, 182, 168)
RED = (204, 78, 92)
GREEN = (147, 190, 139)
BLUE = (135, 206, 235)
YELLOW = (255, 235, 138)
ORANGE = (255, 179, 102)
PURPLE = (180, 160, 200)


colormap = {
    Color.NONE: NONE,
    Color.RED: RED,
    Color.GREEN: GREEN,
    Color.BLUE: BLUE,
    Color.YELLOW: YELLOW,
    Color.ORANGE: ORANGE,
    Color.PURPLE: PURPLE,
}


def outer_space_to_gym_space(space: Dict[str, Space]) -> gym.spaces.Space:
    return gym.spaces.Dict(
        {
            k: gym.spaces.Box(
                low=v.lower_bound,
                high=v.upper_bound,
                dtype=float if v.space_type is SpaceType.CONTINUOUS else int,
            )
            for k, v in space.items()
        }
    )


class GymEnvironment(gym.Env):
    metadata = {
        "render_modes": [
            "human_state",
            "human_observation",
            "rgb_array_state",
            "rgb_array_observation",
        ],
        "render_fps": 50,
    }

    # NOTE accepting an environment instance as input is a bad idea because it
    # would need to be instantiated during gym registration
    def __init__(self, outer_env: OuterEnv, render_mode: Optional[str] = None):
        super().__init__()

        self.outer_env = outer_env

        # Environment state space, if any.
        self.state_space = (
            outer_space_to_gym_space(outer_env.state_representation.space)
            if outer_env.state_representation is not None
            else None
        )

        # Environment action space.
        self.action_space = gym.spaces.Discrete(
            outer_env.action_space.num_actions
        )

        # Environment observation space, if any.
        self.observation_space = (
            outer_space_to_gym_space(outer_env.observation_representation.space)
            if outer_env.observation_representation is not None
            else None
        )

        # Set up rendering details.
        assert (
            render_mode is None or render_mode in self.metadata["render_modes"]
        )
        self.render_mode = render_mode
        self.window_scaling = (
            50  # Multiplier for converting state/obs grids to pixels
        )

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def set_state_representation(self, name: str):
        """Changes the state representation."""
        # TODO: test
        self.outer_env.state_representation = make_state_representation(
            name, self.outer_env.inner_env.state_space
        )
        self.state_space = outer_space_to_gym_space(
            self.outer_env.state_representation.space
        )

    def set_observation_representation(self, name: str):
        """Changes the observation representation."""
        # TODO: test
        self.outer_env.observation_representation = (
            make_observation_representation(
                name, self.outer_env.inner_env.observation_space
            )
        )
        self.observation_space = outer_space_to_gym_space(
            self.outer_env.observation_representation.space
        )

    @property
    def state(self) -> Dict[str, np.ndarray]:
        """Returns the representation of the current state."""
        return self.outer_env.state

    @property
    def observation(self) -> Dict[str, np.ndarray]:
        """Returns the representation of the current observation."""
        return self.outer_env.observation

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        """Resets the state of the environment.

        Returns:
            Dict[str, numpy.ndarray]: initial observation
        """
        # Pass this seed as "None" because we generate our
        # own random generator within inner env
        super().reset(seed=None)

        # Actually seed the environment through inner env
        self.outer_env.inner_env.set_seed(seed)

        self.outer_env.reset()

        if (
            self.render_mode == "human_state"
            or self.render_mode == "human_observation"
        ):
            self._render_frame()
        return self.observation, {}

    def step(self, action: int):
        """Runs the environment dynamics for one timestep.

        Args:
            action (int): agent's action

        Returns:
            Tuple[Dict[str, numpy.ndarray], float, bool, bool, Dict]: (observation, reward, terminated, truncated, info dictionary)
        """
        action_ = self.outer_env.action_space.int_to_action(action)
        reward, terminated = self.outer_env.step(action_)

        if (
            self.render_mode == "human_state"
            or self.render_mode == "human_observation"
        ):
            self._render_frame()
        return self.observation, reward, terminated, False, {}

    def render(self):
        if (
            self.render_mode == "rgb_array_state"
            or self.render_mode == "rgb_array_observation"
        ):
            return self._render_frame()

    def _render_frame(self):
        # Not reset yet
        if self.outer_env.inner_env.state is None:
            return

        # Initialize PyGame and clock
        if self.window is None and (
            self.render_mode == "human_state"
            or self.render_mode == "human_observation"
        ):
            pygame.init()
            pygame.display.init()
        if self.clock is None and (
            self.render_mode == "human_state"
            or self.render_mode == "human_observation"
        ):
            self.clock = pygame.time.Clock()

        # Get grid shape and state/observation depending on state or observation rendering
        if (
            self.render_mode == "human_state"
            or self.render_mode == "rgb_array_state"
        ):
            grid_shape = self.outer_env.inner_env.state_space.grid_shape
            state_or_observation = self.outer_env.inner_env.state
        elif (
            self.render_mode == "human_observation"
            or self.render_mode == "rgb_array_observation"
        ):
            grid_shape = self.outer_env.inner_env.observation_space.grid_shape
            state_or_observation = self.outer_env.inner_env.observation
        else:
            raise ValueError('Render mode not recognized!')

        # Do the rendering
        grid_height = grid_shape.height
        grid_width = grid_shape.width
        window_height = grid_height * self.window_scaling
        window_width = grid_width * self.window_scaling
        if (
            self.render_mode == "human_state"
            or self.render_mode == "human_observation"
        ):
            self.window = pygame.display.set_mode((window_width, window_height))

        # Render state or observation
        canvas = pygame.Surface((window_width, window_height))
        canvas.fill((255, 255, 255))
        for position in state_or_observation.grid.area.positions():
            obj = state_or_observation.grid[position]
            # Modify y position because pyglet (0, 0) is bottom left,
            # while GV (0, 0) is top left
            obj_position = (position.x, position.y)

            if isinstance(obj, Floor):
                create_floor(canvas, obj_position, self.window_scaling)

            elif isinstance(obj, Hidden):
                create_hidden(canvas, obj_position, self.window_scaling)

            elif isinstance(obj, Wall):
                create_wall(canvas, obj_position, self.window_scaling)

            elif isinstance(obj, Key):
                create_key(canvas, obj_position, self.window_scaling)

            elif isinstance(obj, Door):
                if obj.is_open:
                    create_door_open(canvas, obj_position, self.window_scaling)
                elif obj.is_locked:
                    create_door_closed_locked(
                        canvas, obj_position, self.window_scaling
                    )
                else:
                    create_door_closed_unlocked(
                        canvas, obj_position, self.window_scaling
                    )

            elif isinstance(obj, Exit):
                color = colormap[obj.color]
                create_exit(canvas, obj_position, self.window_scaling, color)

            elif isinstance(obj, MovingObstacle):
                create_moving_obstacle(
                    canvas, obj_position, self.window_scaling
                )

            elif isinstance(obj, Telepod):
                create_portal(canvas, obj_position, self.window_scaling)

            elif isinstance(obj, Beacon):
                color = colormap[obj.color]
                create_beacon(canvas, obj_position, self.window_scaling, color)
            else:
                create_unknown(canvas, obj_position, self.window_scaling)

        # Draw agent
        agent = state_or_observation.agent
        agent_position = (agent.position.x, agent.position.y)
        agent_orientation = orientation_as_degrees[agent.orientation]
        create_agent(
            canvas,
            agent_position,
            agent_orientation,
            (1, 1),
            self.window_scaling,
        )

        # Draw grid
        create_grid(canvas, (grid_width, grid_height), self.window_scaling)

        if (
            self.render_mode == "human_state"
            or self.render_mode == "human_observation"
        ):
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


class GymStateWrapper(gym.Wrapper):
    """
    Gym Wrapper to replace the standard observation representation with state instead.

    Doesn't change underlying environment, won't change render
    """

    def __init__(self, env: GymEnvironment):
        # Make sure we have a valid state representation
        if env.state_space is None:
            ValueError('GymEnvironment does not have a state space')

        super().__init__(env)
        self.observation_space = env.state_space

    @property
    def observation(self) -> Dict[str, np.ndarray]:
        return self.env.state

    def reset(self, **kwargs) -> Dict[str, np.ndarray]:
        """reset the environment state

        Returns:
            Dict[str, numpy.ndarray]: initial state
        """
        observation, info = self.env.reset(**kwargs)
        info['observation'] = observation

        return self.observation, info

    def step(self, action: int):
        """performs environment step

        Args:
            action (int): agent's action

        Returns:
            Tuple[Dict[str, numpy.ndarray], float, bool, bool, Dict]: (state, reward, terminated, truncated, info dictionary)
        """
        observation, reward, terminated, truncated, info = self.env.step(action)
        info['observation'] = observation

        return self.observation, reward, terminated, truncated, info


STRING_TO_YAML_FILE: Dict[str, str] = {
    "GV-Crossing-5x5-v0": "gv_crossing.5x5.yaml",
    "GV-Crossing-7x7-v0": "gv_crossing.7x7.yaml",
    "GV-DynamicObstacles-5x5-v0": "gv_dynamic_obstacles.5x5.yaml",
    "GV-DynamicObstacles-7x7-v0": "gv_dynamic_obstacles.7x7.yaml",
    "GV-Empty-4x4-v0": "gv_empty.4x4.yaml",
    "GV-Empty-8x8-v0": "gv_empty.8x8.yaml",
    "GV-FourRooms-7x7-v0": "gv_four_rooms.7x7.yaml",
    "GV-FourRooms-9x9-v0": "gv_four_rooms.9x9.yaml",
    "GV-Keydoor-5x5-v0": "gv_keydoor.5x5.yaml",
    "GV-Keydoor-7x7-v0": "gv_keydoor.7x7.yaml",
    "GV-Keydoor-9x9-v0": "gv_keydoor.9x9.yaml",
    "GV-Memory-5x5-v0": "gv_memory.5x5.yaml",
    "GV-Memory-9x9-v0": "gv_memory.9x9.yaml",
    "GV-MemoryFourRooms-7x7-v0": "gv_memory_four_rooms.7x7.yaml",
    "GV-MemoryFourRooms-9x9-v0": "gv_memory_four_rooms.9x9.yaml",
    "GV-MemoryNineRooms-10x10-v0": "gv_memory_nine_rooms.10x10.yaml",
    "GV-MemoryNineRooms-13x13-v0": "gv_memory_nine_rooms.13x13.yaml",
    "GV-NineRooms-10x10-v0": "gv_nine_rooms.10x10.yaml",
    "GV-NineRooms-13x13-v0": "gv_nine_rooms.13x13.yaml",
    "GV-Teleport-5x5-v0": "gv_teleport.5x5.yaml",
    "GV-Teleport-7x7-v0": "gv_teleport.7x7.yaml",
}

OuterEnvFactory = Callable[[], OuterEnv]


def from_factory(factory: OuterEnvFactory, render_mode: Optional[str] = None):
    return GymEnvironment(factory(), render_mode)


# This is added for compatibility with the gymnasium.make function
from_factory.metadata = GymEnvironment.metadata


def outer_env_factory(yaml_filename: str) -> OuterEnv:
    env = factory_env_from_yaml(yaml_filename)
    observation_representation = make_observation_representation(
        'default', env.observation_space
    )
    return OuterEnv(
        env,
        observation_representation=observation_representation,
    )


for key, yaml_filename in STRING_TO_YAML_FILE.items():
    yaml_filepath = pkg_resources.resource_filename(
        'gym_gridverse', f'registered_envs/{yaml_filename}'
    )
    factory = partial(outer_env_factory, yaml_filepath)

    # registering using factory to avoid allocation of outer envs
    gym.register(
        key,
        entry_point='gym_gridverse.gym:from_factory',
        kwargs={'factory': factory},
    )

env_ids = list(STRING_TO_YAML_FILE.keys())
