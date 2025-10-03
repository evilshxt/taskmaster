"""Main window for TaskMaster Pro.

This module contains the main application window and its components.
"""
from PyQt6.QtGui import QShortcut
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QFrame, QSplitter,
    QToolBar, QStatusBar, QComboBox, QLineEdit, QStyle, QMessageBox,
    QTabWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer, QDateTime
from PyQt6.QtGui import QIcon, QAction, QPixmap, QColor, QPalette
import qtawesome as qta

from ..db.database import db
from ..models.task import Task, Status, Priority
from .dialogs.task_dialog import TaskDialog
from .widgets.dashboard_widget import DashboardWidget


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
        """Create the main content area with tabs for dashboard and task list."""
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Dashboard tab
        self.dashboard = DashboardWidget()
        self.tab_widget.addTab(self.dashboard, "Dashboard")
        
        # Tasks tab
        tasks_tab = QWidget()
        tasks_layout = QVBoxLayout(tasks_tab)
        tasks_layout.setContentsMargins(0, 0, 0, 0)
        tasks_layout.setSpacing(0)
        
        # Search and filter bar
        filter_bar = QWidget()
        filter_layout = QHBoxLayout(filter_bar)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tasks...")
        self.search_box.setClearButtonEnabled(True)
        
        # Sort combo
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Due Date", "Priority", "Title"])
        
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_box)
        filter_layout.addWidget(QLabel("Sort by:"))
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addStretch()
        
        # Task list
        self.tasks_list = QListWidget()
        self.tasks_list.setAlternatingRowColors(True)
        self.tasks_list.setStyleSheet("""
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
        
        tasks_layout.addWidget(filter_bar)
        tasks_layout.addWidget(self.tasks_list)
        
        # Add tasks tab
        self.tab_widget.addTab(tasks_tab, "Tasks")
        
        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        return self.tab_widget
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Task", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.show_new_task_dialog)
        file_menu.addAction(new_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.dark_mode_action = QAction("Dark Mode", self, checkable=True)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def load_tasks(self, filter_text=None):
        """Load tasks from the database with optional filtering and sorting."""
        # Get tasks from database
        tasks = db.get_tasks()
        
        # Apply filters if any
        if filter_text:
            filter_text = filter_text.lower()
            filtered_tasks = [t for t in tasks 
                           if filter_text in t.title.lower() 
                           or filter_text in (t.description or '').lower()
                           or any(filter_text in tag.lower() for tag in t.tags)]
        else:
            filtered_tasks = tasks
        
        # Sort tasks
        sort_by = self.sort_combo.currentText()
        if sort_by == "Due Date":
            filtered_tasks.sort(key=lambda t: (t.due_date is None, t.due_date or QDateTime.currentDateTime()))
        elif sort_by == "Priority":
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            filtered_tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
        else:  # Title
            filtered_tasks.sort(key=lambda t: t.title.lower())
        
        # Update tasks list
        self.update_tasks_list(filtered_tasks)
        
        # Update dashboard if it's the current tab
        if hasattr(self, 'tab_widget') and self.tab_widget.currentIndex() == 0:  # Dashboard tab
            self.dashboard.update_stats(tasks)  # Use all tasks for dashboard stats
        
        # Update status bar
        self.statusBar().showMessage(f"Loaded {len(filtered_tasks)} tasks", 3000)
        
        return tasks
    
    def update_tasks_list(self, tasks):
        """Update the tasks list with the given tasks."""
        self.tasks_list.clear()
        for task in tasks:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 80))  # Set fixed height for each item
            
            task_widget = TaskItemWidget(task, self)
            self.tasks_list.addItem(item)
            self.tasks_list.setItemWidget(item, task_widget)
    
    def on_tab_changed(self, index):
        """Handle tab change event."""
        if index == 0:  # Dashboard tab
            # Update dashboard with all tasks
            tasks = db.get_tasks()
            self.dashboard.update_stats(tasks)
    
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
