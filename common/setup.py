"""setup for iotcommon"""

from setuptools import find_packages, setup


# runtime requirements
inst_reqs = [
    "opencensus-ext-azure==1.0.8",
    "opencensus-ext-logging==0.1.0",
    "azure-identity==1.7.1",
    "cachetools==5.0.0",
    "celery==4.4.7",
    "pydantic==1.9.0",
    "redis==3.5.3",
    "types-cachetools==4.2.9",
]

extra_reqs = {
    "test": [
        "pytest",
        "pytest-asyncio",
    ],
    "dev": [
        "pytest",
        "pytest-asyncio",
    ],
}

setup(
    name="iotcommon",
    python_requires=">=3.7",
    description="IoT Edge Cluster - iotcommon",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
