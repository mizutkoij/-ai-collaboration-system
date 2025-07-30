#!/bin/bash

echo "🤖 AI協調システム - オフライン版"
echo "=================================="
echo "✅ APIキー不要 - 完全オフライン動作"
echo "🌐 ブラウザが自動で開きます: http://localhost:8084"
echo "🤖 ChatGPT + Claude + Gemini = 協調開発"
echo "⏹️  Ctrl+C でシステム停止"
echo "=================================="
echo ""
echo "システムを起動中..."
echo ""

python3 ultra_simple_offline.py

echo ""
echo "=================================="
echo "AI協調システムが停止しました"
echo "いつでも ./start_offline_ai.sh で再起動できます"
echo "=================================="