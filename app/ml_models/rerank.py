# app/ml_models/rerank.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from typing import List, Tuple
from app.db.models.processed_article import ProcessedArticle

# 1) Load a cross‑encoder model (fine‑tuned for sentence similarity / ranking)
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def rerank_top_k(
    query: str,
    candidates: List[ProcessedArticle],
    top_n: int = 5,
    device: str = None
) -> List[Tuple[ProcessedArticle, float]]:
    """
    Rerank `candidates` by pairwise scoring against `query` using a cross‑encoder.
    Returns the top_n articles along with their cross‑encoder scores.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    # 2) Build the list of (query, candidate_text) pairs
    texts = [cand.cleaned_text or "" for cand in candidates]
    pairs = [[query, txt] for txt in texts]

    # 3) Tokenize and run in batch
    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits   # shape (len(candidates), num_labels)
        
        # 4) Interpret scores:
        #    - If model is regression-style (single output), use logits.squeeze(-1)
        #    - If binary classification, use logits[:,1] as relevance score
        if logits.size(-1) == 1:
            scores = logits.squeeze(-1)
        else:
            scores = F.softmax(logits, dim=1)[:, 1]

    # 5) Move scores to CPU and pair with candidates
    scores = scores.cpu().tolist()
    scored = list(zip(candidates, scores))

    # 6) Sort by score descending and return top_n
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]
