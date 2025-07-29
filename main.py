#!/usr/bin/env python3
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
        print("\n🛑 AI Collaboration System stopped by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error starting AI Collaboration System: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
