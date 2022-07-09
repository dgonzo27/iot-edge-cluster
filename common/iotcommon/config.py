from typing import Optional

from cachetools.func import lru_cache
from pydantic import BaseSettings, Field

ENV_VAR_DEVICE_MODULE_PREFIX = "DVMOD_"


class DeviceModuleConfig(BaseSettings):
    debug: bool = False
    app_insights_instrumentation_key: Optional[str] = Field(default=None, 
        env="APP_INSIGHTS_INSTRUMENTATION_KEY")
    celery_broker_url: Optional[str] = Field(default="redis://localhost:6379",
        env="CELERY_BROKER_URL")
    celery_result_backend: Optional[str] = Field(default="redis://localhost:6379",
        env="CELERY_RESULT_BACKEND")

    @classmethod
    @lru_cache(maxsize=1)
    def from_environment(cls) -> "DeviceModuleConfig":
        return DeviceModuleConfig()
    
    class Config:
        env_prefix = ENV_VAR_DEVICE_MODULE_PREFIX
        extra = "ignore"
        env_nested_delimiter = "__"
