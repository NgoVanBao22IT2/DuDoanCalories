from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timezone, timedelta

import pickle
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'calories_prediction_app_secret_key'

# Enable CSRF protection
csrf = CSRFProtect(app)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/calories_prediction_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    body_temp = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    user_name = session.get('user_name')
    return render_template('home.html', user_name=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        flash('Please log in to access the prediction page.', 'danger')
        return redirect(url_for('login'))

    result = None
    if request.method == 'POST':
        try:
            # Get form data
            gender = request.form.get('gender')
            age = int(request.form.get('age'))
            height = float(request.form.get('height'))
            weight = float(request.form.get('weight'))
            duration = int(request.form.get('duration'))
            heart_rate = int(request.form.get('heart_rate'))
            body_temp = float(request.form.get('body_temp'))

            # Call the prediction function
            calories = predict_calories(gender, age, height, weight, duration, heart_rate, body_temp)

            # Save the prediction to the database
            new_prediction = Prediction(
                user_id=session['user_id'],  # Get the logged-in user's ID from the session
                gender=gender,
                age=age,
                height=height,
                weight=weight,
                duration=duration,
                heart_rate=heart_rate,
                body_temp=body_temp,
                calories=calories
            )
            db.session.add(new_prediction)
            db.session.commit()

            # Set the result to display in the template
            result = calories
            flash('Prediction successful! The result has been saved to your history.', 'success')
        except Exception as e:
            flash(f'Error during prediction: {e}', 'danger')

    return render_template('predict.html', result=result)

@app.route('/history')
def history():
    if 'user_id' not in session:
        flash('Please log in to view your prediction history.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    predictions = Prediction.query.filter_by(user_id=user_id).all()
    return render_template('history.html', predictions=predictions)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Prediction function
def predict_calories(gender, age, height, weight, duration, heart_rate, body_temp):
    try:
        # Load model chỉ 1 lần (tối ưu hơn nếu bạn load ngoài hàm và truyền vào)
        with open('pipeline.pkl', 'rb') as file:
            model = pickle.load(file)

        # Chuyển đổi giới tính về dạng số như lúc train (male: 0, female: 1)
        gender_numeric = 0 if gender.lower() == 'male' else 1

        # Tạo DataFrame đầu vào
        input_data = pd.DataFrame({
            'Gender': [gender_numeric],
            'Age': [age],
            'Height': [height],
            'Weight': [weight],
            'Duration': [duration],
            'Heart_Rate': [heart_rate],
            'Body_Temp': [body_temp]
        })

        # Dự đoán
        prediction = model.predict(input_data)
        return float(prediction[0])
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)