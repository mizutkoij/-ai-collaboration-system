# モデル選択機能ガイド

## 機能概要

AI Collaboration SystemのWebUIで、使用するAIモデルを選択できるようになりました。
OpenAIとAnthropicの各種モデルから、プロジェクトに最適なモデルを選択可能です。

## 対応モデル

### OpenAI（ChatGPT）
- **GPT-4**: 最高品質の推論と創造性
- **GPT-4 Turbo**: 高速かつ高品質な処理
- **GPT-3.5 Turbo**: コスト効率的で高速

### Anthropic（Claude）
- **Claude 3 Sonnet**: バランスの取れた性能（推奨）
- **Claude 3 Haiku**: 高速で効率的
- **Claude 3 Opus**: 最高品質の分析とコーディング

### Google（Gemini）
- **Gemini 1.5 Pro**: 高性能で多機能（推奨）
- **Gemini 1.5 Flash**: 高速で効率的な処理
- **Gemini Pro**: 汎用的でバランスの良い性能

## 使用方法

### 1. WebUIでの選択
1. WebUI (`http://localhost:8080`) にアクセス
2. サイドバーの「AIモデル選択」セクションを確認
3. ChatGPT、Claude、Geminiのドロップダウンからモデルを選択
4. 選択は自動的に保存されます

### 2. API接続状態の確認
- サイドバー下部にAPI接続状態が表示されます
- 「全接続済み」: 全3つのAPIキーが設定済み
- 「接続済み」: 2つ以上のAPIキーが設定済み
- 「一部接続」: 1つのAPIキーが設定済み
- 「未接続」: APIキーが未設定

### 3. 会話での使用
- 新しい会話を開始すると、選択されたモデルが使用されます
- 既存の会話でも、モデル変更時に更新されます
- システムメッセージで使用モデルが表示されます

## 設定の保存

### ローカルストレージ
- ブラウザのローカルストレージに設定が保存されます
- ページリロード後も設定が維持されます

### 会話履歴
- 各会話ごとに使用したモデル情報が保存されます
- `conversations/` ディレクトリのJSONファイルに記録されます

## APIキーの設定

モデルを使用するには、対応するAPIキーの設定が必要です：

```bash
# 環境変数として設定
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export GEMINI_API_KEY="your_gemini_api_key"

# または .env ファイルに記載
echo "OPENAI_API_KEY=your_openai_api_key" >> .env
echo "ANTHROPIC_API_KEY=your_anthropic_api_key" >> .env
echo "GEMINI_API_KEY=your_gemini_api_key" >> .env
```

## モデル選択の推奨

### プロジェクトタイプ別推奨モデル

#### ウェブアプリケーション開発
- **ChatGPT**: GPT-4 Turbo
- **Claude**: Claude 3 Sonnet
- **Gemini**: Gemini 1.5 Pro
- 理由: バランスの取れた性能で実用的なコード生成

#### 複雑なシステム設計
- **ChatGPT**: GPT-4
- **Claude**: Claude 3 Opus
- **Gemini**: Gemini 1.5 Pro
- 理由: 最高品質の分析と設計能力

#### プロトタイプ・学習目的
- **ChatGPT**: GPT-3.5 Turbo
- **Claude**: Claude 3 Haiku
- **Gemini**: Gemini 1.5 Flash
- 理由: 高速で効率的、コスト効果的

#### データ分析・処理
- **ChatGPT**: GPT-4
- **Claude**: Claude 3 Opus
- **Gemini**: Gemini 1.5 Pro
- 理由: 高精度な分析と処理能力

#### 高速プロトタイピング
- **ChatGPT**: GPT-4 Turbo
- **Claude**: Claude 3 Haiku
- **Gemini**: Gemini 1.5 Flash
- 理由: 迅速な開発とイテレーション

## 技術仕様

### フロントエンド
- リアルタイム選択変更
- ローカルストレージ自動保存
- WebSocket経由でバックエンドに通知

### バックエンド
- モデル情報をWebSocketメッセージに含める
- 会話データにモデル選択を永続化
- API状態チェック機能

### データ形式
```json
{
  "selected_models": {
    "openai": "gpt-4-turbo",
    "anthropic": "claude-3-sonnet-20240229",
    "gemini": "gemini-1.5-pro"
  }
}
```

## トラブルシューティング

### モデル選択が保存されない
1. ブラウザのJavaScriptが有効になっているか確認
2. ローカルストレージがブロックされていないか確認
3. WebSocket接続が正常か確認

### API接続エラー
1. APIキーが正しく設定されているか確認
2. APIキーに必要な権限があるか確認
3. ネットワーク接続を確認

### モデルが反映されない
1. 新しい会話を開始して確認
2. ページをリフレッシュして再試行
3. ブラウザの開発者ツールでエラーを確認

## 更新履歴

- v1.2.0: Geminiモデル対応を追加
- 3つのAIプロバイダーをサポート (OpenAI + Anthropic + Google)
- 3-way AI協調開発が可能に
- v1.1.0: モデル選択機能を追加
- フロントエンド: サイドバーにモデル選択UI
- バックエンド: モデル情報の保存・取得機能
- API: モデル状態チェック機能

## 今後の予定

- AI協調パターンの最適化
- モデル固有の設定オプション
- 使用量・コスト追跡機能
- カスタムモデル設定
- より多くのAIプロバイダー対応

---

この機能により、3つの主要AIプロバイダー（OpenAI、Anthropic、Google）から最適なモデルを選択し、3-way AI協調開発による強力で効果的な開発体験が可能になりました。各AIの特徴を活かした多角的なアプローチで、より高品質なプロジェクト開発を実現できます。