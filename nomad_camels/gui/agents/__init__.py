"""
NOMAD-CAMELS Multi-Agent System

This package implements a sophisticated multi-agent system for the NOMAD-CAMELS
measurement automation platform. The system provides intelligent assistance through
specialized agents that can handle various tasks and workflows.

Architecture:
- AI Workflow Orchestrator: Main coordinator using GPT-4
- Capability Agents: Specialized agents for different domains
- Context Store: Shared state and memory management

The system supports natural language interactions and can handle complex,
multi-step workflows through intelligent agent coordination.
"""

from .orchestrator import WorkflowOrchestrator
from .context_store import ContextStore
from .sample_manager import SampleManagerAgent
from .protocol_agent import ProtocolAgent
from .status_agent import StatusAgent
from .troubleshoot_agent import TroubleshootAgent
from .nomad_agent import NomadAgent

__all__ = [
    'WorkflowOrchestrator',
    'ContextStore',
    'SampleManagerAgent',
    'ProtocolAgent', 
    'StatusAgent',
    'TroubleshootAgent',
    'NomadAgent'
] 