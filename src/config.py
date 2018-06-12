import math

# the width of the environment
ENVIRONMENT_X: int = 10000
# the height of the environment
ENVIRONMENT_Y: int = 10000
# environment seed
SEED: int = 1
# what's the max number of agents in the environment
MAX_AGENTS: int = 1
# what's the max amount of food found in the environment
MAX_FOOD: int = 10000
# how often should a blob be allowed to breed? Set the value to -1 for no breeding
BIRTH_INTERVAL: int = -1
# how fast much health should the agent loose pr. step
HEALTH_PER_STEP: float = 0.0
# should the game be rendered? options: human, headerless
RENDER_MODE: str = 'headerless'
# the angle of the agents vision cone
VISION_ANGLE: float = 0.2 * math.pi
# agent movement speed (how many pixels pr. action)
MOVEMENT_SPEED: int = 1
# agent rotation speed (how much does the agent rotate pr. action)
ROTATION_SPEED = 0.0055555555556 * math.pi
