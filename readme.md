# Taskmaster GUI

A modern, offline-first task and productivity manager built with PyQt6, SQLite, and Matplotlib. Designed to look and feel like a professional web app, but running locally on your desktop.

## Features

- **Beautiful GUI** with PyQt6 + QtAwesome icons
- **Offline-first** with local SQLite database (no account required)
- **Task management**: Add, edit, delete, search, filter
- **Tagging & Priorities**: Organize tasks by tags, priority levels, and due dates
- **Smart filters**: View tasks by Today, Upcoming, Overdue, or Completed
- **Bulk actions**: Mark multiple tasks done or delete at once
- **Productivity Dashboard** (via Matplotlib):
  - Pie chart: Completed vs Pending tasks
  - Bar chart: Tasks per priority level
  - Line chart: Daily completed tasks
- **System Tray Integration** (optional): Quick-add tasks, reminders, and tray menu
- **Export/Import** tasks in JSON/CSV
- **Dark mode** support with modern QSS themes
- **Keyboard shortcuts** for faster navigation
- **Data backup** functionality

## Tech Stack

- **Python 3.10+**
- **PyQt6** → GUI framework
- **QtAwesome** → FontAwesome-based icons
- **SQLite3** → Local database persistence
- **Matplotlib** → Charts & analytics
- **pandas** → CSV/JSON import/export

## Project Structure

taskmaster/
├── taskmaster/
│   ├── main.py            # App entry point
│   ├── db.py              # Database layer (SQLite helpers)
│   ├── models.py          # Task model class
│   ├── ui/                # Qt Designer .ui files (optional)
│   ├── views/             # PyQt6 widgets & windows
│   ├── charts.py          # Matplotlib integration
│   └── resources/         # Icons, themes, QSS
│
├── tests/
│   └── test_tasks.py      # Unit tests
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/evilshxt/taskmaster.git
   cd taskmaster
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python taskmaster/main.py
   ```

## Usage

### Basic Navigation
- **Add task**: Click the ➕ button or press `Ctrl+N`
- **Edit task**: Double-click on a task in the list
- **Search tasks**: Use the search bar (filters live as you type)
- **Filters**: Switch between All, Today, Upcoming, Completed
- **Dashboard**: View task stats & productivity charts
- **Export/Import**: Use menu bar → File → Export/Import

### Keyboard Shortcuts
- `Ctrl+N`: New Task
- `Ctrl+F`: Focus search bar
- `Ctrl+Q`: Quit application
- `Ctrl+S`: Save changes
- `Delete`: Delete selected task(s)

## Roadmap

### Planned Features
- [ ] Kanban Board View (drag tasks across columns)
- [ ] Calendar Integration (view tasks in monthly calendar)
- [ ] Pomodoro Timer (linked to tasks)
- [ ] Encrypted Database Mode (for privacy)
- [ ] Optional Cloud Sync (Google Tasks / Notion API)

## Contributing

Pull requests and feature suggestions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Changelog

### [1.0.0] - 2025-10-03
#### Added
- Initial release of Taskmaster GUI
- Basic task management functionality
- Productivity dashboard
- Export/Import features
- Dark mode support

## Acknowledgments
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [QtAwesome](https://github.com/spyder-ide/qtawesome) for the beautiful icons
- [Matplotlib](https://matplotlib.org/) for the charts
- [pandas](https://pandas.pydata.org/) for data handling

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.