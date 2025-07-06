"""
Protocol Agent
=============

Specialized agent for handling protocol-related operations in NOMAD-CAMELS.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .context_store import ContextStore


class ProtocolAgent:
    """
    Agent specialized in protocol management and execution.
    
    Handles:
    - Protocol execution
    - Protocol listing and information
    - Protocol configuration
    - Measurement guidance
    """
    
    def __init__(self, main_window, context_store):
        self.main_window = main_window
        self.context_store = context_store
        self.logger = logging.getLogger(__name__)
        self.last_used = None
        
        # Initialize the Agno agent
        self.agent = Agent(
            name="ProtocolAgent",
            instructions="""
            You are a specialized agent for managing protocols in NOMAD-CAMELS measurement automation system.
            
            Your capabilities include:
            - Executing measurement protocols
            - Listing available protocols
            - Providing protocol information and guidance
            - Helping with protocol configuration
            - Monitoring protocol execution status
            
            Always:
            1. Ensure instruments are properly configured before protocol execution
            2. Provide clear status updates during measurements
            3. Handle errors gracefully and suggest solutions
            4. Validate protocol parameters before execution
            5. Maintain measurement data integrity
            
            When executing protocols, check that all required instruments are available and configured.
            When listing protocols, provide relevant details about each protocol's purpose and requirements.
            """,
            model=OpenAIChat(id="gpt-4")
        )
    
    def process_request(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Process a protocol-related request"""
        
        self.last_used = datetime.now()
        
        try:
            # Determine the specific protocol operation
            intent = context.get('system_state', {}).get('intent', 'unknown')
            
            if intent == 'run_protocol':
                return self._run_protocol(user_input, parameters, context)
            elif intent == 'list_protocols':
                return self._list_protocols(user_input, parameters, context)
            else:
                return self._general_protocol_query(user_input, parameters, context)
                
        except Exception as e:
            self.logger.error(f"Error processing protocol request: {e}")
            return f"I encountered an error while processing your protocol request: {str(e)}. Please try again."
    
    def _run_protocol(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Execute a measurement protocol"""
        
        protocol_name = parameters.get('protocol_name')
        
        if not protocol_name:
            return "I need a protocol name to execute. Which protocol would you like to run?"
        
        # Get current system state
        system_state = context.get('system_state', {})
        available_protocols = system_state.get('protocols', {})
        active_sample = system_state.get('active_sample', 'None')
        instruments = system_state.get('instruments', {})
        
        # Check if protocol exists
        if protocol_name not in available_protocols:
            return f"Protocol '{protocol_name}' not found. Available protocols: {list(available_protocols.keys())}"
        
        # Use the agent to guide protocol execution
        execution_prompt = f"""
        The user wants to execute protocol '{protocol_name}':
        "{user_input}"
        
        Current context:
        - Active sample: {active_sample}
        - Available instruments: {list(instruments.keys())}
        - Protocol details: {available_protocols.get(protocol_name, {})}
        
        Provide guidance for protocol execution, including:
        1. Pre-execution checks
        2. Required instruments and their status
        3. Estimated execution time
        4. Any warnings or considerations
        """
        
        try:
            agent_response = self.agent.run(execution_prompt)
            
            # Check if we can actually execute the protocol
            if self._can_execute_protocol(protocol_name, context):
                return f"🔬 Starting protocol '{protocol_name}':\n{agent_response}"
            else:
                return f"⚠️ Cannot execute protocol '{protocol_name}' right now:\n{agent_response}"
                
        except Exception as e:
            self.logger.error(f"Error in protocol execution: {e}")
            return f"I encountered an error while preparing to execute the protocol: {str(e)}"
    
    def _can_execute_protocol(self, protocol_name: str, context: Dict[str, Any]) -> bool:
        """Check if protocol can be executed"""
        
        system_state = context.get('system_state', {})
        
        # Check if there's an active sample
        if system_state.get('active_sample') == 'None':
            return False
        
        # Check if required instruments are available
        # This would need to be implemented based on protocol requirements
        
        return True
    
    def _list_protocols(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """List available protocols"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        available_protocols = system_state.get('protocols', {})
        
        if not available_protocols:
            return "📋 No protocols are currently available. Please load some protocols first."
        
        # Use the agent to format the protocol list
        list_prompt = f"""
        The user wants to see the protocol list:
        "{user_input}"
        
        Available protocols: {available_protocols}
        
        Format this information in a user-friendly way, showing key details for each protocol.
        """
        
        try:
            agent_response = self.agent.run(list_prompt)
            return f"📋 Available Protocols:\n{agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error listing protocols: {e}")
            return f"I encountered an error while listing protocols: {str(e)}"
    
    def _general_protocol_query(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle general protocol-related queries"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        available_protocols = system_state.get('protocols', {})
        
        # Use the agent to handle the general query
        query_prompt = f"""
        The user has a general protocol-related question:
        "{user_input}"
        
        Current context:
        - Available protocols: {list(available_protocols.keys())}
        - Parameters extracted: {parameters}
        
        Provide a helpful response and suggest specific actions if appropriate.
        """
        
        try:
            agent_response = self.agent.run(query_prompt)
            return f"🔬 Protocol Information: {agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error handling protocol query: {e}")
            return f"I encountered an error while processing your protocol query: {str(e)}" 