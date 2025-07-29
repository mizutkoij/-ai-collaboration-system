#!/usr/bin/env python3
"""
AI Collaboration System - Easy Installation Script
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("OK: pip is available")
        return True
    except subprocess.CalledProcessError:
        print("Error: pip is not available")
        return False

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("OK: Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "config",
        "logs", 
        "generated_projects",
        "temp",
        "designs",
        "implementations"
    ]
    
    print("Creating directories...")
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"   - {dir_name}")
    
    print("OK: Directories created")

def create_sample_config():
    """Create sample configuration file"""
    config_content = """{
    "system": {
        "auto_approve": true,
        "max_iterations": 20,
        "output_directory": "./generated_projects",
        "log_level": "INFO"
    },
    "ai": {
        "openai": {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        "anthropic": {
            "model": "claude-3-sonnet-20240229", 
            "max_tokens": 2000,
            "temperature": 0.7
        }
    },
    "ui": {
        "theme": "dark",
        "show_progress": true,
        "auto_refresh": 2000,
        "port": 8080
    },
    "file_generation": {
        "include_tests": true,
        "include_docs": true,
        "include_docker": true,
        "code_style": "black",
        "license": "MIT"
    }
}"""
    
    config_file = Path("config/ai_config.json")
    
    if not config_file.exists():
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("OK: Sample configuration created")
    else:
        print("Info: Configuration file already exists")

def create_environment_template():
    """Create .env template file"""
    env_content = """# AI Collaboration System - Environment Variables
# Copy this file to .env and fill in your API keys

# OpenAI API Key (for ChatGPT/o4)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (for Claude)  
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Custom configuration
# AI_COLLAB_CONFIG=./config/custom_config.json

# Optional: Debug mode
# AI_COLLAB_DEBUG=true
"""
    
    env_file = Path(".env.template")
    
    if not env_file.exists():
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("OK: Environment template created (.env.template)")
    else:
        print("Info: Environment template already exists")

def check_browser():
    """Check if a web browser is available"""
    try:
        import webbrowser
        webbrowser.get()
        print("OK: Web browser available")
        return True
    except:
        print("Warning: Web browser not detected (UI features may be limited)")
        return False

def install_development_tools():
    """Install optional development tools"""
    dev_packages = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0", 
        "black>=23.0.0",
        "flake8>=6.0.0"
    ]
    
    response = input("Install development tools? (y/N): ").lower().strip()
    if response in ['y', 'yes']:
        print("Installing development tools...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + dev_packages)
            print("OK: Development tools installed")
        except subprocess.CalledProcessError:
            print("Warning: Some development tools failed to install")

def create_launcher_scripts():
    """Create convenient launcher scripts"""
    
    # Windows batch file
    if platform.system() == "Windows":
        batch_content = """@echo off
echo Starting AI Collaboration System...
python src/ai_collaboration_core.py %*
pause
"""
        with open("ai-collab.bat", 'w') as f:
            f.write(batch_content)
        print("OK: Windows launcher created (ai-collab.bat)")
    
    # Unix shell script
    shell_content = """#!/bin/bash
echo "Starting AI Collaboration System..."
python3 src/ai_collaboration_core.py "$@"
"""
    
    shell_file = Path("ai-collab.sh")
    with open(shell_file, 'w') as f:
        f.write(shell_content)
    
    # Make executable on Unix systems
    if platform.system() != "Windows":
        shell_file.chmod(0o755)
        print("OK: Unix launcher created (ai-collab.sh)")

def run_installation():
    """Run the complete installation process"""
    print("AI Collaboration System - Installation")
    print("=" * 50)
    
    # System checks
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Installation steps
    steps = [
        ("Installing Python packages", install_requirements),
        ("Creating directories", create_directories),
        ("Creating configuration", create_sample_config),
        ("Creating environment template", create_environment_template),
        ("Creating launcher scripts", create_launcher_scripts),
        ("Checking browser", check_browser)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            if not step_func():
                print(f"Warning: {step_name} had issues")
        except Exception as e:
            print(f"Error in {step_name}: {e}")
    
    # Optional development tools
    install_development_tools()
    
    print("\n" + "=" * 50)
    print("Installation completed!")
    print("\nNext Steps:")
    print("1. Copy .env.template to .env and add your API keys")
    print("2. Run: python src/ai_collaboration_core.py status")
    print("3. Start your first project: python src/ai_collaboration_core.py run 'your project idea'")
    print("\nDocumentation: README.md")
    print("Issues: https://github.com/yourusername/ai-collaboration-system/issues")
    
    return True

if __name__ == "__main__":
    success = run_installation()
    sys.exit(0 if success else 1)