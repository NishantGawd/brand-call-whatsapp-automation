from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import get_password_hash

# Updated to use a valid email
TEST_EMAIL = "owner@gmail.com"
TEST_PASSWORD = "demo-password"
TEST_TENANT_SLUG = "demo-brand"
TEST_TENANT_NAME = "Demo Brand"


def init_test_data() -> None:
    db = SessionLocal()
    try:
        # 1️⃣ Create or retrieve tenant
        tenant = db.query(Tenant).filter(Tenant.slug == TEST_TENANT_SLUG).first()
        if not tenant:
            tenant = Tenant(name=TEST_TENANT_NAME, slug=TEST_TENANT_SLUG)
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            print(f"✔ Created tenant: {tenant.slug}")
        else:
            print(f"ℹ Tenant '{TEST_TENANT_SLUG}' already exists.")

        # 2️⃣ Check if user with new email already exists
        existing_user = db.query(User).filter(User.email == TEST_EMAIL).first()

        if not existing_user:
            # ❗ Delete any test users from previous runs to avoid conflicts
            db.query(User).filter(User.email.like("%demo-brand%")).delete()
            db.commit()

            user = User(
                email=TEST_EMAIL,
                hashed_password=get_password_hash(TEST_PASSWORD),
                full_name="Demo Owner",
                tenant_id=tenant.id,
                is_superuser=True,
                role="owner",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✔ Created user: {TEST_EMAIL} with password '{TEST_PASSWORD}'")
        else:
            print(f"ℹ User '{TEST_EMAIL}' already exists, skipping creation.")

    except Exception as e:
        print(f"⛔ Error while initializing test data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_test_data()
