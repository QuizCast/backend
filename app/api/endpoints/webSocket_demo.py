import os
import dotenv
from supabase import create_client, Client, AClient, acreate_client

dotenv.load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def handle_record_updated(payload):
    print("Record Updated")
    print(payload)

async def main():
    supabase: AClient = await acreate_client(SUPABASE_URL, SUPABASE_KEY)

    await supabase.realtime.connect()

    await (supabase.realtime
            .channel("my_channel")
            .on_postgres_changes("*", schema="public", table="demo-table", callback=handle_record_updated)
            .subscribe())

    await supabase.realtime.listen()

import asyncio
asyncio.run(main())