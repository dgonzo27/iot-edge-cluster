"""setup for s2b"""

from setuptools import find_packages, setup


# runtime requirements
inst_reqs = [
    "iotcommon",
    "aiofiles==0.6.0",
    "fastapi==0.64.0",
    "Jinja2==3.0.3",
    "requests==2.25.1",
    "uvicorn==0.13.4",
]

extra_reqs = {
    "test": [
        "pytest",
        "pytest-asyncio==0.18.*",
    ],
    "dev": [
        "black==22.3.0",
        "flake8==3.8.4",
        "isort==5.9.2",
        "mypy==0.800",
    ],
}

setup(
    name="s2b",
    python_requires=">=3.7",
    description="IoT Edge Cluster - s2b",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
