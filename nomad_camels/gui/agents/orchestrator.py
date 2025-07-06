"""
AI Workflow Orchestrator for Multi-Agent System
===============================================

Main orchestrator that coordinates all agents using Agno
"""

import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from agno.agent import Agent
from agno.workflow import Workflow
from agno.models.openai import OpenAIChat
from openai import OpenAI

from .context_store import ContextStore, ConversationContext


class WorkflowOrchestrator:
    """
    Main orchestrator for the multi-agent system.
    
    Coordinates between specialized agents to handle complex user requests.
    Uses Agno framework for agent management and workflow orchestration.
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.context_store = ContextStore(main_window)
        self.logger = logging.getLogger(__name__)
        
        # Initialize agents
        self.agents = {}
        self.workflows = {}
        
        # Add recursion guard
        self._processing_requests = set()
        
        # Initialize the main orchestrator agent
        self._init_orchestrator_agent()
        
        # Initialize specialized agents
        self._init_capability_agents()
        
    def _init_orchestrator_agent(self):
        """Initialize the main orchestrator agent"""
        self.orchestrator_agent = Agent(
            name="WorkflowOrchestrator",
            instructions="""
            You are the main orchestrator for a NOMAD-CAMELS measurement automation system.
            
            Your role is to:
            1. Analyze user requests and understand their intent
            2. Determine which specialized agents are needed
            3. Coordinate between agents to fulfill complex requests
            4. Ensure proper error handling and user feedback
            5. Maintain conversation context and state
            
            Available specialized agents:
            - SampleManagerAgent: Handles sample creation, editing, deletion
            - ProtocolAgent: Manages protocol execution and configuration
            - StatusAgent: Provides system status and information
            - TroubleshootAgent: Helps with problems and errors
            - NomadAgent: Handles NOMAD integration and uploads
            
            Always respond in a helpful, conversational manner while being precise about technical details.
            """,
            model=OpenAIChat(id="gpt-4")
        )
        
    def _init_capability_agents(self):
        """Initialize specialized capability agents"""
        # Import agents here to avoid circular imports
        from .sample_manager import SampleManagerAgent
        from .protocol_agent import ProtocolAgent
        from .status_agent import StatusAgent
        from .troubleshoot_agent import TroubleshootAgent
        from .nomad_agent import NomadAgent
        
        self.agents = {
            'sample_manager': SampleManagerAgent(self.main_window, self.context_store),
            'protocol': ProtocolAgent(self.main_window, self.context_store),
            'status': StatusAgent(self.main_window, self.context_store),
            'troubleshoot': TroubleshootAgent(self.main_window, self.context_store),
            'nomad': NomadAgent(self.main_window, self.context_store)
        }
        
    def process_user_request(self, user_input: str, session_id: str = "default") -> str:
        """
        Process a user request through the multi-agent system.
        
        Args:
            user_input: The user's input text
            session_id: Session identifier for context tracking
            
        Returns:
            Response from the agent system
        """
        # Create a unique request identifier
        request_id = f"{session_id}:{user_input[:50]}"
        
        # Check for recursion
        if request_id in self._processing_requests:
            self.logger.warning(f"Recursion detected for request: {request_id}")
            return "I'm sorry, but I detected a potential infinite loop in processing your request. Please try rephrasing your question."
        
        try:
            # Add to processing set
            self._processing_requests.add(request_id)
            
            # Create conversation context
            context = self.context_store.create_conversation_context(user_input, session_id)
            self.context_store.add_conversation_context(context)
            
            # Get system state for context
            system_state = self.context_store.get_system_state()
            
            # Analyze the request and determine the workflow
            workflow_plan = self._analyze_request(user_input, context, system_state)
            
            # Execute the workflow
            response = self._execute_workflow(workflow_plan, user_input, context)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing user request: {e}")
            return f"I encountered an error while processing your request: {str(e)}. Please try again or contact support if the issue persists."
        finally:
            # Remove from processing set
            self._processing_requests.discard(request_id)
    
    def _analyze_request(self, user_input: str, context: ConversationContext, system_state) -> Dict[str, Any]:
        """Analyze the user request and create a workflow plan"""
        
        # For general queries and greetings, use fallback directly
        if context.intent in ['general_query', 'get_help']:
            return self._fallback_workflow_plan(context.intent, context.entities)
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze this user request for a NOMAD-CAMELS measurement automation system:
        
        User Input: "{user_input}"
        Detected Intent: {context.intent}
        
        Current Context:
        - Intent: {context.intent}
        - Entities: {context.entities}
        - Active User: {system_state.active_user}
        - Active Sample: {system_state.active_sample}
        - Available Samples: {list(system_state.samples.keys())}
        - Available Protocols: {list(system_state.protocols.keys())}
        - NOMAD Connected: {system_state.nomad_connected}
        
        Available agents (use EXACT names in response):
        - sample_manager: Handles sample creation, editing, deletion
        - protocol: Manages protocol execution and configuration
        - status: Provides system status and information
        - troubleshoot: Helps with problems and errors
        - nomad: Handles NOMAD integration and uploads
        
        IMPORTANT: Use only these exact agent names in your response:
        sample_manager, protocol, status, troubleshoot, nomad
        
        Based on the detected intent "{context.intent}", determine:
        1. Which specialized agents are needed from the available agents (use exact names)
        2. The execution order/workflow
        3. Any parameters or data needed
        4. Expected complexity (simple, medium, complex)
        
        Respond with a JSON object containing:
        {{
            "agents_needed": ["agent1", "agent2"],
            "workflow_type": "simple|sequential|parallel|complex",
            "primary_agent": "main_agent_name",
            "parameters": {{"key": "value"}},
            "complexity": "simple|medium|complex",
            "estimated_steps": 1-5
        }}
        """
        
        try:
            response = self.orchestrator_agent.run(analysis_prompt)
            
            # Extract content from RunResponse object if needed
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # Parse the JSON response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                workflow_plan = json.loads(json_match.group())
            else:
                # Fallback based on intent
                workflow_plan = self._fallback_workflow_plan(context.intent, context.entities)
                
            return workflow_plan
            
        except Exception as e:
            self.logger.error(f"Error analyzing request: {e}")
            return self._fallback_workflow_plan(context.intent, context.entities)
    
    def _fallback_workflow_plan(self, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback workflow plan based on intent"""
        
        workflow_plans = {
            'create_sample': {
                'agents_needed': ['sample_manager'],
                'workflow_type': 'simple',
                'primary_agent': 'sample_manager',
                'parameters': entities,
                'complexity': 'simple',
                'estimated_steps': 1
            },
            'run_protocol': {
                'agents_needed': ['protocol'],
                'workflow_type': 'simple',
                'primary_agent': 'protocol',
                'parameters': entities,
                'complexity': 'medium',
                'estimated_steps': 2
            },
            'get_status': {
                'agents_needed': ['status'],
                'workflow_type': 'simple',
                'primary_agent': 'status',
                'parameters': {},
                'complexity': 'simple',
                'estimated_steps': 1
            },
            'troubleshoot': {
                'agents_needed': ['troubleshoot', 'status'],
                'workflow_type': 'sequential',
                'primary_agent': 'troubleshoot',
                'parameters': entities,
                'complexity': 'medium',
                'estimated_steps': 2
            },
            'nomad_upload': {
                'agents_needed': ['nomad'],
                'workflow_type': 'simple',
                'primary_agent': 'nomad',
                'parameters': entities,
                'complexity': 'medium',
                'estimated_steps': 2
            },
            'general_query': {
                'agents_needed': ['orchestrator'],
                'workflow_type': 'conversational',
                'primary_agent': 'orchestrator',
                'parameters': entities,
                'complexity': 'simple',
                'estimated_steps': 1
            },
            'get_help': {
                'agents_needed': ['orchestrator'],
                'workflow_type': 'conversational',
                'primary_agent': 'orchestrator',
                'parameters': entities,
                'complexity': 'simple',
                'estimated_steps': 1
            }
        }
        
        return workflow_plans.get(intent, {
            'agents_needed': ['orchestrator'],
            'workflow_type': 'conversational',
            'primary_agent': 'orchestrator',
            'parameters': {},
            'complexity': 'simple',
            'estimated_steps': 1
        })
    
    def _execute_workflow(self, workflow_plan: Dict[str, Any], user_input: str, context: ConversationContext) -> str:
        """Execute the workflow based on the plan"""
        
        workflow_type = workflow_plan.get('workflow_type', 'simple')
        agents_needed = workflow_plan.get('agents_needed', [])
        primary_agent = workflow_plan.get('primary_agent')
        parameters = workflow_plan.get('parameters', {})
        
        try:
            if workflow_type == 'simple':
                return self._execute_simple_workflow(primary_agent, user_input, parameters, context)
            elif workflow_type == 'conversational':
                return self._execute_conversational_workflow(user_input, parameters, context)
            elif workflow_type == 'sequential':
                return self._execute_sequential_workflow(agents_needed, user_input, parameters, context)
            elif workflow_type == 'parallel':
                return self._execute_parallel_workflow(agents_needed, user_input, parameters, context)
            elif workflow_type == 'complex':
                return self._execute_complex_workflow(agents_needed, user_input, parameters, context)
            else:
                return self._execute_simple_workflow(primary_agent, user_input, parameters, context)
                
        except Exception as e:
            self.logger.error(f"Error executing workflow: {e}")
            return f"I encountered an error while executing your request: {str(e)}. Please try again."
    
    def _execute_simple_workflow(self, agent_name: str, user_input: str, parameters: Dict[str, Any], context: ConversationContext) -> str:
        """Execute a simple single-agent workflow"""
        
        if agent_name not in self.agents:
            return f"I don't have access to the {agent_name} agent. Please try a different request."
        
        agent = self.agents[agent_name]
        
        # Get context for the agent
        agent_context = self.context_store.get_context_for_agent(agent_name)
        
        # Execute the agent's task
        response = agent.process_request(user_input, parameters, agent_context)
        
        return response
    
    def _execute_sequential_workflow(self, agents_needed: List[str], user_input: str, parameters: Dict[str, Any], context: ConversationContext) -> str:
        """Execute a sequential workflow with multiple agents"""
        
        responses = []
        accumulated_context = parameters.copy()
        
        for agent_name in agents_needed:
            if agent_name not in self.agents:
                continue
                
            agent = self.agents[agent_name]
            agent_context = self.context_store.get_context_for_agent(agent_name)
            
            # Add accumulated context from previous agents
            agent_context['accumulated_results'] = accumulated_context
            
            response = agent.process_request(user_input, accumulated_context, agent_context)
            responses.append(response)
            
            # Update accumulated context with this agent's results
            accumulated_context[f'{agent_name}_result'] = response
        
        # Combine responses intelligently
        return self._combine_responses(responses, user_input)
    
    def _execute_parallel_workflow(self, agents_needed: List[str], user_input: str, parameters: Dict[str, Any], context: ConversationContext) -> str:
        """Execute a parallel workflow with multiple agents"""
        
        responses = []
        
        # Execute all agents in parallel (simulated - could use threading for true parallelism)
        for agent_name in agents_needed:
            if agent_name not in self.agents:
                continue
                
            agent = self.agents[agent_name]
            agent_context = self.context_store.get_context_for_agent(agent_name)
            
            response = agent.process_request(user_input, parameters, agent_context)
            responses.append(response)
        
        # Combine responses
        return self._combine_responses(responses, user_input)
    
    def _execute_complex_workflow(self, agents_needed: List[str], user_input: str, parameters: Dict[str, Any], context: ConversationContext) -> str:
        """Execute a complex multi-step workflow"""
        
        # For complex workflows, we use the orchestrator agent to coordinate
        coordination_prompt = f"""
        You need to coordinate a complex workflow for this user request: "{user_input}"
        
        Available agents: {agents_needed}
        Parameters: {parameters}
        
        Plan and execute the workflow step by step, providing clear feedback to the user.
        """
        
        # This would typically involve more sophisticated coordination
        # For now, fall back to sequential execution
        return self._execute_sequential_workflow(agents_needed, user_input, parameters, context)
    
    def _execute_conversational_workflow(self, user_input: str, parameters: Dict[str, Any], context: ConversationContext) -> str:
        """Execute a conversational workflow for general queries and greetings"""
        
        # Create a conversational prompt for the orchestrator
        conversational_prompt = f"""
        The user said: "{user_input}"
        
        This appears to be a general query or greeting. Respond in a friendly, conversational manner.
        
        Guidelines:
        - For greetings (hi, hello, hey), respond warmly and ask how you can help
        - For general questions, provide helpful information
        - Keep responses concise and friendly
        - Don't provide detailed system status unless specifically requested
        - Be welcoming and professional
        
        Context: You are an AI assistant for the NOMAD-CAMELS measurement automation system.
        """
        
        try:
            response = self.orchestrator_agent.run(conversational_prompt)
            
            # Extract content from RunResponse object if needed
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
            
        except Exception as e:
            self.logger.error(f"Error in conversational workflow: {e}")
            # Fallback to simple responses for common greetings
            user_lower = user_input.lower().strip()
            if user_lower in ['hi', 'hello', 'hey', 'hi there', 'hello there']:
                return "Hello! I'm your NOMAD-CAMELS assistant. How can I help you today? I can help with sample management, running protocols, system status, troubleshooting, or NOMAD integration."
            elif user_lower in ['help', 'what can you do', 'what can you help with']:
                return "I can help you with:\n• Sample management (create, edit, delete samples)\n• Protocol execution and management\n• System status and monitoring\n• Troubleshooting issues\n• NOMAD integration and uploads\n\nWhat would you like to do?"
            else:
                return "I'm here to help with your NOMAD-CAMELS system. Could you please be more specific about what you need assistance with?"
    
    def _combine_responses(self, responses: List[str], user_input: str) -> str:
        """Combine responses from multiple agents into a coherent answer"""
        if not responses:
            return "I wasn't able to get any responses from the agents."
        
        if len(responses) == 1:
            return responses[0]
        
        # Combine multiple responses intelligently
        combined = "Here's what I found:\n\n"
        for i, response in enumerate(responses, 1):
            combined += f"**Response {i}:**\n{response}\n\n"
        
        return combined.strip()
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status information about all agents"""
        try:
            status = {
                'orchestrator': {
                    'status': 'active' if self.orchestrator_agent else 'inactive',
                    'initialized': self.orchestrator_agent is not None
                },
                'agents': {},
                'context_store': {
                    'status': 'active' if self.context_store else 'inactive',
                    'initialized': self.context_store is not None
                }
            }
            
            # Check each capability agent
            for agent_name, agent in self.agents.items():
                status['agents'][agent_name] = {
                    'status': 'active' if agent else 'inactive',
                    'initialized': agent is not None
                }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
            return {
                'orchestrator': {'status': 'error', 'error': str(e)},
                'agents': {},
                'context_store': {'status': 'error', 'error': str(e)}
            } 