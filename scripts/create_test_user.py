import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db
from app.models import User

def create_verified_user():
    app = create_app()
    
    with app.app_context():
        # Configuration for the test user
        test_email = "test@example.com"
        test_enrollment = "TEST001"
        test_password = "password123"
        
        print(f"--- Attempting to create verified test user ---")
        
        # Check if user already exists
        existing_user = User.query.filter((User.email == test_email) | (User.enrollment_no == test_enrollment)).first()
        
        if existing_user:
            print(f"Error: A user with email '{test_email}' or enrollment '{test_enrollment}' already exists.")
            return

        try:
            # Create the user object
            user = User(
                first_name="Test",
                last_name="User",
                email=test_email,
                enrollment_no=test_enrollment,
                university="Test University",
                major="Computer Science",
                batch="2025",
                is_verified=True,      # Bypasses OTP verification
                is_password_set=True,  # Bypasses initial password setup
                status="ACTIVE",        # Ensures account is not PENDING or BLOCKED
                account_type="student"
            )
            
            # Set the password using the model's helper method (handles hashing)
            user.set_password(test_password)
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            print(f"Successfully created verified user!")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print(f"Enrollment No: {test_enrollment}")
            print(f"Status: {user.status}")
            print(f"Verified: {user.is_verified}")
            
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while creating the user: {e}")

if __name__ == "__main__":
    create_verified_user()
