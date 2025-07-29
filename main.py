#!/usr/bin/env python3
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
