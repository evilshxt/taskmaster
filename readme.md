<div align="center">
  <h1>📋 TaskMaster Pro</h1>
  <p>A modern, offline-first task and productivity manager with a beautiful GUI</p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
  [![PyQt6](https://img.shields.io/badge/PyQt6-6.4%2B-41CD52.svg)](https://pypi.org/project/PyQt6/)

  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Project Status: Active">
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey" alt="Platforms">
</div>

## 🚀 Features

| Category | Features |
|----------|----------|
| **Core Functionality** | Add, edit, delete, search, and filter tasks with ease |
| **Organization** | Tags, priority levels, and due dates for better task management |
| **Views** | Multiple views including Today, Upcoming, Overdue, and Completed tasks |
| **Productivity** | Built-in dashboard with visual analytics |
| **Customization** | Dark/Light themes with modern QSS styling |
| **Data** | Import/Export tasks in JSON/CSV formats |

### 📊 Dashboard Features
- 📈 **Activity Overview**: Track your productivity trends
- 🎯 **Task Statistics**: Visualize your task completion rate
- ⏱ **Time Management**: Monitor time spent on tasks
- 📅 **Calendar Integration**: Upcoming deadlines at a glance

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | PyQt6, QtAwesome |
| **Backend** | Python 3.10+ |
| **Database** | SQLite3 |
| **Data Visualization** | Matplotlib |
| **Data Handling** | pandas |

## 📁 Project Structure

```
.
├── taskmaster/              # Main application package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point
│   ├── db.py                # Database models and operations
│   ├── models.py            # Data models
│   ├── views/               # UI view components
│   │   ├── main_window.py   # Main application window
│   │   ├── dialogs/         # Various dialog windows
│   │   └── widgets/         # Custom widgets
│   ├── controllers/         # Business logic
│   ├── utils/               # Utility functions
│   ├── resources/           # Application resources
│   │   ├── icons/           # Application icons
│   │   ├── styles/          # QSS stylesheets
│   │   └── themes/          # Color themes
│   └── tests/               # Unit and integration tests
│
├── docs/                    # Documentation
├── scripts/                 # Build and utility scripts
├── .github/                 # GitHub specific files
│   └── workflows/           # GitHub Actions workflows
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── setup.py               # Package configuration
└── LICENSE                # MIT License
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (for development)

## 🛠 Installation

### Method 1: Using pip (Recommended)
```bash
# Clone the repository
git clone https://github.com/evilshxt/taskmaster.git
cd taskmaster

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m taskmaster.main
```

### Method 2: Development Setup
```bash
# Clone the repository
git clone https://github.com/evilshxt/taskmaster.git
cd taskmaster

# Install in development mode
pip install -e .

# Run tests
pytest
```

## 🎮 Usage

### Basic Commands
| Action | Shortcut | Description |
|--------|----------|-------------|
| New Task | `Ctrl+N` | Create a new task |
| Search | `Ctrl+F` | Focus the search bar |
| Save | `Ctrl+S` | Save all changes |
| Delete | `Del` | Remove selected task(s) |
| Quit | `Ctrl+Q` | Exit the application |

### Task Management
- **Create Tasks**: Add detailed tasks with due dates, tags, and priorities
- **Organize**: Use tags and categories to keep your tasks organized
- **Track Progress**: Visual indicators show task completion status
- **Smart Filters**: Quickly find what you need with powerful filtering options

## 📊 Features in Detail

### Dashboard
- Real-time task statistics
- Visual progress tracking
- Productivity insights

### Task Management
- Rich text formatting
- File attachments
- Subtasks and checklists
- Recurring tasks
- Reminders and notifications

### Data Management
- Local SQLite database
- Automatic backups
- Import/Export (JSON, CSV)
- Data encryption (planned)

## 🚧 Roadmap

### Upcoming Features
| Feature | Status |
|---------|--------|
| Kanban Board View | ⏳ Planned |
| Calendar Integration | ⏳ Planned |
| Pomodoro Timer | ⏳ Planned |
| Encrypted Database | ⏳ Planned |
| Cloud Sync | ⏳ Planned |
| Mobile App | ⏳ Future |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs** using GitHub Issues
2. **Suggest features** by opening an issue
3. **Submit fixes** via Pull Requests
4. **Improve documentation**
5. **Spread the word** about TaskMaster Pro

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### [1.0.0] - 2025-10-03
#### Added
- Initial release with core task management
- Productivity dashboard with charts
- Dark/Light theme support
- Data import/export functionality
- Comprehensive keyboard shortcuts

## 🙏 Acknowledgments
- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Icons by [QtAwesome](https://github.com/spyder-ide/qtawesome)
- Charts powered by [Matplotlib](https://matplotlib.org/)
- Data handling with [pandas](https://pandas.pydata.org/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/evilshxt">evilshxt</a>
</div>