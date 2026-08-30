from app.database.connection import SessionLocal
from app.database.models import RetrievalSession

db = SessionLocal()

session = (
    db.query(RetrievalSession)
    .filter(RetrievalSession.session_id == 1)
    .first()
)

papers = relationship(
    "Paper",
    back_populates="session"
)

