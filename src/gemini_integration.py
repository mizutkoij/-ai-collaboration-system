#!/usr/bin/env python3
"""
Gemini AI Integration for AI Collaboration System
"""

import os
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

class GeminiPersona:
    """Gemini AIのペルソナ"""
    
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model_name = model_name
        self.client = None
        self.conversation_history = []
        
        if GEMINI_AVAILABLE:
            self._initialize_client()
        
    def _initialize_client(self):
        """Gemini クライアントを初期化"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables")
            return
        
        try:
            genai.configure(api_key=api_key)
            
            # 安全設定を設定
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            # 生成設定
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            self.client = genai.GenerativeModel(
                model_name=self.model_name,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            print(f"Gemini client initialized with model: {self.model_name}")
            
        except Exception as e:
            print(f"Failed to initialize Gemini client: {e}")
            self.client = None

    def generate_response(self, project_request: str, conversation_log: list, turn: int) -> str:
        """Gemini風の応答を生成"""
        
        # Gemini が利用できない場合はシミュレーション応答
        if not GEMINI_AVAILABLE or not self.client:
            return self._get_simulation_response(project_request, turn)
        
        try:
            # プロンプトを作成
            system_prompt = """あなたはAI協調開発システムのGemini担当です。ChatGPTとClaudeと連携して、ユーザーのプロジェクトを実装します。

役割:
- 高速で効率的な実装支援
- 多機能な分析とコード生成
- 実用的なソリューション提案
- プロジェクト管理とワークフロー最適化

