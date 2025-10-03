"""
Task model for TaskMaster Pro.

This module defines the Task class which represents a single task in the application.
"""
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional


class Priority(Enum):
    """Task priority levels."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Status(Enum):
    """Task status values."""
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class Task:
    """Represents a task in the TaskMaster application."""
    
    def __init__(self, 
                 title: str, 
                 description: str = "",
                 priority: Priority = Priority.MEDIUM,
                 status: Status = Status.TODO,
                 due_date: Optional[datetime] = None,
                 tags: Optional[List[str]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """Initialize a new task.
        
        Args:
            title: The title of the task.
            description: A detailed description of the task.
            priority: The priority level of the task.
            status: The current status of the task.
            due_date: Optional due date for the task.
            tags: Optional list of tags for categorization.
            created_at: When the task was created. Defaults to now.
            updated_at: When the task was last updated. Defaults to now.
        """
        self.id: Optional[int] = None  # Will be set by the database
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.tags = tags or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def __repr__(self) -> str:
        """Return a string representation of the task."""
        return f"<Task(id={self.id}, title='{self.title}', status={self.status.name})>"
    
    def to_dict(self) -> dict:
        """Convert the task to a dictionary for serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.name,
            'status': self.status.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary."""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority[data.get('priority', 'MEDIUM')],
            status=Status(data.get('status', 'To Do')),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            tags=data.get('tags', [])
        )
        task.id = data.get('id')
        task.created_at = (datetime.fromisoformat(data['created_at']) 
                          if 'created_at' in data else datetime.now())
        task.updated_at = (datetime.fromisoformat(data['updated_at']) 
                          if 'updated_at' in data else datetime.now())
        return task
