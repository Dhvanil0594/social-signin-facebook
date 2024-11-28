
import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import httpx
from urllib.parse import urlencode

FACEBOOK_CLIENT_ID = "572141162350759"
FACEBOOK_CLIENT_SECRET = "0fc5767dd9e4cfca02401f780780450a"
FACEBOOK_REDIRECT_URI = "http://localhost:8001/login/facebook/callback"
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=("DELETE", "GET", "PATCH", "POST", "PUT"),
                   allow_headers=["*"])

# Step 1: Redirect the user to Facebook for login
@app.get("/login/facebook")
async def login_facebook():
    """
    Redirect the user to the Facebook login page.
    """
    # Construct the URL for Facebook's OAuth2 login page
    auth_url = "https://www.facebook.com/v10.0/dialog/oauth"
    params = {
        "client_id": FACEBOOK_CLIENT_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "scope": "email",  # Request access to the user's email
        "response_type": "code",  # We will get an authorization code
    }

    # Encode the parameters and redirect the user to Facebook
    facebook_login_url = f"{auth_url}?{urlencode(params)}"
    return RedirectResponse(url=facebook_login_url)


# Step 2: Handle the callback from Facebook after user login
@app.get("/login/facebook/callback")
async def facebook_callback(request: Request, code: str):
    """
    Handle the callback from Facebook after the user logs in.
    Exchange the authorization code for an access token.
    """
    # Define the URL to exchange the authorization code for an access token
    token_url = "https://graph.facebook.com/v10.0/oauth/access_token"
    token_data = {
        "client_id": FACEBOOK_CLIENT_ID,
        "client_secret": FACEBOOK_CLIENT_SECRET,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "code": code,
    }

    # Make a POST request to Facebook to exchange the code for an access token
    async with httpx.AsyncClient() as client:
        response = await client.get(token_url, params=token_data)
    
    # If successful, retrieve the access token from the response
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get("access_token")

        # Here you can use the access token to fetch the user's profile
        # We will now fetch the user's profile information
        user_profile_url = "https://graph.facebook.com/me"
        params = {"access_token": access_token, "fields": "id,name,email"}

        # ** Create a new client instance for the profile request **
        async with httpx.AsyncClient() as client:
            profile_response = await client.get(user_profile_url, params=params)
        
        if profile_response.status_code == 200:
            user_data = profile_response.json()
            # Handle user profile data (store in DB, create session, etc.)
            return {"user_data": user_data}
        else:
            raise HTTPException(status_code=profile_response.status_code, detail="Failed to fetch user profile.")
    
    # If the token exchange fails, raise an exception
    raise HTTPException(status_code=response.status_code, detail="Error obtaining Facebook tokens.")


    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("facebook_login_without_package:app", host="0.0.0.0", port=8001, reload=True)