常に以下を心がけてください:
- 実用的で実装可能な提案
- 明確で読みやすいコード
- 効率的なアプローチ
- 他のAIとの協調"""

            # 会話履歴から文脈を構築
            context = self._build_context(conversation_log, project_request)
            
            # 完全なプロンプトを作成
            full_prompt = f"{system_prompt}\n\n{context}\n\nターン {turn}: {project_request} について、実装とコード生成の観点から回答してください。"
            
            # Gemini API呼び出し
            response = self.client.generate_content(full_prompt)
            
            if response.text:
                return response.text
            else:
                return self._get_simulation_response(project_request, turn)
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._get_simulation_response(project_request, turn)

    def _build_context(self, conversation_log: list, project_request: str) -> str:
        """会話履歴から文脈を構築"""
        context_parts = [f"プロジェクトリクエスト: {project_request}"]
        
        if conversation_log:
            context_parts.append("\n会話履歴:")
            for msg in conversation_log[-5:]:  # 最新5件のみ
                speaker = msg.get("speaker", "unknown")
                content = msg.get("content", "")[:200]  # 200文字に制限
                context_parts.append(f"{speaker}: {content}")
        
        return "\n".join(context_parts)

    def _get_simulation_response(self, project_request: str, turn: int) -> str:
        """シミュレーション応答（Gemini APIが利用できない場合）"""
        
        responses = [
            # 高速実装開始
            f"Gemini です！{project_request} の高速実装を開始します。\n\n```python\n# 効率的なプロジェクト構造\nfrom fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\nimport uvicorn\n\napp = FastAPI(title=\"AI Generated Project\")\n\nclass ProjectConfig(BaseModel):\n    name: str\n    version: str = \"1.0.0\"\n    features: list = []\n\n@app.get(\"/\")\ndef read_root():\n    return {{\"message\": \"Project initialized successfully\"}}\n\n@app.get(\"/health\")\ndef health_check():\n    return {{\"status\": \"healthy\", \"timestamp\": datetime.now()}}\n\nif __name__ == \"__main__\":\n    uvicorn.run(app, host=\"0.0.0.0\", port=8000)\n```\n\n✅ 作成: main.py - 高速APIサーバー",
            
            # 多機能分析
            f"プロジェクト分析完了！多角的なアプローチを提案します。\n\n```python\n# データベース設計\nfrom sqlalchemy import create_engine, Column, Integer, String, DateTime\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\nfrom datetime import datetime\n\nBase = declarative_base()\n\nclass Project(Base):\n    __tablename__ = \"projects\"\n    \n    id = Column(Integer, primary_key=True)\n    name = Column(String(100), nullable=False)\n    description = Column(String(500))\n    created_at = Column(DateTime, default=datetime.utcnow)\n    status = Column(String(20), default=\"active\")\n\n# 効率的な設定管理\nclass Config:\n    DATABASE_URL = \"sqlite:///./project.db\"\n    DEBUG = True\n    CORS_ORIGINS = [\"*\"]\n```\n\n✅ 作成: models.py + config.py",
            
            # 実用的ソリューション
            f"実用的なソリューションを実装中...\n\n```python\n# ユーティリティ関数群\nimport json\nimport logging\nfrom pathlib import Path\nfrom typing import Dict, Any, Optional\n\nclass ProjectManager:\n    def __init__(self, project_dir: str):\n        self.project_dir = Path(project_dir)\n        self.config_file = self.project_dir / \"config.json\"\n        self.setup_logging()\n    \n    def setup_logging(self):\n        logging.basicConfig(\n            level=logging.INFO,\n            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\n            handlers=[\n                logging.FileHandler('project.log'),\n                logging.StreamHandler()\n            ]\n        )\n        self.logger = logging.getLogger(__name__)\n    \n    def create_structure(self):\n        dirs = ['src', 'tests', 'docs', 'config', 'static']\n        for dir_name in dirs:\n            (self.project_dir / dir_name).mkdir(exist_ok=True)\n        self.logger.info(\"Project structure created\")\n```\n\n✅ 作成: utils.py - プロジェクト管理",
            
            # ワークフロー最適化
            f"ワークフローを最適化します！\n\n```yaml\n# docker-compose.yml - 効率的な開発環境\nversion: '3.8'\nservices:\n  app:\n    build: .\n    ports:\n      - \"8000:8000\"\n    volumes:\n      - .:/app\n    environment:\n      - PYTHONPATH=/app\n      - DEBUG=1\n    depends_on:\n      - db\n      - redis\n  \n  db:\n    image: postgres:15\n    environment:\n      POSTGRES_DB: projectdb\n      POSTGRES_USER: user\n      POSTGRES_PASSWORD: password\n    volumes:\n      - postgres_data:/var/lib/postgresql/data\n  \n  redis:\n    image: redis:7-alpine\n    ports:\n      - \"6379:6379\"\n\nvolumes:\n  postgres_data:\n```\n\n```python\n# tasks.py - タスク管理\nfrom celery import Celery\nimport redis\n\napp = Celery('project_tasks')\napp.config_from_object('celery_config')\n\n@app.task\ndef process_data(data):\n    # 非同期データ処理\n    return {{\"processed\": True, \"items\": len(data)}}\n```\n\n✅ 作成: docker-compose.yml + tasks.py",
            
            # テスト実装
            f"包括的なテストを実装します！\n\n```python\n# tests/test_main.py\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom main import app\n\nclient = TestClient(app)\n\ndef test_read_root():\n    response = client.get(\"/\")\n    assert response.status_code == 200\n    assert \"message\" in response.json()\n\ndef test_health_check():\n    response = client.get(\"/health\")\n    assert response.status_code == 200\n    assert response.json()[\"status\"] == \"healthy\"\n\n@pytest.fixture\ndef sample_project():\n    return {{\n        \"name\": \"Test Project\",\n        \"version\": \"1.0.0\",\n        \"features\": [\"api\", \"database\", \"tests\"]\n    }}\n\ndef test_project_creation(sample_project):\n    response = client.post(\"/projects\", json=sample_project)\n    assert response.status_code == 201\n```\n\n✅ 作成: tests/ - 完全なテストスイート",
            
            # パフォーマンス最適化
            f"パフォーマンス最適化を実装！\n\n```python\n# performance.py - 最適化ツール\nimport asyncio\nimport aiohttp\nfrom functools import lru_cache\nfrom typing import List, Dict\n\nclass OptimizedProcessor:\n    def __init__(self):\n        self.session = None\n    \n    async def __aenter__(self):\n        self.session = aiohttp.ClientSession()\n        return self\n    \n    async def __aexit__(self, exc_type, exc_val, exc_tb):\n        if self.session:\n            await self.session.close()\n    \n    @lru_cache(maxsize=100)\n    def cached_computation(self, input_data: str) -> str:\n        # 計算結果をキャッシュ\n        return f\"processed_{input_data}\"\n    \n    async def batch_process(self, items: List[Dict]):\n        tasks = []\n        async with self.session as session:\n            for item in items:\n                task = asyncio.create_task(\n                    self.process_item(session, item)\n                )\n                tasks.append(task)\n            \n            results = await asyncio.gather(*tasks)\n            return results\n```\n\n✅ 作成: performance.py - 高速処理システム",
            
            # 完成報告
            f"Gemini実装完了！効率的なシステムが構築されました。\n\n📊 **実装サマリー:**\n- ✅ 高速APIサーバー (FastAPI)\n- ✅ データベース設計 (SQLAlchemy)\n- ✅ プロジェクト管理ツール\n- ✅ Docker開発環境\n- ✅ 非同期タスク処理 (Celery)\n- ✅ 包括的テストスイート\n- ✅ パフォーマンス最適化\n\n🚀 **特徴:**\n- 高速・効率的な実装\n- スケーラブルなアーキテクチャ\n- 開発者フレンドリーな構造\n- 本番環境対応\n\n💡 **次のステップ:**\n1. 環境変数設定\n2. データベースマイグレーション実行\n3. テスト実行で品質確認\n4. Docker環境でデプロイ\n\nGeminiが提供する高速で多機能な実装により、堅牢なシステムが完成しました！"
        ]
        
        # ターンに基づいて応答を選択
        response_index = (turn - 1) % len(responses)
        return responses[response_index]

class GeminiIntegration:
    """Gemini統合システム"""
    
    def __init__(self):
        self.personas = {}
        self.available = GEMINI_AVAILABLE
        
    def get_persona(self, model_name: str = "gemini-1.5-pro") -> GeminiPersona:
        """指定されたモデルのペルソナを取得"""
        if model_name not in self.personas:
            self.personas[model_name] = GeminiPersona(model_name)
        return self.personas[model_name]
    
    def is_available(self) -> bool:
        """Gemini APIが利用可能か確認"""
        return self.available and bool(os.getenv("GEMINI_API_KEY"))
    
    def get_supported_models(self) -> List[str]:
        """サポートされているモデル一覧"""
        return [
            "gemini-1.5-pro",
            "gemini-1.5-flash", 
            "gemini-pro"
        ]

# シングルトンインスタンス
gemini_integration = GeminiIntegration()

def get_gemini_integration() -> GeminiIntegration:
    """Gemini統合インスタンスを取得"""
    return gemini_integration