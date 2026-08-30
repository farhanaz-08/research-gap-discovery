from app.database.connection import SessionLocal
from app.database.models import RetrievalSession

db = SessionLocal()

session = (
    db.query(RetrievalSession)
    .filter(RetrievalSession.session_id == 1)
    .first()
)

pending_sessions = (
    db.query(RetrievalSession)
    .filter(RetrievalSession.status == "pending")
    .all()
)



if session:

    print("Session Found!")
    print("ID:", session.session_id)
    print("Query:", session.query)
    print("Status:", session.status)

else:

    print("Session not found.")


print("\nPending Sessions")

for session in pending_sessions:

    print("---------------------")

    print("Session ID:", session.session_id)
    print("Query:", session.query)

db.close()