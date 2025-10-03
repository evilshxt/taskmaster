"""Main window for TaskMaster Pro.

This module contains the main application window and its components.
"""
from PyQt6.QtGui import QShortcut
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QFrame, QSplitter,
    QToolBar, QStatusBar, QComboBox, QLineEdit, QStyle, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap, QColor, QPalette
import qtawesome as qta

from ..db.database import db
from ..models.task import Task, Status, Priority
from .dialogs.task_dialog import TaskDialog


class TaskItemWidget(QWidget):
    """Custom widget for displaying a task in the task list."""
    
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.parent = parent  # Store reference to parent for callbacks
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the task item UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Status indicator
        status_icon = QLabel()
        status_pixmap = self._get_status_icon()
        status_icon.setPixmap(status_pixmap)
        status_icon.setFixedSize(24, 24)
        
        # Task title and due date
        text_layout = QVBoxLayout()
        self.title_label = QLabel(self.task.title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        
        details = []
        if self.task.due_date:
            details.append(f"Due: {self.task.due_date.strftime('%b %d, %Y %H:%M')}")
        if self.task.tags:
            details.append(f"Tags: {', '.join(self.task.tags)}")
            
        self.details_label = QLabel(" • ".join(details))
        self.details_label.setStyleSheet("color: #666; font-size: 10pt;")
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.details_label)
        text_layout.setSpacing(2)
        
        # Priority indicator
        priority_label = QLabel()
        priority_label.setFixedSize(10, 10)
        priority_label.setStyleSheet(f"""
            background-color: {self._get_priority_color()};
            border-radius: 5px;
        """)
        
        # Delete button
        delete_btn = QPushButton()
        delete_btn.setIcon(qta.icon('fa5s.trash', color='#ff6b6b'))
        delete_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: #ffebee;
            }
        """)
        delete_btn.setFixedSize(30, 30)
        delete_btn.clicked.connect(self.on_delete_clicked)
        
        # Add widgets to layout
        layout.addWidget(status_icon)
        layout.addLayout(text_layout, 1)
        layout.addWidget(priority_label)
        layout.addWidget(delete_btn)
        
        # Set up styling
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            TaskItemWidget {
                border-bottom: 1px solid #eee;
                background: white;
            }
            TaskItemWidget:hover {
                background: #f5f5f5;
            }
        """)
    
    def _get_status_icon(self):
        """Get the appropriate status icon for the task."""
        if self.task.status == Status.COMPLETED:
            return qta.icon('fa5s.check-circle', color='#4CAF50').pixmap(24, 24)
        elif self.task.status == Status.IN_PROGRESS:
            return qta.icon('fa5s.spinner', color='#2196F3', animation=qta.Spin(self)).pixmap(24, 24)
        else:
            return qta.icon('fa5s.circle', color='#9E9E9E').pixmap(24, 24)
    
    def _get_priority_color(self):
        """Get the color for the priority indicator."""
        colors = {
            Priority.HIGH: '#F44336',
            Priority.MEDIUM: '#FFC107',
            Priority.LOW: '#8BC34A'
        }
        return colors.get(self.task.priority, '#9E9E9E')
        
    def on_delete_clicked(self):
        """Handle delete button click."""
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, 'Delete Task',
            f'Are you sure you want to delete "{self.task.title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Notify parent to handle the deletion
            if hasattr(self.parent, 'delete_task'):
                self.parent.delete_task(self.task.id)


