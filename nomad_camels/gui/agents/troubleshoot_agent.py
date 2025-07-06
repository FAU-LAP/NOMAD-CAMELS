"""
Troubleshoot Agent
=================

Specialized agent for helping with problems and errors in NOMAD-CAMELS.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .context_store import ContextStore


class TroubleshootAgent:
    """
    Agent specialized in troubleshooting and problem resolution.
    
    Handles:
    - Error diagnosis
    - Problem resolution guidance
    - System health checks
    - Performance optimization suggestions
    """
    
    def __init__(self, main_window, context_store):
        self.main_window = main_window
        self.context_store = context_store
        self.logger = logging.getLogger(__name__)
        self.last_used = None
        
        # Initialize the Agno agent
        self.agent = Agent(
            name="TroubleshootAgent",
            instructions="""
            You are a specialized agent for troubleshooting problems in NOMAD-CAMELS measurement automation system.
            
            Your capabilities include:
            - Diagnosing system problems and errors
            - Providing step-by-step troubleshooting guides
            - Identifying root causes of issues
            - Suggesting solutions and workarounds
            - Performing system health checks
            - Optimizing system performance
            
            Always:
            1. Systematically analyze problems to identify root causes
            2. Provide clear, step-by-step troubleshooting instructions
            3. Suggest multiple solutions when possible
            4. Prioritize safe and non-destructive solutions
            5. Document solutions for future reference
            
            When troubleshooting:
            - Start with basic checks (connections, power, configuration)
            - Progress to more advanced diagnostics
            - Test solutions incrementally
            - Verify fixes before concluding
            - Provide preventive measures to avoid recurrence
            """,
            model=OpenAIChat(id="gpt-4")
        )
    
    def process_request(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Process a troubleshooting request"""
        
        self.last_used = datetime.now()
        
        try:
            # Determine the specific troubleshooting operation
            intent = context.get('system_state', {}).get('intent', 'unknown')
            
            if intent == 'troubleshoot':
                return self._troubleshoot_problem(user_input, parameters, context)
            else:
                return self._general_troubleshoot_query(user_input, parameters, context)
                
        except Exception as e:
            self.logger.error(f"Error processing troubleshoot request: {e}")
            return f"I encountered an error while troubleshooting: {str(e)}. Please try again."
    
    def _troubleshoot_problem(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Troubleshoot a specific problem"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        
        # Use the agent to diagnose and provide solutions
        troubleshoot_prompt = f"""
        The user is experiencing a problem:
        "{user_input}"
        
        Current system state:
        - Active User: {system_state.get('active_user', 'Unknown')}
        - Active Sample: {system_state.get('active_sample', 'None')}
        - Available Samples: {list(system_state.get('samples', {}).keys())}
        - Available Protocols: {list(system_state.get('protocols', {}).keys())}
        - Instruments: {list(system_state.get('instruments', {}).keys())}
        - NOMAD Connected: {system_state.get('nomad_connected', False)}
        - API Server Running: {system_state.get('api_server_running', False)}
        
        Extracted parameters: {parameters}
        
        Provide:
        1. Problem diagnosis
        2. Step-by-step troubleshooting guide
        3. Common causes and solutions
        4. Preventive measures
        """
        
        try:
            agent_response = self.agent.run(troubleshoot_prompt)
            return f"🔧 Troubleshooting Guide:\n{agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error troubleshooting problem: {e}")
            return f"I encountered an error while troubleshooting: {str(e)}"
    
    def _general_troubleshoot_query(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle general troubleshooting queries"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        
        # Use the agent to handle the general query
        query_prompt = f"""
        The user has a general troubleshooting question:
        "{user_input}"
        
        Current system state:
        - Active User: {system_state.get('active_user', 'Unknown')}
        - Active Sample: {system_state.get('active_sample', 'None')}
        - Available Samples: {list(system_state.get('samples', {}).keys())}
        - Available Protocols: {list(system_state.get('protocols', {}).keys())}
        - Instruments: {list(system_state.get('instruments', {}).keys())}
        - NOMAD Connected: {system_state.get('nomad_connected', False)}
        - Parameters extracted: {parameters}
        
        Provide helpful troubleshooting information and suggestions.
        """
        
        try:
            agent_response = self.agent.run(query_prompt)
            return f"🔧 Troubleshooting Information: {agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error handling troubleshoot query: {e}")
            return f"I encountered an error while processing your troubleshooting query: {str(e)}" 