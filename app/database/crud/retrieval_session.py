from app.database.connection import SessionLocal
from app.database.models import RetrievalSession

db = SessionLocal()

new_session = RetrievalSession(
    query="Multi-Agent Research Gap Discovery",
    expanded_query="Multi-Agent Research Gap Discovery using RAG and LLMs",
    status="pending",
    total_papers=0
)

db.add(new_session)

db.commit()

db.refresh(new_session)

print("Session ID:", new_session.session_id)

db.close()

