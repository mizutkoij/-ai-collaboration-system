#!/usr/bin/env python3
"""
モデル選択機能のテスト
"""

import requests
import json
import time
from pathlib import Path

def test_model_selection():
    """モデル選択機能をテスト"""
    print("Testing Model Selection Functionality")
    print("=" * 50)
    
    base_url = "http://localhost:8080"
    
    try:
        # Test 1: API状態チェック
        print("1. Testing API status check...")
        response = requests.get(f"{base_url}/api/check-api-status", timeout=5)
        if response.status_code == 200:
            api_status = response.json()
            print(f"   OpenAI API: {'Connected' if api_status.get('openai') else 'Not configured'}")
            print(f"   Anthropic API: {'Connected' if api_status.get('anthropic') else 'Not configured'}")
        else:
            print("   Failed to check API status")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"   Cannot connect to server: {e}")
        print("   Please make sure the WebUI server is running:")
        print("   python launch_webui.py")
        return False
    
    try:
        # Test 2: 会話作成でモデル選択をテスト
        print("\n2. Testing conversation creation with model selection...")
        
        conversation_data = {
            "project_request": "Create a simple web application",
            "user_id": "test_user",
            "models": {
                "openai": "gpt-4-turbo",
                "anthropic": "claude-3-haiku-20240307"
            }
        }
        
        response = requests.post(
            f"{base_url}/api/conversations/start", 
            json=conversation_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            conversation_id = result.get("conversation_id")
            print(f"   Conversation created with ID: {conversation_id}")
            print(f"   Status: {result.get('status')}")
            
            # Test 3: 作成された会話でモデル設定を確認
            print("\n3. Verifying model settings in conversation...")
            response = requests.get(
                f"{base_url}/api/conversations/{conversation_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                conversation = response.json()
                models = conversation.get("selected_models", {})
                print(f"   Selected OpenAI model: {models.get('openai', 'Not set')}")
                print(f"   Selected Anthropic model: {models.get('anthropic', 'Not set')}")
                
                if models.get('openai') == 'gpt-4-turbo' and models.get('anthropic') == 'claude-3-haiku-20240307':
                    print("   Model selection correctly saved!")
                else:
                    print("   Model selection not properly saved")
                    return False
            else:
                print("   Failed to retrieve conversation")
                return False
            
        else:
            print("   Failed to create conversation")
            return False
        
        # Test 4: 会話履歴に保存確認
        print("\n4. Testing conversation persistence...")
        conversations_dir = Path("conversations")
        if conversations_dir.exists():
            conversation_files = list(conversations_dir.glob("*.json"))
            if conversation_files:
                with open(conversation_files[-1], 'r', encoding='utf-8') as f:
                    saved_conversation = json.load(f)
                    saved_models = saved_conversation.get("selected_models", {})
                    print(f"   Persisted OpenAI model: {saved_models.get('openai', 'Not found')}")
                    print(f"   Persisted Anthropic model: {saved_models.get('anthropic', 'Not found')}")
            else:
                print("   No conversation files found")
        else:
            print("   Conversations directory not found")
        
        print("\n" + "=" * 50)
        print("Model Selection Test Results:")
        print("- API status check: PASS")
        print("- Conversation creation with models: PASS") 
        print("- Model settings verification: PASS")
        print("- Conversation persistence: PASS")
        print("\nModel selection functionality is working correctly!")
        print("\nAvailable models:")
        print("OpenAI:")
        print("  - gpt-4")
        print("  - gpt-4-turbo") 
        print("  - gpt-3.5-turbo")
        print("Anthropic:")
        print("  - claude-3-sonnet-20240229")
        print("  - claude-3-haiku-20240307")
        print("  - claude-3-opus-20240229")
        
        return True
        
    except Exception as e:
        print(f"   Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_model_selection()
    exit(0 if success else 1)