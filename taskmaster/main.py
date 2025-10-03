"""
TaskMaster Pro - Main Application Entry Point
"""
import sys
from PyQt6.QtWidgets import QApplication

from taskmaster.views.main_window import MainWindow
from taskmaster.utils.settings import Settings


def main():
    """Main application entry point."""
    # Initialize the application
    app = QApplication(sys.argv)
    app.setApplicationName("TaskMaster Pro")
    app.setApplicationVersion("1.0.0")
    app.setStyle('Fusion')  # Use Fusion style for a modern look

    # Load application settings
    settings = Settings()
    
    # Create and show the main window
    main_window = MainWindow(settings)
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
