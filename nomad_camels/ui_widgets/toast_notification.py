"""
Toast Notification System for NOMAD CAMELS

This module provides an elegant toast notification system based on QMessageBox
for better user experience. It includes both toast notifications and enhanced 
error handling capabilities.

Features:
- Toast notifications with different types (info, warning, error, success)
- Auto-dismiss functionality
- Non-blocking notifications
- Enhanced error handling with toast integration
- Elegant UI using native QMessageBox styling
- Modular design for easy integration
"""

import logging
from typing import Optional, Union, Callable, Dict, Any
from enum import Enum
from dataclasses import dataclass
from PySide6.QtWidgets import (
    QMessageBox,
    QApplication,
    QWidget,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
    QObject,
    Signal,
    QEvent,
)
from PySide6.QtGui import QIcon


class ToastType(Enum):
    """Enumeration for different types of toast notifications."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ToastConfig:
    """Configuration class for toast notifications."""
    duration: int = 2000  # milliseconds (2 seconds)
    position: str = "top-right"  # top-right, top-left, bottom-right, bottom-left, center
    auto_dismiss: bool = True
    show_icon: bool = True
    stack_notifications: bool = True
    max_stack_count: int = 5


class ToastMessageBox(QMessageBox):
    """
    A toast notification widget based on QMessageBox for elegant UI.
    
    This widget provides a modern, non-blocking notification system that uses
    the native QMessageBox styling for consistency and elegance.
    """
    
    # Signals
    dismissed = Signal()
    clicked = Signal()
    
    def __init__(
        self,
        message: str,
        title: str = "",
        toast_type: ToastType = ToastType.INFO,
        config: Optional[ToastConfig] = None,
        parent: Optional[QWidget] = None,
        callback: Optional[Callable] = None
    ):
        """
        Initialize the toast notification.
        
        Args:
            message: The main message to display
            title: Optional title for the notification
            toast_type: Type of notification (info, success, warning, error)
            config: Configuration object for the toast
            parent: Parent widget
            callback: Optional callback function to execute when clicked
        """
        super().__init__(parent)
        
        self.message = message
        self.title = title
        self.toast_type = toast_type
        self.config = config or ToastConfig()
        self.callback = callback
        self.dismiss_timer = None
        self.is_dismissed = False
        self.main_window = self._find_main_window()
        
        self._setup_ui()
        
        if self.config.auto_dismiss:
            self._start_dismiss_timer()
        
        self._setup_window_resize_handling()
    
    def _find_main_window(self) -> Optional[QWidget]:
        """Find the main application window."""
        if self.parent():
            # Walk up the parent hierarchy to find the main window
            current = self.parent()
            while current:
                if hasattr(current, 'windowTitle') and 'NOMAD CAMELS' in current.windowTitle():
                    return current
                current = current.parent()
        
        # If no parent with NOMAD CAMELS title, try to find any top-level window
        app = QApplication.instance()
        if app:
            for widget in app.topLevelWidgets():
                if widget.isVisible() and hasattr(widget, 'windowTitle'):
                    return widget
        return None
    
    def _setup_ui(self):
        """Setup the user interface components."""
        # Set window flags for toast-like behavior
        self.setWindowFlags(self.windowFlags() | Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Set text and title
        self.setText(self.message)
        if self.title:
            self.setWindowTitle(f"{self.title} - NOMAD CAMELS")
        else:
            self.setWindowTitle("NOMAD CAMELS")
        
        # Set icon based on toast type
        if self.config.show_icon:
            self._set_icon()
        
        # Remove standard buttons for toast-like appearance
        self.setStandardButtons(QMessageBox.NoButton)
        
        # Connect signals
        self.accepted.connect(self._on_clicked)
        self.rejected.connect(self._on_clicked)
    
    def _set_icon(self):
        """Set the appropriate icon for the toast type."""
        icon_map = {
            ToastType.INFO: QMessageBox.Information,
            ToastType.SUCCESS: QMessageBox.Information,  # Use Information for success
            ToastType.WARNING: QMessageBox.Warning,
            ToastType.ERROR: QMessageBox.Critical
        }
        self.setIcon(icon_map.get(self.toast_type, QMessageBox.Information))
    
    def _start_dismiss_timer(self):
        """Start the auto-dismiss timer."""
        self.dismiss_timer = QTimer(self)
        self.dismiss_timer.timeout.connect(self.dismiss)
        self.dismiss_timer.start(self.config.duration)
    
    def show_notification(self):
        """Show the notification with proper positioning."""
        # Make sure the toast is visible and properly sized
        self.adjustSize()
        self._position_notification()
        self.show()
        self.raise_()  # Bring to front
        self.activateWindow()  # Ensure it's active
    
    def _position_notification(self):
        """Position the notification inside the main window."""
        # Get the notification size first
        notification_size = self.size()
        if notification_size.width() <= 0 or notification_size.height() <= 0:
            # If size is not valid, adjust size first
            self.adjustSize()
            notification_size = self.size()
        
        if self.main_window and self.main_window.isVisible():
            # Get the main window's position and size
            window_geometry = self.main_window.geometry()
            
            # Calculate positions inside the main window with margins
            margin = 20  # Small margin from window edges
            positions = {
                "top-right": (
                    window_geometry.x() + window_geometry.width() - notification_size.width() - margin,
                    window_geometry.y() + margin
                ),
                "top-left": (
                    window_geometry.x() + margin,
                    window_geometry.y() + margin
                ),
                "bottom-right": (
                    window_geometry.x() + window_geometry.width() - notification_size.width() - margin,
                    window_geometry.y() + window_geometry.height() - notification_size.height() - margin
                ),
                "bottom-left": (
                    window_geometry.x() + margin,
                    window_geometry.y() + window_geometry.height() - notification_size.height() - margin
                ),
                "center": (
                    window_geometry.x() + (window_geometry.width() - notification_size.width()) // 2,
                    window_geometry.y() + (window_geometry.height() - notification_size.height()) // 2
                )
            }
            
            pos = positions.get(self.config.position, positions["top-right"])
            self.move(pos[0], pos[1])
        else:
            # Fallback to screen positioning
            screen = QApplication.primaryScreen().geometry()
            
            positions = {
                "top-right": (screen.width() - notification_size.width() - 20, 20),
                "top-left": (20, 20),
                "bottom-right": (screen.width() - notification_size.width() - 20, 
                               screen.height() - notification_size.height() - 20),
                "bottom-left": (20, screen.height() - notification_size.height() - 20),
                "center": ((screen.width() - notification_size.width()) // 2,
                          (screen.height() - notification_size.height()) // 2)
            }
            
            pos = positions.get(self.config.position, positions["top-right"])
            self.move(pos[0], pos[1])
    
    def dismiss(self):
        """Dismiss the notification."""
        if self.is_dismissed:
            return
        
        self.is_dismissed = True
        
        if self.dismiss_timer:
            self.dismiss_timer.stop()
        
        self.hide()
        self.dismissed.emit()
        self.deleteLater()
    
    def _on_clicked(self):
        """Handle click events."""
        if self.callback:
            self.callback()
        self.clicked.emit()
        self.dismiss()
    
    def _setup_window_resize_handling(self):
        """Setup window resize event handling for dynamic positioning."""
        if self.main_window:
            # Install event filter on main window to catch resize events
            self.main_window.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        """Filter events to handle window resize."""
        if obj == self.main_window and event.type() == QEvent.Resize:
            # Reposition toast when main window is resized
            self._position_notification()
        elif obj == self.main_window and event.type() == QEvent.Move:
            # Reposition toast when main window is moved
            self._position_notification()
        elif obj == self.main_window and event.type() == QEvent.WindowStateChange:
            # Handle window state changes (minimize/maximize/restore)
            self._handle_window_state_change()
        elif event.type() == QEvent.ScreenChangeInternal:
            # Handle screen geometry changes
            self._position_notification()
        return super().eventFilter(obj, event)
    
    def _handle_window_state_change(self):
        """Handle window state changes."""
        if self.main_window.isMinimized():
            # Hide toast when window is minimized
            self.hide()
        else:
            # Show and reposition toast when window is restored
            self.show()
            self._position_notification()


class ToastManager(QObject):
    """
    Manager class for handling multiple toast notifications.
    
    This class manages the display, stacking, and lifecycle of toast notifications
    throughout the application.
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the toast manager."""
        super().__init__(parent)
        self.active_toasts: Dict[int, ToastMessageBox] = {}
        self.toast_counter = 0
        self.default_config = ToastConfig()
        self.main_window = self._find_main_window()
        self._setup_window_resize_handling()
    
    def _find_main_window(self) -> Optional[QWidget]:
        """Find the main application window."""
        if self.parent():
            # Walk up the parent hierarchy to find the main window
            current = self.parent()
            while current:
                if hasattr(current, 'windowTitle') and 'NOMAD CAMELS' in current.windowTitle():
                    return current
                current = current.parent()
        
        # If no parent with NOMAD CAMELS title, try to find any top-level window
        app = QApplication.instance()
        if app:
            for widget in app.topLevelWidgets():
                if widget.isVisible() and hasattr(widget, 'windowTitle'):
                    return widget
        return None
    
    def _setup_window_resize_handling(self):
        """Setup window resize event handling for dynamic positioning."""
        if self.main_window:
            # Install event filter on main window to catch resize events
            self.main_window.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        """Filter events to handle window resize."""
        if obj == self.main_window and event.type() == QEvent.Resize:
            # Reposition all active toasts when main window is resized
            self._reposition_all_toasts()
        elif obj == self.main_window and event.type() == QEvent.Move:
            # Reposition all active toasts when main window is moved
            self._reposition_all_toasts()
        elif obj == self.main_window and event.type() == QEvent.WindowStateChange:
            # Handle window state changes (minimize/maximize/restore)
            self._handle_window_state_change()
        elif event.type() == QEvent.ScreenChangeInternal:
            # Handle screen geometry changes
            self._reposition_all_toasts()
        return super().eventFilter(obj, event)
    
    def _reposition_all_toasts(self):
        """Reposition all active toast notifications."""
        if not self.active_toasts:
            return
        
        # Get all toasts and their configurations
        toasts_with_configs = []
        for toast_id, toast in self.active_toasts.items():
            toasts_with_configs.append((toast_id, toast))
        
        # Clear active toasts temporarily
        self.active_toasts.clear()
        
        # Reposition each toast
        for toast_id, toast in toasts_with_configs:
            if toast.isVisible():
                self.active_toasts[toast_id] = toast
                if toast.config.stack_notifications:
                    self._stack_notification(toast)
                else:
                    self._position_notification(toast)
    
    def show_toast(
        self,
        message: str,
        title: str = "",
        toast_type: ToastType = ToastType.INFO,
        config: Optional[ToastConfig] = None,
        callback: Optional[Callable] = None
    ) -> int:
        """
        Show a toast notification.
        
        Args:
            message: The message to display
            title: Optional title
            toast_type: Type of notification
            config: Optional configuration
            callback: Optional callback function
            
        Returns:
            The toast ID for later reference
        """
        toast_config = config or self.default_config
        
        # Create toast notification
        toast = ToastMessageBox(
            message=message,
            title=title,
            toast_type=toast_type,
            config=toast_config,
            parent=self.parent(),
            callback=callback
        )
        
        # Handle stacking
        if toast_config.stack_notifications:
            self._stack_notification(toast)
        else:
            self._position_notification(toast)
        
        # Store reference
        toast_id = self.toast_counter
        self.active_toasts[toast_id] = toast
        self.toast_counter += 1
        
        # Connect signals
        toast.dismissed.connect(lambda: self._remove_toast(toast_id))
        
        # Show the toast
        toast.show_notification()
        
        return toast_id
    
    def _stack_notification(self, toast: ToastMessageBox):
        """Stack the notification with existing ones."""
        if len(self.active_toasts) >= toast.config.max_stack_count:
            # Remove oldest toast
            oldest_id = min(self.active_toasts.keys())
            self._remove_toast(oldest_id)
        
        # Calculate position based on current stack
        main_window = toast.main_window
        if main_window and main_window.isVisible():
            window_geometry = main_window.geometry()
            toast_size = toast.size()
            
            # Count visible toasts for this position
            visible_count = 0
            for existing_toast in self.active_toasts.values():
                if (existing_toast.isVisible() and 
                    existing_toast.config.position == toast.config.position):
                    visible_count += 1
            
            # Calculate offset based on visible count
            offset_y = visible_count * (toast_size.height() + 10)
            margin = 20  # Small margin from window edges
            
            if toast.config.position == "top-right":
                pos = (
                    window_geometry.x() + window_geometry.width() - toast_size.width() - margin,
                    window_geometry.y() + margin + offset_y
                )
            elif toast.config.position == "top-left":
                pos = (
                    window_geometry.x() + margin,
                    window_geometry.y() + margin + offset_y
                )
            elif toast.config.position == "bottom-right":
                pos = (
                    window_geometry.x() + window_geometry.width() - toast_size.width() - margin,
                    window_geometry.y() + window_geometry.height() - toast_size.height() - margin - offset_y
                )
            elif toast.config.position == "bottom-left":
                pos = (
                    window_geometry.x() + margin,
                    window_geometry.y() + window_geometry.height() - toast_size.height() - margin - offset_y
                )
            else:  # center
                pos = (
                    window_geometry.x() + (window_geometry.width() - toast_size.width()) // 2,
                    window_geometry.y() + (window_geometry.height() - toast_size.height()) // 2
                )
            
            toast.move(pos[0], pos[1])
        else:
            # Fallback to screen positioning
            screen = QApplication.primaryScreen().geometry()
            toast_size = toast.size()
            
            # Count visible toasts for this position
            visible_count = 0
            for existing_toast in self.active_toasts.values():
                if (existing_toast.isVisible() and 
                    existing_toast.config.position == toast.config.position):
                    visible_count += 1
            
            # Calculate offset based on visible count
            offset_y = visible_count * (toast_size.height() + 10)
            
            if toast.config.position == "top-right":
                pos = (screen.width() - toast_size.width() - 20, 20 + offset_y)
            elif toast.config.position == "top-left":
                pos = (20, 20 + offset_y)
            elif toast.config.position == "bottom-right":
                pos = (screen.width() - toast_size.width() - 20,
                      screen.height() - toast_size.height() - 20 - offset_y)
            elif toast.config.position == "bottom-left":
                pos = (20, screen.height() - toast_size.height() - 20 - offset_y)
            else:  # center
                pos = ((screen.width() - toast_size.width()) // 2,
                      (screen.height() - toast_size.height()) // 2)
            
            toast.move(pos[0], pos[1])
    
    def _position_notification(self, toast: ToastMessageBox):
        """Position a single notification."""
        toast._position_notification()
    
    def _remove_toast(self, toast_id: int):
        """Remove a toast from the active list."""
        if toast_id in self.active_toasts:
            del self.active_toasts[toast_id]
    
    def dismiss_all(self):
        """Dismiss all active toast notifications."""
        for toast in list(self.active_toasts.values()):
            toast.dismiss()
    
    def dismiss_toast(self, toast_id: int):
        """Dismiss a specific toast notification."""
        if toast_id in self.active_toasts:
            self.active_toasts[toast_id].dismiss()
    
    def _handle_window_state_change(self):
        """Handle window state changes."""
        if self.main_window.isMinimized():
            # Hide all toasts when window is minimized
            for toast in self.active_toasts.values():
                if toast.isVisible():
                    toast.hide()
        else:
            # Show and reposition all toasts when window is restored
            self._reposition_all_toasts()
            for toast in self.active_toasts.values():
                if not toast.isVisible():
                    toast.show()


class EnhancedErrorHandler:
    """
    Enhanced error handler that provides better user experience for errors.
    
    This class provides methods to handle errors gracefully with toast notifications
    instead of raising exceptions or showing blocking dialogs.
    """
    
    def __init__(self, toast_manager: ToastManager, parent: Optional[QWidget] = None):
        """
        Initialize the enhanced error handler.
        
        Args:
            toast_manager: The toast manager instance
            parent: Parent widget for fallback dialogs
        """
        self.toast_manager = toast_manager
        self.parent = parent
        self.logger = logging.getLogger(__name__)
    
    def handle_validation_error(
        self,
        error_message: str,
        title: str = "Validation Error",
        show_dialog: bool = False,
        log_error: bool = True
    ) -> bool:
        """
        Handle validation errors with toast notification.
        
        Args:
            error_message: The error message to display
            title: Title for the notification
            show_dialog: Whether to also show a dialog
            log_error: Whether to log the error
            
        Returns:
            False to indicate validation failure
        """
        if log_error:
            self.logger.warning(f"Validation error: {error_message}")
        
        # Show toast notification
        self.toast_manager.show_toast(
            message=error_message,
            title=title,
            toast_type=ToastType.ERROR,
            config=ToastConfig(duration=2000, auto_dismiss=True)
        )
        
        # Optionally show dialog
        if show_dialog:
            self._show_error_dialog(error_message, title)
        
        return False
    
    def handle_general_error(
        self,
        error: Exception,
        context: str = "",
        show_dialog: bool = False,
        log_error: bool = True
    ) -> None:
        """
        Handle general errors with toast notification.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
            show_dialog: Whether to also show a dialog
            log_error: Whether to log the error
        """
        error_message = str(error)
        title = "Error"
        
        if log_error:
            self.logger.error(f"Error in {context}: {error_message}", exc_info=True)
        
        # Show toast notification
        self.toast_manager.show_toast(
            message=error_message,
            title=title,
            toast_type=ToastType.ERROR,
            config=ToastConfig(duration=2000, auto_dismiss=True)
        )
        
        # Optionally show dialog
        if show_dialog:
            self._show_error_dialog(error_message, title)
    
    def _show_error_dialog(self, message: str, title: str):
        """Show a fallback error dialog."""
        if self.parent:
            QMessageBox.critical(self.parent, title, message)
        else:
            QMessageBox.critical(None, title, message)


# Global toast manager instance
_global_toast_manager: Optional[ToastManager] = None
_global_error_handler: Optional[EnhancedErrorHandler] = None


def get_toast_manager(parent: Optional[QWidget] = None) -> ToastManager:
    """
    Get the global toast manager instance.
    
    Args:
        parent: Parent widget for the toast manager
        
    Returns:
        The global toast manager instance
    """
    global _global_toast_manager
    if _global_toast_manager is None:
        _global_toast_manager = ToastManager(parent)
    return _global_toast_manager


def get_error_handler(parent: Optional[QWidget] = None) -> EnhancedErrorHandler:
    """
    Get the global error handler instance.
    
    Args:
        parent: Parent widget for the error handler
        
    Returns:
        The global error handler instance
    """
    global _global_error_handler
    if _global_error_handler is None:
        toast_manager = get_toast_manager(parent)
        _global_error_handler = EnhancedErrorHandler(toast_manager, parent)
    return _global_error_handler


def show_toast(
    message: str,
    title: str = "",
    toast_type: ToastType = ToastType.INFO,
    config: Optional[ToastConfig] = None,
    callback: Optional[Callable] = None,
    parent: Optional[QWidget] = None
) -> int:
    """
    Convenience function to show a toast notification.
    
    Args:
        message: The message to display
        title: Optional title
        toast_type: Type of notification
        config: Optional configuration
        callback: Optional callback function
        parent: Parent widget
        
    Returns:
        The toast ID
    """
    toast_manager = get_toast_manager(parent)
    return toast_manager.show_toast(message, title, toast_type, config, callback)


def handle_validation_error(
    error_message: str,
    title: str = "Validation Error",
    show_dialog: bool = False,
    parent: Optional[QWidget] = None
) -> bool:
    """
    Convenience function to handle validation errors.
    
    Args:
        error_message: The error message
        title: Title for the notification
        show_dialog: Whether to also show a dialog
        parent: Parent widget
        
    Returns:
        False to indicate validation failure
    """
    error_handler = get_error_handler(parent)
    return error_handler.handle_validation_error(error_message, title, show_dialog)


def handle_general_error(
    error: Exception,
    context: str = "",
    show_dialog: bool = False,
    parent: Optional[QWidget] = None
) -> None:
    """
    Convenience function to handle general errors.
    
    Args:
        error: The exception that occurred
        context: Additional context
        show_dialog: Whether to also show a dialog
        parent: Parent widget
    """
    error_handler = get_error_handler(parent)
    error_handler.handle_general_error(error, context, show_dialog) 