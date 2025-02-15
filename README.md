# Simple Django user api

#### Django user api with email verification

This project creates simple a user django app which contains API's with email verification using [Postmark](https://postmarkapp.com/).<br>

Included Are the following API endpoints:
- [login](#log-in)
- [logout](#log-out)
- [soft delete](#delete-user)
- [get user info](#get-user)
- [sign up](#sign-up) (sends email)
- [activate account](#sign-up)
- [reset password request](#password-reset) (sends email)
- [confirm password reset](#password-reset)

## Build With

- [Django](https://www.djangoproject.com/)
- [Django rest framework](https://www.django-rest-framework.org/)
- [Postmarker](https://postmarker.readthedocs.io/en/latest/index.html)

## Getting started

### Prerequisites

A fresh Django project is required. Tested in django version 4.2.19

In order to use this app in a new project follow the following:
1. Create a virtual environment:
    ```bash
    python -m venv myenv
    ```

2. Activate virtual environment:
    - On windows:
    ```bash
    myenv/Scripts/activate
    ```
    - On macOS/Linux:
    ```
    source myenv/bin/activate
    ```

3. Install Django:
    ```bash
    pip install django==4.2.19
    ```

4. Create new project:
    ```bash
    django-admin startproject <project_name>
    cd <project_name>
    ```

5. Register Postmark:<br>
    Create a Postmark account and get your Postmark server token.
    Follow this [link](https://postmarkapp.com/) to get stared.

### Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/dylanvanl/user-api.git users
    ```
2. Install requirements:
    ```bash
    pip install -r users/requirements.txt
    ```

3. Register apps in your settings.py:
    ```python
    INSTALLED_APPS = [
    ...,    
    "rest_framework",
    "rest_framework.authtoken",
    "users",
    ]
    ```
4. Add extra settings to your settings.py:
    ```python
    # Use custom user model
    AUTH_USER_MODEL = "users.User"
    # Register front end url
    FRONT_END_URL = "http://localhost:3000"
    # Register Postmark settings
    POSTMARK_API_KEY = "your-postmark-server-token"
    POSTMARK_SENDER_EMAIL = "your-email@example.com"

    # In Debug mode you might not want to send any email
    # Set True if you DO want to send them
    # If False it will print the html template as it would be send.
    POSTMARK_DEBUG_SEND_EMAIL = False
    # In Debug mode all email will be send to this email address.
    # If you want to send them to correct email set as <None>
    # Only usefull if emails are send at all
    POSTMARK_DEBUG_RECEIVER_EMAIL = None
    # front end path for when email is first verified
    FRONT_END_CONFIRM_LINK = "/user/verified"
    # front end path for when password is reset
    FRONT_END_PASSWORD_RESET = "/user/reset-succes"
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
6. Migrate Models:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. Run server:
    ```bash
    python manage.py runserver
    ```

## Usage

Users can make requests as specified under [Details](#details). Please note that the html template is barebones and requires customization. You can find the templates in the users/templates folder.

You might need to enable CORS headers in order to make calls to back-end. View [django-cors-headers](https://pypi.org/project/django-cors-headers/) for instructions

For further details and use cases for authentication view [Django rest framework](https://www.django-rest-framework.org/) documentation.



### [Log in](#login-detail)

The login API returns an authentication token. If you want a view to be protected you can use the following format:
```python
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_endpoint(request):
    pass
```
Use
```
-H "Authorization: Token <authtoken>"
```
To authenticate your calls.

### [Log out](#logout-detail)

Deletes all auth and verification tokens associated with the authenticated user.

### [Sign up](#sign-up-detail)

Please note that the default email contains a link to a front-end url which 
must exist in you front-end project.

For the sign up verification the default is: 
```
FRONT_END_URL/user/verified?idvalue=4ff52547-225e-43f9-b56b-4c880dd8ab0d
```
which includes a query string. On your front-end, use this 'idvalue' to make a request as described in [activate](#activate-account-detail) to activate the account.

### [Password reset](#password-reset-detail)

In order for the user to make reset their password send a request as described in 'Reset password request' in the details below. This send an email which contains a link to 
```
FRONT_END_URL/user/reset-succes?idvalue=4ff52547-225e-43f9-b56b-4c880dd8ab0d
```
This is 'idvalue' is required to reset the password in the [confirm-password-reset](#confirm-password-reset-detail) call.

### [Delete user](#delete-user-detail)

Sets the user model as inactive and sets the date of 'deleted_at' in the user model.

### [Get user](#get-user-detail)

Returns username and email of the user.

## Details

This app allows the following API calls:
<ul>
    <li id="login-detail">
        Login:
        <pre><code>
curl -X POST "http://localhost:8000/api/login/" \
     -H "Content-Type: application/json" \
     -d '{  
         "username_or_email": "username",
         "password": "password"  
     }' | jq .
        </code></pre>
    <details>
    <summary>Responses</summary>
        <ul>
            <li><p style="color: #00FF00">200 OK</p>
                <pre><code>
{
    "token": "&ltauth-token&gt",
    "user": {
        "username": "&ltusername&gt",
        "email": "&ltexamplemail@example.com&gt"
    }
}
                </code></pre>
            </li>
            <li><p style="color:#ff0000">400 BAD REQUEST</p>
                <pre><code>
{
    "detail": "No User matches the given query."
}
                </code></pre>
            </li>
        </ul>
    </details>
    </li>
    <hr>
    <li id="logout-detail">
        Logout:
        <pre><code>
curl -X POST "http://localhost:8000/api/logout/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Token &lt;authtoken&gt;"
        </code></pre>
        <details>
        <summary>Responses</summary>
            <ul>
                <li><p style="color: #00FF00">200 OK</p>
                    <pre><code>
&ltempty&gt
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">403 FORBIDDEN</p>
                    <pre><code>
{
    "detail": "Invalid token."
}
                    </code></pre>
                </li>
            </ul>
        </details>
    </li>
    <hr>
    <li id="delete-user-detail">
        Soft delete:
        <pre><code>
curl -X DELETE "http://localhost:8000/api/delete/" \
     -H "Authorization: Token &lt;authtoken&gt;"
        </code></pre>
        <details>
    <summary>Responses</summary>
        <ul>
            <li><p style="color: #00FF00">200 OK</p>
                <pre><code>
&ltempty&gt
                </code></pre>
            </li>
            <li><p style="color:#ff0000">403 FORBIDDEN</p>
                <pre><code>
{
    "detail": "Invalid token."
}
                </code></pre>
            </li>
            <li><p style="color:#ff0000">400 BAD REQUEST</p>
                <pre><code>
&ltempty&gt
                </code></pre>            
            </li>
        </ul>
    </details>
    </li>
    <hr>
    <li id="get-user-detail">
        Get user info:
        <pre><code>
curl -X GET "http://localhost:8000/api/get-user/" \
     -H "Authorization: Token &lt;authtoken&gt;"
        </code></pre>
        <details>
        <summary>Responses</summary>
            <ul>
                <li><p style="color: #00FF00">200 OK</p>
                    <pre><code>
{
    "detail": {
        "username": "Dylan",
        "email": "dylan_van_lith@hotmail.com"
    }
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">403 FORBIDDEN</p>
                    <pre><code>
{
    "detail": "Invalid token."
}
                    </code></pre>
                </li>
            </ul>
        </details>
    </li>
    <hr>
    <li id="sign-up-detail">
        Sign up: (sends email)
        <pre><code>
curl -X POST "http://localhost:8000/api/signup/" \
     -H "Content-Type: application/json" \
     -d '{
            "username": "username",
            "password": "password",
            "password_confirmation": "password",
            "email":"email"
        }' | jq .
        </code></pre>
        <details>
        <summary>Responses</summary>
            <ul>
                <li><p style="color: #00FF00">201 CREATED</p>
                    <pre><code>
{
    "detail": "User created. Confirmation email sent."
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": "Password confirmation failed."
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": {
        "username": [
            "A user with that username already exists."
        ],
        "email": [
            "user with this email already exists."
        ]
    }
}
                    </code></pre>
                </li>
            </ul>
        </details>
    </li>
    <hr>
    <li id="activate-account-detail">
        Activate account:
        <pre><code>
curl -X GET "http://localhost:8000/api/activate/&lt;activation-token&gt;/"
        </code></pre>
        <details>
        <summary>Responses</summary>
            <ul>
                <li><p style="color: #00FF00">200 OK</p>
                    <pre><code>
{
    "detail": "Account activated succesfully."
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": "Invalid token: &lttoken&gt"
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": "Expired token: &lttoken&gt"
}
                    </code></pre>
                </li>
            </ul>
        </details>
    </li>
    <hr>
    <li id="password-reset-detail">
        Reset password request: (sends email)
        <pre><code>
curl -X POST "http://localhost:8000/api/reset-password/"
     -H "Content-Type: application/json"
     -d '{"email":"email"}'
        </code></pre>
        <details>
        <summary>Responses</summary>
            <ul>
                <li><p style="color: #00FF00">200 OK</p>
                    <pre><code>
{
    "detail": "Account activated succesfully."
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">404 NOT FOUND</p>
                    <pre><code>
{
    "detail": "User does not exist."
}
                    </code></pre>
                </li>
            </ul>
        </details>
    </li>
    <hr>
    <li id="confirm-password-reset-detail">
        Confirm password reset:
        <pre><code>
curl -X PATCH "http://localhost:8000/api/confirm-password-reset/"
     -H "Content-Type: application/json"
     -d '{
         "token": "{{activationToken}}",
         "password": "{{password}}",
         "password_confirmation": "{{password}}"
     }' | jq .
        </code></pre>
        <details>
        <summary>Responses</summary>
            <ul>
                <li><p style="color: #00FF00">200 OK</p>
                    <pre><code>
{
    "detail": "Password succesfully reset."
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": "Password confirmation failed."
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": "Invalid token: &lttoken&gt"
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": "Expired token: &lttoken&gt"
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">400 BAD REQUEST</p>
                    <pre><code>
{
    "detail": {
        "password": [
            "Password must be at least 8 characters long.",
            "Password must contain at least one uppercase letter.",
            "Password must contain at least one digit.",
            "Password must contain at least one special character."
        ]
    }
}
                    </code></pre>
                </li>
                <li><p style="color:#ff0000">404 NOT FOUND</p>
                    <pre><code>
{
    "detail": "No User matches the given query."
}
                    </code></pre>
                </li>
            </ul>
        </details>
    </li>
</ul>
