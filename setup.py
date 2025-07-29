#!/usr/bin/env python3
"""
AI Collaboration System Setup
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-collaboration-system",
    version="1.2.0",
    author="AI Collaboration Team",
    author_email="contact@ai-collaboration.dev",
    description="3-way AI Collaboration System - ChatGPT + Claude + Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-collaboration-system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "full": [
            "tiktoken>=0.5.0",
            "langchain>=0.0.350",
            "docker>=6.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-collab=ai_collaboration_core:main",
            "ai-webui=webui_server:main",
            "ai-design=design_system:main",
            "ai-implement=implementation_system:main",
            "ai-monitor=conversation_engine:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "static/*", "config/*.yaml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-collaboration-system/issues",
        "Source": "https://github.com/yourusername/ai-collaboration-system",
        "Documentation": "https://ai-collaboration-system.readthedocs.io/",
    },
)