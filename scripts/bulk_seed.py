import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from app.extensions import db
from app.models import User
from datetime import datetime

app = create_app()

CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "students.csv")

def bulk_seed():
    with app.app_context():
        print("Fetching existing enrollments...")
        existing = {u.enrollment_no for u in User.query.with_entities(User.enrollment_no).all()}
        
        users_to_add = []
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            next(reader)
            
            for i, row in enumerate(reader, start=3):
                if len(row) < 3: continue
                branch, enrollment_no, name = [field.strip() for field in row]
                if not all([branch, enrollment_no, name]): continue
                
                if enrollment_no in existing:
                    continue
                
                name_parts = name.strip().split()
                first_name = ""
                last_name = ""
                if len(name_parts) >= 2:
                    last_name = name_parts[0].title()
                    first_name = name_parts[1].title()
                elif len(name_parts) == 1:
                    first_name = name_parts[0].title()
                
                current_century = (datetime.now().year // 100) * 100
                year_prefix = enrollment_no[:2]
                admission_year = current_century + int(year_prefix)
                batch = str(admission_year + 4) if year_prefix.isdigit() else "N/A"
                
                user = User(
                    first_name=first_name, last_name=last_name,
                    email=f"{enrollment_no}@mail.ljku.edu.in",
                    university="L.J. University", major=branch, batch=batch,
                    account_type="student", is_verified=False,
                    enrollment_no=enrollment_no
                )
                users_to_add.append(user)
                existing.add(enrollment_no)
        
        if users_to_add:
            print(f"Bulk inserting {len(users_to_add)} users... This might take a few seconds.")
            db.session.add_all(users_to_add)
            db.session.commit()
            print("Successfully inserted all users!")
        else:
            print("No new users to insert.")

if __name__ == "__main__":
    bulk_seed()
