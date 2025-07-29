# 🤖 Interactive AI Collaboration Example

## Enhanced User Interaction Features

このシステムは問題発生時やユーザー判断が必要な時に自動的に対話を開始します。

## 🔄 典型的な対話フロー

### 1. プロジェクト開始時の確認
```
🔍 CONFIRMATION REQUIRED
==================================================
Action: Start AI collaboration for: Create a modern e-commerce website
Details:
  - mode: full
  - estimated_time: 5-10 minutes

Are you sure you want to proceed with: Start AI collaboration for: Create a modern e-commerce website?
1. yes
2. no

Your decision: yes
✓ Decision recorded: yes
```

### 2. 設計レビュー時の対話
```
📋 Design Review
==================================================
Project: Modern E-commerce Platform
Technology: React, Node.js, MongoDB, Stripe
Features:
  - User authentication and profiles
  - Product catalog with search
  - Shopping cart functionality
  - Payment processing
  - Order management
  - Admin dashboard

Do you approve this design?
1. yes
2. no  
3. modify

Your decision: modify

📝 INPUT REQUIRED
==================================================
What modifications would you like to make to the design?

Input: Add real-time chat support and product reviews
✓ Input recorded: Add real-time chat support and product reviews
```

### 3. エラー発生時の問題解決
```
❌ ERROR OCCURRED
==================================================
Error: API key not found for OpenAI service
Type: ConfigurationError
Context: {
  "phase": "implementation",
  "retry_count": 1,
  "max_retries": 3
}

💡 Suggested Solutions:
  1. Check if API keys are set in environment variables
  2. Verify API key format and validity
  3. Check API key permissions and quotas

🤔 USER DECISION REQUIRED
==================================================
How would you like to proceed?
1. retry
2. skip
3. abort
4. manual_fix
5. solution_1
6. solution_2
7. solution_3

Your decision: solution_1
✓ Decision recorded: solution_1

🔧 Applying solution: Check if API keys are set in environment variables
```

### 4. 問題解決セッション
```
🔧 PROBLEM SOLVING SESSION
============================================================
Problem: Claude Code is not responding to implementation requests

Already tried:
  1. Restart the application
  2. Check API connectivity

Let's work together to solve this problem.

🤔 USER DECISION REQUIRED
==================================================
What would you like to do?
1. Suggest a solution
2. Provide more information
3. Try automated troubleshooting
4. Skip this problem
5. Abort the process

Your decision: Try automated troubleshooting
✓ Decision recorded: Try automated troubleshooting

🤖 Running automated troubleshooting...
✓ Generated 4 potential solutions:
  - Check internet connection
  - Verify firewall settings
  - Try different network endpoint
  - Clear temporary files
```

### 5. ファイル生成時の確認
```
📁 Phase 3: File Generation
Files to be generated:
  - main.py: Main application file
  - package.json: Node.js dependencies
  - components/: React components directory
  - api/: Backend API routes
  - database/: Database models and migrations
  - tests/: Test files
  - README.md: Project documentation
  - docker-compose.yml: Container configuration

🔍 CONFIRMATION REQUIRED
==================================================
Action: Generate 8 files
Details:
  - output_directory: ./generated_projects

Are you sure you want to proceed with: Generate 8 files?
1. yes
2. no

Your decision: yes
✓ Decision recorded: yes

✅ Successfully generated 8 files:
  ✓ ./generated_projects/ecommerce-app/main.py
  ✓ ./generated_projects/ecommerce-app/package.json
  ✓ ./generated_projects/ecommerce-app/components/Header.jsx
  ✓ ./generated_projects/ecommerce-app/components/ProductCard.jsx
  ✓ ./generated_projects/ecommerce-app/api/products.js
  ✓ ./generated_projects/ecommerce-app/api/auth.js
  ✓ ./generated_projects/ecommerce-app/tests/api.test.js
  ✓ ./generated_projects/ecommerce-app/README.md
```

## 🎯 主要な対話機能

### ✅ 自動エラーハンドリング
- API接続エラー → 自動解決策提案
- ファイル権限エラー → 権限修正提案
- ネットワークエラー → 接続診断と修正

### ✅ インテリジェントな確認
- 重要な決定 → ユーザー確認を求める
- リスクのある操作 → 詳細説明と選択肢
- 設定変更 → 影響範囲の説明

### ✅ 柔軟な入力システム
- テキスト入力 → 自由記述
- 選択式 → 番号または文字列選択
- ファイルパス → 存在確認付き入力
- Yes/No → 明確な二択

### ✅ 問題解決支援
- 自動トラブルシューティング
- 段階的な解決プロセス
- ユーザーとAIの協調問題解決

## 🚀 使用方法

```bash
# Enhanced版を使用
python src/enhanced_ai_collaboration.py

# または通常版に対話機能を追加
python src/ai_collaboration_core.py run "your project" --interactive
```

## 📊 対話ログの保存

全ての対話は自動的にログファイルに保存されます：
```
interaction_log_20241129_143022.json
```

ログには以下が含まれます：
- 全ての質問と回答
- エラーと解決策
- 決定の理由とコンテキスト
- タイムスタンプ付きの完全な履歴