"""
Chat Interface Widget for NOMAD-CAMELS
Provides a ChatGPT-like interface for user assistance and automated actions.
"""

import json
import asyncio
from typing import Dict, Any, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QScrollArea, QLabel, QSplitter, QMessageBox, QDialog, QFormLayout,
    QDialogButtonBox, QCheckBox, QSpinBox, QComboBox, QFrame, QMainWindow, QStyle
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QTextCursor, QIcon, QPixmap
import logging

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ChatMessage(QWidget):
    """A single chat message widget"""
    
    def __init__(self, message: str, is_user: bool = True, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(800)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Message bubble
        message_widget = QLabel(message)
        message_widget.setWordWrap(True)
        message_widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_widget.setStyleSheet(
            f"""
            QLabel {{
                background-color: {'#007ACC' if is_user else '#f0f0f0'};
                color: {'white' if is_user else 'black'};
                padding: 10px;
                border-radius: 10px;
                max-width: 600px;
            }}
            """
        )
        
        if is_user:
            layout.addStretch()
            layout.addWidget(message_widget)
        else:
            layout.addWidget(message_widget)
            layout.addStretch()
        
        self.setLayout(layout)


class APIKeyDialog(QDialog):
    """Dialog for entering OpenAI API key"""
    
    def __init__(self, parent=None, current_key: str = ""):
        super().__init__(parent)
        self.setWindowTitle("OpenAI API Key Configuration")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Info label
        info_label = QLabel(
            "Please enter your OpenAI API key to enable AI chat functionality.\n"
            "You can get your API key from https://platform.openai.com/account/api-keys"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setText(current_key)
        self.api_key_input.setPlaceholderText("sk-...")
        form_layout.addRow("API Key:", self.api_key_input)
        
        self.save_key_checkbox = QCheckBox("Save API key (stored locally)")
        self.save_key_checkbox.setChecked(True)
        form_layout.addRow("", self.save_key_checkbox)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def get_api_key(self) -> tuple[str, bool]:
        return self.api_key_input.text().strip(), self.save_key_checkbox.isChecked()


class ChatWorker(QThread):
    """Worker thread for OpenAI API calls"""
    
    message_received = Signal(str)
    error_occurred = Signal(str)
    action_requested = Signal(str, dict)  # action_type, parameters
    
    def __init__(self, api_key: str, message: str, chat_history: list):
        super().__init__()
        self.api_key = api_key
        self.message = message
        self.chat_history = chat_history
        
    def run(self):
        try:
            if not OPENAI_AVAILABLE:
                self.error_occurred.emit("OpenAI library not installed. Please install it with: pip install openai")
                return
            
            # Configure OpenAI client
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            # Prepare system prompt
            system_prompt = """You are an AI assistant for NOMAD-CAMELS, a configurable measurement software for experimental solid-state physics. 

You can help users with:
- Understanding how to use NOMAD-CAMELS
- Creating and managing samples
- Setting up measurements
- Troubleshooting issues

When a user asks to add a new sample, respond with a helpful message asking for the sample details, then call the add_sample function.

For sample creation, you need these details:
- Sample name (required)
- Sample ID (optional)
- Description (optional)
- Owner (will be set to current user)

If the user wants to add a sample, ask for the required information and then use the following format to trigger the action:
ACTION:add_sample:{"name": "sample_name", "sample_id": "optional_id", "description": "optional_description"}

Always be helpful and guide users through the process step by step."""
            
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history
            for msg in self.chat_history[-10:]:  # Last 10 messages for context
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": self.message})
            
            # Make API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Check if response contains an action
            if reply.startswith("ACTION:"):
                parts = reply.split(":", 2)
                if len(parts) >= 3:
                    action_type = parts[1]
                    try:
                        parameters = json.loads(parts[2])
                        self.action_requested.emit(action_type, parameters)
                        # Also send a user-friendly message
                        self.message_received.emit("I'll help you add that sample now. Opening the sample dialog...")
                    except json.JSONDecodeError:
                        self.message_received.emit(reply)
                else:
                    self.message_received.emit(reply)
            else:
                self.message_received.emit(reply)
                
        except Exception as e:
            self.error_occurred.emit(f"Error communicating with OpenAI: {str(e)}")


class ChatWindow(QMainWindow):
    """Standalone chat window"""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowTitle("NOMAD-CAMELS AI Assistant")
        self.setMinimumSize(600, 500)
        self.resize(800, 600)
        
        # Create chat interface
        self.chat_interface = ChatInterface(main_window, self)
        self.setCentralWidget(self.chat_interface)
        
        # Set window icon
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.hide()
        event.ignore()  # Don't actually close, just hide


class ChatInterface(QWidget):
    """Main chat interface widget"""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.chat_history = []
        self.api_key = ""
        self.worker = None
        
        self.setup_ui()
        self.load_api_key()
        
    def setup_ui(self):
        """Setup the chat interface UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("NOMAD-CAMELS AI Assistant")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # API Key button
        self.api_key_button = QPushButton("Configure API Key")
        self.api_key_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #005A9B;
            }
        """)
        self.api_key_button.clicked.connect(self.configure_api_key)
        header_layout.addWidget(self.api_key_button)
        
        layout.addLayout(header_layout)
        
        # Chat area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(10)
        
        self.chat_scroll.setWidget(self.chat_widget)
        layout.addWidget(self.chat_scroll)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here... (e.g., 'I want to add a new sample')")
        self.message_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005A9B;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Status label
        self.status_label = QLabel("Ready. Configure your OpenAI API key to start chatting.")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Add welcome message
        self.add_message("Hello! I'm your NOMAD-CAMELS AI assistant. I can help you with:\n\n"
                        "• Adding new samples\n"
                        "• Managing measurement protocols\n"
                        "• Understanding NOMAD-CAMELS features\n"
                        "• Troubleshooting issues\n\n"
                        "Try saying: 'I want to add a new sample'", False)
        
    def load_api_key(self):
        """Load API key from preferences"""
        if hasattr(self.main_window, 'preferences') and 'openai_api_key' in self.main_window.preferences:
            self.api_key = self.main_window.preferences['openai_api_key']
            if self.api_key:
                self.status_label.setText("API key configured. Ready to chat!")
                
    def configure_api_key(self):
        """Open API key configuration dialog"""
        dialog = APIKeyDialog(self, self.api_key)
        if dialog.exec():
            api_key, save_key = dialog.get_api_key()
            if api_key:
                self.api_key = api_key
                if save_key:
                    # Save to preferences
                    if hasattr(self.main_window, 'preferences'):
                        self.main_window.preferences['openai_api_key'] = api_key
                        from nomad_camels.utility import load_save_functions
                        load_save_functions.save_preferences(self.main_window.preferences)
                self.status_label.setText("API key configured successfully!")
            else:
                QMessageBox.warning(self, "Invalid API Key", "Please enter a valid OpenAI API key.")
                
    def add_message(self, message: str, is_user: bool = True):
        """Add a message to the chat"""
        message_widget = ChatMessage(message, is_user)
        self.chat_layout.addWidget(message_widget)
        
        # Scroll to bottom
        QTimer.singleShot(10, self.scroll_to_bottom)
        
        # Add to history
        role = "user" if is_user else "assistant"
        self.chat_history.append({"role": role, "content": message})
        
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        """Send a message to the AI"""
        message = self.message_input.text().strip()
        if not message:
            return
            
        if not self.api_key:
            QMessageBox.warning(self, "API Key Required", 
                              "Please configure your OpenAI API key first.")
            self.configure_api_key()
            return
            
        if not OPENAI_AVAILABLE:
            QMessageBox.warning(self, "OpenAI Not Available", 
                              "OpenAI library is not installed. Please install it with:\npip install openai")
            return
            
        # Add user message
        self.add_message(message, True)
        self.message_input.clear()
        
        # Disable input while processing
        self.message_input.setEnabled(False)
        self.send_button.setEnabled(False)
        self.status_label.setText("AI is thinking...")
        
        # Start worker thread
        self.worker = ChatWorker(self.api_key, message, self.chat_history)
        self.worker.message_received.connect(self.on_message_received)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.action_requested.connect(self.on_action_requested)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()
        
    def on_message_received(self, message: str):
        """Handle received AI message"""
        self.add_message(message, False)
        
    def on_error(self, error: str):
        """Handle error"""
        self.add_message(f"Error: {error}", False)
        
    def on_action_requested(self, action_type: str, parameters: dict):
        """Handle action request from AI"""
        if action_type == "add_sample":
            self.handle_add_sample_action(parameters)
        else:
            self.add_message(f"Unknown action requested: {action_type}", False)
            
    def handle_add_sample_action(self, parameters: dict):
        """Handle add sample action"""
        try:
            # Extract sample information
            sample_name = parameters.get('name', '')
            sample_id = parameters.get('sample_id', '')
            description = parameters.get('description', '')
            
            if not sample_name:
                self.add_message("I need a sample name to create the sample. Please provide a name.", False)
                return
            
            # Add sample to the main window's sample data
            sample_data = {
                'name': sample_name,
                'sample_id': sample_id,
                'description': description,
                'owner': self.main_window.active_user
            }
            
            # Add to sampledata
            self.main_window.sampledata[sample_name] = sample_data
            
            # Update UI
            self.main_window.update_shown_samples()
            self.main_window.save_sample_data()
            
            # Set as active sample
            self.main_window.active_sample = sample_name
            self.main_window.comboBox_sample.setCurrentText(sample_name)
            
            # Show success message
            success_message = f"✅ Sample '{sample_name}' has been successfully added!"
            if sample_id:
                success_message += f"\nSample ID: {sample_id}"
            if description:
                success_message += f"\nDescription: {description}"
            success_message += f"\nOwner: {self.main_window.active_user}"
            
            self.add_message(success_message, False)
            
            # Optional: Open the sample edit dialog to show the created sample
            QTimer.singleShot(1000, self.show_sample_dialog)
            
        except Exception as e:
            self.add_message(f"Error adding sample: {str(e)}", False)
            logging.error(f"Error in handle_add_sample_action: {e}")
            
    def show_sample_dialog(self):
        """Show the sample edit dialog"""
        try:
            self.main_window.edit_sample_info()
            self.add_message("The sample information dialog has been opened so you can see and edit the sample details.", False)
        except Exception as e:
            logging.error(f"Error showing sample dialog: {e}")
            
    def on_worker_finished(self):
        """Handle worker thread completion"""
        self.message_input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.status_label.setText("Ready to chat!")
        
        if self.worker:
            self.worker.deleteLater()
            self.worker = None 