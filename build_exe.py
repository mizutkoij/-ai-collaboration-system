#!/usr/bin/env python3
"""
Build executable for AI Collaboration System
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def install_pyinstaller():
    """PyInstallerをインストール"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")

def create_main_entry():
    """メインエントリーポイントを作成"""
    main_content = '''#!/usr/bin/env python3
"""
AI Collaboration System - Main Entry Point
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def main():
    """メイン実行関数"""
    try:
        from webui_server import WebUIServer
        
        print("AI Collaboration System - Executable Version")
        print("=" * 60)
        print("Starting AI Collaboration WebUI...")
        print("Access at: http://localhost:8080")
        print("Press Ctrl+C to stop")
        print("")
        print("Features:")
        print("- 3-way AI Collaboration (ChatGPT + Claude + Gemini)")
        print("- Complete browser-based interface")  
        print("- Real-time conversation and file generation")
        print("- Model selection and configuration")
        print("")
        
        server = WebUIServer()
        server.run(host="localhost", port=8080)
        
    except ImportError as e:
        print(f"Error: Required modules not found: {e}")
        print("Please ensure all dependencies are properly installed")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting AI Collaboration System: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(main_content)
    print("Created main.py entry point")

def create_pyinstaller_spec():
    """PyInstaller仕様ファイルを作成"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# データファイルを含める
datas = [
    ('templates', 'templates'),
    ('src', 'src'),
    ('*.md', '.'),
    ('requirements.txt', '.'),
]

# 隠れたインポートを指定
hiddenimports = [
    'uvicorn',
    'fastapi',
    'websockets',
    'aiohttp',
    'openai',
    'anthropic', 
    'google.generativeai',
    'pydantic',
    'jinja2',
    'sqlalchemy',
    'pathlib',
    'json',
    'asyncio',
    'datetime',
    'uuid',
    'typing',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AICollaborationSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if Path('assets/icon.ico').exists() else None,
)
'''
    
    with open("ai_collaboration.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("Created PyInstaller spec file")

def build_executable():
    """実行ファイルをビルド"""
    try:
        print("Building executable...")
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed" if sys.platform == "win32" else "",
            "--name=AICollaborationSystem",
            "--add-data=templates;templates",
            "--add-data=src;src", 
            "--add-data=*.md;.",
            "--hidden-import=uvicorn",
            "--hidden-import=fastapi",
            "--hidden-import=websockets",
            "--hidden-import=openai",
            "--hidden-import=anthropic",
            "--hidden-import=google.generativeai",
            "main.py"
        ]
        
        # 空の文字列を除去
        cmd = [arg for arg in cmd if arg]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Executable built successfully!")
            
            # distフォルダの場所を確認
            dist_dir = Path("dist")
            if dist_dir.exists():
                exe_files = list(dist_dir.glob("*.exe"))
                if exe_files:
                    print(f"Executable location: {exe_files[0]}")
                else:
                    print("Executable created in dist/ directory")
            
            return True
        else:
            print(f"Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error building executable: {e}")
        return False

def create_portable_package():
    """ポータブルパッケージを作成"""
    try:
        package_dir = Path("AI_Collaboration_System_Portable")
        
        # パッケージディレクトリを作成
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # 必要なファイルをコピー
        files_to_copy = [
            "dist/AICollaborationSystem.exe",
            "requirements.txt",
            "MODEL_SELECTION_GUIDE.md",
            "README.md",
            "templates",
            "src"
        ]
        
        for item in files_to_copy:
            source = Path(item)
            if source.exists():
                if source.is_file():
                    shutil.copy2(source, package_dir)
                else:
                    shutil.copytree(source, package_dir / source.name)
                print(f"Copied: {item}")
        
        # 起動スクリプトを作成
        launcher_content = '''@echo off
echo AI Collaboration System - Portable Version
echo ==========================================
echo.
echo Starting AI Collaboration WebUI...
echo Access at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

AICollaborationSystem.exe

pause
'''
        
        with open(package_dir / "start.bat", "w", encoding="utf-8") as f:
            f.write(launcher_content)
        
        # README for portable version
        portable_readme = '''# AI Collaboration System - Portable Version

## Quick Start

1. Double-click `start.bat` to launch the application
2. Open your web browser and go to http://localhost:8080
3. Start collaborating with AI!

## Features

- 3-way AI Collaboration (ChatGPT + Claude + Gemini)
- Complete browser-based interface
- Real-time conversation and file generation
- Model selection and configuration

## API Keys Setup

Before using, set up your API keys as environment variables:

```
set OPENAI_API_KEY=your_openai_api_key
set ANTHROPIC_API_KEY=your_anthropic_api_key  
set GEMINI_API_KEY=your_gemini_api_key
```

Or create a `.env` file in this directory with:

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## System Requirements

- Windows 10/11
- Internet connection for AI APIs
- Modern web browser

## Support

For support and updates, visit: https://github.com/yourusername/ai-collaboration-system
'''
        
        with open(package_dir / "README_PORTABLE.md", "w", encoding="utf-8") as f:
            f.write(portable_readme)
        
        print(f"Portable package created: {package_dir}")
        return True
        
    except Exception as e:
        print(f"Error creating portable package: {e}")
        return False

def main():
    """メイン実行"""
    print("AI Collaboration System - Build Script")
    print("=" * 50)
    
    # PyInstallerをインストール
    install_pyinstaller()
    
    # メインエントリーポイントを作成
    create_main_entry()
    
    # PyInstaller仕様ファイルを作成
    create_pyinstaller_spec()
    
    # 実行ファイルをビルド
    if build_executable():
        print("\nBuild completed successfully!")
        
        # ポータブルパッケージを作成
        if create_portable_package():
            print("Portable package created successfully!")
        
        print("\nFiles created:")
        print("- dist/AICollaborationSystem.exe")
        print("- AI_Collaboration_System_Portable/ (portable package)")
        print("\nYou can now distribute the executable or portable package!")
        
    else:
        print("Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main()