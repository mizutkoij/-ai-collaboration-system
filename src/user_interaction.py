#!/usr/bin/env python3
"""
User Interaction System - 問題発生時やユーザー判断が必要な時の対話システム
"""

import sys
import json
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path
from enum import Enum

class InteractionType(Enum):
    ERROR = "error"
    WARNING = "warning"
    DECISION = "decision"
    CONFIRMATION = "confirmation"
    INPUT_REQUEST = "input_request"
    PROBLEM_SOLVING = "problem_solving"

class UserInteractionManager:
    """ユーザーとの対話を管理するクラス"""
    
    def __init__(self, auto_mode: bool = False):
        self.auto_mode = auto_mode
        self.interaction_history = []
        self.default_responses = {}
        
    def ask_user_decision(self, 
                         question: str, 
                         options: List[str] = None,
                         default: str = None,
                         context: Dict[str, Any] = None) -> str:
        """ユーザーに決定を求める"""
        
        interaction = {
            "type": InteractionType.DECISION,
            "question": question,
            "options": options or [],
            "default": default,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*60}")
        print(f"🤔 USER DECISION REQUIRED")
        print(f"{'='*60}")
        
        if context:
            print(f"Context: {context.get('description', 'No additional context')}")
            if context.get('current_task'):
                print(f"Current Task: {context['current_task']}")
        
        print(f"\nQuestion: {question}")
        
        if options:
            print(f"\nAvailable options:")
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
        
        if default:
            print(f"\nDefault: {default}")
        
        # 自動モードの場合
        if self.auto_mode and default:
            print(f"[AUTO MODE] Using default: {default}")
            response = default
        else:
            try:
                if options:
                    response = input(f"\nEnter your choice (1-{len(options)}) or text: ").strip()
                    
                    # 数字の場合は選択肢から選択
                    if response.isdigit():
                        choice_idx = int(response) - 1
                        if 0 <= choice_idx < len(options):
                            response = options[choice_idx]
                else:
                    response = input(f"\nYour decision: ").strip()
                
                if not response and default:
                    response = default
                    print(f"Using default: {default}")
                    
            except (EOFError, KeyboardInterrupt):
                if default:
                    response = default
                    print(f"\nUsing default due to input error: {default}")
                else:
                    response = "skip"
                    print(f"\nSkipping due to input error")
        
        interaction["response"] = response
        self.interaction_history.append(interaction)
        
        print(f"✓ Decision recorded: {response}")
        return response

    def handle_error(self, 
                    error: Exception,
                    context: Dict[str, Any] = None,
                    suggested_solutions: List[str] = None) -> Dict[str, Any]:
        """エラー発生時の対話"""
        
        interaction = {
            "type": InteractionType.ERROR,
            "error": str(error),
            "error_type": type(error).__name__,
            "context": context or {},
            "suggested_solutions": suggested_solutions or [],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*60}")
        print(f"❌ ERROR OCCURRED")
        print(f"{'='*60}")
        
        print(f"Error: {error}")
        print(f"Type: {type(error).__name__}")
        
        if context:
            print(f"Context: {json.dumps(context, indent=2, ensure_ascii=False)}")
        
        if suggested_solutions:
            print(f"\n💡 Suggested Solutions:")
            for i, solution in enumerate(suggested_solutions, 1):
                print(f"  {i}. {solution}")
        
        options = ["retry", "skip", "abort", "manual_fix"]
        if suggested_solutions:
            options.extend([f"solution_{i}" for i in range(1, len(suggested_solutions) + 1)])
        
        response = self.ask_user_decision(
            "How would you like to proceed?",
            options,
            default="retry",
            context={"error": str(error), "solutions_available": bool(suggested_solutions)}
        )
        
        interaction["user_response"] = response
        self.interaction_history.append(interaction)
        
        return {
            "action": response,
            "retry": response == "retry",
            "skip": response == "skip", 
            "abort": response == "abort",
            "solution_index": self._extract_solution_index(response) if "solution_" in response else None
        }

    def ask_for_input(self, 
                     prompt: str,
                     input_type: str = "text",
                     validation: Optional[callable] = None,
                     context: Dict[str, Any] = None) -> Any:
        """ユーザーに入力を求める"""
        
        interaction = {
            "type": InteractionType.INPUT_REQUEST,
            "prompt": prompt,
            "input_type": input_type,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*50}")
        print(f"📝 INPUT REQUIRED")
        print(f"{'='*50}")
        
        if context:
            print(f"Context: {context.get('description', '')}")
        
        print(f"\n{prompt}")
        
        while True:
            try:
                if input_type == "file_path":
                    user_input = input("File path: ").strip()
                    if user_input and Path(user_input).exists():
                        break
                    elif user_input:
                        print(f"❌ File not found: {user_input}")
                        continue
                    else:
                        print("❌ File path cannot be empty")
                        continue
                        
                elif input_type == "number":
                    user_input = input("Number: ").strip()
                    try:
                        user_input = float(user_input)
                        break
                    except ValueError:
                        print("❌ Please enter a valid number")
                        continue
                        
                elif input_type == "yes_no":
                    user_input = input("(y/n): ").strip().lower()
                    if user_input in ['y', 'yes', 'n', 'no']:
                        user_input = user_input in ['y', 'yes']
                        break
                    else:
                        print("❌ Please enter y/yes or n/no")
                        continue
                        
                else:  # text
                    user_input = input("Input: ").strip()
                    if user_input:
                        break
                    else:
                        print("❌ Input cannot be empty")
                        continue
                
                # Custom validation
                if validation and not validation(user_input):
                    print("❌ Invalid input. Please try again.")
                    continue
                    
                break
                
            except (EOFError, KeyboardInterrupt):
                print(f"\n⏸️ Input cancelled by user")
                return None
        
        interaction["user_input"] = user_input
        self.interaction_history.append(interaction)
        
        print(f"✓ Input recorded: {user_input}")
        return user_input

    def show_warning(self, 
                    message: str,
                    context: Dict[str, Any] = None,
                    require_confirmation: bool = False) -> bool:
        """警告を表示"""
        
        interaction = {
            "type": InteractionType.WARNING,
            "message": message,
            "context": context or {},
            "require_confirmation": require_confirmation,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*50}")
        print(f"⚠️ WARNING")
        print(f"{'='*50}")
        
        print(f"Message: {message}")
        
        if context:
            print(f"Details: {json.dumps(context, indent=2, ensure_ascii=False)}")
        
        if require_confirmation:
            response = self.ask_user_decision(
                "Do you want to continue despite this warning?",
                ["yes", "no"],
                default="no",
                context={"warning": message}
            )
            
            interaction["user_confirmed"] = response == "yes"
            self.interaction_history.append(interaction)
            
            return response == "yes"
        else:
            self.interaction_history.append(interaction)
            input("\nPress Enter to continue...")
            return True

    def request_confirmation(self, 
                           action: str,
                           details: Dict[str, Any] = None,
                           default: bool = False) -> bool:
        """確認を求める"""
        
        interaction = {
            "type": InteractionType.CONFIRMATION,
            "action": action,
            "details": details or {},
            "default": default,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*50}")
        print(f"🔍 CONFIRMATION REQUIRED")
        print(f"{'='*50}")
        
        print(f"Action: {action}")
        
        if details:
            print(f"Details:")
            for key, value in details.items():
                print(f"  - {key}: {value}")
        
        response = self.ask_user_decision(
            f"Are you sure you want to proceed with: {action}?",
            ["yes", "no"],
            default="yes" if default else "no"
        )
        
        confirmed = response == "yes"
        interaction["confirmed"] = confirmed
        self.interaction_history.append(interaction)
        
        return confirmed

    def problem_solving_session(self, 
                               problem_description: str,
                               attempted_solutions: List[str] = None) -> Dict[str, Any]:
        """問題解決のための対話セッション"""
        
        print(f"\n{'='*60}")
        print(f"🔧 PROBLEM SOLVING SESSION")
        print(f"{'='*60}")
        
        print(f"Problem: {problem_description}")
        
        if attempted_solutions:
            print(f"\nAlready tried:")
            for i, solution in enumerate(attempted_solutions, 1):
                print(f"  {i}. {solution}")
        
        solutions_to_try = []
        
        print(f"\nLet's work together to solve this problem.")
        
        while True:
            action = self.ask_user_decision(
                "What would you like to do?",
                [
                    "Suggest a solution",
                    "Provide more information", 
                    "Try automated troubleshooting",
                    "Skip this problem",
                    "Abort the process"
                ],
                default="Try automated troubleshooting"
            )
            
            if action == "Suggest a solution":
                solution = self.ask_for_input(
                    "Please describe your suggested solution:",
                    "text"
                )
                if solution:
                    solutions_to_try.append(solution)
                    print(f"✓ Solution added: {solution}")
                    
            elif action == "Provide more information":
                info = self.ask_for_input(
                    "Please provide additional information about the problem:",
                    "text"
                )
                if info:
                    print(f"✓ Additional info recorded: {info}")
                    
            elif action == "Try automated troubleshooting":
                print("🤖 Running automated troubleshooting...")
                # ここで自動トラブルシューティングのロジック
                auto_solutions = self._generate_automated_solutions(problem_description)
                solutions_to_try.extend(auto_solutions)
                print(f"✓ Generated {len(auto_solutions)} potential solutions")
                
            elif action in ["Skip this problem", "Abort the process"]:
                break
        
        return {
            "problem": problem_description,
            "user_solutions": solutions_to_try,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }

    def _extract_solution_index(self, response: str) -> Optional[int]:
        """solution_X形式から番号を抽出"""
        if response.startswith("solution_"):
            try:
                return int(response.split("_")[1])
            except (IndexError, ValueError):
                return None
        return None

    def _generate_automated_solutions(self, problem: str) -> List[str]:
        """問題に基づいて自動的な解決策を生成"""
        solutions = []
        
        problem_lower = problem.lower()
        
        if "api" in problem_lower and "key" in problem_lower:
            solutions.extend([
                "Check if API keys are set in environment variables",
                "Verify API key format and validity",
                "Check API key permissions and quotas"
            ])
        
        if "file" in problem_lower and "not found" in problem_lower:
            solutions.extend([
                "Check if file path is correct",
                "Verify file permissions",
                "Create missing directories"
            ])
        
        if "network" in problem_lower or "connection" in problem_lower:
            solutions.extend([
                "Check internet connection",
                "Verify firewall settings", 
                "Try different network endpoint"
            ])
        
        if "permission" in problem_lower:
            solutions.extend([
                "Run with administrator privileges",
                "Check file/folder permissions",
                "Change ownership of files"
            ])
        
        # デフォルトの一般的な解決策
        if not solutions:
            solutions.extend([
                "Restart the application",
                "Check system requirements",
                "Update dependencies",
                "Clear temporary files"
            ])
        
        return solutions

    def get_interaction_summary(self) -> Dict[str, Any]:
        """対話履歴の要約を取得"""
        total_interactions = len(self.interaction_history)
        
        by_type = {}
        for interaction in self.interaction_history:
            interaction_type = interaction["type"]
            if interaction_type not in by_type:
                by_type[interaction_type] = 0
            by_type[interaction_type] += 1
        
        return {
            "total_interactions": total_interactions,
            "by_type": by_type,
            "history": self.interaction_history,
            "generated_at": datetime.now().isoformat()
        }

    def save_interaction_log(self, filepath: str = None) -> str:
        """対話ログを保存"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"interaction_log_{timestamp}.json"
        
        summary = self.get_interaction_summary()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Interaction log saved: {filepath}")
        return filepath


# グローバルインスタンス
user_interaction = UserInteractionManager()

# 便利な関数
def ask_user(question: str, options: List[str] = None, default: str = None) -> str:
    """簡単なユーザー質問"""
    return user_interaction.ask_user_decision(question, options, default)

def handle_error_with_user(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """エラーをユーザーと一緒に処理"""
    return user_interaction.handle_error(error, context)

def confirm_action(action: str, details: Dict[str, Any] = None) -> bool:
    """アクションの確認"""
    return user_interaction.request_confirmation(action, details)

def get_user_input(prompt: str, input_type: str = "text") -> Any:
    """ユーザー入力を取得"""
    return user_interaction.ask_for_input(prompt, input_type)

def show_warning(message: str, require_confirmation: bool = False) -> bool:
    """警告表示"""
    return user_interaction.show_warning(message, require_confirmation=require_confirmation)