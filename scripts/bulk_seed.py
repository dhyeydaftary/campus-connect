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
        skipped_count = 0
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            next(reader)

            for i, row in enumerate(reader, start=3):
                try:
                    if len(row) < 3:
                        skipped_count += 1
                        continue
                    branch, enrollment_no, name = [field.strip() for field in row]
                    if not all([branch, enrollment_no, name]):
                        skipped_count += 1
                        continue

                    if enrollment_no in existing:
                        skipped_count += 1
                        continue

                    name_parts = name.strip().split()
                    first_name = ""
                    last_name = ""
                    if len(name_parts) >= 2:
                        last_name = name_parts[0].title()
                        first_name = name_parts[1].title()
                    elif len(name_parts) == 1:
                        first_name = name_parts[0].title()

                    year_prefix = enrollment_no[:2]
                    if year_prefix.isdigit():
                        current_century = (datetime.now().year // 100) * 100
                        admission_year = current_century + int(year_prefix)
                        batch = str(admission_year + 4)
                    else:
                        batch = "N/A"

                    user = User(
                        first_name=first_name, last_name=last_name,
                        email=f"{enrollment_no}@mail.ljku.edu.in",
                        university="L.J. University", major=branch, batch=batch,
                        account_type="student", is_verified=False,
                        enrollment_no=enrollment_no
                    )
                    users_to_add.append(user)
                    existing.add(enrollment_no)

                except Exception as e:
                    skipped_count += 1
                    print(f"Skipping row #{i} due to error: {e}")
                    continue

        if users_to_add:
            print(f"Bulk inserting {len(users_to_add)} users... This might take a few seconds.")
            try:
                db.session.add_all(users_to_add)
                db.session.commit()
                print(f"Successfully inserted {len(users_to_add)} users! Skipped {skipped_count} rows.")
            except Exception as e:
                db.session.rollback()
                print(f"Bulk insert failed, nothing was committed: {e}")
        else:
            print(f"No new users to insert. Skipped {skipped_count} rows.")

if __name__ == "__main__":
    bulk_seed()