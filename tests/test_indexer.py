"""Unit tests for dynamic-symbol-dependency-indexer."""
import unittest
from dynamic_symbol_dependency_indexer.indexer import SymbolIndexer


class TestSymbolIndexer(unittest.TestCase):
    def setUp(self):
        self.indexer = SymbolIndexer()

    def test_indexing_functions_and_classes(self):
        code = "class Engine:\n    pass\ndef start():\n    pass\n"
        self.indexer.index_file("test.py", code)

        cls_loc = self.indexer.find_symbol("Engine")
        self.assertEqual(len(cls_loc), 1)
        self.assertEqual(cls_loc[0].kind, "class")

        fn_loc = self.indexer.find_symbol("start")
        self.assertEqual(len(fn_loc), 1)
        self.assertEqual(fn_loc[0].kind, "function")
