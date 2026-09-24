"""tombgc.py：墓碑清理（基线：只标不扫）。"""
from __future__ import annotations


class TombStore:
    def __init__(self, budget: int = 2):
        self.budget = budget
        self.entries = {}
        self.tombstones = {}
        self.cleared = 0

    def put(self, key: str, value: str, at: int) -> dict:
        self.entries[key] = {"value": value, "at": at}
        self.tombstones.pop(key, None)
        return {"keys": len(self.entries)}

    def delete(self, key: str, at: int) -> dict:
        """基线：留个墓碑，永远不清。"""
        if key in self.entries:
            self.entries.pop(key)
            self.tombstones[key] = at
        return {"tombstones": len(self.tombstones)}

    def reader(self, snapshot: int) -> dict:
        return {"snapshot": snapshot}

    def sweep(self, watermark: int) -> dict:
        raise NotImplementedError("墓碑清理还没实现")

    def persist(self) -> bytes:
        raise NotImplementedError("快照还没实现")

    def restore(self, blob: bytes = None) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"keys": len(self.entries), "tombstones": len(self.tombstones),
                "cleared": self.cleared, "budget": self.budget}
