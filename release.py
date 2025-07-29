#!/usr/bin/env python3
"""
Release Script for AI Collaboration System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import zipfile

def run_command(cmd, description=""):
    """コマンドを実行"""
    print(f"Running: {description or ' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def clean_build_dirs():
    """ビルドディレクトリをクリーンアップ"""
    dirs_to_clean = ["build", "dist", "__pycache__", "*.egg-info"]
    
    for pattern in dirs_to_clean:
        if "*" in pattern:
            # glob pattern
            for path in Path(".").glob("**/" + pattern):
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"Removed: {path}")
        else:
            path = Path(pattern)
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"Removed: {path}")

def create_main_entry():
    """メインエントリーポイントを作成"""
    main_content = '''#!/usr/bin/env python3
"""
AI Collaboration System - Main Launcher
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
if getattr(sys, 'frozen', False):
    # PyInstallerで実行されている場合
    application_path = Path(sys.executable).parent
else:
    # 通常のPythonで実行されている場合
    application_path = Path(__file__).parent

sys.path.insert(0, str(application_path))
sys.path.insert(0, str(application_path / "src"))

def main():
    """メイン実行関数"""
    print("🤖 AI Collaboration System v1.2.0")
    print("=" * 60)
    print("🚀 3-way AI Collaboration: ChatGPT + Claude + Gemini")
    print("🌐 Complete WebUI Interface")
    print("💬 Real-time AI Conversation")
    print("📁 Automatic File Generation")
    print("⚙️  Model Selection & Configuration")
    print("=" * 60)
    print("")
    print("Starting WebUI server...")
    print("🌍 Access at: http://localhost:8080")
    print("⏹️  Press Ctrl+C to stop")
    print("")
    
    try:
        from webui_server import WebUIServer
        server = WebUIServer()
        server.run(host="localhost", port=8080)
        
    except ImportError as e:
        print(f"❌ Error: Required modules not found: {e}")
        print("")
        print("📋 Setup Instructions:")
        print("1. Install Python 3.8+")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Set API keys as environment variables:")
        print("   - OPENAI_API_KEY=your_openai_key")
        print("   - ANTHROPIC_API_KEY=your_anthropic_key") 
        print("   - GEMINI_API_KEY=your_gemini_key")
        input("Press Enter to exit...")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\\n🛑 AI Collaboration System stopped by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error starting AI Collaboration System: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(main_content)
    print("Created main.py entry point")

def build_executable():
    """実行ファイルをビルド"""
    print("Building executable with PyInstaller...")
    
    # メインエントリーポイントを作成
    create_main_entry()
    
    # PyInstallerコマンドを構築
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=AICollaborationSystem",
        "--add-data=templates;templates",
        "--add-data=src;src",
        "--add-data=*.md;.",
        "--add-data=requirements.txt;.",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.lifespan.off", 
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets.websockets_impl",
        "--hidden-import=uvicorn.protocols.http.httptools_impl",
        "--hidden-import=uvicorn.protocols.http.h11_impl",
        "--hidden-import=fastapi",
        "--hidden-import=websockets",
        "--hidden-import=openai",
        "--hidden-import=anthropic",
        "--hidden-import=google.generativeai",
        "--hidden-import=pydantic",
        "--hidden-import=jinja2",
        "--hidden-import=starlette.applications",
        "--hidden-import=starlette.middleware",
        "--hidden-import=starlette.routing",
        "main.py"
    ]
    
    return run_command(cmd, "Building executable")

