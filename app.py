from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from models import db, User
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Print database path for debugging
import os
print("Database Path:", os.path.abspath('db.sqlite'))

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        logger.info(f"Received registration data: {username}, {email}")

        # Ensure all fields are filled
        if not username or not email or not password or not confirm_password:
            flash("All fields are required!", "danger")
            return redirect(url_for('index'))

        # Ensure passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template('index.html')  # Stay on the registration page

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists!', 'danger')
            return redirect(url_for('index'))

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        logger.info("User registered successfully!")
        flash('Registration successful! Now you can log in.', 'success')
        return redirect(url_for('index'))  # Redirect to the login page after successful registration

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))




@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists in database
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('index'))  # Stay on login page

        # Check if password is correct
        if not bcrypt.check_password_hash(user.password, password):
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('index'))  # Stay on login page

        # If credentials are correct, log the user in
        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))  # Stay on login page


@app.route('/dashboard')
@login_required
def dashboard():
    logger.info(f"Redirecting to dashboard... Current user: {current_user.username}")
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures the database tables are created
    app.run(debug=True)

