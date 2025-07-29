#!/usr/bin/env python3
"""
AI Collaboration System - Core Engine
"""

import os
import sys
import json
import click
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import our modules
from design_system import DesignSystem
from implementation_system import ImplementationSystem
from conversation_engine import ConversationEngine
from file_generator import FileGenerator
from utils.config_manager import ConfigManager
from utils.logger import setup_logger

class AICollaborationCore:
    """Core orchestrator for AI collaboration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = ConfigManager(config_path)
        self.logger = setup_logger("ai_collaboration")
        self.project_dir = Path.cwd()
        
        # Initialize subsystems
        self.design_system = DesignSystem(self.config)
        self.implementation_system = ImplementationSystem(self.config)
        self.conversation_engine = ConversationEngine(self.config)
        self.file_generator = FileGenerator(self.config)
        
        self.logger.info("AI Collaboration System initialized")

    def run_complete_workflow(self, project_request: str, mode: str = "full") -> Dict[str, Any]:
        """Run the complete design-to-implementation workflow"""
        self.logger.info(f"Starting complete workflow: {project_request}")
        
        results = {
            "project_request": project_request,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }
        
        try:
            if mode in ["full", "design"]:
                # Phase 1: Design with o4
                self.logger.info("Phase 1: Design collaboration with o4")
                design_result = self.design_system.run_design_phase(project_request)
                results["phases"]["design"] = design_result
                
                if mode == "design":
                    return results
            
            if mode in ["full", "implementation"]:
                # Phase 2: AI-to-AI Implementation
                self.logger.info("Phase 2: AI implementation")
                
                design_data = results.get("phases", {}).get("design", {})
                if not design_data and mode == "implementation":
                    # Load previous design or use default
                    design_data = self._load_previous_design() or self._create_default_design(project_request)
                
                impl_result = self.implementation_system.run_implementation(design_data)
                results["phases"]["implementation"] = impl_result
            
            # Phase 3: File Generation
            if results.get("phases", {}).get("implementation"):
                self.logger.info("Phase 3: File generation")
                files_result = self.file_generator.generate_project_files(
                    results["phases"]["implementation"]
                )
                results["phases"]["file_generation"] = files_result
            
            results["status"] = "completed"
            self.logger.info("Complete workflow finished successfully")
            
        except Exception as e:
            self.logger.error(f"Workflow error: {e}")
            results["status"] = "error"
            results["error"] = str(e)
        
        return results

    def run_ai_conversation_only(self, project_request: str) -> Dict[str, Any]:
        """Run only AI-to-AI conversation without design phase"""
        self.logger.info("Starting AI conversation mode")
        
        return self.conversation_engine.start_conversation(
            project_request,
            max_turns=self.config.get("system.max_iterations", 20)
        )

    def run_design_only(self, project_request: str) -> Dict[str, Any]:
        """Run only the design phase with o4"""
        self.logger.info("Starting design-only mode")
        
        return self.design_system.run_design_phase(project_request)

    def launch_browser_cli_mode(self) -> None:
        """Launch browser + CLI integration mode"""
        self.logger.info("Launching browser + CLI mode")
        
        try:
            from simple_ai_launcher import main as launch_simple
            launch_simple()
        except ImportError:
            self.logger.error("Browser + CLI mode not available")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "version": "1.1.0",
            "config_loaded": bool(self.config),
            "subsystems": {
                "design_system": bool(self.design_system),
                "implementation_system": bool(self.implementation_system),
                "conversation_engine": bool(self.conversation_engine),
                "file_generator": bool(self.file_generator)
            },
            "api_keys_configured": {
                "openai": bool(os.getenv("OPENAI_API_KEY")),
                "anthropic": bool(os.getenv("ANTHROPIC_API_KEY"))
            },
            "project_dir": str(self.project_dir),
            "timestamp": datetime.now().isoformat()
        }

    def _load_previous_design(self) -> Optional[Dict[str, Any]]:
        """Load previous design session if available"""
        design_file = self.project_dir / "design_session.json"
        if design_file.exists():
            try:
                with open(design_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load previous design: {e}")
        return None

    def _create_default_design(self, project_request: str) -> Dict[str, Any]:
        """Create a default design for implementation-only mode"""
        return {
            "project_name": "AI Generated Project",
            "project_overview": project_request,
            "tech_stack": "Python, FastAPI, SQLAlchemy, React",
            "main_features": [
                "Core functionality based on request",
                "Database integration",
                "API endpoints",
                "Basic UI components"
            ],
            "architecture": "Modern web application architecture",
            "implementation_priority": "Core features first, then enhancements",
            "special_requirements": "Clean, maintainable code with tests"
        }


# CLI Interface
@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """AI Collaboration System - Automated AI-to-AI Programming"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose

@cli.command()
@click.argument('project_request')
@click.option('--mode', '-m', 
              type=click.Choice(['full', 'design', 'implementation', 'conversation']),
              default='full', 
              help='Execution mode')
@click.pass_context
def run(ctx, project_request, mode):
    """Run AI collaboration workflow"""
    system = AICollaborationCore(ctx.obj.get('config'))
    
    if mode == 'full':
        result = system.run_complete_workflow(project_request)
    elif mode == 'design':
        result = system.run_design_only(project_request)
    elif mode == 'implementation':
        result = system.run_complete_workflow(project_request, mode='implementation')
    elif mode == 'conversation':
        result = system.run_ai_conversation_only(project_request)
    
    if ctx.obj.get('verbose'):
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        click.echo(f"Status: {result.get('status', 'unknown')}")
        if result.get('status') == 'completed':
            click.echo(f"✅ Workflow completed successfully")
        elif result.get('status') == 'error':
            click.echo(f"❌ Error: {result.get('error', 'Unknown error')}")

@cli.command()
@click.pass_context
def browser_cli(ctx):
    """Launch browser + CLI integration mode"""
    system = AICollaborationCore(ctx.obj.get('config'))
    system.launch_browser_cli_mode()

@cli.command()
@click.pass_context
def status(ctx):
    """Show system status"""
    system = AICollaborationCore(ctx.obj.get('config'))
    status_info = system.get_system_status()
    
    click.echo("🤖 AI Collaboration System Status")
    click.echo("=" * 40)
    click.echo(f"Version: {status_info['version']}")
    click.echo(f"Config: {'✅' if status_info['config_loaded'] else '❌'}")
    click.echo(f"OpenAI API: {'✅' if status_info['api_keys_configured']['openai'] else '❌'}")
    click.echo(f"Anthropic API: {'✅' if status_info['api_keys_configured']['anthropic'] else '❌'}")
    click.echo(f"Project Directory: {status_info['project_dir']}")

@cli.command()
def init():
    """Initialize a new AI collaboration project"""
    project_dir = Path.cwd()
    
    # Create basic project structure
    directories = ['designs', 'implementations', 'generated', 'config']
    for dir_name in directories:
        (project_dir / dir_name).mkdir(exist_ok=True)
    
    # Create basic config file
    config_content = {
        "system": {
            "auto_approve": True,
            "max_iterations": 20,
            "output_directory": "./generated"
        },
        "ui": {
            "theme": "dark",
            "show_progress": True,
            "auto_refresh": 2000
        }
    }
    
    config_file = project_dir / "config" / "ai_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_content, f, indent=2)
    
    click.echo("🎉 AI Collaboration project initialized!")
    click.echo(f"Configuration: {config_file}")
    click.echo("Ready to start AI collaboration!")

def main():
    """Main entry point"""
    cli()

if __name__ == "__main__":
    main()