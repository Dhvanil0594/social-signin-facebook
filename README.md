# Facebook Login with FastAPI
==========================

## Description

This is a FastAPI application that provides Facebook login functionality using two approaches:

1. Using the `fastapi-sso` package
2. Without using any package ( manual implementation )

## Usage

To use this application, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Create a Facebook Developer account and create a new Facebook App.
3. Obtain the Facebook App's Client ID, Client Secret, and Redirect URI, and add them to a `.env` file in the root of the project with the following format:

```
FACEBOOK_CLIENT_ID=your_client_id_here
FACEBOOK_CLIENT_SECRET=your_client_secret_here
FACEBOOK_REDIRECT_URI=your_redirect_uri_here
```
4. Run the application using `python facebook_login.py`.

## Endpoints

### Using Package

#### GET /auth/login

Initialize the Facebook login flow and redirect the user to the Facebook login page.

#### GET /auth/callback

Verify the user's login credentials and return the user's information.

### Without Using Package

#### GET /login/facebook

Redirect the user to the Facebook login page.

#### GET /login/facebook/callback

Handle the callback from Facebook after user login, exchange the authorization code for an access token, and fetch the user's profile information.

## Notes

* The `allow_insecure_http=True` parameter is used to allow insecure HTTP connections for development purposes only. In production, this parameter should be set to `False`.
* The `reload=True` parameter is used to enable automatic reloading of the application when changes are made to the code.
* The manual implementation without using any package uses the `httpx` library to make requests to Facebook's API.
* The user's profile information is fetched using the `https://graph.facebook.com/me` endpoint with the `access_token` obtained from the token exchange.
* You should handle the user's profile data (store in DB, create session, etc.) in the `/login/facebook/callback` endpoint.