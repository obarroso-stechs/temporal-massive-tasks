from configurations.env import env

TEMPORAL_TARGET_HOST: str = env.str("TEMPORAL_HOST", "localhost:7233")
TEMPORAL_NAMESPACE: str = env.str("TEMPORAL_NAMESPACE", "default")
TEMPORAL_TASK_QUEUE: str = env.str("TEMPORAL_TASK_QUEUE", "nbi-parent-child-task-queue")
