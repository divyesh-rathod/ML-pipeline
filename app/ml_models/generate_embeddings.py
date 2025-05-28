# app/preprocessing/embed_runner.py

import asyncio
from app.utils.sbert_helper import embed_articles  # async helper

async def main():
    total_embedded = 0

    while True:
        # Process a batch of articles (returns e.g. "50 articles embedded and saved.")
        result_message = await embed_articles(batch_size=100)

        # Extract the count from the message
        try:
            batch_count = int(result_message.split()[0])
        except (ValueError, IndexError):
            print("Unexpected result message format:", result_message)
            break

        total_embedded += batch_count
        print(result_message)

        # Stop when no more articles to embed
        if batch_count == 0:
            break

    print(f"Done! Total documents embedded: {total_embedded}")

if __name__ == "__main__":
    asyncio.run(main())
