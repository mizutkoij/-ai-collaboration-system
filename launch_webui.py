#!/usr/bin/env python3
"""
WebUI Launcher - 簡単起動スクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

try:
    from webui_server import WebUIServer
    
    def main():
        print("AI Collaboration System - WebUI")
        print("=" * 50)
        print("Starting web interface...")
        print("Access at: http://localhost:8080")
        print("Press Ctrl+C to stop")
        print("")
        
        server = WebUIServer()
        server.run(host="localhost", port=8080)
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print("Error: Required modules not found")
    print(f"Details: {e}")
    print("")
    print("Please install requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting WebUI: {e}")
    sys.exit(1)