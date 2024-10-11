# MovieLads Backend

This is the backend for the MovieLads web application, built using Django and hosted on AWS. It handles user authentication, movie data management, and integrates with various AWS services for storage and database management.

## Features

- User authentication using JWT
- Movie search, reviews, and watchlist management
- RESTful API with Django REST Framework
- AWS RDS for MySQL database
- Media file storage using AWS S3
- Hosted on AWS EC2 with Nginx and Gunicorn for serving the application

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: MySQL (AWS RDS)
- **Hosting**: AWS EC2, Nginx, Gunicorn
- **Storage**: AWS S3 for media files

## Prerequisites

- Python 3.x
- AWS account with RDS, S3, and EC2 configured
- MySQL database instance running on AWS RDS

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/hassanzaker/movielads-back.git
    cd movielads-back
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configuration**:
   Create a `.env` file in the root directory and add your configuration:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_host
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
