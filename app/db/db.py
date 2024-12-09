from supabase import create_client, Client
from app.core.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET


if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET]):
    raise EnvironmentError("One or more Supabase environment variables are missing")

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)