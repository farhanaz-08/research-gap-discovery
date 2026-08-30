from app.database.connection import SessionLocal
from app.database.models import RetrievalSession

db = SessionLocal()

sessions = db.query(
    RetrievalSession
).all()

for session in sessions:

    print("---------------------")

    print("Session ID:", session.session_id)

    print("Query:", session.query)

    print("Status:", session.status)

    print("Total Papers:", session.total_papers)
    
    
db.close()