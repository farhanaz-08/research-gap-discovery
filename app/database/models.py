from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    String,
    Text,
    DateTime,
    ForeignKey,
    func
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)


Base = declarative_base()

# 1 ***********************************
class RetrievalSession(Base):

    __tablename__ = "retrieval_sessions"

    session_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    query = Column(
    Text,
    nullable=False
)
    expanded_query = Column(
    Text,
    nullable=True
)
    status = Column(
    String(30),
    nullable=False,
    server_default="pending"
)

    total_papers = Column(
    Integer,
    nullable=False,
    server_default="0"
)
    created_at = Column(
    DateTime,
    server_default=func.now(),
    nullable=False
)
    papers = relationship(
    "Paper",
    back_populates="session"
)
    comparisons = relationship(
    "Comparison",
    back_populates="retrieval_session"
)
    agent_logs = relationship(
    "AgentLog",
    back_populates="session"
)
    session_processing_status = relationship(
    "SessionProcessingStatus",
    back_populates="session",
    uselist=False
)
  
    

# 2 *****************************************

    
class Paper(Base):

    __tablename__ = "papers"

    paper_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    session_id = Column(
    Integer,
    ForeignKey("retrieval_sessions.session_id"),
    nullable=False
)
    title = Column(
    Text,
    nullable=False
)
    authors = Column(
    Text,
    nullable=False
)
    abstract = Column(
    Text,
    nullable=True
)
    doi = Column(
    String(255),
    nullable=True,
    unique=True
)
    year = Column(
    Integer,
    nullable=True
)
    journal = Column(
    String(255),
    nullable=True
)
    pdf_path = Column(
    Text,
    nullable=True
)
    source = Column(
    String(50),
    nullable=False
)
    download_status = Column(
    String(30),
    nullable=False,
    server_default="pending"
)
    created_at = Column(
    DateTime,
    nullable=False,
    server_default=func.now()
)
    session = relationship(
    "RetrievalSession",
    back_populates="papers"
)
    chunks = relationship(
    "PaperChunk",
    back_populates="paper"
)
    summary = relationship(
    "Summary",
    back_populates="paper",
    uselist=False
)
    evidence = relationship(
    "Evidence",
    back_populates="paper"
)
    methodology = relationship(
    "Methodology",
    back_populates="paper",
    uselist=False
)
    comparison_members = relationship(
    "ComparisonMember",
    back_populates="paper"
)
    gap_papers = relationship(
    "GapPaper",
    back_populates="paper"
)
    processing_status = relationship(
    "ProcessingStatus",
    back_populates="paper",
    uselist=False
)
    agent_logs = relationship(
    "AgentLog",
    back_populates="paper"
)



# 3 *********************************************
class PaperChunk(Base):

    __tablename__ = "paper_chunks"

    chunk_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False
)
    chunk_number = Column(
    Integer,
    nullable=False
)
    section = Column(
    String(100),
    nullable=True
)
    chunk_text = Column(
    Text,
    nullable=False
)
    embedding_id = Column(
    String(100),
    nullable=False,
    unique=True
)
    page_start = Column(
    Integer,
    nullable=True
)
    page_end = Column(
    Integer,
    nullable=True
)
    paper = relationship(
    "Paper",
    back_populates="chunks"
)
    evidence = relationship(
    "Evidence",
    back_populates="chunk"
)


# 4 ********************************************

class Summary(Base):

    __tablename__ = "summaries"

    summary_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False,
    unique=True
)
    executive_summary = Column(
    Text,
    nullable=False
)
    research_problem = Column(
    Text,
    nullable=True
)
    key_contributions = Column(
    Text,
    nullable=True
)
    methodology_summary = Column(
    Text,
    nullable=True
)
    main_findings = Column(
    Text,
    nullable=True
)
    limitations = Column(
    Text,
    nullable=True
)
    future_work = Column(
    Text,
    nullable=True
)
    model = Column(
    String(100),
    nullable=False
)
    processing_time = Column(
    Float,
    nullable=True
)
    paper = relationship(
    "Paper",
    back_populates="summary"
)


# 5 ************************************************8

class Evidence(Base):

    __tablename__ = "evidence"

    evidence_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False
)
    chunk_id = Column(
    Integer,
    ForeignKey("paper_chunks.chunk_id"),
    nullable=False
)
    claim = Column(
    Text,
    nullable=False
)
    supporting_text = Column(
    Text,
    nullable=False
)
    confidence = Column(
    Integer,
    nullable=False
)
    page_number = Column(
    Integer,
    nullable=True
)
    paper = relationship(
    "Paper",
    back_populates="evidence"
)

    chunk = relationship(
    "PaperChunk",
    back_populates="evidence"
)


# 6 ***********************************************

class Methodology(Base):

    __tablename__ = "methodologies"

    methodology_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False,
    unique=True
)
    dataset = Column(
    String(255),
    nullable=False
)
    model = Column(
    String(255),
    nullable=False
)
    preprocessing = Column(
    Text,
    nullable=False
)
    evaluation_metrics = Column(
    Text,
    nullable=False
)
    limitations = Column(
    Text,
    nullable=False
)
    paper = relationship(
    "Paper",
    back_populates="methodology"
)
    

# 7 *********************************************

