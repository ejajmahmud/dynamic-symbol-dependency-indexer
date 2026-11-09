"""Core Dynamic Symbol Dependency Indexer implementation."""
import ast
from typing import Dict, List, Set, Optional, Any


class SymbolLocation:
    def __init__(self, symbol_name: str, file_path: str, line_no: int, kind: str):
        self.symbol_name = symbol_name
        self.file_path = file_path
        self.line_no = line_no
        self.kind = kind  # "function", "class", "variable"


class SymbolIndexer:
    def __init__(self):
        self.symbol_table: Dict[str, List[SymbolLocation]] = {}
        self.file_imports: Dict[str, Set[str]] = {}  # file_path -> {imported_modules}

    def index_file(self, file_path: str, content: str):
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        self.file_imports[file_path] = set()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._add_symbol(node.name, file_path, node.lineno, "function")
            elif isinstance(node, ast.ClassDef):
                self._add_symbol(node.name, file_path, node.lineno, "class")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.file_imports[file_path].add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.file_imports[file_path].add(node.module)

    def _add_symbol(self, name: str, file_path: str, line: int, kind: str):
        if name not in self.symbol_table:
            self.symbol_table[name] = []
        self.symbol_table[name].append(SymbolLocation(name, file_path, line, kind))

    def find_symbol(self, name: str) -> List[SymbolLocation]:
        return self.symbol_table.get(name, [])

    def get_imported_modules(self, file_path: str) -> Set[str]:
        return self.file_imports.get(file_path, set())
