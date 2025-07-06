"""
Status Agent
===========

Specialized agent for providing system status and information in NOMAD-CAMELS.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .context_store import ContextStore


class StatusAgent:
    """
    Agent specialized in providing system status and information.
    
    Handles:
    - System overview and status
    - Instrument status
    - Sample information
    - User information
    - General system queries
    """
    
    def __init__(self, main_window, context_store):
        self.main_window = main_window
        self.context_store = context_store
        self.logger = logging.getLogger(__name__)
        self.last_used = None
        
        # Initialize the Agno agent
        self.agent = Agent(
            name="StatusAgent",
            instructions="""
            You are a specialized agent for providing system status and information in NOMAD-CAMELS measurement automation system.
            
            Your capabilities include:
            - Retrieving system status information
            - Reporting instrument status and connectivity
            - Providing sample information
            - Monitoring system health and performance
            - Generating status reports
            
            Always:
            1. Provide accurate and up-to-date status information
            2. Format status reports in a clear, readable manner
            3. Highlight any issues or warnings in the system
            4. Include relevant timestamps and measurements
            5. Maintain professional and informative communication
            
            When reporting status, include information about:
            - Connected instruments and their status
            - Current sample information
            - System performance metrics
            - Any active measurements or protocols
            - Error conditions or warnings
            """,
            model=OpenAIChat(id="gpt-4")
        )
    
    def process_request(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Process a status-related request"""
        
        self.last_used = datetime.now()
        
        try:
            # Determine the specific status operation
            intent = context.get('system_state', {}).get('intent', 'unknown')
            
            if intent == 'get_status':
                return self._get_system_status(user_input, parameters, context)
            else:
                return self._general_status_query(user_input, parameters, context)
                
        except Exception as e:
            self.logger.error(f"Error processing status request: {e}")
            return f"I encountered an error while getting system status: {str(e)}. Please try again."
    
    def _get_system_status(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Get comprehensive system status"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        
        # Use the agent to format the status information
        status_prompt = f"""
        The user wants to see the system status:
        "{user_input}"
        
        Current system state:
        - Active User: {system_state.get('active_user', 'Unknown')}
        - Active Sample: {system_state.get('active_sample', 'None')}
        - Available Samples: {list(system_state.get('samples', {}).keys())}
        - Available Protocols: {list(system_state.get('protocols', {}).keys())}
        - Instruments: {list(system_state.get('instruments', {}).keys())}
        - NOMAD Connected: {system_state.get('nomad_connected', False)}
        - NOMAD User: {system_state.get('nomad_user', 'None')}
        - API Server Running: {system_state.get('api_server_running', False)}
        
        Format this information in a comprehensive, user-friendly status report.
        """
        
        try:
            agent_response = self.agent.run(status_prompt)
            
            # Extract content from RunResponse object if needed
            if hasattr(agent_response, 'content'):
                response_text = agent_response.content
            else:
                response_text = str(agent_response)
            
            return f"📊 System Status Report:\n{response_text}"
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return f"I encountered an error while generating the status report: {str(e)}"
    
    def _general_status_query(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle general status-related queries"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        
        # Use the agent to handle the general query
        query_prompt = f"""
        The user has a general status-related question:
        "{user_input}"
        
        Current system state:
        - Active User: {system_state.get('active_user', 'Unknown')}
        - Active Sample: {system_state.get('active_sample', 'None')}
        - Available Samples: {list(system_state.get('samples', {}).keys())}
        - Available Protocols: {list(system_state.get('protocols', {}).keys())}
        - Instruments: {list(system_state.get('instruments', {}).keys())}
        - NOMAD Connected: {system_state.get('nomad_connected', False)}
        - Parameters extracted: {parameters}
        
        Provide a helpful response with relevant status information.
        """
        
        try:
            agent_response = self.agent.run(query_prompt)
            
            # Extract content from RunResponse object if needed
            if hasattr(agent_response, 'content'):
                response_text = agent_response.content
            else:
                response_text = str(agent_response)
            
            return f"ℹ️ System Information: {response_text}"
            
        except Exception as e:
            self.logger.error(f"Error handling status query: {e}")
            return f"I encountered an error while processing your status query: {str(e)}" 