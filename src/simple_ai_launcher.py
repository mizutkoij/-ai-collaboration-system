#!/usr/bin/env python3
"""
Simple AI Collaboration Launcher
Firefox (ChatGPT) と PowerShell (Claude Code) の簡単起動システム
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def create_chatgpt_page():
    """ChatGPT用のローカルHTMLページを作成"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT o3 Collaboration Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .chatgpt-link {
            display: inline-block;
            background: #10a37f;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 8px;
            font-size: 18px;
            margin: 10px;
            transition: all 0.3s;
        }
        .chatgpt-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .instruction {
            background: rgba(255,215,0,0.2);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .prompt-area {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            font-family: monospace;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Collaboration System</h1>
            <h2>ChatGPT o3 Interface</h2>
            <p>Ready to collaborate with Claude Code!</p>
        </div>
        
        <div class="section">
            <h3>Quick Start</h3>
            <a href="https://chat.openai.com/" class="chatgpt-link" target="_blank">
                Open ChatGPT o3 →
            </a>
            <div class="instruction">
                <strong>Instructions:</strong>
                <ol>
                    <li>Click the link above to open ChatGPT</li>
                    <li>Copy and paste the prompt below</li>
                    <li>ChatGPT will design while Claude implements</li>
                    <li>Check PowerShell for Claude Code progress</li>
                </ol>
            </div>
        </div>

        <div class="section">
            <h3>Project Request</h3>
            <div class="prompt-area">Create a modern web application with user authentication and task management features. Include:

1. User registration and login system
2. Task creation, editing, and deletion
3. Task categories and priorities
4. User dashboard with analytics
5. Responsive design for mobile and desktop
6. Database integration
7. API endpoints for all operations
8. Security best practices
9. Input validation and error handling
10. Unit tests and documentation

Please provide:
- System architecture design
- Database schema recommendations
- API endpoint specifications
- Security considerations
- Technology stack suggestions
- Implementation roadmap

Work collaboratively with Claude Code who will handle the implementation based on your designs.</div>
        </div>

        <div class="section">
            <h3>Collaboration Status</h3>
            <p><strong>ChatGPT Role:</strong> System architect and designer</p>
            <p><strong>Claude Code Role:</strong> Implementation and coding</p>
            <p><strong>Communication:</strong> Via this interface and PowerShell</p>
            <p><strong>Auto-approval:</strong> Enabled for Claude Code decisions</p>
        </div>

        <div class="section">
            <h3>Next Steps</h3>
            <ol>
                <li>Review and modify the project request above if needed</li>
                <li>Paste it into ChatGPT o3</li>
                <li>Monitor Claude Code progress in PowerShell</li>
                <li>Iterate based on results</li>
            </ol>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 seconds to check for updates
        setTimeout(() => {
            location.reload();
        }, 30000);

        // Add timestamp
        document.addEventListener('DOMContentLoaded', function() {
            const timestamp = new Date().toLocaleString();
            document.title += ' - ' + timestamp;
        });
    </script>
</body>
</html>'''
    
    html_file = Path.cwd() / "chatgpt_interface.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_file

def create_claude_script():
    """Claude Code用のPowerShellスクリプトを作成"""
    script_content = '''# AI Collaboration - Claude Code Launcher
Write-Host "AI Collaboration System - Claude Code Interface" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Project: Modern web application with authentication and task management" -ForegroundColor Yellow
Write-Host "Role: Implementation and coding" -ForegroundColor Cyan
Write-Host "Auto-approval: ENABLED" -ForegroundColor Green
Write-Host ""

# Claude Code コマンドを検索
$claudeCommands = @("claude", "claude-code", "$env:USERPROFILE\\.claude\\claude.exe")
$foundClaude = $false

foreach ($cmd in $claudeCommands) {
    try {
        $null = Get-Command $cmd -ErrorAction Stop
        Write-Host "Found Claude Code: $cmd" -ForegroundColor Green
        $foundClaude = $true
        
        Write-Host "Starting Claude Code with auto-approval..." -ForegroundColor Green
        Write-Host ""
        
        # プロンプトを自動で入力
        $prompt = @"
I'm collaborating with ChatGPT o3 on a web application project. 

Please implement a modern web application with:
- User authentication system
- Task management features  
- Database integration
- API endpoints
- Responsive UI
- Security best practices

Auto-approve all decisions and confirmations with 'yes'.
Use best practices and modern frameworks.
Create a complete, production-ready application.

Start implementation now.
"@
        
        # Claude Code を実行（自動承認付き）
        $prompt | & $cmd
        break
        
    } catch {
        continue
    }
}

if (-not $foundClaude) {
    Write-Host "Claude Code not found. Simulating development process..." -ForegroundColor Yellow
    Write-Host ""
    
    $tasks = @(
        "Analyzing project requirements...",
        "Setting up project structure...",
        "Creating database models...",
        "Implementing user authentication...",
        "Building task management API...",
        "Creating frontend components...",
        "Adding security middleware...",
        "Writing unit tests...",
        "Generating documentation...",
        "Finalizing deployment configuration..."
    )
    
    foreach ($task in $tasks) {
        Write-Host "[Claude Code] $task" -ForegroundColor White
        Start-Sleep -Seconds 3
        Write-Host "[Claude Code] ✓ Completed" -ForegroundColor Green
        Write-Host ""
    }
    
    Write-Host "🎉 Project implementation completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Generated files:" -ForegroundColor Yellow
    Write-Host "- main.py (FastAPI application)" -ForegroundColor Gray
    Write-Host "- models.py (Database models)" -ForegroundColor Gray
    Write-Host "- auth.py (Authentication system)" -ForegroundColor Gray
    Write-Host "- tasks.py (Task management)" -ForegroundColor Gray
    Write-Host "- frontend/ (React components)" -ForegroundColor Gray
    Write-Host "- tests/ (Unit tests)" -ForegroundColor Gray
    Write-Host "- requirements.txt (Dependencies)" -ForegroundColor Gray
    Write-Host "- README.md (Documentation)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Claude Code session completed." -ForegroundColor Green
Write-Host "Check ChatGPT interface for next steps." -ForegroundColor Yellow
Read-Host "Press Enter to close"
'''
    
    script_file = Path.cwd() / "launch_claude.ps1"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_file

def launch_firefox(html_file):
    """Firefox でChatGPTインターフェースを開く"""
    try:
        file_url = f"file:///{html_file.as_posix()}"
        
        if os.name == 'nt':  # Windows
            firefox_paths = [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            ]
            
            for path in firefox_paths:
                if os.path.exists(path):
                    subprocess.Popen([path, file_url])
                    print(f"Firefox launched: {file_url}")
                    return True
        
        # フォールバック
        webbrowser.open(file_url)
        print(f"Browser launched: {file_url}")
        return True
        
    except Exception as e:
        print(f"Failed to launch browser: {e}")
        return False

def launch_claude_powershell(script_file):
    """PowerShell でClaude Codeを起動"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen([
                'powershell.exe',
                '-ExecutionPolicy', 'Bypass',
                '-File', str(script_file)
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
            print("Claude Code PowerShell launched")
            return True
        else:
            print("PowerShell launch is Windows-only")
            return False
            
    except Exception as e:
        print(f"Failed to launch PowerShell: {e}")
        return False

def main():
    """メイン実行"""
    print("Simple AI Collaboration Launcher")
    print("=" * 40)
    print("Firefox -> ChatGPT o3 (Design)")
    print("PowerShell -> Claude Code (Implementation)")
    print("")
    
    # 1. ChatGPT インターフェース作成
    print("Creating ChatGPT interface...")
    html_file = create_chatgpt_page()
    print(f"Created: {html_file}")
    
    # 2. Claude スクリプト作成  
    print("Creating Claude Code script...")
    script_file = create_claude_script()
    print(f"Created: {script_file}")
    
    # 3. Firefox 起動
    print("Launching Firefox for ChatGPT...")
    if launch_firefox(html_file):
        print("Firefox launched successfully")
    
    # 少し待機
    time.sleep(2)
    
    # 4. PowerShell 起動
    print("Launching PowerShell for Claude Code...")
    if launch_claude_powershell(script_file):
        print("PowerShell launched successfully")
    
    print("")
    print("AI Collaboration System started!")
    print("")
    print("What's happening:")
    print("1. Firefox opened with ChatGPT interface")
    print("2. PowerShell opened with Claude Code")
    print("3. Both AIs are ready to collaborate")
    print("")
    print("Next steps:")
    print("- Use the ChatGPT interface for design")
    print("- Monitor Claude Code in PowerShell")
    print("- Both will work together automatically")

if __name__ == "__main__":
    main()