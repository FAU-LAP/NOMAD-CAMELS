"""
Sample Manager Agent
===================

Specialized agent for handling sample-related operations in NOMAD-CAMELS.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .context_store import ContextStore


class SampleManagerAgent:
    """
    Agent specialized in sample management operations.
    
    Handles:
    - Sample creation
    - Sample editing
    - Sample deletion
    - Sample listing and information
    """
    
    def __init__(self, main_window, context_store):
        self.main_window = main_window
        self.context_store = context_store
        self.logger = logging.getLogger(__name__)
        self.last_used = None
        
        # Initialize the Agno agent
        self.agent = Agent(
            name="SampleManagerAgent",
            instructions="""
            You are a specialized agent for managing samples in NOMAD-CAMELS measurement automation system.
            
            Your capabilities include:
            - Creating new samples with proper metadata
            - Editing existing sample information
            - Deleting samples (with appropriate warnings)
            - Listing and searching samples
            - Validating sample data and parameters
            - Providing sample-related guidance and best practices
            
            Always:
            1. Validate all sample data before processing
            2. Provide clear feedback on operations
            3. Warn users about destructive operations
            4. Ensure data integrity and consistency
            5. Follow proper naming conventions and metadata standards
            
            When creating samples, ensure all required fields are provided and validate the data format.
            When editing samples, preserve existing data unless explicitly told to change it.
            When deleting samples, warn about potential data loss and confirm the action.
            """,
            model=OpenAIChat(id="gpt-4")
        )
    
    def process_request(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Process a sample management request"""
        
        self.last_used = datetime.now()
        
        try:
            # Get the intent from the conversation history or parameters
            intent = 'unknown'
            
            # Check if intent is in the conversation history
            if 'conversation_history' in context and context['conversation_history']:
                latest_context = context['conversation_history'][-1]
                intent = latest_context.get('intent', 'unknown')
            
            # Check if we can determine intent from parameters
            if intent == 'unknown':
                if parameters.get('sample_name') or parameters.get('sample_id'):
                    # If we have sample parameters, it's likely a create request
                    intent = 'create_sample'
            
            # Log the detected intent for debugging
            self.logger.info(f"Sample manager processing intent: {intent} with parameters: {parameters}")
            
            if intent == 'create_sample':
                return self._create_sample(user_input, parameters, context)
            elif intent == 'edit_sample':
                return self._edit_sample(user_input, parameters, context)
            elif intent == 'delete_sample':
                return self._delete_sample(user_input, parameters, context)
            elif intent == 'list_samples':
                return self._list_samples(user_input, parameters, context)
            else:
                return self._general_sample_query(user_input, parameters, context)
                
        except Exception as e:
            self.logger.error(f"Error processing sample request: {e}")
            return f"I encountered an error while processing your sample request: {str(e)}. Please try again."
    
    def _create_sample(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create a new sample"""
        
        # Extract sample information from parameters and user input
        sample_name = parameters.get('sample_name')
        sample_id = parameters.get('sample_id')
        
        if not sample_name and not sample_id:
            return "I need either a sample name or sample ID to create a sample. Could you please provide one?"
        
        # Get current system state
        system_state = context.get('system_state', {})
        existing_samples = system_state.get('samples', {})
        
        # Check if sample already exists
        if sample_id and sample_id in existing_samples:
            return f"A sample with ID '{sample_id}' already exists. Would you like to edit it instead?"
        
        # If we have enough information, directly create the sample
        if sample_name or sample_id:
            try:
                success = self._execute_sample_creation(sample_name, sample_id, parameters)
                if success:
                    return f"✅ Successfully created sample '{sample_name or sample_id}' with ID '{sample_id or sample_name.replace(' ', '_').upper()}'! The sample has been added to your system and is ready for use."
                else:
                    return f"❌ Failed to create sample '{sample_name or sample_id}'. Please check the system logs for more details."
            except Exception as e:
                self.logger.error(f"Error in sample creation: {e}")
                return f"I encountered an error while creating the sample: {str(e)}"
        
        # If we somehow don't have enough information, ask the agent for guidance
        creation_prompt = f"""
        The user wants to create a sample with the following information:
        - User Input: "{user_input}"
        - Sample Name: {sample_name or 'Not specified'}
        - Sample ID: {sample_id or 'Not specified'}
        - Existing Samples: {list(existing_samples.keys())}
        
        Help create the sample by:
        1. Suggesting a sample ID if not provided
        2. Identifying any missing required information
        3. Providing guidance on sample creation
        
        Respond with specific instructions for the user.
        """
        
        try:
            agent_response = self.agent.run(creation_prompt)
            
            # Extract content from RunResponse object if needed
            if hasattr(agent_response, 'content'):
                response_text = agent_response.content
            else:
                response_text = str(agent_response)
            
            return response_text
                
        except Exception as e:
            self.logger.error(f"Error in sample creation: {e}")
            return f"I encountered an error while creating the sample: {str(e)}"
    
    def _execute_sample_creation(self, sample_name: str, sample_id: str, parameters: Dict[str, Any]) -> bool:
        """Execute the actual sample creation"""
        
        try:
            # Use the provided sample_id or generate one from sample_name
            if not sample_id and sample_name:
                sample_id = sample_name.replace(' ', '_').upper()
            
            # Create sample data structure that matches the expected format
            sample_data = {
                'name': sample_name or sample_id,
                'sample_id': sample_id,
                'description': parameters.get('description', ''),
                'owner': getattr(self.main_window, 'active_user', 'default_user')
            }
            
            # Ensure sample_data is a dictionary (safety check)
            if not isinstance(sample_data, dict):
                self.logger.warning(f"Sample data for '{sample_id}' is not a dictionary. Converting...")
                sample_data = {
                    'name': sample_name or sample_id,
                    'sample_id': sample_id,
                    'description': str(sample_data),
                    'owner': getattr(self.main_window, 'active_user', 'default_user')
                }
            
            # Add to main window's sample data
            if hasattr(self.main_window, 'sampledata'):
                self.main_window.sampledata[sample_id] = sample_data
                self.logger.info(f"Successfully added sample '{sample_id}' to sampledata as {type(sample_data)}")
            
            # Update context store
            self.context_store.set_shared_knowledge(f'sample_{sample_id}', sample_data)
            
            # Trigger UI update if available
            if hasattr(self.main_window, 'update_sample_list'):
                self.main_window.update_sample_list()
            
            # Update shown samples if available
            if hasattr(self.main_window, 'update_shown_samples'):
                self.main_window.update_shown_samples()
            
            # Save sample data if available
            if hasattr(self.main_window, 'save_sample_data'):
                self.main_window.save_sample_data()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing sample creation: {e}")
            return False
    
    def _edit_sample(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Edit an existing sample"""
        
        sample_id = parameters.get('sample_id')
        sample_name = parameters.get('sample_name')
        
        if not sample_id and not sample_name:
            return "I need a sample ID or name to edit a sample. Which sample would you like to edit?"
        
        # Get current system state
        system_state = context.get('system_state', {})
        existing_samples = system_state.get('samples', {})
        
        # Find the sample to edit
        target_sample_id = None
        if sample_id and sample_id in existing_samples:
            target_sample_id = sample_id
        elif sample_name:
            # Search by name
            for sid, sample_data in existing_samples.items():
                if sample_data.get('name', '').lower() == sample_name.lower():
                    target_sample_id = sid
                    break
        
        if not target_sample_id:
            return f"I couldn't find a sample with {'ID' if sample_id else 'name'} '{sample_id or sample_name}'. Available samples: {list(existing_samples.keys())}"
        
        # Use the agent to help with editing
        edit_prompt = f"""
        The user wants to edit sample '{target_sample_id}' with the following request:
        "{user_input}"
        
        Current sample data: {existing_samples.get(target_sample_id, {})}
        
        Help determine what changes to make and provide guidance.
        """
        
        try:
            agent_response = self.agent.run(edit_prompt)
            
            # For now, return the agent's guidance
            # In a full implementation, this would parse the changes and apply them
            return f"📝 Sample '{target_sample_id}' editing guidance: {agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error in sample editing: {e}")
            return f"I encountered an error while editing the sample: {str(e)}"
    
    def _delete_sample(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Delete a sample"""
        
        sample_id = parameters.get('sample_id')
        sample_name = parameters.get('sample_name')
        
        if not sample_id and not sample_name:
            return "I need a sample ID or name to delete a sample. Which sample would you like to delete?"
        
        # Get current system state
        system_state = context.get('system_state', {})
        existing_samples = system_state.get('samples', {})
        
        # Find the sample to delete
        target_sample_id = None
        if sample_id and sample_id in existing_samples:
            target_sample_id = sample_id
        elif sample_name:
            # Search by name
            for sid, sample_data in existing_samples.items():
                if sample_data.get('name', '').lower() == sample_name.lower():
                    target_sample_id = sid
                    break
        
        if not target_sample_id:
            return f"I couldn't find a sample with {'ID' if sample_id else 'name'} '{sample_id or sample_name}' to delete."
        
        # Use the agent to provide deletion guidance
        delete_prompt = f"""
        The user wants to delete sample '{target_sample_id}':
        "{user_input}"
        
        Sample data: {existing_samples.get(target_sample_id, {})}
        
        Provide appropriate warnings and confirm the deletion request.
        """
        
        try:
            agent_response = self.agent.run(delete_prompt)
            return f"🗑️ Sample deletion request for '{target_sample_id}': {agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error in sample deletion: {e}")
            return f"I encountered an error while processing the deletion request: {str(e)}"
    
    def _list_samples(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """List available samples"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        existing_samples = system_state.get('samples', {})
        
        if not existing_samples:
            return "📋 No samples are currently available. Would you like to create one?"
        
        # Use the agent to format the sample list
        list_prompt = f"""
        The user wants to see the sample list:
        "{user_input}"
        
        Available samples: {existing_samples}
        
        Format this information in a user-friendly way, showing key details for each sample.
        """
        
        try:
            agent_response = self.agent.run(list_prompt)
            return f"📋 Sample List:\n{agent_response}"
            
        except Exception as e:
            self.logger.error(f"Error listing samples: {e}")
            return f"I encountered an error while listing samples: {str(e)}"
    
    def _general_sample_query(self, user_input: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle general sample-related queries"""
        
        # Get current system state
        system_state = context.get('system_state', {})
        existing_samples = system_state.get('samples', {})
        
        # Use the agent to handle the general query
        query_prompt = f"""
        The user has a general sample-related question:
        "{user_input}"
        
        Current context:
        - Available samples: {list(existing_samples.keys())}
        - Active sample: {system_state.get('active_sample', 'None')}
        - Parameters extracted: {parameters}
        
        Provide a helpful response and suggest specific actions if appropriate.
        """
        
        try:
            agent_response = self.agent.run(query_prompt)
            
            # Extract content from RunResponse object if needed
            if hasattr(agent_response, 'content'):
                response_text = agent_response.content
            else:
                response_text = str(agent_response)
            
            return f"🔬 Sample Information: {response_text}"
            
        except Exception as e:
            self.logger.error(f"Error handling sample query: {e}")
            return f"I encountered an error while processing your sample query: {str(e)}" 