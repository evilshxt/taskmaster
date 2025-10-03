"""
Database module for TaskMaster Pro.

This module handles all database operations for the application.
"""
import os
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.task import Task, Priority, Status


class Database:
    """Handles all database operations for TaskMaster Pro."""
    
    def __init__(self, db_path: str = None):
        """Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses a default location.
        """
        if db_path is None:
            # Default database location in user's app data directory
            app_data = os.getenv('APPDATA') or os.path.expanduser('~')
            db_dir = os.path.join(app_data, 'TaskMasterPro')
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'taskmaster.db')
        
        self.db_path = db_path
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    
    def _init_db(self):
        """Initialize the database schema if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Enable foreign key support
            cursor.execute('PRAGMA foreign_keys = ON')
            
            # Create tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    due_date TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create tags table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')
            
            # Create task_tags junction table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_tags (
                    task_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (task_id, tag_id),
                    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
    
    # Task CRUD operations
    def add_task(self, task: Task) -> int:
        """Add a new task to the database.
        
        Args:
            task: The task to add.
            
        Returns:
            The ID of the newly created task.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert the task
            cursor.execute('''
                INSERT INTO tasks (title, description, priority, status, due_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.title,
                task.description,
                task.priority.name,
                task.status.value,
                task.due_date.isoformat() if task.due_date else None,
                task.created_at.isoformat(),
                task.updated_at.isoformat()
            ))
            
            task_id = cursor.lastrowid
            
            # Add tags
            if task.tags:
                self._update_task_tags(cursor, task_id, task.tags)
            
            conn.commit()
            return task_id
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            The Task object, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task_data = cursor.fetchone()
            
            if not task_data:
                return None
            
            # Get tags for this task
            cursor.execute('''
                SELECT t.name FROM tags t
                JOIN task_tags tt ON t.id = tt.tag_id
                WHERE tt.task_id = ?
            ''', (task_id,))
            tags = [row['name'] for row in cursor.fetchall()]
            
            return self._row_to_task(dict(task_data), tags)
    
    def update_task(self, task: Task) -> bool:
        """Update an existing task.
        
        Args:
            task: The task with updated information.
            
        Returns:
            True if the task was updated, False otherwise.
        """
        if task.id is None:
            return False
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Update the task
            cursor.execute('''
                UPDATE tasks
                SET title = ?, description = ?, priority = ?, status = ?, 
                    due_date = ?, updated_at = ?
                WHERE id = ?
            ''', (
                task.title,
                task.description,
                task.priority.name,
                task.status.value,
                task.due_date.isoformat() if task.due_date else None,
                datetime.now().isoformat(),
                task.id
            ))
            
            if cursor.rowcount == 0:
                return False
            
            # Update tags
            if hasattr(task, 'tags') and task.tags is not None:
                self._update_task_tags(cursor, task.id, task.tags)
            
            conn.commit()
            return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete.
            
        Returns:
            True if the task was deleted, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
    
    def get_all_tasks(self, status: Status = None) -> List[Task]:
        """Get all tasks, optionally filtered by status.
        
        Args:
            status: If provided, only return tasks with this status.
            
        Returns:
            A list of Task objects.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if status:
                cursor.execute('SELECT * FROM tasks WHERE status = ?', (status.value,))
            else:
                cursor.execute('SELECT * FROM tasks')
            
            tasks = []
            for row in cursor.fetchall():
                task_id = row['id']
                
                # Get tags for this task
                cursor.execute('''
                    SELECT t.name FROM tags t
                    JOIN task_tags tt ON t.id = tt.tag_id
                    WHERE tt.task_id = ?
                ''', (task_id,))
                tags = [tag_row['name'] for tag_row in cursor.fetchall()]
                
                tasks.append(self._row_to_task(dict(row), tags))
            
            return tasks
    
    # Helper methods
    def _update_task_tags(self, cursor: sqlite3.Cursor, task_id: int, tags: List[str]):
        """Update the tags for a task.
        
        Args:
            cursor: Database cursor.
            task_id: ID of the task.
            tags: List of tag names.
        """
        # Remove existing tags
        cursor.execute('DELETE FROM task_tags WHERE task_id = ?', (task_id,))
        
        if not tags:
            return
        
        # Add new tags
        for tag_name in tags:
            # Get or create the tag
            cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
            tag_row = cursor.fetchone()
            
            if tag_row:
                tag_id = tag_row['id']
            else:
                cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
                tag_id = cursor.lastrowid
            
            # Link tag to task
            cursor.execute('''
                INSERT OR IGNORE INTO task_tags (task_id, tag_id)
                VALUES (?, ?)
            ''', (task_id, tag_id))
    
    @staticmethod
    def _row_to_task(row: Dict[str, Any], tags: List[str]) -> Task:
        """Convert a database row to a Task object."""
        from datetime import datetime
        
        task = Task(
            title=row['title'],
            description=row['description'],
            priority=Priority[row['priority']],
            status=Status(row['status']),
            due_date=datetime.fromisoformat(row['due_date']) if row['due_date'] else None,
            tags=tags,
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )
        task.id = row['id']
        return task


# Create a default database instance
db = Database()
