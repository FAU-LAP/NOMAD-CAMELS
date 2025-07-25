"""
NOMAD Agent
==========

Specialized agent for handling NOMAD integration and uploads in NOMAD-CAMELS.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .context_store import ContextStore


class NomadAgent:
    """
    Agent specialized in NOMAD integration and data management.
    
    Handles:
    - NOMAD connection and authentication
    - Data upload to NOMAD
    - NOMAD status and configuration
    - Data synchronization
    """
    
    def __init__(self, main_window, context_store):
        self.main_window = main_window
        self.context_store = context_store
        self.logger = logging.getLogger(__name__)
        self.last_used = None
        
        # Initialize the Agno agent
        self.agent = Agent(
            name="NomadAgent",
            instructions="""
            You are a specialized agent for managing NOMAD integration in NOMAD-CAMELS measurement automation system.
            
            Your capabilities include:
            - Managing NOMAD connections and authentication
            - Uploading measurement data to NOMAD
            - Checking NOMAD status and connectivity
            - Handling NOMAD metadata and schemas
            - Managing data uploads and synchronization
            
            Always:
            1. Ensure secure connections to NOMAD servers
            2. Validate data before upload
            3. Provide clear feedback on upload status
            4. Handle authentication and authorization properly
            5. Maintain data integrity during transfers
            
            When working with NOMAD:
            - Verify connection status before operations
            - Check data format and metadata compliance
            - Provide progress updates for long operations
            - Handle errors gracefully with clear explanations
            - Ensure proper data organization and tagging
            """,
            model=OpenAIChat(id="gpt-4")
        )
    
    def process_request(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Process a NOMAD-related request"""
        
        self.last_used = datetime.now()
        
        try:
            # Determine the specific NOMAD operation
            intent = context.get('system_state', {}).get('intent', 'unknown')
            
            if intent == 'nomad_upload':
                return self._upload_to_nomad(user_input, parameters, context)
            elif intent == 'nomad_connect':
                return self._connect_to_nomad(user_input, parameters, context)
            elif intent == 'nomad_status':
                return self._get_nomad_status(user_input, parameters, context)
            else:
                return self._general_nomad_query(user_input, parameters, context)
                
        except Exception as e:
            self.logger.error(f"Error processing NOMAD request: {e}")
            return f"I encountered an error while processing your NOMAD request: {str(e)}. Please try again."
    
    def _upload_to_nomad(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Upload data to NOMAD"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        nomad_connected = system_state.get('nomad_connected', False)
        nomad_user = system_state.get('nomad_user', None)
        
        if not nomad_connected:
            return "❌ NOMAD is not connected. Please connect to NOMAD first before uploading data."
        
        # Use the agent to guide the upload process
        upload_prompt = f"""
        The user wants to upload data to NOMAD:
        "{user_input}"
        
        Current context:
        - NOMAD Connected: {nomad_connected}
        - NOMAD User: {nomad_user}
        - Active Sample: {system_state.get('active_sample', 'None')}
        - Available Samples: {list(system_state.get('samples', {}).keys())}
        - Parameters extracted: {parameters}
        
        Provide guidance for the upload process, including:
        1. Data preparation steps
        2. Required metadata
        3. Upload procedures
        4. Verification steps
        """
        
        try:
            agent_response = self.agent.run(upload_prompt)
            return f"📤 NOMAD Upload Guide:\n{agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error in NOMAD upload: {e}")
            return f"I encountered an error while preparing the NOMAD upload: {str(e)}"
    
    def _connect_to_nomad(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Connect to NOMAD"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        nomad_connected = system_state.get('nomad_connected', False)
        nomad_user = system_state.get('nomad_user', None)
        
        # Use the agent to guide the connection process
        connect_prompt = f"""
        The user wants to connect to NOMAD:
        "{user_input}"
        
        Current context:
        - NOMAD Connected: {nomad_connected}
        - NOMAD User: {nomad_user}
        - Parameters extracted: {parameters}
        
        Provide guidance for connecting to NOMAD, including:
        1. Authentication requirements
        2. Connection procedures
        3. Troubleshooting common issues
        4. Next steps after connection
        """
        
        try:
            agent_response = self.agent.run(connect_prompt)
            
            if nomad_connected:
                return f"✅ Already connected to NOMAD as {nomad_user}:\n{agent_response}"
            else:
                return f"🔗 NOMAD Connection Guide:\n{agent_response}"
                
        except Exception as e:
            self.logger.error(f"Error in NOMAD connection: {e}")
            return f"I encountered an error while connecting to NOMAD: {str(e)}"
    
    def _get_nomad_status(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Get NOMAD status"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        nomad_connected = system_state.get('nomad_connected', False)
        nomad_user = system_state.get('nomad_user', None)
        
        # Use the agent to format the status information
        status_prompt = f"""
        The user wants to check NOMAD status:
        "{user_input}"
        
        Current NOMAD status:
        - Connected: {nomad_connected}
        - User: {nomad_user}
        - Parameters extracted: {parameters}
        
        Provide a comprehensive NOMAD status report.
        """
        
        try:
            agent_response = self.agent.run(status_prompt)
            return f"📊 NOMAD Status:\n{agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error getting NOMAD status: {e}")
            return f"I encountered an error while getting NOMAD status: {str(e)}"
    
    def _general_nomad_query(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle general NOMAD-related queries"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        nomad_connected = system_state.get('nomad_connected', False)
        nomad_user = system_state.get('nomad_user', None)
        
        # Use the agent to handle the general query
        query_prompt = f"""
        The user has a general NOMAD-related question:
        "{user_input}"
        
        Current context:
        - NOMAD Connected: {nomad_connected}
        - NOMAD User: {nomad_user}
        - Parameters extracted: {parameters}
        
        Provide helpful information about NOMAD integration and suggest specific actions if appropriate.
        """
        
        try:
            agent_response = self.agent.run(query_prompt)
            return f"🌐 NOMAD Information: {agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error handling NOMAD query: {e}")
            return f"I encountered an error while processing your NOMAD query: {str(e)}" 