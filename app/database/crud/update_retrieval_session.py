from app.database.connection import SessionLocal
from app.database.models import RetrievalSession

db = SessionLocal()

session = (
    db.query(RetrievalSession)
    .filter(RetrievalSession.session_id == 1)
    .first()
)

if session:

    print("Before Update")
    print("----------------")
    print("Status:", session.status)
    print("Total Papers:", session.total_papers)

    session.status = "completed"
    session.total_papers = 25

    db.commit()

    db.refresh(session)

    print("\nAfter Update")
    print("----------------")
    print("Status:", session.status)
    print("Total Papers:", session.total_papers)

else:

    print("Session not found.")

db.close()