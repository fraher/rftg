"""
Race for the Galaxy - Python Implementation
===========================================

A faithful Python implementation of the Race for the Galaxy card game,
designed to be fully compatible with the original C implementation.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rftg-python",
    version="0.9.5",  # Match original C version
    author="Race for the Galaxy Python Team",
    description="Python implementation of Race for the Galaxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest", "pytest-cov", "mypy", "black", "flake8"],
        "pygame": ["pygame>=2.1.0"],
        "image": ["pillow>=9.0.0"],
    },
    entry_points={
        "console_scripts": [
            "rftg=core.main:main",
        ],
    },
)