def create_portable_package():
    """ポータブルパッケージを作成"""
    print("Creating portable package...")
    
    package_name = f"AI_Collaboration_System_v1.2.0_Portable"
    package_dir = Path(package_name)
    
    # 既存のパッケージディレクトリを削除
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # 必要なファイルをコピー
    files_to_copy = [
        ("dist/AICollaborationSystem.exe", "AICollaborationSystem.exe"),
        ("requirements.txt", "requirements.txt"),
        ("MODEL_SELECTION_GUIDE.md", "MODEL_SELECTION_GUIDE.md"),
        ("README.md", "README.md"),
        ("templates", "templates"),
    ]
    
    for source, dest in files_to_copy:
        source_path = Path(source)
        dest_path = package_dir / dest
        
        if source_path.exists():
            if source_path.is_file():
                shutil.copy2(source_path, dest_path)
            else:
                shutil.copytree(source_path, dest_path)
            print(f"Copied: {source} -> {dest}")
        else:
            print(f"Warning: {source} not found")
    
    # Windows起動スクリプトを作成
    launcher_bat = '''@echo off
title AI Collaboration System v1.2.0
color 0A

echo.
echo     █████╗ ██╗    ██████╗  ██████╗ ██╗     ██╗      █████╗ ██████╗ 
echo    ██╔══██╗██║   ██╔════╝ ██╔═══██╗██║     ██║     ██╔══██╗██╔══██╗
echo    ███████║██║   ██║      ██║   ██║██║     ██║     ███████║██████╔╝
echo    ██╔══██║██║   ██║      ██║   ██║██║     ██║     ██╔══██║██╔══██╗
echo    ██║  ██║██║   ╚██████╗ ╚██████╔╝███████╗███████╗██║  ██║██████╔╝
echo    ╚═╝  ╚═╝╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ 
echo.
echo                    3-way AI Collaboration System
echo                  ChatGPT + Claude + Gemini = Magic!
echo.
echo ================================================================================
echo.
echo Starting AI Collaboration System...
echo.
echo 🌐 Web Interface will open at: http://localhost:8080
echo ⏹️  Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

AICollaborationSystem.exe

echo.
echo ================================================================================
echo AI Collaboration System has stopped.
echo Thank you for using our 3-way AI collaboration platform!
echo ================================================================================
echo.
pause
'''
    
    with open(package_dir / "🚀 Start AI Collaboration.bat", "w", encoding="utf-8") as f:
        f.write(launcher_bat)
    
    # Linux/Mac起動スクリプトを作成
    launcher_sh = '''#!/bin/bash

echo "🤖 AI Collaboration System v1.2.0"
echo "=================================="
echo "🚀 3-way AI Collaboration: ChatGPT + Claude + Gemini"
echo "🌐 Web Interface: http://localhost:8080"
echo "⏹️  Press Ctrl+C to stop"
echo "=================================="
echo ""

# 実行権限を確認
if [ ! -x "./AICollaborationSystem" ]; then
    chmod +x "./AICollaborationSystem"
fi

./AICollaborationSystem
'''
    
    launcher_sh_path = package_dir / "start.sh"
    with open(launcher_sh_path, "w", encoding="utf-8") as f:
        f.write(launcher_sh)
    
    # 実行権限を付与（Linuxの場合）
    if sys.platform != "win32":
        os.chmod(launcher_sh_path, 0o755)
    
    # ポータブル版README
    portable_readme = '''# 🤖 AI Collaboration System - Portable Version

## 🚀 Quick Start

### Windows
1. Double-click `🚀 Start AI Collaboration.bat`
2. Open your browser and go to http://localhost:8080
3. Start collaborating with AI!

### Linux/Mac
1. Run `./start.sh` in terminal
2. Open your browser and go to http://localhost:8080
3. Start collaborating with AI!

## ✨ Features

- **3-way AI Collaboration**: ChatGPT + Claude + Gemini working together
- **Complete WebUI**: No command line needed - everything in your browser
- **Real-time Conversation**: Watch AIs collaborate in real-time
- **Automatic File Generation**: Get complete projects generated automatically
- **Model Selection**: Choose the best AI models for your project
- **Conversation History**: All conversations saved and searchable

## 🔑 API Keys Setup

Before using, set up your API keys:

### Method 1: Environment Variables
```bash
# Windows (Command Prompt)
set OPENAI_API_KEY=your_openai_key
set ANTHROPIC_API_KEY=your_anthropic_key
set GEMINI_API_KEY=your_gemini_key

# Windows (PowerShell)
$env:OPENAI_API_KEY="your_openai_key"
$env:ANTHROPIC_API_KEY="your_anthropic_key"  
$env:GEMINI_API_KEY="your_gemini_key"

# Linux/Mac
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
export GEMINI_API_KEY="your_gemini_key"
```

### Method 2: .env File
Create a `.env` file in this directory with:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
```

## 🎯 How to Use

1. **Start the Application**: Use the launcher script
2. **Open Browser**: Go to http://localhost:8080
3. **Select Models**: Choose your preferred AI models in the sidebar
4. **Start Project**: Type your project description and hit Enter
5. **Watch Magic**: See ChatGPT + Claude + Gemini collaborate to build your project
6. **Download Results**: Get generated files when complete

## 📋 System Requirements

- **Operating System**: Windows 10/11, Linux, or macOS
- **Memory**: 4GB RAM minimum, 8GB+ recommended
- **Internet**: Required for AI API access
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

## 🛠️ Troubleshooting

### Application won't start
- Check that port 8080 is not in use
- Verify API keys are set correctly
- Try running as administrator (Windows)

### AI responses not working
- Verify internet connection
- Check API keys are valid and have credits
- Try different AI models

### Browser can't connect
- Make sure application is running
- Try http://127.0.0.1:8080 instead
- Disable firewall/antivirus temporarily

## 📞 Support

- **GitHub**: https://github.com/yourusername/ai-collaboration-system
- **Issues**: Report bugs and request features
- **Discussions**: Share your projects and get help

## 📜 License

MIT License - Free for personal and commercial use

---

**Made with ❤️ by the AI Collaboration Team**

*Bringing the future of AI-powered development to everyone!*
'''
    
    with open(package_dir / "README_PORTABLE.md", "w", encoding="utf-8") as f:
        f.write(portable_readme)
    
    print(f"Portable package created: {package_dir}")
    return package_dir

