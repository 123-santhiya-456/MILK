from app.db.database import engine, Base, SessionLocal
from app.models.milk_model import MilkRecord
from app.models.vendor_model import Vendor
from app.models.admin_model import Admin
from app.auth.auth_utils import hash_password


def init_db():
    # 1️⃣ Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # ==============================
        # 2️⃣ Insert Sample Vendors
        # ==============================
        if db.query(Vendor).count() == 0:
            vendor1 = Vendor(
                name="Vendor A",
                location="Chennai",
                phone="9876543210"
            )

            vendor2 = Vendor(
                name="Vendor B",
                location="Madurai",
                phone="9123456780"
            )

            vendor3 = Vendor(
                name="Vendor C",
                location="Coimbatore",
                phone="9988776655"
            )

            db.add_all([vendor1, vendor2, vendor3])
            db.commit()
            print("✅ Sample vendors inserted successfully")
        else:
            print("ℹ️ Vendors already exist")

        # ==============================
        # 3️⃣ Create Default Admin
        # ==============================
        if db.query(Admin).count() == 0:
            default_admin = Admin(
                username="admin",
                password=hash_password("admin123")
            )

            db.add(default_admin)
            db.commit()
            print("✅ Default admin created")
            print("   ➜ Username: admin")
            print("   ➜ Password: admin123")
        else:
            print("ℹ️ Admin already exists")

    except Exception as e:
        db.rollback()
        print("❌ Error during database initialization:", e)

    finally:
        db.close()

    print("✅ Database initialized successfully")


if __name__ == "__main__":
    init_db()
