import unittest

from tombapi import Index
from tombgc import TombStore


class TestTombStore(unittest.TestCase):
    def test_put_counts(self):
        store = TombStore()
        self.assertEqual(store.put("a", "1", 1)["keys"], 1)

    def test_delete_marks(self):
        store = TombStore()
        store.put("a", "1", 1)
        self.assertEqual(store.delete("a", 2)["tombstones"], 1)

    def test_delete_missing(self):
        self.assertEqual(TombStore().delete("a", 1)["tombstones"], 0)

    def test_stats_shape(self):
        self.assertIn("budget", TombStore().stats())

    def test_index_wraps_store(self):
        index = Index()
        index.put("a", "1", 1)
        self.assertEqual(index.store.stats()["keys"], 1)


if __name__ == "__main__":
    unittest.main()
