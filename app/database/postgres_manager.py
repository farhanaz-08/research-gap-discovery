from app.database.connection import SessionLocal

from sqlalchemy import or_

from app.database.models import (
    RetrievalSession,
    Paper,
    PaperChunk,
    Summary,
    Evidence,
    Methodology,
    Comparison,
    ResearchGap,
    Validation,
    ConfidenceScore
)


class PostgreSQLManager:

    def __init__(self):
        pass

    # ==================================================
    # Retrieval Session Methods
    # ==================================================

    def create_retrieval_session(
        self,
        query,
        expanded_query,
        status="pending"
    ):

        db = SessionLocal()

        try:

            session = RetrievalSession(
                query=query,
                expanded_query=expanded_query,
                status=status,
                total_papers=0
            )

            db.add(session)

            db.commit()

            db.refresh(session)

            return session

        finally:
            db.close()

    def get_retrieval_session(
        self,
        session_id
    ):

        db = SessionLocal()

        try:

            session = db.get(
                RetrievalSession,
                session_id
            )

            return session

        finally:
            db.close()

    def update_session_status(
        self,
        session_id,
        status
    ):

        db = SessionLocal()

        try:

            session = db.get(
                RetrievalSession,
                session_id
            )

            if session is None:
                return None

            session.status = status

            db.commit()

            db.refresh(session)

            return session

        finally:
            db.close()

    def increment_total_papers(
        self,
        session_id
    ):

        db = SessionLocal()

        try:

            session = db.get(
                RetrievalSession,
                session_id
            )

            if session is None:
                return None

            session.total_papers += 1

            db.commit()

            db.refresh(session)

            return session

        finally:
            db.close()

    # ==================================================
    # Paper Methods
    # ==================================================

    def create_paper(
        self,
        session_id,
        title,
        authors,
        abstract,
        doi,
        year,
        journal,
        pdf_path,
        source,
        download_status="pending"
    ):

        db = SessionLocal()

        try:

            paper = Paper(
                session_id=session_id,
                title=title,
                authors=authors,
                abstract=abstract,
                doi=doi,
                year=year,
                journal=journal,
                pdf_path=pdf_path,
                source=source,
                download_status=download_status
            )

            db.add(paper)

            db.commit()

            db.refresh(paper)

            return paper

        finally:
            db.close()

    def get_paper(
        self,
        paper_id
    ):

        db = SessionLocal()

        try:

            paper = db.get(
                Paper,
                paper_id
            )

            return paper

        finally:
            db.close()

    def get_papers_by_session(
        self,
        session_id
    ):

        db = SessionLocal()

        try:

            papers = (
                db.query(Paper)
                .filter(
                    Paper.session_id == session_id
                )
                .all()
            )

            return papers

        finally:
            db.close()

    def update_download_status(
        self,
        paper_id,
        status
    ):

        db = SessionLocal()

        try:

            paper = db.get(
                Paper,
                paper_id
            )

            if paper is None:
                return None

            paper.download_status = status

            db.commit()

            db.refresh(paper)

            return paper

        finally:
            db.close()
            
            
        # ==================================================
    # Paper Chunk Methods
    # ==================================================

    def paper_exists_by_doi(
        self,
        doi
    ):

        db = SessionLocal()

        try:

            if doi is None:
                return False

            paper = (
                db.query(Paper)
                .filter(Paper.doi == doi)
                .first()
            )

            return paper is not None

        finally:
            db.close()

    def paper_exists_by_title(
        self,
        title
    ):

        db = SessionLocal()

        try:

            paper = (
                db.query(Paper)
                .filter(Paper.title == title)
                .first()
            )

            return paper is not None

        finally:
            db.close()

    def create_paper_chunk(
        self,
        paper_id,
        chunk_number,
        section,
        chunk_text,
        embedding_id,
        page_start,
        page_end
    ):

        db = SessionLocal()

        try:

            chunk = PaperChunk(
                paper_id=paper_id,
                chunk_number=chunk_number,
                section=section,
                chunk_text=chunk_text,
                embedding_id=embedding_id,
                page_start=page_start,
                page_end=page_end
            )

            db.add(chunk)

            db.commit()

            db.refresh(chunk)

            return chunk

        finally:
            db.close()

    def get_chunks_by_paper(
        self,
        paper_id
    ):

        db = SessionLocal()

        try:

            chunks = (
                db.query(PaperChunk)
                .filter(
                    PaperChunk.paper_id == paper_id
                )
                .order_by(
                    PaperChunk.chunk_number
                )
                .all()
            )

            return chunks

        finally:
            db.close()

    def delete_chunks_by_paper(
        self,
        paper_id
    ):

        db = SessionLocal()

        try:

            (
                db.query(PaperChunk)
                .filter(
                    PaperChunk.paper_id == paper_id
                )
                .delete()
            )

            db.commit()

        finally:
            db.close()
    
    
def search_papers(
    self,
    keyword_list,
    limit=20
):

    db = SessionLocal()

    try:

        conditions = []

        for keyword in keyword_list:

            conditions.append(
                Paper.title.ilike(f"%{keyword}%")
            )

            conditions.append(
                Paper.abstract.ilike(f"%{keyword}%")
            )

        papers = (
            db.query(Paper)
            .filter(
                or_(*conditions)
            )
            .limit(limit)
            .all()
        )

        return papers

    finally:
        db.close()
        

def search_and_rank_papers(
    self,
    keyword_list,
    limit=20
):

    papers = self.search_papers(
        keyword_list,
        limit
    )

    ranked_papers = []

    for paper in papers:

        score = 0

        title = (paper.title or "").lower()
        abstract = (paper.abstract or "").lower()

        for keyword in keyword_list:

            keyword = keyword.lower()

            if keyword in title:
                score += 2

            if keyword in abstract:
                score += 1

        ranked_papers.append(
            {
                "paper": paper,
                "score": score
            }
        )

    ranked_papers.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked_papers