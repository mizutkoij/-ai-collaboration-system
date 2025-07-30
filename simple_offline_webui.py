#!/usr/bin/env python3
"""
Simple Offline AI Collaboration WebUI
APIキーなしで動作するスタンドアロン版
"""

import json
import asyncio
import webbrowser
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Simple Offline AI Collaboration")

# シンプルなオフラインAIシミュレーター
class SimpleOfflineAI:
    def __init__(self):
        self.responses = {
            "chatgpt": [
                "プロジェクト「{request}」について分析しました。\n\n【要件分析】\n- 主要機能: {request}\n- 推奨技術スタック: Python/JavaScript\n- 実装期間: 1-2週間\n\n【設計方針】\n1. シンプルで分かりやすい構造\n2. 拡張性を考慮した設計\n3. エラーハンドリングの充実\n\n次はClaudeが具体的な実装を行います。",
                "「{request}」の要件を整理しました。\n\n【機能要件】\n- コア機能の実装\n- ユーザーインターフェース\n- データ処理ロジック\n\n【技術要件】\n- 言語: Python推奨\n- フレームワーク: Flask/FastAPI\n- データベース: SQLite\n\nClaudeに実装をお任せします。"
            ],
            "claude": [
                "ChatGPTの設計を受けて、「{request}」を実装します。\n\n【実装コード】\n```python\n#!/usr/bin/env python3\n\"\"\"\n{request} - 実装例\n\"\"\"\n\nimport os\nimport hashlib\nfrom cryptography.fernet import Fernet\n\nclass KeyDecoder:\n    def __init__(self):\n        self.key = None\n        \n    def generate_key(self):\n        \"\"\"新しいキーを生成\"\"\"\n        return Fernet.generate_key()\n    \n    def decode_key(self, encoded_key, method='base64'):\n        \"\"\"エンコードされたキーをデコード\"\"\"\n        try:\n            if method == 'base64':\n                import base64\n                return base64.b64decode(encoded_key)\n            elif method == 'hex':\n                return bytes.fromhex(encoded_key)\n            else:\n                return encoded_key.encode()\n        except Exception as e:\n            print(f\"デコードエラー: {e}\")\n            return None\n    \n    def decrypt_data(self, encrypted_data, key):\n        \"\"\"データを復号化\"\"\"\n        try:\n            f = Fernet(key)\n            return f.decrypt(encrypted_data).decode()\n        except Exception as e:\n            print(f\"復号化エラー: {e}\")\n            return None\n\nif __name__ == \"__main__\":\n    decoder = KeyDecoder()\n    \n    # 使用例\n    key = decoder.generate_key()\n    print(f\"生成されたキー: {key.decode()}\")\n    \n    # キーのデコード例\n    decoded = decoder.decode_key(key.decode(), 'base64')\n    print(f\"デコード結果: {decoded}\")\n```\n\n【実装のポイント】\n- セキュアな暗号化ライブラリを使用\n- エラーハンドリングを充実\n- 複数の復号化方式に対応\n\nGeminiが最適化を行います。",
                "「{request}」の実装が完了しました。\n\n【コード構造】\n```\nproject/\n├── main.py          # メインアプリケーション\n├── key_decoder.py   # キー解読モジュール\n├── utils.py         # ユーティリティ関数\n├── tests/           # テストファイル\n└── README.md        # ドキュメント\n```\n\n【テストコード】\n```python\nimport unittest\nfrom key_decoder import KeyDecoder\n\nclass TestKeyDecoder(unittest.TestCase):\n    def setUp(self):\n        self.decoder = KeyDecoder()\n    \n    def test_key_generation(self):\n        key = self.decoder.generate_key()\n        self.assertIsNotNone(key)\n        self.assertIsInstance(key, bytes)\n    \n    def test_key_decoding(self):\n        test_key = \"dGVzdF9rZXk=\"  # base64エンコード済み\n        result = self.decoder.decode_key(test_key, 'base64')\n        self.assertEqual(result, b'test_key')\n\nif __name__ == '__main__':\n    unittest.main()\n```\n\nGeminiで最終チェックをお願いします。"
            ],
            "gemini": [
                "Claudeの実装を最適化しました。\n\n【パフォーマンス改善】\n- メモリ使用量: 30% 削減\n- 処理速度: 50% 向上\n- エラー回復: 自動リトライ機能追加\n\n【セキュリティ強化】\n```python\nimport secrets\nimport logging\nfrom typing import Optional, Union\n\nclass SecureKeyDecoder:\n    def __init__(self):\n        self.logger = logging.getLogger(__name__)\n        \n    def generate_secure_key(self) -> bytes:\n        \"\"\"暗号学的に安全なキーを生成\"\"\"\n        return secrets.token_bytes(32)  # 256-bit key\n    \n    def validate_key_format(self, key: Union[str, bytes]) -> bool:\n        \"\"\"キーフォーマットを検証\"\"\"\n        try:\n            if isinstance(key, str):\n                key = key.encode()\n            return len(key) >= 16  # 最小128-bit\n        except Exception:\n            return False\n    \n    def safe_decode(self, encoded_key: str, method: str = 'base64') -> Optional[bytes]:\n        \"\"\"安全なキーデコード（例外処理強化）\"\"\"\n        try:\n            if not self.validate_key_format(encoded_key):\n                self.logger.warning(\"Invalid key format\")\n                return None\n                \n            if method == 'base64':\n                import base64\n                return base64.b64decode(encoded_key, validate=True)\n            elif method == 'hex':\n                return bytes.fromhex(encoded_key)\n            else:\n                return encoded_key.encode('utf-8')\n                \n        except Exception as e:\n            self.logger.error(f\"Key decode error: {e}\")\n            return None\n```\n\n【総合評価】\n✅ セキュリティ: 高レベル\n✅ パフォーマンス: 最適化済み\n✅ 可読性: 優秀\n✅ テスト: 包括的\n\n「{request}」の実装が完了しました！",
                "最終的な最適化と品質チェックを実行しました。\n\n【実行可能なプロジェクト】\n```bash\n# インストール\npip install cryptography\n\n# 実行\npython main.py\n```\n\n【追加機能】\n1. **GUI版も作成可能**\n```python\nimport tkinter as tk\nfrom tkinter import ttk, filedialog, messagebox\n\nclass KeyDecoderGUI:\n    def __init__(self):\n        self.root = tk.Tk()\n        self.root.title(\"Key Decoder\")\n        self.setup_ui()\n    \n    def setup_ui(self):\n        # キー入力欄\n        ttk.Label(self.root, text=\"暗号化キー:\").pack(pady=5)\n        self.key_entry = ttk.Entry(self.root, width=50)\n        self.key_entry.pack(pady=5)\n        \n        # デコード方式選択\n        ttk.Label(self.root, text=\"方式:\").pack(pady=5)\n        self.method_var = tk.StringVar(value=\"base64\")\n        method_frame = ttk.Frame(self.root)\n        method_frame.pack(pady=5)\n        \n        ttk.Radiobutton(method_frame, text=\"Base64\", variable=self.method_var, value=\"base64\").pack(side=tk.LEFT)\n        ttk.Radiobutton(method_frame, text=\"Hex\", variable=self.method_var, value=\"hex\").pack(side=tk.LEFT)\n        \n        # デコードボタン\n        ttk.Button(self.root, text=\"デコード実行\", command=self.decode_key).pack(pady=10)\n        \n        # 結果表示\n        self.result_text = tk.Text(self.root, height=10, width=60)\n        self.result_text.pack(pady=5)\n```\n\n【プロジェクト完成】\n「{request}」の完全な実装が完了しました！\n- 基本機能: ✅ 完了\n- セキュリティ: ✅ 強化済み\n- GUI版: ✅ 利用可能\n- テスト: ✅ 充実\n- ドキュメント: ✅ 完備"
            ]
        }
    
    def get_response(self, ai_type: str, request: str) -> str:
        """指定されたAIタイプの応答を取得"""
        import random
        responses = self.responses.get(ai_type, ["応答を生成中..."])
        response_template = random.choice(responses)
        try:
            return response_template.format(request=request)
        except KeyError:
            # フォーマット文字列にエラーがある場合は、単純に置換
            return response_template.replace("{request}", request)

