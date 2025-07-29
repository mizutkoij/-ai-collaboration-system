#!/usr/bin/env python3
"""
WebUI Server - ユーザーフレンドリーなWeb統合インターフェース
"""

import os
import json
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from enhanced_ai_collaboration import EnhancedAICollaboration
from user_interaction import UserInteractionManager

class ConversationManager:
    """会話の保存と管理"""
    
    def __init__(self):
        self.conversations_dir = Path("conversations")
        self.conversations_dir.mkdir(exist_ok=True)
        self.active_conversations = {}
        
    def create_conversation(self, user_id: str, project_request: str) -> str:
        """新しい会話を作成"""
        conversation_id = str(uuid.uuid4())
        
        conversation_data = {
            "id": conversation_id,
            "user_id": user_id,
            "project_request": project_request,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "messages": [],
            "ai_interactions": [],
            "generated_files": [],
            "user_decisions": []
        }
        
        self.active_conversations[conversation_id] = conversation_data
        self._save_conversation(conversation_id)
        
        return conversation_id
    
    def add_message(self, conversation_id: str, message_type: str, content: str, metadata: Dict = None):
        """メッセージを追加"""
        if conversation_id not in self.active_conversations:
            return False
        
        message = {
            "id": str(uuid.uuid4()),
            "type": message_type,  # user, system, chatgpt, claude, error, decision
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.active_conversations[conversation_id]["messages"].append(message)
        self._save_conversation(conversation_id)
        
        return True
    
    def add_user_decision(self, conversation_id: str, question: str, answer: str, context: Dict = None):
        """ユーザー決定を記録"""
        if conversation_id not in self.active_conversations:
            return False
        
        decision = {
            "id": str(uuid.uuid4()),
            "question": question,
            "answer": answer,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.active_conversations[conversation_id]["user_decisions"].append(decision)
        self._save_conversation(conversation_id)
        
        return True
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """会話を取得"""
        return self.active_conversations.get(conversation_id)
    
    def get_all_conversations(self, user_id: str = None) -> List[Dict]:
        """全ての会話を取得"""
        conversations = []
        
        for file_path in self.conversations_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    conversation = json.load(f)
                    
                if user_id is None or conversation.get("user_id") == user_id:
                    # サマリー情報のみ返す
                    conversations.append({
                        "id": conversation["id"],
                        "project_request": conversation["project_request"],
                        "created_at": conversation["created_at"],
                        "status": conversation["status"],
                        "message_count": len(conversation.get("messages", [])),
                        "decision_count": len(conversation.get("user_decisions", []))
                    })
            except Exception as e:
                print(f"Error loading conversation {file_path}: {e}")
        
        return sorted(conversations, key=lambda x: x["created_at"], reverse=True)
    
    def _save_conversation(self, conversation_id: str):
        """会話をファイルに保存"""
        if conversation_id not in self.active_conversations:
            return
        
        file_path = self.conversations_dir / f"{conversation_id}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.active_conversations[conversation_id], f, 
                     indent=2, ensure_ascii=False)

class WebUIServer:
    """WebUI サーバー"""
    
    def __init__(self):
        self.app = FastAPI(title="AI Collaboration WebUI")
        self.conversation_manager = ConversationManager()
        self.active_websockets = {}
        self.ai_system = None
        
        self._setup_routes()
        self._setup_middleware()
    
    def _setup_middleware(self):
        """ミドルウェアの設定"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """ルートの設定"""
        
        @self.app.get("/")
        async def get_index():
            """メインページ"""
            return FileResponse("templates/webui_main.html")
        
        @self.app.get("/api/conversations")
        async def get_conversations(user_id: str = "default"):
            """会話履歴を取得"""
            conversations = self.conversation_manager.get_all_conversations(user_id)
            return {"conversations": conversations}
        
        @self.app.get("/api/conversations/{conversation_id}")
        async def get_conversation(conversation_id: str):
            """特定の会話を取得"""
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            return conversation
        
        @self.app.post("/api/conversations/start")
        async def start_conversation(request: dict):
            """新しい会話を開始"""
            project_request = request.get("project_request", "")
            user_id = request.get("user_id", "default")
            models = request.get("models", {"openai": "gpt-4", "anthropic": "claude-3-sonnet-20240229", "gemini": "gemini-1.5-pro"})
            
            if not project_request:
                raise HTTPException(status_code=400, detail="Project request is required")
            
            conversation_id = self.conversation_manager.create_conversation(user_id, project_request)
            
            # モデル選択を会話に保存
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if conversation:
                conversation["selected_models"] = models
                self.conversation_manager._save_conversation(conversation_id)
            
            # 開始メッセージを追加
            self.conversation_manager.add_message(
                conversation_id, 
                "system", 
                f"AI Collaboration started for: {project_request}\nUsing models: {models['openai']} + {models['anthropic']} + {models['gemini']}"
            )
            
            return {"conversation_id": conversation_id, "status": "started"}
        
        @self.app.get("/api/check-api-status")
        async def check_api_status():
            """API接続状態をチェック"""
            import os
            return {
                "openai": bool(os.getenv("OPENAI_API_KEY")),
                "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
                "gemini": bool(os.getenv("GEMINI_API_KEY"))
            }
        
        @self.app.websocket("/ws/{conversation_id}")
        async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
            """WebSocket接続"""
            await websocket.accept()
            self.active_websockets[conversation_id] = websocket
            
            try:
                # 既存の会話データを送信
                conversation = self.conversation_manager.get_conversation(conversation_id)
                if conversation:
                    await websocket.send_json({
                        "type": "conversation_data",
                        "data": conversation
                    })
                
                # メッセージループ
                while True:
                    data = await websocket.receive_json()
                    await self._handle_websocket_message(conversation_id, data, websocket)
                    
            except WebSocketDisconnect:
                if conversation_id in self.active_websockets:
                    del self.active_websockets[conversation_id]
    
    async def _handle_websocket_message(self, conversation_id: str, data: dict, websocket: WebSocket):
        """WebSocketメッセージの処理"""
        
        message_type = data.get("type")
        content = data.get("content", "")
        
        if message_type == "user_message":
            # ユーザーメッセージを保存
            self.conversation_manager.add_message(
                conversation_id, "user", content
            )
            
            # モデル選択を取得
            models = data.get("models", {})
            if models:
                # 会話にモデル選択を保存
                conversation = self.conversation_manager.get_conversation(conversation_id)
                if conversation:
                    conversation["selected_models"] = models
                    self.conversation_manager._save_conversation(conversation_id)
            
            # 確認応答
            await websocket.send_json({
                "type": "message_received",
                "content": "Message received"
            })
            
            # メッセージが実際のプロジェクトリクエストの場合、AI協調作業を開始
            if content and len(content.strip()) > 10:  # 実際のリクエストと判断
                ai_data = {
                    "project_request": content,
                    "mode": "full",
                    "models": models
                }
                await self._start_ai_process(conversation_id, ai_data, websocket)
        
        elif message_type == "start_ai_collaboration":
            # AI協調作業を開始
            await self._start_ai_process(conversation_id, data, websocket)
        
        elif message_type == "user_decision":
            # ユーザー決定を処理
            question = data.get("question", "")
            answer = data.get("answer", "")
            context = data.get("context", {})
            
            self.conversation_manager.add_user_decision(
                conversation_id, question, answer, context
            )
            
            await websocket.send_json({
                "type": "decision_recorded",
                "content": f"Decision recorded: {answer}"
            })
        
        elif message_type == "model_selection":
            # モデル選択を更新
            models = data.get("models", {})
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if conversation:
                conversation["selected_models"] = models
                self.conversation_manager._save_conversation(conversation_id)
                
                # システムメッセージを追加
                self.conversation_manager.add_message(
                    conversation_id, 
                    "system", 
                    f"Models updated: {models.get('openai', 'N/A')} + {models.get('anthropic', 'N/A')} + {models.get('gemini', 'N/A')}"
                )
                
                await websocket.send_json({
                    "type": "model_updated",
                    "content": "Model selection updated",
                    "models": models
                })
        
        elif message_type == "get_conversation":
            # 会話データを送信
            conversation = self.conversation_manager.get_conversation(conversation_id)
            await websocket.send_json({
                "type": "conversation_data",
                "data": conversation
            })
    
    async def _start_ai_process(self, conversation_id: str, data: dict, websocket: WebSocket):
        """AI処理を開始"""
        
        try:
            # AI システムを初期化
            if not self.ai_system:
                self.ai_system = EnhancedAICollaboration()
            
            project_request = data.get("project_request", "")
            mode = data.get("mode", "full")
            models = data.get("models", {})
            
            # もしモデルが指定されていない場合、会話から取得
            if not models:
                conversation = self.conversation_manager.get_conversation(conversation_id)
                models = conversation.get("selected_models", {"openai": "gpt-4", "anthropic": "claude-3-sonnet-20240229", "gemini": "gemini-1.5-pro"})
            
            # 処理開始を通知
            await websocket.send_json({
                "type": "ai_process_started",
                "content": f"Starting AI collaboration in {mode} mode...\nUsing: {models.get('openai', 'N/A')} + {models.get('anthropic', 'N/A')} + {models.get('gemini', 'N/A')}"
            })
            
            # AI処理を実行（非同期で）
            asyncio.create_task(
                self._run_ai_collaboration(conversation_id, project_request, mode, websocket, models)
            )
            
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "content": f"Error starting AI process: {str(e)}"
            })
    
    async def _run_ai_collaboration(self, conversation_id: str, project_request: str, mode: str, websocket: WebSocket, models: dict = None):
        """AI協調作業を実行"""
        
        try:
            # カスタム WebSocket 対話マネージャー
            class WebSocketInteractionManager(UserInteractionManager):
                def __init__(self, websocket, conversation_id, conversation_manager):
                    super().__init__()
                    self.websocket = websocket
                    self.conversation_id = conversation_id
                    self.conversation_manager = conversation_manager
                    self.pending_decisions = {}
                
                async def ask_user_decision_async(self, question: str, options: List[str] = None, default: str = None, context: Dict = None):
                    """非同期でユーザー決定を求める"""
                    
                    decision_id = str(uuid.uuid4())
                    
                    # 質問を送信
                    await self.websocket.send_json({
                        "type": "user_decision_required",
                        "decision_id": decision_id,
                        "question": question,
                        "options": options or [],
                        "default": default,
                        "context": context or {}
                    })
                    
                    # 応答を待機
                    self.pending_decisions[decision_id] = None
                    
                    # タイムアウト付きで応答を待つ
                    timeout = 300  # 5分
                    start_time = asyncio.get_event_loop().time()
                    
                    while self.pending_decisions[decision_id] is None:
                        if asyncio.get_event_loop().time() - start_time > timeout:
                            # タイムアウト時はデフォルト値を使用
                            response = default or "timeout"
                            break
                        
                        await asyncio.sleep(0.5)
                    
                    response = self.pending_decisions.pop(decision_id, default or "no_response")
                    
                    # 決定を記録
                    self.conversation_manager.add_user_decision(
                        self.conversation_id, question, response, context
                    )
                    
                    return response
            
            # WebSocket対話マネージャーを設定
            websocket_interaction = WebSocketInteractionManager(
                websocket, conversation_id, self.conversation_manager
            )
            
            # AI システムに WebSocket 対話マネージャーを設定
            self.ai_system.user_interaction = websocket_interaction
            
            # 進捗更新を送信する関数
            async def send_progress(phase: str, message: str):
                await websocket.send_json({
                    "type": "progress_update",
                    "phase": phase,
                    "content": message
                })
                
                self.conversation_manager.add_message(
                    conversation_id, "system", f"[{phase}] {message}"
                )
            
            # デフォルトモデル設定
            if not models:
                models = {"openai": "gpt-4", "anthropic": "claude-3-sonnet-20240229", "gemini": "gemini-1.5-pro"}
            
            # 各フェーズで進捗を送信
            await send_progress("initialization", f"Initializing AI collaboration system...\nUsing models: {models['openai']} + {models['anthropic']} + {models['gemini']}")
            
            if mode in ["full", "design"]:
                await send_progress("design", "Starting design phase with o4...")
            
            if mode in ["full", "implementation"]:
                await send_progress("implementation", "ChatGPT and Claude starting implementation...")
            
            # 実際のAI処理を実行
            results = self.ai_system.run_complete_workflow_with_interaction(project_request, mode)
            
            # 結果を送信
            await websocket.send_json({
                "type": "ai_process_completed",
                "results": results
            })
            
            # 最終メッセージを保存
            self.conversation_manager.add_message(
                conversation_id, 
                "system", 
                f"AI collaboration completed. Status: {results.get('status', 'unknown')}"
            )
            
        except Exception as e:
            error_message = f"AI collaboration error: {str(e)}"
            
            await websocket.send_json({
                "type": "error",
                "content": error_message
            })
            
            self.conversation_manager.add_message(
                conversation_id, "error", error_message
            )
    
    def run(self, host: str = "localhost", port: int = 8080):
        """サーバーを起動"""
        print("Starting AI Collaboration WebUI Server")
        print(f"Access at: http://{host}:{port}")
        print(f"Conversations saved to: {self.conversation_manager.conversations_dir}")
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info"
        )

def main():
    """メイン実行"""
    server = WebUIServer()
    server.run()

if __name__ == "__main__":
    main()