from typing import Optional

import gymnasium as gym
import numpy as np
import pytest

from gym_gridverse.gym import GymStateWrapper


@pytest.mark.parametrize(
    'env_id',
    [
        "GV-Crossing-5x5-v0",
        "GV-Crossing-7x7-v0",
        "GV-DynamicObstacles-5x5-v0",
        "GV-DynamicObstacles-7x7-v0",
        "GV-Empty-4x4-v0",
        "GV-Empty-8x8-v0",
        "GV-FourRooms-7x7-v0",
        "GV-FourRooms-9x9-v0",
        "GV-Keydoor-5x5-v0",
        "GV-Keydoor-7x7-v0",
        "GV-Keydoor-9x9-v0",
        "GV-Memory-5x5-v0",
        "GV-Memory-9x9-v0",
        "GV-MemoryFourRooms-7x7-v0",
        "GV-MemoryFourRooms-9x9-v0",
        "GV-MemoryNineRooms-10x10-v0",
        "GV-MemoryNineRooms-13x13-v0",
        "GV-NineRooms-10x10-v0",
        "GV-NineRooms-13x13-v0",
        "GV-Teleport-5x5-v0",
        "GV-Teleport-7x7-v0",
    ],
)
def test_gym_registration(env_id: str):
    gym.make(env_id)


@pytest.mark.parametrize(
    'env_id',
    [
        "GV-Empty-4x4-v0",
        "GV-Empty-8x8-v0",
        "GV-DynamicObstacles-5x5-v0",
        "GV-DynamicObstacles-7x7-v0",
    ],
)
@pytest.mark.parametrize('seed', [1, 10, 1337, 0xDEADBEEF])
def test_gym_seed(env_id: str, seed: Optional[int]):
    env = gym.make("CartPole-v0")
    env = gym.wrappers.RecordEpisodeStatistics(env)

    episode_returns1 = []
    episode_count = 0
    obs, info = env.reset(seed=seed)
    env.action_space.seed(seed=seed)
    while episode_count < 5:
        action = env.action_space.sample()
        _, _, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            episode_count += 1
            episode_returns1.append(info['episode']['r'][0])
            obs, info = env.reset()

    episode_returns2 = []
    episode_count = 0
    obs, info = env.reset(seed=seed)
    env.action_space.seed(seed=seed)
    while episode_count < 5:
        action = env.action_space.sample()
        _, _, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            episode_count += 1
            episode_returns2.append(info['episode']['r'][0])
            obs, info = env.reset()

    np.testing.assert_equal(episode_returns1, episode_returns2)


def test_gym_control_loop():
    env = gym.make('GV-Empty-4x4-v0')

    env.reset()
    for _ in range(10):
        action = env.action_space.sample()
        _, _, terminated, truncated, _ = env.step(action)

        if terminated or truncated:
            env.reset()


@pytest.mark.parametrize('env_id', ['GV-Empty-4x4-v0', 'GV-Keydoor-9x9-v0'])
@pytest.mark.parametrize('representation', ['default', 'no-overlap'])
def test_gym_state_wrapper(env_id: str, representation: str):
    env = gym.make(env_id)
    env.set_state_representation(representation)
    env = GymStateWrapper(env)

    np.testing.assert_equal(env.observation_space, env.unwrapped.state_space)

    observation, info = env.reset()
    np.testing.assert_equal(observation, env.unwrapped.state)
    for _ in range(10):
        action = env.action_space.sample()
        observation, _, terminated, truncated, _ = env.step(action)
        np.testing.assert_equal(observation, env.unwrapped.state)

        if terminated or truncated:
            env.reset()
