import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id="2048-v0", entry_point="game_gym.envs:GameEnv", max_episode_steps=1000,
)
