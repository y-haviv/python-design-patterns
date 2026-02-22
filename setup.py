"""Setup configuration for Python Design Patterns package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-design-patterns",
    version="1.0.0",
    author="Python Design Patterns Contributors",
    description="Comprehensive implementation of Gang of Four design patterns in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-haviv/python-design-patterns",
    packages=find_packages(exclude=["tests", "tests.*", "docs", ".github"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
    ],
    python_requires=">=3.9",
    project_urls={
        "Bug Tracker": "https://github.com/y-haviv/python-design-patterns/issues",
        "Documentation": "https://github.com/y-haviv/python-design-patterns#readme",
        "Source Code": "https://github.com/y-haviv/python-design-patterns",
    },
)
