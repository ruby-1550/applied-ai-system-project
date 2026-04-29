from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt
from typing import Dict, Iterable, List, Sequence, Tuple
import re

try:
    from .catalog import SongRecord
except ImportError:  # Allows running as scripts
    from catalog import SongRecord


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())


def _term_freq(tokens: Sequence[str]) -> Dict[str, float]:
    tf: Dict[str, float] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0.0) + 1.0
    if not tf:
        return tf
    norm = max(tf.values())
    for k in list(tf.keys()):
        tf[k] = tf[k] / norm
    return tf


def _idf(docs: List[List[str]]) -> Dict[str, float]:
    df: Dict[str, int] = {}
    for doc in docs:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1
    n = len(docs)
    return {term: log((n + 1) / (count + 1)) + 1.0 for term, count in df.items()}


def _tfidf_vec(tf: Dict[str, float], idf: Dict[str, float]) -> Dict[str, float]:
    return {t: tf_val * idf.get(t, 0.0) for t, tf_val in tf.items() if t in idf}


def _dot(a: Dict[str, float], b: Dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def _norm(a: Dict[str, float]) -> float:
    return sqrt(sum(v * v for v in a.values()))


def cosine_similarity(a: Dict[str, float], b: Dict[str, float]) -> float:
    denom = _norm(a) * _norm(b)
    if denom == 0.0:
        return 0.0
    return _dot(a, b) / denom


@dataclass(frozen=True)
class RetrievalHit:
    song: SongRecord
    score: float


class TfidfRetriever:
    def __init__(self, catalog: List[SongRecord]):
        self.catalog = catalog
        self._docs = [tokenize(s.text) for s in catalog]
        self._idf = _idf(self._docs)
        self._doc_vecs = [_tfidf_vec(_term_freq(doc), self._idf) for doc in self._docs]

    def search(self, query: str, k: int = 20) -> List[RetrievalHit]:
        q_vec = _tfidf_vec(_term_freq(tokenize(query)), self._idf)
        scored: List[RetrievalHit] = []
        for song, doc_vec in zip(self.catalog, self._doc_vecs):
            scored.append(RetrievalHit(song=song, score=cosine_similarity(q_vec, doc_vec)))
        scored.sort(key=lambda h: h.score, reverse=True)
        return scored[:k]
