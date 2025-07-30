# 🚀 AI協調システム クイックスタートガイド

## 📦 最も簡単な起動方法

### 1. 超シンプル版（推奨）
```bash
python ultra_simple_offline.py
```
- ✅ APIキー不要
- ✅ 自動でブラウザが開く
- ✅ 完全オフライン動作
- ✅ http://localhost:8084 でアクセス

### 2. 高機能版
```bash
python launch_webui.py
```
- 🔑 APIキー必要（または自動でオフラインモードに切り替え）
- 🌐 http://localhost:8082 でアクセス
- 📊 詳細な機能とモード選択

## 🎯 使用方法

### 超シンプル版の場合
1. **起動**: `python ultra_simple_offline.py`
2. **ブラウザアクセス**: 自動で開く（または http://localhost:8084）
3. **システム開始**: 「システム開始」ボタンをクリック
4. **プロジェクト入力**: 「keyの解読プログラムを作りたい」など
5. **AI協調観察**: ChatGPT → Claude → Gemini の順で自動実行

### 高機能版の場合
1. **起動**: `python launch_webui.py`
2. **ブラウザアクセス**: http://localhost:8082
3. **モード選択**: 
   - 3-way協調 (推奨)
   - ChatGPTのみ
   - Claudeのみ  
   - Geminiのみ
   - オフライン (API不要)
4. **新しい会話**: 「+ 新しい会話を開始」
5. **プロジェクト開発**: AI協調開発を体験

## 🔑 APIキー設定（高機能版で実際のAIを使う場合）

### 環境変数で設定
```bash
# Windows
set OPENAI_API_KEY=your_openai_key
set ANTHROPIC_API_KEY=your_anthropic_key
set GEMINI_API_KEY=your_gemini_key

# Linux/Mac
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
export GEMINI_API_KEY="your_gemini_key"
```

### .envファイルで設定
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
```

## 📝 APIキー取得先

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google AI Studio**: https://makersuite.google.com/app/apikey

## 🛠️ トラブルシューティング

### ポートが使用中の場合
```python
# ultra_simple_offline.py の最後の行を変更
uvicorn.run(app, host="localhost", port=8085)  # ポート番号を変更
```

### ブラウザが開かない場合
- 手動で http://localhost:8084 にアクセス

### 依存関係エラーの場合
```bash
pip install fastapi uvicorn websockets
```

## 🎉 完全オフライン体験

**ultra_simple_offline.py** を使えば：
- インターネット接続不要
- APIキー不要
- リアルなAI協調開発体験
- 3つのAI（ChatGPT、Claude、Gemini）が順番に作業
- 実際のコード生成とプロジェクト指導

**完全に自己完結したシステムです！**