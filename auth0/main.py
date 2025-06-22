import os
from flask import render_template
from flask import Flask, redirect, request, jsonify, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # Make sure to set a secure secret key in production

# URL fallback
url = os.environ.get("URL", "http://ccie.pl")

# Auth0 configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "dev-vad8cgihf1nept5s.us.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "aaz3BknF8sQ4TXihAXfSe80yI2Es3SJ1")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "zwYCwmtONO0RuJEstXsqSWtu9RylQsZ6ty8-IB6hWcv1UdD3-UaT5VqoXydqVV9I")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://centos.kuligowski.co.uk:5155/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/userinfo")

# Auth0 OAuth setup
oauth = OAuth(app)
auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=f"https://{AUTH0_DOMAIN}",
    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",
    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",
    client_kwargs={"scope": "openid profile email"},
    jwks_uri=f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
)

# Authentication helper
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route("/")
def main():
    return "Usage: Paths '/headers', '/redirect', '/status', '/login', '/logout', '/dashboard'"

@app.route("/headers")
@requires_auth
def headers():
    return dict(request.headers)

@app.route("/redirect")
@requires_auth
def redirect_request():
    return redirect(url, code=302)

@app.route("/status")
@requires_auth
def random_status_code():
    if "code" in request.headers:
        try:
            codes = int(request.headers["code"])  # Ensure the code is an integer
            data = {"F5 response code": codes}
            return jsonify(data), codes
        except ValueError:
            error_msg = {"error": "Invalid status code"}
            return jsonify(error_msg), 400
    else:
        error_msg = {"error": "Bad request, 'code' header is missing"}
        return jsonify(error_msg), 400

@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

@app.route("/callback")
def callback():
    try:
        auth0.authorize_access_token()  # Retrieve and validate access token
        user_info = auth0.get("userinfo").json()  # Get user info
        session["user"] = user_info  # Store user info in session
        return redirect("/dashboard")
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors and provide feedback

@app.route("/dashboard")
@requires_auth
def dashboard():
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        f"client_id={AUTH0_CLIENT_ID}&returnTo={url_for('main', _external=True)}"
    )

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5155
    port = int(os.environ.get("PORT", 5155))
    app.run(host="0.0.0.0", port=port)