class MainWindow(QMainWindow):
    """Main application window for TaskMaster Pro."""
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.current_filter = "All Tasks"
        self.setup_ui()
        self.load_tasks()
        
        # Connect signals
        self.search_box.textChanged.connect(
            lambda: self.load_tasks(self.search_box.text()))
        self.sort_combo.currentTextChanged.connect(
            lambda: self.load_tasks(self.search_box.text()))
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # New task
        new_shortcut = QShortcut("Ctrl+N", self)
        new_shortcut.activated.connect(self.show_new_task_dialog)
        
        # Search
        search_shortcut = QShortcut("Ctrl+F", self)
        search_shortcut.activated.connect(self.focus_search)
    
    def focus_search(self):
        """Set focus to the search box."""
        self.search_box.setFocus()
        self.search_box.selectAll()
    
    def edit_task(self, task):
        """Edit an existing task."""
        dialog = TaskDialog(task=task, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_task = dialog.get_task()
            if db.update_task(updated_task):
                self.statusBar().showMessage("Task updated successfully!", 3000)
                self.load_tasks()
            else:
                self.statusBar().showMessage("Failed to update task", 3000)
    
    def setup_ui(self):
        """Set up the main window UI."""
        self.setWindowTitle("TaskMaster Pro")
        self.setMinimumSize(1000, 700)
        
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create a splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left sidebar
        sidebar = self.create_sidebar()
        sidebar.setMaximumWidth(250)
        splitter.addWidget(sidebar)
        
        # Main content area
        content = self.create_content_area()
        splitter.addWidget(content)
        
        # Set initial sizes
        splitter.setSizes([200, 800])
        main_layout.addWidget(splitter)
        
        # Set up the menu bar
        self.setup_menu_bar()
        
        # Set up the status bar
        self.statusBar().showMessage("Ready")
        
        # Apply styles
        self.apply_styles()
    
    def create_sidebar(self):
        """Create the sidebar with navigation and filters."""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(15)
        
        # App title
        title = QLabel("TaskMaster Pro")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            padding: 10px;
        """)
        
        # Add task button
        add_button = QPushButton("New Task")
        add_button.setIcon(qta.icon('fa5s.plus'))
        add_button.clicked.connect(self.show_new_task_dialog)
        
        # Filter section
        filter_label = QLabel("FILTERS")
        filter_label.setStyleSheet("""
            color: #666;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 10px;
        """)
        
        # Filter buttons
        filters = [
            ("All Tasks", 'fa5s.tasks'),
            ("Today", 'fa5s.calendar-day'),
            ("Upcoming", 'fa5s.calendar-week'),
            ("Completed", 'fa5s.check-double'),
            ("Overdue", 'fa5s.exclamation-triangle')
        ]
        
        for text, icon in filters:
            btn = QPushButton(text)
            btn.setIcon(qta.icon(icon))
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 15px;
                    border-radius: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                }
                QPushButton:checked {
                    background: #e3f2fd;
                    color: #1976d2;
                    font-weight: bold;
                }
            """)
            btn.setCheckable(True)
            if text == "All Tasks":
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, t=text: self.filter_tasks(t))
            layout.addWidget(btn)
        
        # Add widgets to sidebar
        layout.addWidget(title)
        layout.addWidget(add_button)
        layout.addWidget(filter_label)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return sidebar
    
    def create_content_area(self):
        """Create the main content area with task list and details."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tasks...")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 10px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        
        # Sort combo
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Sort by: Due Date", "Sort by: Priority", "Sort by: Title"])
        
        # Add widgets to toolbar
        toolbar.addWidget(self.search_box)
        toolbar.addSeparator()
        toolbar.addWidget(self.sort_combo)
        
        # Task list
        self.task_list = QListWidget()
        self.task_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.task_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.task_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: white;
            }
            QListWidget::item {
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background: #e3f2fd;
            }
        """)
        
        # Add widgets to layout
        layout.addWidget(toolbar)
        layout.addWidget(self.task_list)
        
        return container
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Task", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.show_new_task_dialog)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        dark_mode = QAction("Dark Mode", self, checkable=True)
        dark_mode.triggered.connect(self.toggle_dark_mode)
        
        view_menu.addAction(dark_mode)
    
    def apply_styles(self):
        """Apply application-wide styles."""
        self.setStyleSheet("""
            QMainWindow {
                background: #f5f5f5;
            }
            #sidebar {
                background: white;
                border-right: 1px solid #e0e0e0;
            }
            QListWidget {
                background: white;
                border: none;
            }
            QToolBar {
                background: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 5px;
                spacing: 5px;
            }
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
        """)
    
    def load_tasks(self, filter_text=None):
        """Load tasks from the database with optional filtering and sorting."""
        self.task_list.clear()
        
        # Get tasks from database
        tasks = db.get_all_tasks()
        
        # Apply filters
        if hasattr(self, 'current_filter'):
            now = datetime.now()
            if self.current_filter == "Today":
                tasks = [t for t in tasks if t.due_date and 
                        t.due_date.date() == now.date()]
            elif self.current_filter == "Upcoming":
                tasks = [t for t in tasks if t.due_date and 
                        t.due_date.date() > now.date() and 
                        t.status != Status.COMPLETED]
            elif self.current_filter == "Completed":
                tasks = [t for t in tasks if t.status == Status.COMPLETED]
            elif self.current_filter == "Overdue":
                tasks = [t for t in tasks if t.due_date and 
                        t.due_date < now and 
                        t.status != Status.COMPLETED]
        
        # Apply search filter
        if filter_text:
            search = filter_text.lower()
            tasks = [t for t in tasks if 
                    search in t.title.lower() or 
                    (t.description and search in t.description.lower()) or
                    any(search in tag.lower() for tag in t.tags)]
        
        # Sort tasks
        sort_by = self.sort_combo.currentText()
        if "Due Date" in sort_by:
            tasks.sort(key=lambda t: (t.due_date is None, t.due_date or datetime.max))
        elif "Priority" in sort_by:
            tasks.sort(key=lambda t: t.priority.value, reverse=True)
        else:  # Title
            tasks.sort(key=lambda t: t.title.lower())
        
        # Add overdue tasks to the top of the list
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.now()]
        tasks = overdue_tasks + [t for t in tasks if t not in overdue_tasks]
        
        for task in tasks:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 80))
            item.setData(Qt.ItemDataRole.UserRole, task.id)
            
            task_widget = TaskItemWidget(task)
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, task_widget)
            
            # Connect double-click to edit
            task_widget.mouseDoubleClickEvent = lambda e, t=task: self.edit_task(t)
    
    def filter_tasks(self, filter_type):
        """Filter tasks based on the selected filter."""
        self.current_filter = filter_type
        self.load_tasks()
        self.statusBar().showMessage(f"Filter: {filter_type}", 2000)
    
    def show_new_task_dialog(self):
        """Show the new task dialog."""
        dialog = TaskDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task = dialog.get_task()
            task_id = db.add_task(task)
            if task_id:
                self.statusBar().showMessage("Task created successfully!", 3000)
                self.load_tasks()
            else:
                self.statusBar().showMessage("Failed to create task", 3000)
    
    def toggle_dark_mode(self, checked):
        """Toggle dark mode."""
        # TODO: Implement dark mode
        if checked:
            self.setStyleSheet("""
                QMainWindow {
                    background: #121212;
                    color: #ffffff;
                }
                #sidebar {
                    background: #1e1e1e;
                    border-right: 1px solid #333;
                }
                QListWidget {
                    background: #1e1e1e;
                    color: #ffffff;
                }
            """)
        else:
            self.apply_styles()
