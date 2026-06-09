# Jungle Integration Guide

This project now uses **Jungle** for task automation.

## Available Commands

Run any task using:
```bash
jungle [task-name]
```

### Core Django Tasks

- **`jungle runserver`** - Start development server on port 8000
  - Usage: `jungle runserver 8000` or `jungle runserver 3000`

- **`jungle migrate`** - Apply database migrations
  
- **`jungle makemigrations`** - Create new migration files from model changes

- **`jungle collectstatic`** - Collect static files

- **`jungle createsuperuser`** - Create a Django admin user

- **`jungle test`** - Run all Django tests

- **`jungle shell`** - Open Django interactive shell

- **`jungle dbshell`** - Open database shell

### Utility Tasks

- **`jungle build`** - Run migrations + collect static files (production setup)

- **`jungle setup`** - Initial project setup (migrations + superuser + static files)

- **`jungle clean`** - Remove Python cache files (__pycache__, .pytest_cache)

- **`jungle flush`** - Clear the database (be careful!)

- **`jungle info`** - Display Django project information

## Examples

```bash
# Start the development server
jungle runserver

# Prepare for production
jungle build

# Initial setup after cloning project
jungle setup

# Run tests
jungle test

# Clean up cache files
jungle clean
```

## Installation

Jungle is already installed in your requirements.txt. To install all dependencies:
```bash
pip install -r requirements.txt
```

## Junglefile

All tasks are defined in `Junglefile` at the project root. You can view or modify tasks there.
