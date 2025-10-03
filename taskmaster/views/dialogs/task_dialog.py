"""Task creation and editing dialog for TaskMaster Pro."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QDateTimeEdit, QDialogButtonBox,
    QPushButton, QListWidget, QListWidgetItem, QWidget
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIcon
import qtawesome as qta

from ...models.task import Task, Priority, Status


class TaskDialog(QDialog):
    """Dialog for creating or editing a task."""
    
    def __init__(self, task=None, parent=None):
        """Initialize the dialog.
        
        Args:
            task: Optional Task object to edit. If None, creates a new task.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.task = task if task else Task("")
        self.setup_ui()
        self.setWindowTitle("Edit Task" if task else "New Task")
        self.setMinimumWidth(500)
    
    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Title
        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit(self.task.title)
        layout.addWidget(self.title_edit)
        
        # Description
        layout.addWidget(QLabel("Description"))
        self.desc_edit = QTextEdit(self.task.description)
        self.desc_edit.setMaximumHeight(100)
        layout.addWidget(self.desc_edit)
        
        # Priority
        layout.addWidget(QLabel("Priority"))
        self.priority_combo = QComboBox()
        for priority in Priority:
            self.priority_combo.addItem(priority.name.title(), priority)
        self.priority_combo.setCurrentText(self.task.priority.name.title())
        layout.addWidget(self.priority_combo)
        
        # Status
        layout.addWidget(QLabel("Status"))
        self.status_combo = QComboBox()
        for status in Status:
            self.status_combo.addItem(status.value, status)
        self.status_combo.setCurrentText(self.task.status.value)
        layout.addWidget(self.status_combo)
        
        # Due Date
        layout.addWidget(QLabel("Due Date"))
        self.due_date_edit = QDateTimeEdit()
        self.due_date_edit.setCalendarPopup(True)
        if self.task.due_date:
            self.due_date_edit.setDateTime(self.task.due_date)
        else:
            self.due_date_edit.setDateTime(QDateTime.currentDateTime().addDays(7))
        layout.addWidget(self.due_date_edit)
        
        # Tags
        layout.addWidget(QLabel("Tags (comma separated)"))
        self.tags_edit = QLineEdit(", ".join(self.task.tags))
        layout.addWidget(self.tags_edit)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_task(self):
        """Get the task with updated values from the form.
        
        Returns:
            Task: The updated task.
        """
        self.task.title = self.title_edit.text().strip()
        self.task.description = self.desc_edit.toPlainText().strip()
        self.task.priority = self.priority_combo.currentData()
        self.task.status = self.status_combo.currentData()
        self.task.due_date = self.due_date_edit.dateTime().toPyDateTime()
        self.task.tags = [t.strip() for t in self.tags_edit.text().split(",") if t.strip()]
        return self.task
