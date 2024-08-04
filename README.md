
# Ticket System

This project is a ticket management system built with Django and Docker.

### Role-Based Access Control (RBAC)

This project uses Role-Based Access Control (RBAC) through permissions. The permissions are assigned to roles, which are then assigned to users. This makes the system scalable and easy to modify as new roles or permissions can be added without changing the underlying code.


## Getting Started

These instructions will help you set up and run the project in your local development environment.

### Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    ```

2. **Create and configure environment variables**:

    Copy the `.env.sample` file to a new `.env` file:

    ```sh
    cp .env.sample .env
    ```

    Then open the `.env` file and enter the necessary data:

    ```env
    # Django settings
    DJANGO_SECRET_KEY=your_secret_key_here
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

    # Database settings
    POSTGRES_NAME=ticket_system
    POSTGRES_USER=ticket_user
    POSTGRES_PASSWORD=ticket_password
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ```

### Running the Project

1. **Build and run the Docker containers**:

    ```sh
    docker-compose up --build
    ```

    This command will build the Docker images and start the containers.

2. **Initialize the database and create default roles, permissions, and users** (only needed on the first run):

    Open a new terminal and run the following commands:

    ```sh
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py create_roles_permissions
    docker-compose exec web python manage.py create_default_data
    ```

### Running Tests

To run tests for the project, use the following command:

```sh
docker-compose exec web python manage.py test
```

This will execute all the tests in the Django project.

### Accessing the Application

- The application will be accessible at `http://localhost:8000`.
- The PostgreSQL database will be running on port `5432`.

### Stopping the Project

To stop the running containers, use:

```sh
docker-compose down
```

### Additional Commands

- **Create a superuser**:

    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```
