"""tombapi.py：对外门面（老接口 put/delete 不能改）。"""
from __future__ import annotations

from tombgc import TombStore


class Index:
    def __init__(self, budget: int = 2):
        self.store = TombStore(budget)

    def put(self, key: str, value: str, at: int) -> dict:
        return self.store.put(key, value, at)

    def delete(self, key: str, at: int) -> dict:
        return self.store.delete(key, at)

    def reader(self, snapshot: int) -> dict:
        return self.store.reader(snapshot)

    def sweep(self, watermark: int) -> dict:
        return self.store.sweep(watermark)

    def snapshot(self) -> bytes:
        return self.store.persist()

    def rebuild(self, blob: bytes = None) -> dict:
        return self.store.restore(blob)
