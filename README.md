# Movie Management System

A comprehensive Django-based web application for managing movies, showtimes, bookings, and user reviews. This system provides a complete solution for movie theaters or cinemas to manage their operations online.

## Features

- **Movie Management**
  - Add, edit, and manage movie details
  - Categorize movies by genres
  - Track movie status (Now Showing, Coming Soon, Archived)
  - Upload movie posters and trailer URLs
  - Manage showtimes and ticket prices

- **User Authentication**
  - User registration and login
  - User profile management
  - Role-based access control

- **Booking System**
  - Seat selection and booking
  - Multiple showtimes management
  - Booking confirmation and history
  - Payment integration

- **Review System**
  - User reviews and ratings
  - Admin approval system for reviews
  - Movie rating calculation

- **Admin Panel**
  - Comprehensive dashboard
  - Manage movies, showtimes, and bookings
  - User and review management
  - Site settings configuration

## Technology Stack

- **Backend**: Django 4.2 (Python)
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local file system (configurable for AWS S3)

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Movie_management_System_3
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
Movie_management_System_3/
├── accounts/               # User authentication and profile management
├── movies/                 # Core movie and booking functionality
│   ├── management/         # Custom management commands
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── __init__.py
│   ├── admin.py           # Admin site configuration
│   ├── apps.py            # App configuration
│   ├── models.py          # Database models
│   ├── urls.py            # URL routing
│   └── views.py           # View functions
├── media/                  # User-uploaded files
├── Movie_management_system_3/  # Project settings
├── static/                 # Static files
└── manage.py              # Django management script
```

## Configuration

1. **Environment Variables**
   Create a `.env` file in the project root with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   ```

2. **Database**
   The default configuration uses SQLite. To use PostgreSQL or MySQL, update the `DATABASES` setting in `settings.py`.

## Usage

1. **Admin Panel**
   - Access the admin panel at `/admin`
   - Log in with your superuser credentials
   - Manage movies, showtimes, bookings, and user accounts

2. **User Registration**
   - Users can register at `/accounts/register/`
   - After registration, users can log in and start booking movies

3. **Booking Process**
   - Browse available movies
   - Select showtime and number of seats
   - Complete the booking process
   - Receive booking confirmation

## Custom Management Commands

- `python manage.py update_movie_ratings` - Update movie ratings based on reviews
- `python manage.py create_default_admin` - Create a default admin user

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Bootstrap 5
- Font Awesome for icons
- All contributors who helped in development
