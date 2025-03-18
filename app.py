from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
import re

# Flask App Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ================== USER MODEL ==================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "admin" or "user"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================== ROUTES ==================

@app.route('/')
def index():
    return render_template('choose_role.html')

# ================== ADMIN REGISTRATION ==================
@app.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # ✅ Only allow fixed admin credentials
        if username != 'admin' or email != 'admin@qaoncloud.com' or password != 'admin@123':
            flash("❌ You are not an Admin!", "danger")
            return redirect(url_for('admin_register'))

        # ✅ Check if the admin already exists
        existing_admin = User.query.filter_by(email=email).first()
        if existing_admin:
            flash("⚠️ Admin already exists! Please log in.", "warning")
            return redirect(url_for('admin_register'))  # Redirect to login section

        # ✅ Hash password & create new admin
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = User(username=username, email=email, password=hashed_password, role='admin')
        db.session.add(new_admin)
        db.session.commit()

        flash("✅ Successfully registered as Admin! Please log in.", "success")
        return redirect(url_for('admin_register'))

    return render_template('adminRegister.html')


# ================== USER REGISTRATION ==================
@app.route('/user-register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate username (only letters)
        if not re.match("^[A-Za-z]+$", username):
            flash("❌ Username should contain only characters!", "danger")
            return redirect(url_for('user_register'))

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@(gmail\.com|qaoncloud\.com|desicrew\.com)$', email):
            flash("❌ Invalid email domain! Allowed: @gmail.com, @qaoncloud.com, @desicrew.com", "danger")
            return redirect(url_for('user_register'))

        # Check if passwords match
        if password != confirm_password:
            flash("❌ Passwords do not match!", "danger")
            return redirect(url_for('user_register'))

        # Hash the password & store
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, role="user")
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Successfully Registered! Redirecting...", "success")
        return redirect(url_for('login'))

    return render_template('userRegister.html')

# ================== LOGIN ==================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("✅ Login Successful!", "success")

            # ✅ Redirect to Update Profile if Admin Logs In
            if user.role == 'admin':
                return redirect(url_for('update_profile'))

            return redirect(url_for('update_profile'))  # Redirect users to profile update too

        flash("❌ Invalid Credentials!", "danger")
        return redirect(url_for('login'))

    return render_template('adminRegister.html')  # Ensure the login form is inside this page



# ================== UPDATE PROFILE ==================
@app.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        phone = request.form.get('phone', '').strip()

        # ✅ If any required field is empty, log out the user
        if not first_name or not last_name:
            flash("⚠️ Profile update failed! Logging out due to incomplete details.", "warning")
            return redirect(url_for('logout'))

        # ✅ Check if profile picture is uploaded
        if 'profile_pic' in request.files and request.files['profile_pic'].filename != '':
            profile_pic = request.files['profile_pic']
            filename = secure_filename(profile_pic.filename)
            profile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_pic.save(profile_path)
            current_user.profile_pic = filename  # Store file name in DB

        # ✅ Update user details
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.phone = phone

        db.session.commit()
        flash("✅ Profile Updated Successfully!", "success")
        
        return redirect(url_for('update_profile'))  # Refresh page

    return render_template('updateProfile.html', user=current_user)



# ================== LOGOUT ==================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("✅ Logged out successfully!", "success")
    return redirect(url_for('index'))  # Redirect to Choose Role page


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
