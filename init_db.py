from app.infrastructure.database.session import engine
from sqlmodel import SQLModel

# Import all entities to register them with SQLModel
from app.domain.entities.student import Student
from app.domain.entities.parent import Parent
from app.domain.entities.admin import Admin
from app.domain.entities.wallet import Wallet
from app.domain.entities.fee import Fee
from app.domain.entities.fee_category import FeeCategory
from app.domain.entities.student_fee import StudentFee
from app.domain.entities.transaction import Transaction

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully!")
    print("\nTables created:")
    print("  - student")
    print("  - parent")
    print("  - admin")
    print("  - wallet")
    print("  - fee")
    print("  - fee_category")
    print("  - student_fee")
    print("  - transaction")

if __name__ == "__main__":
    init_database()
