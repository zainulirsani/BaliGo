import random
import string
import base64
import hashlib
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import JsonResponse


# Helper function to generate the code verifier
def generate_code_verifier(length=64):
    chars = string.ascii_letters + string.digits + "-._~"
    return ''.join(random.choice(chars) for _ in range(length))


# Helper function to generate code challenge from the code verifier
def generate_code_challenge(code_verifier):
    code_verifier_bytes = code_verifier.encode('utf-8')
    sha256 = hashlib.sha256(code_verifier_bytes).digest()
    return base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip("=")


# Redirect to the OAuth provider to authorize the application
def oauth_redirect(request):
    code_verifier = generate_code_verifier()  # Generate code verifier
    request.session['code_verifier'] = code_verifier  # Store in session

    code_challenge = generate_code_challenge(code_verifier)  # Generate code challenge
    client_id = settings.OAUTH_CLIENT_ID
    redirect_uri = settings.OAUTH_REDIRECT_URI
    authorization_url = f"{settings.OAUTH_PROVIDER_URL}/o/authorize?"

    auth_url = f"{authorization_url}response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&code_challenge={code_challenge}&code_challenge_method=S256"
    return redirect(auth_url)


# Callback from the OAuth provider
def oauth_callback(request):
    # Get the authorization code from the query parameters
    authorization_code = request.GET.get('code')

    if not authorization_code:
        return JsonResponse({'error': 'Missing authorization code'}, status=400)

    # Get the code verifier from the session
    code_verifier = request.session.get('code_verifier')

    if not code_verifier:
        return JsonResponse({'error': 'Missing code verifier'}, status=400)

    # Exchange the authorization code for an access token
    token_url = f"{settings.OAUTH_PROVIDER_URL}/o/token/"
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': settings.OAUTH_REDIRECT_URI,
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        'code_verifier': code_verifier,
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to obtain access token', 'details': response.json()}, status=500)

    token_data = response.json()
    access_token = token_data.get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Access token not found'}, status=500)

    # Fetch user data using the access token
    user_info_url = f"{settings.OAUTH_PROVIDER_URL}/api/userinfo/"
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)

    if user_info_response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch user info', 'details': user_info_response.json()}, status=500)

    user_data = user_info_response.json()

    # Store the user data in session or database
    request.session['user_data'] = user_data
    request.session['access_token'] = access_token

    # Optionally, redirect to the dashboard or another page after successful login
    return redirect('/admin/dashboard_SSO')  # Adjust the redirect as per your needs


# Dashboard view
def dashboard_SSO(request):
    user_data = request.session.get('user_data', {})
    access_token = request.session.get('access_token')

    if not user_data:
        return redirect('oauth_redirect')  # Jika belum login, kembalikan ke redirect

    return render(request, 'dashboard.html', {
        'user_data': user_data,
        'access_token': access_token,
    })
