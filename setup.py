#!/usr/bin/env python3
"""
Setup script for Child's Automatic Printer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="childs-automatic-printer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Finnish voice-controlled printing system for children",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kidPrinter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Printing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points={
        "console_scripts": [
            "kidprinter=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/**/*", "config/*"],
    },
)