class Comparison(Base):

    __tablename__ = "comparisons"

    comparison_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    session_id = Column(
    Integer,
    ForeignKey("retrieval_sessions.session_id"),
    nullable=False
)
    similarities = Column(
    Text,
    nullable=False
)
    differences = Column(
    Text,
    nullable=False
)
    contradictions = Column(
    Text,
    nullable=False
)
    research_trends = Column(
    Text,
    nullable=False
)
    research_clusters = Column(
    Text,
    nullable=False
)
    comparison_summary = Column(
    Text,
    nullable=False
)
    retrieval_session = relationship(
    "RetrievalSession",
    back_populates="comparisons"
)
    comparison_members = relationship(
    "ComparisonMember",
    back_populates="comparison"
)



# 8 ***********************************************


class ComparisonMember(Base):

    __tablename__ = "comparison_members"

    comparison_member_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    comparison_id = Column(
    Integer,
    ForeignKey("comparisons.comparison_id"),
    nullable=False
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False
)
    comparison = relationship(
    "Comparison",
    back_populates="comparison_members"
)

    paper = relationship(
    "Paper",
    back_populates="comparison_members"
)



# 9 ***********************************************

class ResearchGap(Base):

    __tablename__ = "research_gaps"

    gap_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    
    title = Column(
    String(300),
    nullable=False
)
    description = Column(
    Text,
    nullable=False
)
    importance = Column(
    Text,
    nullable=False
)
    future_direction = Column(
    Text,
    nullable=False
)
    generated_at = Column(
    DateTime,
    server_default=func.now(),
    nullable=False
)
    gap_papers = relationship(
    "GapPaper",
    back_populates="research_gap"
)
    validation = relationship(
    "Validation",
    back_populates="research_gap",
    uselist=False
)
    confidence_score = relationship(
    "ConfidenceScore",
    back_populates="research_gap",
    uselist=False
)
  



# 10 *******************************************8

class GapPaper(Base):

    __tablename__ = "gap_papers"

    gap_paper_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    gap_id = Column(
    Integer,
    ForeignKey("research_gaps.gap_id"),
    nullable=False
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False
)
    research_gap = relationship(
    "ResearchGap",
    back_populates="gap_papers"
)
    paper = relationship(
    "Paper",
    back_populates="gap_papers"
)


# 11 *************************************************


class Validation(Base):

    __tablename__ = "validations"

    validation_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    gap_id = Column(
    Integer,
    ForeignKey("research_gaps.gap_id"),
    nullable=False,
    unique=True
)
    validation_result = Column(
    String(20),
    nullable=False
)
    supporting_reason = Column(
    Text,
    nullable=False
)
    contradicting_reason = Column(
    Text,
    nullable=False
)
    validated_at = Column(
    DateTime,
    server_default=func.now(),
    nullable=False
)
    research_gap = relationship(
    "ResearchGap",
    back_populates="validation"
)



# 12 ***************************************

class ConfidenceScore(Base):

    __tablename__ = "confidence_scores"

    confidence_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    gap_id = Column(
    Integer,
    ForeignKey("research_gaps.gap_id"),
    nullable=False,
    unique=True
)
    confidence_score = Column(
    Float,
    nullable=False
)
    explanation = Column(
    Text,
    nullable=False
)
    model = Column(
    String(100),
    nullable=False
)
    timestamp = Column(
    DateTime,
    server_default=func.now(),
    nullable=False
)
    research_gap = relationship(
    "ResearchGap",
    back_populates="confidence_score"
)


# 13 *************************************

class ProcessingStatus(Base):

    __tablename__ = "processing_status"

    status_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=False,
    unique=True
)
    downloaded = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    parsed = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    chunked = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    embedded = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    summarized = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    evidence_done = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    methodology_done = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    paper = relationship(
    "Paper",
    back_populates="processing_status"
)



# 14 ********************************************

class AgentLog(Base):

    __tablename__ = "agent_logs"

    log_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    session_id = Column(
    Integer,
    ForeignKey("retrieval_sessions.session_id"),
    nullable=False
)
    paper_id = Column(
    Integer,
    ForeignKey("papers.paper_id"),
    nullable=True
)       # OPTIONAL LINK TO PAPER

    agent_name = Column(
    String(100),
    nullable=False
)
    action = Column(
    String(200),
    nullable=False
)
    status = Column(
    String(20),
    nullable=False
)
    execution_time = Column(
    Float,
    nullable=True
)
    error_message = Column(
    Text,
    nullable=True
)
    timestamp = Column(
    DateTime,
    server_default=func.now(),
    nullable=False
)
    session = relationship(
    "RetrievalSession",
    back_populates="agent_logs"
)
    paper = relationship(
    "Paper",
    back_populates="agent_logs"
)


# 15 **********************************

class SessionProcessingStatus(Base):

    __tablename__ = "session_processing_status"

    session_status_id = Column(
    Integer,
    primary_key=True,
    index=True
)
    session_id = Column(
    Integer,
    ForeignKey("retrieval_sessions.session_id"),
    nullable=False,
    unique=True
)
    comparison_done = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    gap_discovery_done = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    validation_done = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    confidence_done = Column(
    Boolean,
    nullable=False,
    server_default="false"
)
    started_at = Column(
    DateTime,
    server_default=func.now(),
    nullable=False
)
    completed_at = Column(
    DateTime,
    nullable=True
)
    session = relationship(
    "RetrievalSession",
    back_populates="session_processing_status"
)
    