# グローバル変数
ai_simulator = SimpleOfflineAI()
active_websockets = {}

@app.get("/")
async def get_index():
    """メインページのHTML"""
    html_content = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>シンプルオフラインAI協調システム</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .status {
            background: #2196F3;
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 12px;
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            background: #f9f9f9;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .message.user {
            background: #e3f2fd;
            margin-left: auto;
            text-align: right;
        }
        
        .message.ai {
            background: #f1f8e9;
        }
        
        .message.system {
            background: #fff3e0;
            text-align: center;
            max-width: 100%;
            font-style: italic;
        }
        
        .message-header {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 12px;
            opacity: 0.7;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }
        
        .input-box {
            flex: 1;
            min-height: 40px;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 20px;
            resize: none;
            font-family: inherit;
        }
        
        .send-btn {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        }
        
        .start-btn {
            background: linear-gradient(135deg, #FF9800, #F57C00);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 20px;
            align-self: center;
        }
        
        .start-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 152, 0, 0.3);
        }
        
        .welcome {
            text-align: center;
            padding: 40px 20px;
            color: #666;
        }
        
        .welcome h2 {
            margin-bottom: 15px;
            color: #333;
        }
        
        .ai-typing {
            display: none;
            padding: 10px;
            font-style: italic;
            color: #666;
            text-align: center;
        }
        
        pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 シンプルオフライン AI協調システム</h1>
            <div class="status">オフライン動作中 - APIキー不要</div>
        </div>
        
        <div class="chat-area">
            <div class="messages" id="messages">
                <div class="welcome">
                    <h2>AI協調開発システムへようこそ！</h2>
                    <p>ChatGPT、Claude、Geminiの3つのAIが協力してプロジェクトを開発します</p>
                    <p>（オフラインシミュレーション - APIキー不要）</p>
                    <button class="start-btn" onclick="startDemo()">デモを開始</button>
                </div>
            </div>
            
            <div class="ai-typing" id="aiTyping">
                AI が考え中... 💭
            </div>
            
            <div class="input-area" id="inputArea" style="display: none;">
                <textarea class="input-box" id="messageInput" placeholder="プロジェクトの内容を入力してください...（例：ユーザー管理システムを作りたい）" onkeypress="handleKeyPress(event)"></textarea>
                <button class="send-btn" onclick="sendMessage()">送信 🚀</button>
            </div>
        </div>
    </div>

    <script>
        let websocket = null;
        let messageId = 0;
        
        function startDemo() {
            document.querySelector('.welcome').style.display = 'none';
            document.getElementById('inputArea').style.display = 'flex';
            addMessage('system', 'デモモードを開始しました。プロジェクトの内容を入力してください。');
            connectWebSocket();
        }
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            websocket = new WebSocket(wsUrl);
            
            websocket.onopen = function() {
                console.log('WebSocket connected');
            };
            
            websocket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            };
            
            websocket.onclose = function() {
                console.log('WebSocket disconnected');
            };
        }
        
        function handleWebSocketMessage(data) {
            if (data.type === 'ai_response') {
                hideTyping();
                addMessage('ai', data.content, data.speaker);
            } else if (data.type === 'system_message') {
                addMessage('system', data.content);
            } else if (data.type === 'ai_thinking') {
                showTyping(data.speaker);
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message || !websocket) return;
            
            addMessage('user', message);
            input.value = '';
            
            websocket.send(JSON.stringify({
                type: 'user_message',
                content: message
            }));
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }
        
        function addMessage(type, content, speaker = null) {
            const messages = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            let header = '';
            if (type === 'user') {
                header = 'あなた';
            } else if (type === 'ai') {
                header = speaker === 'chatgpt' ? 'ChatGPT 🧠' : 
                        speaker === 'claude' ? 'Claude ⚡' : 
                        speaker === 'gemini' ? 'Gemini 💎' : 'AI';
            } else if (type === 'system') {
                header = 'システム 🤖';
            }
            
            messageDiv.innerHTML = `
                <div class="message-header">${header}</div>
                <div>${content.replace(/\\n/g, '<br>').replace(/```([\\s\\S]*?)```/g, '<pre>$1</pre>')}</div>
            `;
            
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function showTyping(speaker) {
            const typing = document.getElementById('aiTyping');
            const speakerName = speaker === 'chatgpt' ? 'ChatGPT' : 
                              speaker === 'claude' ? 'Claude' : 
                              speaker === 'gemini' ? 'Gemini' : 'AI';
            typing.textContent = `${speakerName} が考え中... 💭`;
            typing.style.display = 'block';
        }
        
        function hideTyping() {
            document.getElementById('aiTyping').style.display = 'none';
        }
        
        // 自動でブラウザを開く
        window.addEventListener('load', function() {
            console.log('シンプルオフラインAI協調システムが起動しました');
        });
    </script>
</body>
</html>
    '''
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket接続処理"""
    await websocket.accept()
    connection_id = id(websocket)
    active_websockets[connection_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "user_message":
                content = message_data.get("content", "")
                
                # システムメッセージを送信
                await websocket.send_text(json.dumps({
                    "type": "system_message",
                    "content": f"AI協調開発を開始します: 「{content}」"
                }))
                
                # 3つのAIが順番に応答
                ai_types = ["chatgpt", "claude", "gemini"]
                
                for ai_type in ai_types:
                    # タイピング表示
                    await websocket.send_text(json.dumps({
                        "type": "ai_thinking",
                        "speaker": ai_type
                    }))
                    
                    # 少し待機（リアリティのため）
                    await asyncio.sleep(2)
                    
                    # AI応答を生成
                    response = ai_simulator.get_response(ai_type, content)
                    
                    # 応答を送信
                    await websocket.send_text(json.dumps({
                        "type": "ai_response",
                        "speaker": ai_type,
                        "content": response
                    }))
                    
                    # 次のAIまで少し待機
                    await asyncio.sleep(1)
                
                # 完了メッセージ
                await websocket.send_text(json.dumps({
                    "type": "system_message",
                    "content": "🎉 AI協調開発が完了しました！上記のコードとガイダンスをご活用ください。"
                }))
                
    except WebSocketDisconnect:
        if connection_id in active_websockets:
            del active_websockets[connection_id]

def main():
    """メイン実行関数"""
    print("Simple Offline AI Collaboration System")
    print("=" * 60)
    print("APIキー不要で動作します")
    print("ブラウザが自動で開きます")
    print("ChatGPT + Claude + Gemini の協調開発体験")
    print("Ctrl+C で停止")
    print("=" * 60)
    print()
    
    # ブラウザを自動で開く
    def open_browser():
        import time
        time.sleep(1.5)  # サーバー起動を待つ
        webbrowser.open("http://localhost:8083")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # サーバー起動
    uvicorn.run(app, host="localhost", port=8083, log_level="error")

if __name__ == "__main__":
    main()