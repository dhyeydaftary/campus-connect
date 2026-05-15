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
        
        print(f"--- Resetting and creating verified test user ---")
        
        # Delete existing user if they exist to ensure clean state
        existing_user = User.query.filter((User.email == test_email) | (User.enrollment_no == test_enrollment)).first()
        if existing_user:
            print(f"Removing existing user: {existing_user.email}")
            db.session.delete(existing_user)
            db.session.commit()

        try:
            # Create the user object using manual assignment to avoid constructor issues
            user = User()
            user.first_name = "Test"
            user.last_name = "User"
            user.email = test_email
            user.enrollment_no = test_enrollment
            user.university = "Test University"
            user.major = "CSE"  # Valid branch from the login dropdown
            user.batch = "2025"
            user.account_type = "student"
            
            # Set flags manually to avoid constructor conflicts
            user.is_verified = True      # Bypasses OTP verification
            user.is_password_set = True  # Bypasses initial password setup
            user.status = "ACTIVE"       # Ensures account is not PENDING or BLOCKED
            
            # Set the password using the model's helper method (handles hashing)
            user.set_password(test_password)
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            print(f"Successfully created verified user!")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print(f"Enrollment No: {test_enrollment}")
            print(f"Branch (Major): {user.major}")
            print(f"Status: {user.status}")
            print(f"Verified: {user.is_verified}")
            
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while creating the user: {e}")

if __name__ == "__main__":
    create_verified_user()
