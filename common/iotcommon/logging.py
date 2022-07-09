"""common logging"""

import logging
import sys
from typing import Any, Dict

from opencensus.ext.azure.log_exporter import AzureLogHandler

from iotcommon.config import DeviceModuleConfig


class ServiceName:
    B2S = "blob_to_samba"
    S2B = "samba_to_blob"
    WORKER = "worker"


PACKAGES = {
    ServiceName.B2S: "blob_to_samba",
    ServiceName.S2B: "samba_to_blob",
    ServiceName.WORKER: "worker",
}


class OptionalCustomDimensionsFilter(logging.Formatter):
    """filter that outputs `custom_dimensions` if present"""
    def __init__(self, message_fmt: str, service_name: str) -> None:
        logging.Formatter.__init__(self, message_fmt, None)
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        if "custom_dimensions" not in record.__dict__:
            record.__dict__["custom_dimensions"] = ""
        else:
            # add the service name to custom_dimensions, so it's queryable
            record.__dict__["custom_dimensions"]["service"] = self.service_name
        return super().format(record)


class CustomDimensionsFilter(logging.Filter):
    """filter for azure-targeted messages containing `custom_dimensions`"""
    def filter(self, record: logging.LogRecord) -> bool:
        return bool(record.__dict__["custom_dimensions"])


def init_logging(service_name: str) -> logging.Logger:
    """initialize log handlers"""
    config = DeviceModuleConfig.from_environment()

    package = PACKAGES[service_name]
    logger = logging.getLogger(package)
    logger.setLevel(logging.INFO)

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_format = "[%(levelname)s] %(asctime)s - %(message)s %(custom_dimensions)s"
    formatter = OptionalCustomDimensionsFilter(console_format, service_name)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if config.debug:
        logger.setLevel(logging.DEBUG)
    
    # azure log handler
    instrumentation_key = config.app_insights_instrumentation_key
    if instrumentation_key:
        azure_handler = AzureLogHandler(
            connection_string=f"InstrumentationKey={instrumentation_key}"
        )
        azure_handler.addFilter(CustomDimensionsFilter())
        logger.addHandler(azure_handler)
    else:
        logger.info(f"azure log handler not attached: {package} (missing key")
    return logger


def get_custom_dimensions(dimensions: Dict[str, Any], service_name: str) -> Dict[str, Any]:
    """merge the base dimensions with the given dimensions"""
    base_dimensions = {"service": service_name}
    base_dimensions.update(dimensions)
    return {"custom_dimensions": base_dimensions}
