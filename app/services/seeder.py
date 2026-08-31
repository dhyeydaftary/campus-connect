"""
Admin user seeder for Campus Connect.
Creates or updates the primary admin account from environment variables.
"""

import os
from flask import current_app
from app.extensions import db
from app.models import User


def seed_admin():
    """
    Seeds or updates the primary admin user from .env variables.
    This ensures the admin account is always available and credentials are
    synchronized with the environment configuration on startup.
    """
    email = os.environ.get("ADMIN_EMAIL", "").strip()
    password = os.environ.get("ADMIN_PASSWORD")

    if not email or not password:
        return
    current_app.logger.info(f"[SEED] Seeding admin with email: {email}")

    # Find the specific admin by email to ensure we update the correct one.
    admin = User.query.filter_by(email=email.lower()).first()

    if admin:
        # Update existing admin to ensure credentials match .env and hash is correct
        admin.email = email.lower()
        admin.set_password(password)  # Use the model's method
        db.session.commit()
        current_app.logger.info("[OK] Admin account updated")
        return

    admin = User(
        first_name="Admin",
        last_name="User",
        email=email.lower(),
        university="Campus Connect University",
        major="Administration",
        batch="N/A",
        account_type="admin",
        is_verified=True,  # Admin is trusted by default
        enrollment_no="ADMIN001"
    )
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()
    current_app.logger.info("[OK] Default admin created")


def seed_demo_account():
    """
    Seeds or updates the public demo student account from .env variables.
    Powers the "Try Demo Account" quick-login button on the login page.
    No-ops silently if DEMO_ACCOUNT_EMAIL / DEMO_ACCOUNT_PASSWORD are unset.
    """
    email = os.environ.get("DEMO_ACCOUNT_EMAIL", "").strip()
    password = os.environ.get("DEMO_ACCOUNT_PASSWORD")

    if not email or not password:
        return
    current_app.logger.info(f"[SEED] Seeding demo account with email: {email}")

    enrollment_no = os.environ.get("DEMO_ACCOUNT_ENROLLMENT", "").strip() or "DEMO001"

    # Find the specific demo user by email to ensure we update the correct one.
    demo = User.query.filter_by(email=email.lower()).first()

    if demo:
        # Keep credentials and student flags synced with .env on startup.
        demo.email = email.lower()
        demo.enrollment_no = enrollment_no
        demo.account_type = "student"
        demo.is_verified = True
        demo.is_password_set = True
        demo.status = "ACTIVE"
        demo.set_password(password)
        db.session.commit()
        current_app.logger.info("[OK] Demo account updated")
        return

    demo = User(
        first_name="Demo",
        last_name="Student",
        email=email.lower(),
        university="Campus Connect University",
        major="CSE",
        batch="2025",
        account_type="student",
        enrollment_no=enrollment_no
    )
    demo.is_verified = True
    demo.is_password_set = True
    demo.status = "ACTIVE"
    demo.set_password(password)

    db.session.add(demo)
    db.session.commit()
    current_app.logger.info("[OK] Demo account created")


def seed_test_user():
    """
    Seeds a test student user for development purposes.
    """
    if current_app.config.get("IS_PRODUCTION", False):
        return  # Do not seed test user in production

    test_email = "test@example.com"
    test_enrollment = "TEST001"
    test_password = "password123"

    current_app.logger.info(f"[SEED] Seeding test user with email: {test_email}")

    user = User.query.filter((User.email == test_email) | (User.enrollment_no == test_enrollment)).first()

    if user:
        # Update existing test user to ensure it works
        user.set_password(test_password)
        user.status = "ACTIVE"
        user.is_verified = True
        user.is_password_set = True
        db.session.commit()
        current_app.logger.info("[OK] Test user account updated")
        return

    user = User(
        first_name="Test",
        last_name="User",
        email=test_email,
        enrollment_no=test_enrollment,
        university="Test University",
        major="CSE",
        batch="2025",
        account_type="student"
    )
    user.is_verified = True
    user.is_password_set = True
    user.status = "ACTIVE"
    user.set_password(test_password)

    db.session.add(user)
    db.session.commit()
    current_app.logger.info("[OK] Default test student created")
