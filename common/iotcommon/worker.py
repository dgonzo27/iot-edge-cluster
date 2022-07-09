"""celery worker"""

import time

from celery import Celery
from celery.signals import after_setup_logger

from iotcommon.config import DeviceModuleConfig
from iotcommon.logging import ServiceName, init_logging

config = DeviceModuleConfig.from_environment()

celery = Celery(__name__)
celery.conf.broker_url = config.celery_broker_url
celery.conf.result_backend = config.celery_result_backend


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs) -> None:
    """setup logging for celery"""
    init_logging(ServiceName.WORKER)


@celery.task(name="create_task")
def create_task(task_type) -> bool:
    time.sleep(int(task_type) * 3)
    return True
