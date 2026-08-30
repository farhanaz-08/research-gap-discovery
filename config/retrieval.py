"""
Configuration for the retrieval pipeline.
"""

# ==========================
# Local Knowledge Check
# ==========================

MIN_LOCAL_PAPERS = 10
MIN_AVERAGE_SCORE = 4
TOP_K_LOCAL_SEARCH = 20

# ==========================
# Retrieval Agent
# ==========================

MAX_RETRIEVED_PAPERS = 100
ARXIV_RESULTS_PER_REQUEST = 100
SEMANTIC_SCHOLAR_RESULTS = 100

# ==========================
# Working Memory
# ==========================

WORKING_SET_SIZE = 20

# ==========================
# Vector Search (Qdrant)
# ==========================

TOP_K_VECTOR_SEARCH = 20
MIN_VECTOR_SIMILARITY = 0.80