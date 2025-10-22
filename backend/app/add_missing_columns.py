from sqlalchemy import text
from database import SessionLocal

def add_missing_columns():
    db = SessionLocal()
    try:
        print("Adding missing columns to dealer_profiles...")
        
        # Add columns if they don't exist
        db.execute(text("""
            ALTER TABLE dealer_profiles 
            ADD COLUMN IF NOT EXISTS license_number VARCHAR(100),
            ADD COLUMN IF NOT EXISTS phone VARCHAR(50),
            ADD COLUMN IF NOT EXISTS address TEXT,
            ADD COLUMN IF NOT EXISTS city VARCHAR(100),
            ADD COLUMN IF NOT EXISTS state VARCHAR(50),
            ADD COLUMN IF NOT EXISTS zip_code VARCHAR(20),
            ADD COLUMN IF NOT EXISTS website VARCHAR(255),
            ADD COLUMN IF NOT EXISTS verification_status VARCHAR(50) DEFAULT 'pending',
            ADD COLUMN IF NOT EXISTS auto_followup_enabled BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS followup_day_1 BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS followup_day_3 BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS followup_day_7 BOOLEAN DEFAULT true
        """))
        
        db.commit()
        print("✅ All missing columns added successfully!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_missing_columns()