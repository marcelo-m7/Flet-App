# Flet-App: Cross-Platform Todo List Manager

A modern, multi-platform todo list application built with [Flet](https://flet.dev/) that compiles to native desktop and mobile apps with persistent cloud-synced tasks.

## ✨ Features

### 🔐 **User Authentication**
- Secure user registration and login system
- Session-based authentication management
- Individual task isolation per user
- Password-protected accounts

### 📝 **Task Management**
- Create, edit, and delete tasks seamlessly
- Mark tasks as complete/incomplete with checkboxes
- Real-time task filtering (All, Active, Completed)
- Task completion counter showing active items
- One-click clear completed tasks feature
- Persistent storage in MySQL database

### 🌐 **Multi-Platform Support**
- **Desktop** (Windows, macOS, Linux) - Native application experience
- **Web** - Browser-based access with responsive design
- **Mobile** (iOS, Android) - Full-featured mobile apps

### 💾 **Data Persistence**
- MySQL database backend for reliable data storage
- Automatic synchronization of changes
- User-specific task isolation
- Data maintained across sessions

### 🎨 **User Interface**
- Clean, intuitive Material Design interface
- Responsive layout adapting to different screen sizes
- Smooth transitions between views (display/edit modes)
- Organized task display with action buttons

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MySQL Server
- Package manager: `uv` (recommended) or `Poetry`

### Installation

#### Using uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/marcelo-m7/Flet-App.git
cd Flet-App

# Install dependencies
uv sync
```

#### Using Poetry
```bash
# Clone the repository
git clone https://github.com/marcelo-m7/Flet-App.git
cd Flet-App

# Install dependencies
poetry install
```

### Configuration

1. Set up your MySQL database:
```sql
CREATE DATABASE todoapp;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

2. Create a `.env` file in the `src/` directory:
```env
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=todoapp
```

## ▶️ Running the Application

### Desktop Application

**Using uv:**
```bash
uv run flet run
```

**Using Poetry:**
```bash
poetry run flet run
```

The app will launch in a native desktop window (port 3000).

### Web Application

**Using uv:**
```bash
uv run flet run --web
```

**Using Poetry:**
```bash
poetry run flet run --web
```

Access the web app at `http://localhost:8000`

### Database Viewer (Development)

Inspect your database in a web interface:
```bash
python src/db_viwer.py
```

Visit `http://localhost:3001` to view users and tasks tables.

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env

# Deploy
docker-compose up -d
```

Access the app at `http://localhost:8000`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 📦 Building for Distribution

### Android

```bash
flet build apk -v
```

See [Android Packaging Guide](https://flet.dev/docs/publish/android/) for details on signing and distribution.

### iOS

```bash
flet build ipa -v
```

See [iOS Packaging Guide](https://flet.dev/docs/publish/ios/) for details on signing and App Store distribution.

### macOS

```bash
flet build macos -v
```

See [macOS Packaging Guide](https://flet.dev/docs/publish/macos/) for details.

### Linux

```bash
flet build linux -v
```

See [Linux Packaging Guide](https://flet.dev/docs/publish/linux/) for details.

### Windows

```bash
flet build windows -v
```

See [Windows Packaging Guide](https://flet.dev/docs/publish/windows/) for details.

## 🏗️ Project Architecture

```
Flet-App/
├── src/
│   ├── main.py              # App entry point, handles routing
│   ├── auth.py              # Authentication manager
│   ├── todo.py              # Task management and UI
│   ├── config.py            # Configuration and environment variables
│   ├── db_viwer.py          # Database inspection utility
│   └── assets/
│       └── icons/           # Application icons
├── Dockerfile               # Production Docker image
├── docker-compose.yml       # Multi-container orchestration
├── init.sql                 # Database schema initialization
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata and Flet config
└── README.md               # This file
```

### Key Components

- **AuthManager** (`auth.py`): Handles user registration, login, and session management
- **TodoApp** (`todo.py`): Main UI container with task list, filters, and database operations
- **Task** (`todo.py`): Individual task component with edit/delete capabilities
- **Config** (`config.py`): Centralized environment and database configuration

## 🔧 Development

### Project Structure
- All application code is in the `src/` directory
- Configuration is managed through environment variables
- Database connections are centralized in `config.py`
- UI components are built with Flet's widget system

### Adding Features

#### Add a New Task Property
1. Modify the `Task` class in `todo.py` to include new fields
2. Update the database schema to add new columns
3. Modify `save_tasks()` and `load_tasks()` to handle the new field
4. Update the UI in `_display_view()` to show the new property

#### Create a New Screen
1. Create a new class extending `ft.Column`
2. Add transition logic in `main.py`
3. Use `page.clean()` and `page.add()` for screen transitions
4. Pass user context via `page.session["user_id"]`

## 🗄️ Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| username | VARCHAR(255) | UNIQUE, NOT NULL |
| password | VARCHAR(255) | NOT NULL |

### Tasks Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| user_id | INT | FOREIGN KEY → users.id |
| task_name | VARCHAR(255) | NOT NULL |
| completed | BOOLEAN | DEFAULT FALSE |

## 🛡️ Security Considerations

⚠️ **Current Implementation Notes:**
- Passwords are stored in plaintext (should be hashed in production)
- Database credentials are loaded from environment variables
- Use HTTPS in production deployments
- Consider implementing password hashing with `bcrypt` or `argon2`

**Recommended for Production:**
- Hash passwords using industry-standard algorithms
- Use environment variables or secret management systems
- Enable database SSL connections
- Implement rate limiting on authentication endpoints
- Add CSRF protection for web deployments

## 📚 Dependencies

- **flet** (0.27.1+) - Cross-platform UI framework
- **pymysql** - MySQL database connector
- **cryptography** - Encryption utilities
- **python-dotenv** - Environment variable management

See [requirements.txt](requirements.txt) for the complete dependency list.

## 📖 Additional Resources

- [Flet Documentation](https://flet.dev/docs/)
- [Flet Getting Started Guide](https://flet.dev/docs/getting-started/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 👤 Author

**Marcelo Santos**
- Email: marcelo@monynha.com
- Company: Monynha Softwares

---

**Created with ❤️ using Flet** - A framework for building beautiful, cross-platform applications with Python.