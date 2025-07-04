"""
Toast Notification System for NOMAD CAMELS

This module provides a professional toast notification system that can be used
throughout the application for better user experience. It includes both toast
notifications and enhanced error handling capabilities.

Features:
- Toast notifications with different types (info, warning, error, success)
- Auto-dismiss functionality
- Customizable duration and styling
- Non-blocking notifications
- Enhanced error handling with toast integration
- Modular design for easy integration
"""

import logging
from typing import Optional, Union, Callable, Dict, Any
from enum import Enum
from dataclasses import dataclass
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsOpacityEffect,
    QApplication,
    QMessageBox,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    Signal,
    QThread,
    QObject,
    QRect,
)
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap, QPainter, QPen


class ToastType(Enum):
    """Enumeration for different types of toast notifications."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ToastConfig:
    """Configuration class for toast notifications."""
    duration: int = 5000  # milliseconds
    position: str = "top-right"  # top-right, top-left, bottom-right, bottom-left, center
    max_width: int = 400
    min_width: int = 300
    auto_dismiss: bool = True
    show_icon: bool = True
    show_close_button: bool = True
    animation_duration: int = 300
    stack_notifications: bool = True
    max_stack_count: int = 5


class ToastNotification(QFrame):
    """
    A professional toast notification widget.
    
    This widget provides a modern, non-blocking notification system that can be
    used throughout the application for better user experience.
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
        self.animation = None
        self.is_dismissed = False
        self.main_window = self._find_main_window()
        self.opacity_effect = None
        self.shadow_effect = None
        
        self._setup_ui()
        self._setup_styling()
        self._setup_effects()
        
        if self.config.auto_dismiss:
            self._start_dismiss_timer()
    
    def _find_main_window(self) -> Optional[QWidget]:
        """Find the main application window."""
        if self.parent():
            # Walk up the parent hierarchy to find the main window
            current = self.parent()
            while current:
                if hasattr(current, 'windowTitle') and 'NOMAD CAMELS' in current.windowTitle():
                    return current
                current = current.parent()
        return None
    
    def _setup_ui(self):
        """Setup the user interface components."""
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        # Remove translucent background to make it completely opaque
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header row (title + close button)
        if self.title or self.config.show_close_button:
            header_layout = QHBoxLayout()
            header_layout.setSpacing(12)
            
            # Icon
            if self.config.show_icon:
                icon_label = QLabel()
                icon_label.setFixedSize(28, 28)
                icon_label.setPixmap(self._get_icon_pixmap())
                header_layout.addWidget(icon_label)
            
            # Title
            if self.title:
                title_label = QLabel(self.title)
                title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
                title_label.setWordWrap(True)
                header_layout.addWidget(title_label)
            
            header_layout.addStretch()
            
            # Close button
            if self.config.show_close_button:
                close_button = QLabel("✕")
                close_button.setFixedSize(28, 28)
                close_button.setAlignment(Qt.AlignCenter)
                close_button.setStyleSheet("""
                    QLabel {
                        color: #999;
                        font-size: 18px;
                        font-weight: bold;
                        background: transparent;
                        border: none;
                        border-radius: 14px;
                    }
                    QLabel:hover {
                        color: #fff;
                        background-color: rgba(255, 255, 255, 0.2);
                    }
                """)
                close_button.mousePressEvent = lambda e: self.dismiss()
                header_layout.addWidget(close_button)
            
            layout.addLayout(header_layout)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Segoe UI", 14))
        layout.addWidget(message_label)
        
        # Set size constraints
        self.setMaximumWidth(self.config.max_width)
        self.setMinimumWidth(self.config.min_width)
        self.adjustSize()
    
    def _setup_styling(self):
        """Setup the visual styling based on toast type."""
        # Color schemes for different toast types with improved colors
        color_schemes = {
            ToastType.INFO: {
                "bg": "#000000",
                "border": "#2196F3",
                "text": "#FFFFFF",
                "icon_bg": "#2196F3"
            },
            ToastType.SUCCESS: {
                "bg": "#000000",
                "border": "#4CAF50",
                "text": "#FFFFFF",
                "icon_bg": "#4CAF50"
            },
            ToastType.WARNING: {
                "bg": "#000000",
                "border": "#FF9800",
                "text": "#FFFFFF",
                "icon_bg": "#FF9800"
            },
            ToastType.ERROR: {
                "bg": "#000000",
                "border": "#FF4444",
                "text": "#FFFFFF",
                "icon_bg": "#FF4444"
            }
        }
        
        colors = color_schemes[self.toast_type]
        
        # Modern styling with completely opaque black background
        style = f"""
            QFrame {{
                background-color: {colors['bg']};
                border: 2px solid {colors['border']};
                border-radius: 12px;
                color: {colors['text']};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.5;
            }}
            QLabel {{
                color: {colors['text']};
                background: transparent;
                border: none;
            }}
        """
        
        self.setStyleSheet(style)
    
    def _setup_effects(self):
        """Setup both shadow and opacity effects properly."""
        # Create a combined effect container
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setColor(QColor(0, 0, 0, 60))
        self.shadow_effect.setOffset(0, 4)
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0)
        
        # Apply shadow effect first
        self.setGraphicsEffect(self.shadow_effect)
    
    def _get_icon_pixmap(self) -> QPixmap:
        """Get the appropriate icon pixmap for the toast type."""
        # Create a modern circular icon
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Color mapping for icons
        color_map = {
            ToastType.INFO: QColor("#2196F3"),     # Blue
            ToastType.SUCCESS: QColor("#4CAF50"),  # Green
            ToastType.WARNING: QColor("#FF9800"),  # Orange
            ToastType.ERROR: QColor("#D32F2F")     # Dark Red (a shade of red)
        }
        color = color_map[self.toast_type]
        
        # Draw circular background
        painter.setBrush(color)
        painter.setPen(QPen(color, 1))
        painter.drawEllipse(2, 2, 20, 20)
        
        # Draw icon symbol based on type
        painter.setPen(QPen(Qt.white, 2))
        if self.toast_type == ToastType.INFO:
            # Info icon (i)
            painter.drawText(QRect(0, 0, 24, 24), Qt.AlignCenter, "i")
        elif self.toast_type == ToastType.SUCCESS:
            # Checkmark
            painter.drawLine(7, 12, 11, 16)
            painter.drawLine(11, 16, 17, 8)
        elif self.toast_type == ToastType.WARNING:
            # Warning triangle
            painter.drawLine(12, 5, 5, 19)
            painter.drawLine(5, 19, 19, 19)
            painter.drawLine(19, 19, 12, 5)
            painter.drawEllipse(11, 13, 2, 2)
        elif self.toast_type == ToastType.ERROR:
            # X mark
            painter.drawLine(7, 7, 17, 17)
            painter.drawLine(17, 7, 7, 17)
        
        painter.end()
        return pixmap
    
    def _start_dismiss_timer(self):
        """Start the auto-dismiss timer."""
        self.dismiss_timer = QTimer(self)
        self.dismiss_timer.timeout.connect(self.dismiss)
        self.dismiss_timer.start(self.config.duration)
    
    def show_notification(self):
        """Show the notification with entrance animation."""
        self._position_notification()
        self.show()
        
        # Create a new opacity effect for animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self.opacity_effect)
        
        # Entrance animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(self.config.animation_duration)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
    
    def _position_notification(self):
        """Position the notification relative to the main window or screen."""
        if self.main_window and self.main_window.isVisible():
            # Position relative to main window
            window_geometry = self.main_window.geometry()
            notification_size = self.size()
            
            # Calculate positions relative to main window
            positions = {
                "top-right": QPoint(
                    window_geometry.x() + window_geometry.width() - notification_size.width() - 20,
                    window_geometry.y() + 20
                ),
                "top-left": QPoint(
                    window_geometry.x() + 20,
                    window_geometry.y() + 20
                ),
                "bottom-right": QPoint(
                    window_geometry.x() + window_geometry.width() - notification_size.width() - 20,
                    window_geometry.y() + window_geometry.height() - notification_size.height() - 20
                ),
                "bottom-left": QPoint(
                    window_geometry.x() + 20,
                    window_geometry.y() + window_geometry.height() - notification_size.height() - 20
                ),
                "center": QPoint(
                    window_geometry.x() + (window_geometry.width() - notification_size.width()) // 2,
                    window_geometry.y() + (window_geometry.height() - notification_size.height()) // 2
                )
            }
        else:
            # Fallback to screen positioning
            screen = QApplication.primaryScreen().geometry()
            notification_size = self.size()
            
            positions = {
                "top-right": QPoint(screen.width() - notification_size.width() - 20, 20),
                "top-left": QPoint(20, 20),
                "bottom-right": QPoint(screen.width() - notification_size.width() - 20, 
                                     screen.height() - notification_size.height() - 20),
                "bottom-left": QPoint(20, screen.height() - notification_size.height() - 20),
                "center": QPoint((screen.width() - notification_size.width()) // 2,
                               (screen.height() - notification_size.height()) // 2)
            }
        
        pos = positions.get(self.config.position, positions["top-right"])
        self.move(pos)
    
    def dismiss(self):
        """Dismiss the notification with exit animation."""
        if self.is_dismissed:
            return
        
        self.is_dismissed = True
        
        if self.dismiss_timer:
            self.dismiss_timer.stop()
        
        # Create a new opacity effect for exit animation
        if self.opacity_effect is None:
            self.opacity_effect = QGraphicsOpacityEffect()
            self.opacity_effect.setOpacity(1.0)
            self.setGraphicsEffect(self.opacity_effect)
        
        # Exit animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(self.config.animation_duration)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self._on_dismiss_finished)
        self.animation.start()
    
    def _on_dismiss_finished(self):
        """Handle the completion of dismiss animation."""
        self.hide()
        self.dismissed.emit()
        self.deleteLater()
    
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.LeftButton and self.callback:
            self.callback()
            self.clicked.emit()
        super().mousePressEvent(event)


class ToastManager(QObject):
    """
    Manager class for handling multiple toast notifications.
    
    This class manages the display, stacking, and lifecycle of toast notifications
    throughout the application.
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the toast manager."""
        super().__init__(parent)
        self.active_toasts: Dict[int, ToastNotification] = {}
        self.toast_counter = 0
        self.default_config = ToastConfig()
    
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
        toast = ToastNotification(
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
    
    def _stack_notification(self, toast: ToastNotification):
        """Stack the notification with existing ones."""
        if len(self.active_toasts) >= toast.config.max_stack_count:
            # Remove oldest toast
            oldest_id = min(self.active_toasts.keys())
            self._remove_toast(oldest_id)
        
        # Adjust position for stacking
        main_window = toast.main_window
        if main_window and main_window.isVisible():
            window_geometry = main_window.geometry()
            toast_size = toast.size()
            
            # Calculate position based on stack
            stack_index = len(self.active_toasts)
            offset_y = stack_index * (toast_size.height() + 10)
            
            if toast.config.position == "top-right":
                pos = QPoint(
                    window_geometry.x() + window_geometry.width() - toast_size.width() - 20,
                    window_geometry.y() + 20 + offset_y
                )
            elif toast.config.position == "top-left":
                pos = QPoint(
                    window_geometry.x() + 20,
                    window_geometry.y() + 20 + offset_y
                )
            elif toast.config.position == "bottom-right":
                pos = QPoint(
                    window_geometry.x() + window_geometry.width() - toast_size.width() - 20,
                    window_geometry.y() + window_geometry.height() - toast_size.height() - 20 - offset_y
                )
            elif toast.config.position == "bottom-left":
                pos = QPoint(
                    window_geometry.x() + 20,
                    window_geometry.y() + window_geometry.height() - toast_size.height() - 20 - offset_y
                )
            else:  # center
                pos = QPoint(
                    window_geometry.x() + (window_geometry.width() - toast_size.width()) // 2,
                    window_geometry.y() + (window_geometry.height() - toast_size.height()) // 2
                )
        else:
            # Fallback to screen positioning
            screen = QApplication.primaryScreen().geometry()
            toast_size = toast.size()
            
            # Calculate position based on stack
            stack_index = len(self.active_toasts)
            offset_y = stack_index * (toast_size.height() + 10)
            
            if toast.config.position == "top-right":
                pos = QPoint(screen.width() - toast_size.width() - 20, 20 + offset_y)
            elif toast.config.position == "top-left":
                pos = QPoint(20, 20 + offset_y)
            elif toast.config.position == "bottom-right":
                pos = QPoint(screen.width() - toast_size.width() - 20,
                            screen.height() - toast_size.height() - 20 - offset_y)
            elif toast.config.position == "bottom-left":
                pos = QPoint(20, screen.height() - toast_size.height() - 20 - offset_y)
            else:  # center
                pos = QPoint((screen.width() - toast_size.width()) // 2,
                            (screen.height() - toast_size.height()) // 2)
        
        toast.move(pos)
    
    def _position_notification(self, toast: ToastNotification):
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
            config=ToastConfig(duration=8000, auto_dismiss=True)
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
            config=ToastConfig(duration=10000, auto_dismiss=True)
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