def create_release_archive():
    """リリースアーカイブを作成"""
    print("Creating release archive...")
    
    version = "v1.2.0"
    archive_name = f"AI_Collaboration_System_{version}_Release"
    
    # ZIPファイルを作成
    with zipfile.ZipFile(f"{archive_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        # ポータブルパッケージを追加
        package_dir = Path(f"AI_Collaboration_System_v1.2.0_Portable")
        if package_dir.exists():
            for file_path in package_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir.parent)
                    zipf.write(file_path, arcname)
                    
        # 追加ドキュメント
        additional_files = [
            "CHANGELOG.md",
            "LICENSE",
        ]
        
        for file_name in additional_files:
            file_path = Path(file_name)
            if file_path.exists():
                zipf.write(file_path, file_path.name)
    
    print(f"Release archive created: {archive_name}.zip")
    return f"{archive_name}.zip"

def update_version_info():
    """バージョン情報を更新"""
    print("Updating version information...")
    
    version_info = f'''# Version Information

## AI Collaboration System v1.2.0

**Release Date**: {datetime.now().strftime("%Y-%m-%d")}

### 🎉 What's New

#### 🤖 3-way AI Collaboration
- **ChatGPT Integration**: Design and architecture planning
- **Claude Integration**: Implementation and coding
- **Gemini Integration**: Optimization and high-speed processing
- **Seamless Collaboration**: All three AIs working together automatically

#### 🌐 Complete WebUI Experience
- **Browser-based Interface**: No command line required
- **Real-time Updates**: Watch AI collaboration live
- **Model Selection**: Choose optimal models for each provider
- **Conversation History**: Complete persistence and searchability

#### ⚡ Performance & Features
- **High-speed Processing**: Gemini Flash for rapid prototyping
- **Quality Assurance**: GPT-4 + Claude Opus for premium results
- **Flexible Configuration**: Environment variables and .env support
- **Portable Distribution**: Single executable with all dependencies

### 🔧 Technical Improvements
- WebSocket real-time communication
- Enhanced error handling and recovery
- Improved UI/UX with modern design
- Better API management and status checking
- Comprehensive logging and debugging

### 📦 Distribution Options
1. **Portable Executable**: Single .exe file with all dependencies
2. **Python Package**: `pip install ai-collaboration-system`
3. **Source Code**: Full source with setup instructions

### 🎯 System Requirements
- Windows 10/11, Linux, or macOS
- 4GB+ RAM (8GB+ recommended)
- Internet connection for AI APIs
- Modern web browser

### 🚀 Getting Started
1. Download the portable version
2. Set up your API keys
3. Run the launcher
4. Open http://localhost:8080
5. Start collaborating with AI!

---

*The future of AI-powered development is here!*
'''
    
    with open("VERSION_INFO.md", "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print("Version information updated")

def main():
    """メインリリース処理"""
    print("AI Collaboration System - Release Builder")
    print("=" * 60)
    print("Building v1.2.0 with 3-way AI Collaboration")
    print("=" * 60)
    
    try:
        # ビルドディレクトリをクリーンアップ
        print("\nCleaning build directories...")
        clean_build_dirs()
        
        # バージョン情報を更新
        update_version_info()
        
        # 実行ファイルをビルド
        print("\nBuilding executable...")
        if not build_executable():
            print("Executable build failed!")
            return False
        
        # ポータブルパッケージを作成
        print("\nCreating portable package...")
        package_dir = create_portable_package()
        
        # リリースアーカイブを作成
        print("\nCreating release archive...")
        archive_file = create_release_archive()
        
        # 成功メッセージ
        print("\n" + "=" * 60)
        print("RELEASE BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Portable Package: {package_dir}")
        print(f"Release Archive: {archive_file}")
        print(f"Executable: dist/AICollaborationSystem.exe")
        print("=" * 60)
        print("\nReady for distribution!")
        print("Upload files to GitHub Releases")
        print("Share with the community!")
        
        return True
        
    except Exception as e:
        print(f"\nRelease build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)