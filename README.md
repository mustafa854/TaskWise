### Please check [ProblemStatement.md](./doc/tasks/ProblemStatement.md) to check the tasks assigned for the project! [or CLICK HERE](./doc/tasks/ProblemStatement.md)

### Please check [Endpoints Folder](./doc/endpoints) to check all the endpoints for the project! [or CLICK HERE](./doc/endpoints)

# TaskWise- Project Planner Tool: [DRF REST API]

The TaskWise is a Django application designed to implement a team project planner tool. This tool provides APIs for managing users, teams, and tasks within a team board. The application follows a modular structure, with base abstract classes defining API methods. Concrete implementations of these base classes extend the base classes to create modules for the application. The inputs and outputs of the APIs are in JSON format, adhering to method-specific constraints and raising exceptions for invalid inputs. The application uses local file storage for persistence, with the db folder containing files for storing application data. Users interact with the application only through the APIs, without direct exposure to the internal file storage.

#### [Installation](#installation) | [Technologies Used](#technologies-used)

## Table of Contents

1. [About](#about)
2. [Project Overview](#project-overview)
3. [Installation](#installation)
4. [Usage/API Endpoints, Responses](#usage)
5. [Features](#Features)
6. [Technologies Used](#technologies-used)

## About

TaskWise is a Django REST framework (DRF) API project designed to facilitate team project planning. This application provides APIs for managing users, teams, and tasks with a team board. TaskWise aims to simplify the process of organizing and tracking project tasks within a team, ensuring efficient collaboration and task management.

## Project Overview

TaskWise consists of the following components:

1. Users Management: Create, list users, update, retrieve, and get a user's team.
2. Teams Management: Create, List, update, retrieve, add user to team, remove user from team, and list team users .
3. Team Board: Create, Close, List, and Export Board.
4. Tasks Management: Add Task, update/close Task.
5. Modular Structure: The application follows a modular structure with abstract base classes defining API methods, allowing for easy extension and customization.

## Installation

To run TaskWise locally, follow these steps:

1. **Clone Repositories:**

   - git clone https://github.com/mustafa854/TaskWise.git
   - cd taskwise/

2. **Create and activate a virtual environment:**

```
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies from requirements.txt:**

```
pip install -r requirements.txt
```

4. **Set up the local file storage:**

   - The application creates the necessary directory structure on startup.

5. **Start the Django development server:**

```
python manage.py runserver
```

6. **The API will be available at:**

```
http://localhost:8000/api/
```

## Usage

### API Endpoints

1. Users

- GET /api/users/
  - View all users.
- GET /api/users/teams/
  - View teams associated with users.

2. Teams

- GET /api/teams/
  - View all teams.
- POST /api/teams/
  - Create a new team.
- GET /api/teams/users/
  - List users in a team.

3. Boards

- GET /api/boards/
  - List all boards.
- POST /api/boards/
  - Create a new board.
- PATCH /api/boards/
  - Update board status or close a board.

### API Responses

1. **200 OK:**
   - Successful request.
2. **201 Created:**
   - Successful creation of a resource.
3. **400 Bad Request:**
   - Invalid request data.
4. **404 Not Found:**
   - Resource not found.

### URL Patterns

1. /api/users/: View and manage users.
2. /api/users/teams: View user's teams.
3. /api/teams/: View and manage teams.
4. /api/teams/users: List users in a team.
5. /api/boards/: View and manage boards

## Features

TaskWise is a comprehensive team project planner API with a range of features designed to facilitate efficient team collaboration and task management. Here are the key features provided by TaskWise:

1. User Management:

   - Create User: API to create new users with unique names and display names.
   - List Users: API to retrieve a list of all users with their details.
   - Describe User: API to get detailed information about a specific user.
   - Update User: API to update user details, including display names.

2. Team Management:

   - Create Team: API to create new teams with unique names and descriptions.
   - List Teams: API to retrieve a list of all teams with their details.
   - Describe Team: API to get detailed information about a specific team.
   - Update Team: API to update team details, such as names and descriptions.
   - Add Users to Team: API to add users to a team, with a maximum limit of 50 users.
   - Remove Users from Team: API to remove users from a team.

3. Project Board Management:

   - Create Board: API to create new project boards with unique names and descriptions.
   - Close Board: API to close a board, setting its status to CLOSED when all tasks are marked as COMPLETE.
   - Add Task to Board: API to add tasks to a board, assigning them to a user with specific details.
   - Update Task Status: API to update the status of a task to OPEN, IN_PROGRESS, or COMPLETE.
   - List Boards: API to list all open boards for a specific team.
   - Export Board: API to export a board in a presentable format to a text file in the "out" folder.

4. Persistence:

   - TaskWise uses local file storage for persistence, ensuring data integrity and easy access.
   - The db/ folder contains all files created to persist application data, maintaining separation from the user-facing APIs.
   - Developers can choose the file format and data type for storage.

5. Input and Output:

   - All APIs accept and return JSON strings as input and output, ensuring easy integration with various applications.
   - The structure of JSON inputs and outputs is clearly defined in the method docstrings of each API.
   - Constraints and Error Handling:
   - Each API adheres to specific constraints, such as unique names, character limits, and maximum user additions.
   - The APIs raise exceptions for invalid inputs, ensuring data integrity and error-free operation.

6. Scalability and Modularity:

   - TaskWise follows a modular structure with base abstract classes defining API methods.
   - Concrete implementation modules extend these base classes, allowing for easy scalability and customization.

7. Ease of Deployment:

   - TaskWise can be easily deployed locally or on a server using Django's development server or production-grade deployment options.

## Technologies Used

1. **Django:**

   - Web framework for building the API.

2. **Django REST framework (DRF):**

   - Provides RESTful API development capabilities.
