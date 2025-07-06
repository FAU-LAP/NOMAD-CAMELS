"""
Context Store for Multi-Agent System
====================================

Manages shared state, memory, and context across all agents in the system.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from threading import Lock


@dataclass
class ConversationContext:
    """Context for a single conversation"""
    user_id: str
    session_id: str
    timestamp: datetime
    intent: str
    entities: Dict[str, Any]
    current_task: Optional[str] = None
    task_progress: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat(),
            'intent': self.intent,
            'entities': self.entities,
            'current_task': self.current_task,
            'task_progress': self.task_progress or {}
        }


@dataclass
class SystemState:
    """Current state of NOMAD-CAMELS system"""
    active_user: str
    active_sample: str
    samples: Dict[str, Any]
    users: Dict[str, Any]
    protocols: Dict[str, Any]
    instruments: Dict[str, Any]
    nomad_connected: bool
    nomad_user: Optional[str] = None
    api_server_running: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ContextStore:
    """
    Centralized context and state management for the multi-agent system.
    
    Provides:
    - Conversation context tracking
    - System state management
    - Agent memory and knowledge sharing
    - Task progress tracking
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self._lock = Lock()
        self._conversation_history: List[ConversationContext] = []
        self._agent_memory: Dict[str, Dict[str, Any]] = {}
        self._task_queue: List[Dict[str, Any]] = []
        self._shared_knowledge: Dict[str, Any] = {}
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        
    def get_system_state(self) -> SystemState:
        """Get current system state from NOMAD-CAMELS"""
        try:
            return SystemState(
                active_user=getattr(self.main_window, 'active_user', 'unknown'),
                active_sample=getattr(self.main_window, 'active_sample', 'unknown'),
                samples=getattr(self.main_window, 'sampledata', {}),
                users=getattr(self.main_window, 'userdata', {}),
                protocols=getattr(self.main_window, 'protocols_dict', {}),
                instruments=getattr(self.main_window, 'active_instruments', {}),
                nomad_connected=getattr(self.main_window, 'nomad_user', None) is not None,
                nomad_user=getattr(self.main_window, 'nomad_user', None),
                api_server_running=getattr(self.main_window, 'current_api_port', None) is not None
            )
        except Exception as e:
            self.logger.error(f"Error getting system state: {e}")
            return SystemState(
                active_user='unknown',
                active_sample='unknown',
                samples={},
                users={},
                protocols={},
                instruments={},
                nomad_connected=False
            )
    
    def add_conversation_context(self, context: ConversationContext):
        """Add conversation context to history"""
        with self._lock:
            self._conversation_history.append(context)
            # Keep only last 100 conversations
            if len(self._conversation_history) > 100:
                self._conversation_history = self._conversation_history[-100:]
    
    def get_conversation_history(self, limit: int = 10) -> List[ConversationContext]:
        """Get recent conversation history"""
        with self._lock:
            return self._conversation_history[-limit:] if self._conversation_history else []
    
    def set_agent_memory(self, agent_name: str, key: str, value: Any):
        """Store information in agent's memory"""
        with self._lock:
            if agent_name not in self._agent_memory:
                self._agent_memory[agent_name] = {}
            self._agent_memory[agent_name][key] = value
    
    def get_agent_memory(self, agent_name: str, key: str = None) -> Any:
        """Retrieve information from agent's memory"""
        with self._lock:
            if agent_name not in self._agent_memory:
                return None if key else {}
            
            if key:
                return self._agent_memory[agent_name].get(key)
            return self._agent_memory[agent_name].copy()
    
    def add_task(self, task: Dict[str, Any]):
        """Add task to the queue"""
        with self._lock:
            task['timestamp'] = datetime.now().isoformat()
            task['status'] = 'pending'
            self._task_queue.append(task)
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks"""
        with self._lock:
            return [task for task in self._task_queue if task.get('status') == 'pending']
    
    def update_task_status(self, task_id: str, status: str, result: Any = None):
        """Update task status"""
        with self._lock:
            for task in self._task_queue:
                if task.get('id') == task_id:
                    task['status'] = status
                    task['updated'] = datetime.now().isoformat()
                    if result:
                        task['result'] = result
                    break
    
    def set_shared_knowledge(self, key: str, value: Any):
        """Store shared knowledge accessible to all agents"""
        with self._lock:
            self._shared_knowledge[key] = value
    
    def get_shared_knowledge(self, key: str = None) -> Any:
        """Get shared knowledge"""
        with self._lock:
            if key:
                return self._shared_knowledge.get(key)
            return self._shared_knowledge.copy()
    
    def get_context_for_agent(self, agent_name: str) -> Dict[str, Any]:
        """Get comprehensive context for a specific agent"""
        try:
            system_state = self.get_system_state()
            # Limit conversation history to prevent recursion
            conversation_history = self.get_conversation_history(limit=3)  # Reduced from 10
            agent_memory = self.get_agent_memory(agent_name)
            shared_knowledge = self.get_shared_knowledge()
            
            # Create a simplified context to avoid circular references
            context = {
                'system_state': {
                    'active_user': system_state.active_user,
                    'active_sample': system_state.active_sample,
                    'samples': system_state.samples,
                    'protocols': system_state.protocols,
                    'instruments': system_state.instruments,
                    'nomad_connected': system_state.nomad_connected,
                    'nomad_user': system_state.nomad_user,
                    'api_server_running': system_state.api_server_running
                },
                'agent_memory': agent_memory or {},
                'shared_knowledge': shared_knowledge or {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Only add conversation history if it's not empty and limited
            if conversation_history:
                context['conversation_history'] = [
                    {
                        'intent': ctx.intent,
                        'entities': ctx.entities,
                        'timestamp': ctx.timestamp.isoformat()
                    } for ctx in conversation_history[-2:]  # Only last 2 conversations
                ]
            
            return context
            
        except Exception as e:
            self.logger.error(f"Error getting context for agent {agent_name}: {e}")
            # Return minimal context on error
            return {
                'system_state': {
                    'active_user': 'unknown',
                    'active_sample': 'unknown',
                    'samples': {},
                    'protocols': {},
                    'instruments': {},
                    'nomad_connected': False,
                    'nomad_user': None,
                    'api_server_running': False
                },
                'agent_memory': {},
                'shared_knowledge': {},
                'timestamp': datetime.now().isoformat()
            }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from user input using simple pattern matching"""
        entities = {}
        
        # Sample name patterns
        sample_patterns = [
            r'sample\s+(?:called\s+)?["\']?([^"\']+?)["\']?(?:\s|$)',
            r'create\s+(?:a\s+)?["\']?([^"\']+?)["\']?(?:\s+sample)',
            r'sample\s+["\']?([^"\']+?)["\']?(?:\s+with)',
        ]
        
        # Sample ID patterns
        id_patterns = [
            r'(?:ID|id)\s+([A-Z0-9]+)',
            r'with\s+ID\s+([A-Z0-9]+)',
        ]
        
        # Protocol patterns
        protocol_patterns = [
            r'protocol\s+["\']?([^"\']+?)["\']?',
            r'run\s+(?:the\s+)?["\']?([^"\']+?)["\']?(?:\s+protocol|\s+measurement)',
        ]
        
        import re
        
        # Extract sample names
        for pattern in sample_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities['sample_name'] = match.group(1).strip()
                break
        
        # Extract sample IDs
        for pattern in id_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities['sample_id'] = match.group(1).strip()
                break
        
        # Extract protocols
        for pattern in protocol_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities['protocol_name'] = match.group(1).strip()
                break
        
        return entities
    
    def analyze_intent(self, text: str) -> str:
        """Analyze user intent from text"""
        text_lower = text.lower()
        
        # Sample management intents
        if any(word in text_lower for word in ['create', 'add', 'new']) and 'sample' in text_lower:
            return 'create_sample'
        elif any(word in text_lower for word in ['delete', 'remove']) and 'sample' in text_lower:
            return 'delete_sample'
        elif any(word in text_lower for word in ['list', 'show']) and 'sample' in text_lower:
            return 'list_samples'
        elif 'edit' in text_lower and 'sample' in text_lower:
            return 'edit_sample'
        
        # Protocol intents
        elif any(word in text_lower for word in ['run', 'execute', 'start']) and any(word in text_lower for word in ['protocol', 'measurement']):
            return 'run_protocol'
        elif any(word in text_lower for word in ['list', 'show']) and 'protocol' in text_lower:
            return 'list_protocols'
        
        # Status and information intents
        elif any(word in text_lower for word in ['status', 'state', 'overview']):
            return 'get_status'
        elif any(word in text_lower for word in ['help', 'how', 'what']):
            return 'get_help'
        
        # Troubleshooting intents
        elif any(word in text_lower for word in ['why', 'problem', 'issue', 'error', 'not working']):
            return 'troubleshoot'
        
        # NOMAD intents
        elif 'nomad' in text_lower:
            if any(word in text_lower for word in ['upload', 'sync']):
                return 'nomad_upload'
            elif any(word in text_lower for word in ['login', 'connect']):
                return 'nomad_connect'
            else:
                return 'nomad_status'
        
        # Default
        return 'general_query'
    
    def create_conversation_context(self, user_input: str, session_id: str = "default") -> ConversationContext:
        """Create conversation context from user input"""
        intent = self.analyze_intent(user_input)
        entities = self.extract_entities(user_input)
        
        return ConversationContext(
            user_id=getattr(self.main_window, 'active_user', 'unknown'),
            session_id=session_id,
            timestamp=datetime.now(),
            intent=intent,
            entities=entities
        ) 