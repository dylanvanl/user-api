# Simple Django user api

#### Django user api with email verification

This project creates simple a user django app which contains API's with email verification using [Postmark](https://postmarkapp.com/).<br>

Included Are the following API endpoints:
- login
- logout
- soft delete
- get user info
- signup (sends email)
- activate account
- reset password request (sends email)
- confirm password reset

## Build With

- [Django](https://www.djangoproject.com/)
- [Django rest framework](https://www.django-rest-framework.org/)
- [Postmarker](https://postmarker.readthedocs.io/en/latest/index.html)

## Getting started

### Prerequisites

A fresh Django project is required.<br>
In order to use this app in a new project follow the following:
1. Create a virtual environment:
    ```sh
    python -m venv myenv
    ```

2. Activate virtual environment:
    - On windows:
    ```sh
    myenv/Scripts/activate
    ```
    - On macOS/Linux:
    ```
    source myenv/bin/activate
    ```

3. Install Django:
    ```sh
    pip install django==4.2.19
    ```

4. Create new project:
    ```sh
    django-admin startproject <project_name>
    cd <project_name>
    ```

### Installation

1. Clone the repo:
    ```sh
    git clone https://github.com/dylanvanl/user-api.git
    ```
2. Install requirements:
    ```sh
    pip install -r user-api/requirements.txt
    ```

3. Register apps in your settings.py:
    ```Python
    INSTALLED_APPS = [
    ...,    
    "rest_framework",
    "rest_framework.authtoken",
    "users",
    ]
    ```
4. Add extra settings to settings.py:
    ```Python
    # Use custom user model
    AUTH_USER_MODEL = "users.User"
    # Register front end url
    FRONT_END_URL = "http://localhost:3000"
    # Register Postmark settings
    POSTMARK_API_KEY = "your-postmark-server-token"
    POSTMARK_SENDER_EMAIL = "your-email@example.com"

    # In Debug mode you might not want to send any email
    # Set True if you DO want to send them
    # If False it will print the html template as would be send.
    POSTMARK_DEBUG_SEND_EMAIL = False
    # In Debug mode all email will be send to this email address.
    # If you want to send them to correct email set as <None>
    # Only usefull if emails are send at all
    POSTMARK_DEBUG_RECEIVER_EMAIL = None
    ```

5. Register API url's in your urls.py:
    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include("users.urls"))
    ]

    ```

### Usage