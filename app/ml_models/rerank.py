# app/ml_models/rerank.py

import asyncio
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from typing import List, Tuple
from app.db.models.processed_article import ProcessedArticle

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

async def rerank_top_k(
    query: str,
    candidates: List[ProcessedArticle],
    top_n: int = 5,
    device: str | None = None
) -> List[Tuple[ProcessedArticle, float]]:
    """
    Async wrapper around the synchronous cross-encoder inference.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Prepare input pairs
    texts = [cand.cleaned_text or "" for cand in candidates]
    pairs = [[query, txt] for txt in texts]
    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    loop = asyncio.get_running_loop()

    def _sync_inference():
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            # Handle regression vs. classification heads
            if logits.size(-1) == 1:
                scores_tensor = logits.squeeze(-1)
            else:
                scores_tensor = F.softmax(logits, dim=1)[:, 1]
            return scores_tensor.cpu().tolist()

    # Run the blocking inference in a threadpool
    scores = await loop.run_in_executor(None, _sync_inference)

    # Pair, sort, and return top_n
    scored = list(zip(candidates, scores))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]
