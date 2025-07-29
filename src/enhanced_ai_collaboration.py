#!/usr/bin/env python3
"""
Enhanced AI Collaboration System - ユーザー対話機能付き
"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import existing modules
from ai_collaboration_core import AICollaborationCore
from user_interaction import UserInteractionManager, ask_user, handle_error_with_user, confirm_action

class EnhancedAICollaboration(AICollaborationCore):
    """ユーザー対話機能を強化したAI協調システム"""
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)
        self.user_interaction = UserInteractionManager(
            auto_mode=self.config.get("system.auto_approve", True)
        )
        self.error_count = 0
        self.max_retries = self.config.get("system.max_retries", 3)
        
    def run_complete_workflow_with_interaction(self, project_request: str, mode: str = "full") -> Dict[str, Any]:
        """ユーザー対話付きの完全ワークフロー実行"""
        
        print(f"🚀 Starting Enhanced AI Collaboration")
        print(f"Project: {project_request}")
        print(f"Mode: {mode}")
        
        # プロジェクト開始の確認
        if not confirm_action(
            f"Start AI collaboration for: {project_request}",
            {"mode": mode, "estimated_time": "5-10 minutes"}
        ):
            return {"status": "cancelled_by_user", "reason": "User cancelled at start"}
        
        results = {
            "project_request": project_request,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "user_interactions": [],
            "errors_encountered": []
        }
        
        try:
            # Phase 1: Design (if applicable)
            if mode in ["full", "design"]:
                results["phases"]["design"] = self._run_design_phase_with_interaction(project_request)
                
                if results["phases"]["design"].get("status") == "error":
                    return self._handle_phase_error("design", results)
            
            # Phase 2: Implementation (if applicable)  
            if mode in ["full", "implementation"]:
                design_data = results.get("phases", {}).get("design", {})
                
                if not design_data and mode == "implementation":
                    # Ask user for design input
                    design_data = self._get_design_from_user(project_request)
                
                results["phases"]["implementation"] = self._run_implementation_phase_with_interaction(design_data)
                
                if results["phases"]["implementation"].get("status") == "error":
                    return self._handle_phase_error("implementation", results)
            
            # Phase 3: File Generation
            if results.get("phases", {}).get("implementation"):
                results["phases"]["file_generation"] = self._run_file_generation_with_interaction(
                    results["phases"]["implementation"]
                )
            
            # Final confirmation
            if self._confirm_completion(results):
                results["status"] = "completed"
                results["user_approved"] = True
            else:
                results["status"] = "completed_pending_review"
                results["user_approved"] = False
            
        except Exception as e:
            results = self._handle_system_error(e, results)
        
        # Save interaction log
        log_path = self.user_interaction.save_interaction_log()
        results["interaction_log"] = log_path
        
        return results

    def _run_design_phase_with_interaction(self, project_request: str) -> Dict[str, Any]:
        """対話付き設計フェーズ"""
        
        print(f"\n📋 Phase 1: Design Collaboration")
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # Design phase implementation
                design_result = self.design_system.run_design_phase(project_request)
                
                # Check if design was successful
                if not design_result or design_result.get("error"):
                    raise Exception(f"Design phase failed: {design_result.get('error', 'Unknown error')}")
                
                # Ask user to review design
                if self._review_design_with_user(design_result):
                    return {"status": "success", "data": design_result}
                else:
                    # User wants to modify design
                    modifications = self.user_interaction.ask_for_input(
                        "What modifications would you like to make to the design?",
                        "text"
                    )
                    
                    if modifications:
                        # Apply modifications (simplified)
                        design_result["user_modifications"] = modifications
                        print(f"✓ Design modifications noted: {modifications}")
                    
                    return {"status": "success", "data": design_result}
                
            except Exception as e:
                retry_count += 1
                self.error_count += 1
                
                error_response = handle_error_with_user(
                    e,
                    context={
                        "phase": "design",
                        "retry_count": retry_count,
                        "max_retries": self.max_retries
                    }
                )
                
                if error_response["abort"]:
                    return {"status": "error", "error": str(e), "aborted_by_user": True}
                elif error_response["skip"]:
                    return {"status": "skipped", "reason": "Skipped by user after error"}
                elif not error_response["retry"]:
                    return {"status": "error", "error": str(e)}
                
                print(f"🔄 Retrying design phase... ({retry_count}/{self.max_retries})")
        
        return {"status": "error", "error": f"Max retries ({self.max_retries}) exceeded"}

    def _run_implementation_phase_with_interaction(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """対話付き実装フェーズ"""
        
        print(f"\n⚡ Phase 2: AI Implementation")
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # Show implementation plan
                if design_data:
                    self._show_implementation_plan(design_data)
                
                # Run implementation
                impl_result = self.implementation_system.run_implementation(design_data)
                
                if not impl_result or impl_result.get("error"):
                    raise Exception(f"Implementation failed: {impl_result.get('error', 'Unknown error')}")
                
                # Ask user to review implementation
                if self._review_implementation_with_user(impl_result):
                    return {"status": "success", "data": impl_result}
                else:
                    # User wants modifications
                    return self._handle_implementation_modifications(impl_result)
                
            except Exception as e:
                retry_count += 1
                self.error_count += 1
                
                # Suggest solutions based on error type
                solutions = self._generate_implementation_solutions(e)
                
                error_response = handle_error_with_user(
                    e,
                    context={
                        "phase": "implementation",
                        "retry_count": retry_count,
                        "max_retries": self.max_retries
                    },
                    suggested_solutions=solutions
                )
                
                if error_response["abort"]:
                    return {"status": "error", "error": str(e), "aborted_by_user": True}
                elif error_response["skip"]:
                    return {"status": "skipped", "reason": "Skipped by user after error"}
                elif error_response["solution_index"]:
                    # Try applying suggested solution
                    solution = solutions[error_response["solution_index"] - 1]
                    print(f"🔧 Applying solution: {solution}")
                    # Apply solution logic here
                
                print(f"🔄 Retrying implementation... ({retry_count}/{self.max_retries})")
        
        return {"status": "error", "error": f"Max retries ({self.max_retries}) exceeded"}

    def _run_file_generation_with_interaction(self, impl_data: Dict[str, Any]) -> Dict[str, Any]:
        """対話付きファイル生成フェーズ"""
        
        print(f"\n📁 Phase 3: File Generation")
        
        try:
            # Show what files will be generated
            files_to_generate = self._get_files_list(impl_data)
            
            if files_to_generate:
                print(f"Files to be generated:")
                for file_info in files_to_generate:
                    print(f"  - {file_info['name']}: {file_info.get('description', 'No description')}")
                
                if not confirm_action(
                    f"Generate {len(files_to_generate)} files",
                    {"output_directory": self.config.get("system.output_directory", "./generated_projects")}
                ):
                    return {"status": "cancelled", "reason": "File generation cancelled by user"}
            
            # Generate files
            files_result = self.file_generator.generate_project_files(impl_data)
            
            # Show generated files
            if files_result.get("files_created"):
                print(f"\n✅ Successfully generated {len(files_result['files_created'])} files:")
                for file_path in files_result["files_created"]:
                    print(f"  ✓ {file_path}")
            
            return {"status": "success", "data": files_result}
            
        except Exception as e:
            return handle_error_with_user(e, context={"phase": "file_generation"})

    def _review_design_with_user(self, design_result: Dict[str, Any]) -> bool:
        """ユーザーによる設計レビュー"""
        
        print(f"\n📋 Design Review")
        print(f"=" * 50)
        
        if design_result.get("project_name"):
            print(f"Project: {design_result['project_name']}")
        
        if design_result.get("tech_stack"):
            print(f"Technology: {design_result['tech_stack']}")
        
        if design_result.get("main_features"):
            print(f"Features:")
            for feature in design_result["main_features"]:
                print(f"  - {feature}")
        
        return ask_user(
            "Do you approve this design?",
            ["yes", "no", "modify"],
            default="yes"
        ) != "no"

    def _review_implementation_with_user(self, impl_result: Dict[str, Any]) -> bool:
        """ユーザーによる実装レビュー"""
        
        print(f"\n⚡ Implementation Review")
        print(f"=" * 50)
        
        if impl_result.get("conversation_log"):
            print(f"AI Conversation: {len(impl_result['conversation_log'])} exchanges")
        
        if impl_result.get("generated_components"):
            print(f"Components generated:")
            for component in impl_result["generated_components"]:
                print(f"  - {component}")
        
        return ask_user(
            "Do you approve this implementation?",
            ["yes", "no", "modify"],
            default="yes"
        ) != "no"

    def _show_implementation_plan(self, design_data: Dict[str, Any]):
        """実装計画を表示"""
        
        print(f"\n📋 Implementation Plan")
        print(f"Based on design: {design_data.get('project_name', 'Unnamed Project')}")
        
        if design_data.get("implementation_priority"):
            print(f"Priority: {design_data['implementation_priority']}")
        
        if design_data.get("main_features"):
            print(f"Features to implement:")
            for feature in design_data["main_features"]:
                print(f"  ⚡ {feature}")

    def _get_design_from_user(self, project_request: str) -> Dict[str, Any]:
        """ユーザーから設計情報を取得"""
        
        print(f"\n📝 Design Input Required")
        print(f"Since no design was provided, please help define the project:")
        
        project_name = self.user_interaction.ask_for_input(
            f"Project name (default: AI Generated Project):",
            "text"
        ) or "AI Generated Project"
        
        tech_stack = self.user_interaction.ask_for_input(
            f"Preferred technology stack (e.g., Python, FastAPI, React):",
            "text"
        ) or "Python, FastAPI, SQLAlchemy"
        
        return {
            "project_name": project_name,
            "project_overview": project_request,
            "tech_stack": tech_stack,
            "main_features": [
                "Core functionality based on request",
                "Database integration",
                "API endpoints"
            ],
            "user_provided": True
        }

    def _generate_implementation_solutions(self, error: Exception) -> List[str]:
        """実装エラーに対する解決策を生成"""
        
        error_str = str(error).lower()
        solutions = []
        
        if "api" in error_str and ("key" in error_str or "token" in error_str):
            solutions.extend([
                "Check API keys configuration",
                "Verify API key permissions",
                "Switch to demo mode without API calls"
            ])
        
        if "import" in error_str or "module" in error_str:
            solutions.extend([
                "Install missing dependencies",
                "Check Python path configuration",
                "Use alternative implementation"
            ])
        
        if "timeout" in error_str or "connection" in error_str:
            solutions.extend([
                "Increase timeout settings",
                "Check network connectivity",
                "Use cached responses"
            ])
        
        if not solutions:
            solutions.extend([
                "Simplify the implementation",
                "Use fallback implementation",
                "Skip this component"
            ])
        
        return solutions

    def _handle_implementation_modifications(self, impl_result: Dict[str, Any]) -> Dict[str, Any]:
        """実装の修正を処理"""
        
        modifications = self.user_interaction.ask_for_input(
            "What modifications would you like to make?",
            "text"
        )
        
        if modifications:
            impl_result["user_modifications"] = modifications
            print(f"✓ Modifications noted: {modifications}")
        
        return {"status": "success", "data": impl_result}

    def _get_files_list(self, impl_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """生成されるファイルのリストを取得"""
        
        # This would normally analyze impl_data to determine files
        return [
            {"name": "main.py", "description": "Main application file"},
            {"name": "requirements.txt", "description": "Python dependencies"},
            {"name": "README.md", "description": "Project documentation"},
            {"name": "config.json", "description": "Configuration file"}
        ]

    def _confirm_completion(self, results: Dict[str, Any]) -> bool:
        """完了の確認"""
        
        print(f"\n🎉 AI Collaboration Completed!")
        print(f"=" * 50)
        
        completed_phases = list(results.get("phases", {}).keys())
        print(f"Completed phases: {', '.join(completed_phases)}")
        
        if results.get("error_count", 0) > 0:
            print(f"Errors encountered: {results['error_count']}")
        
        return confirm_action(
            "Mark this collaboration as completed",
            {"phases": completed_phases, "errors": results.get("error_count", 0)}
        )

    def _handle_phase_error(self, phase: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """フェーズエラーの処理"""
        
        results["status"] = "error"
        results["failed_phase"] = phase
        results["error_count"] = self.error_count
        
        return results

    def _handle_system_error(self, error: Exception, results: Dict[str, Any]) -> Dict[str, Any]:
        """システムエラーの処理"""
        
        print(f"\n💥 System Error Occurred")
        print(f"Error: {error}")
        print(f"Traceback: {traceback.format_exc()}")
        
        error_response = handle_error_with_user(
            error,
            context={"type": "system_error", "results_so_far": len(results.get("phases", {}))}
        )
        
        results["status"] = "system_error"
        results["error"] = str(error)
        results["error_response"] = error_response
        results["error_count"] = self.error_count
        
        return results

def main():
    """Enhanced main function with user interaction"""
    
    print("🤖 Enhanced AI Collaboration System")
    print("With intelligent user interaction and error handling")
    print("=" * 60)
    
    try:
        system = EnhancedAICollaboration()
        
        # Get project request from user
        project_request = system.user_interaction.ask_for_input(
            "What would you like to create? (Describe your project idea)",
            "text"
        )
        
        if not project_request:
            print("❌ No project request provided. Exiting.")
            return
        
        # Choose mode
        mode = ask_user(
            "Which mode would you like to use?",
            ["full", "design", "implementation", "conversation"],
            default="full"
        )
        
        # Run the collaboration
        results = system.run_complete_workflow_with_interaction(project_request, mode)
        
        # Show final results
        print(f"\n🏁 Final Results:")
        print(f"Status: {results.get('status', 'unknown')}")
        print(f"Phases completed: {list(results.get('phases', {}).keys())}")
        print(f"User interactions: {len(results.get('user_interactions', []))}")
        
        if results.get('interaction_log'):
            print(f"Interaction log saved: {results['interaction_log']}")
        
    except KeyboardInterrupt:
        print(f"\n⏸️ Collaboration interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()