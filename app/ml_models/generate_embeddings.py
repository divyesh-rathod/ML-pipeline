from app.db.session import SessionLocal
from app.utils.sbert_helper import embed_articles  # our helper function

def main():
    # Create a new database session
    db = SessionLocal()
    try:
        total_embedded = 0
        while True:
            # Process a batch of articles that don't yet have an embedding.
            # embed_articles returns a string like "50 articles embedded and saved."
            result_message = embed_articles(db, batch_size=100)
            
            # You can parse the result message or modify embed_articles to return an int.
            # Here, we'll extract the number from the message.
            try:
                # Expecting result_message to start with the count; for example: "50 articles embedded and saved."
                batch_count = int(result_message.split()[0])
            except (ValueError, IndexError):
                print("Unexpected result message format:", result_message)
                break

            total_embedded += batch_count
            print(result_message)
            # When there are no more articles to process, break the loop.
            if batch_count == 0:
                break

        print(f"Done! Total documents embedded: {total_embedded}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
