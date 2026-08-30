from app.database.connection import SessionLocal
from app.database.models import RetrievalSession


def test_database_write():
    db = SessionLocal()

    try:
        session = RetrievalSession(
            query="Test research query",
            expanded_query="Test expanded research query"
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        print("✅ Test record inserted!")
        print(f"Session ID: {session.session_id}")

    except Exception as e:
        db.rollback()
        print("❌ Database write failed!")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    test_database_write()