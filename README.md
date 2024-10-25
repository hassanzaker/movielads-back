
# MovieLads - Backend

This repository contains the backend code for the **MovieLads** application, which is built using **Django** and serves as the API and business logic layer of the platform. The backend manages user authentication, movie data handling, profile management, and provides APIs for the frontend to interact with.

## Features

- **User Authentication**: Sign-up, sign-in, logout, and profile management using JWT (JSON Web Token).
- **Movie Management**: Handles movie data for search, watchlist, and seen lists.
- **JWT Authentication**: Secure API authentication using SimpleJWT.
- **Profile Management**: Allows users to update profile data, including avatars.
- **Django REST Framework**: API endpoints for the frontend to interact with the backend.
- **Hosted on AWS EC2**: The backend is deployed on an EC2 instance for production.

## Tech Stack

- **Backend Framework**: [Django](https://www.djangoproject.com/) with [Django REST Framework](https://www.django-rest-framework.org/)
- **Authentication**: [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for secure token-based authentication
- **Database**: [PostgreSQL](https://www.postgresql.org/) or any other supported Django database
- **Storage**: AWS S3 for media file storage (avatars)

## Installation

### Prerequisites

- Python 3.x
- Django
- PostgreSQL or SQLite
- AWS Account (for EC2 and S3 configuration)

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/hassanzaker/movielads-back.git
   ```

2. Navigate to the project directory:

   ```bash
   cd movielads-back
   ```

3. Create a virtual environment and activate it:

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up the environment variables for Django, such as the database credentials and secret keys. Create a `.env` file in the project root and add the following:

   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://username:password@localhost:5432/dbname
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
   ```

6. Apply migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/`.

## EC2 Deployment

This backend is deployed on an **AWS EC2 instance**. To set up your Django project on EC2:

1. Launch an EC2 instance with Ubuntu or any preferred OS.
2. SSH into your EC2 instance.
3. Install necessary dependencies (Python, pip, PostgreSQL, Nginx, etc.).
4. Clone this repository to the EC2 instance.
5. Set up your virtual environment and install the dependencies.
6. Configure your Django settings for production, including setting `DEBUG=False`, configuring your PostgreSQL database, and setting up AWS S3 for static and media files.
7. Use **Gunicorn** and **Nginx** to serve the Django application.
8. Make sure your EC2 instance security groups allow HTTP/HTTPS traffic.

## API Endpoints

Here are some of the key API endpoints available:

- **Authentication**:
  - `/users/signin/`: Obtain JWT access and refresh tokens
  - `/users/signup/`: Create a new user account
  - `/users/refresh/`: Refresh the access token using the refresh token
  - `/users/logout/`: Logout the user

- **Profile Management**:
  - `/users/profile/`: Get the authenticated user's profile
  - `/users/profile/update/`: Update the user's profile (including avatar)

- **Movies**:
  - `/movies/`: List all movies
  - `/movies/:id/`: Get details of a specific movie

## Environment Variables

Here are the main environment variables you'll need to set for the project:

- `SECRET_KEY`: Your Django secret key
- `DEBUG`: Set to `False` in production
- `DATABASE_URL`: PostgreSQL database connection string
- `AWS_ACCESS_KEY_ID`: AWS access key for S3
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key for S3
- `AWS_STORAGE_BUCKET_NAME`: The name of your S3 bucket for static and media files

## Contribution

Feel free to fork this repository, make improvements, and open pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
