import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY   = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY      = os.environ["OPENAI_API_KEY"]
SUPABASE_URL        = os.environ["SUPABASE_URL"]
SUPABASE_KEY        = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

EMBEDDING_MODEL     = "text-embedding-3-small"
EMBEDDING_DIM       = 1536
CLAUDE_MODEL        = "claude-sonnet-4-6"
