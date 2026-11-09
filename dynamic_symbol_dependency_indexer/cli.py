"""CLI for dynamic-symbol-dependency-indexer."""
import sys
import argparse
from .indexer import SymbolIndexer


def main():
    parser = argparse.ArgumentParser(description="Dynamic Symbol Dependency Indexer CLI")
    parser.add_argument("--demo", action="store_true", help="Run symbol indexing demo")
    args = parser.parse_args()

    if args.demo:
        indexer = SymbolIndexer()
        code1 = "class UserManager:\n    def create_user(self):\n        pass\n"
        code2 = "from core import UserManager\ndef login():\n    pass\n"

        indexer.index_file("core/user.py", code1)
        indexer.index_file("api/auth.py", code2)

        locs = indexer.find_symbol("UserManager")
        print("Found Symbol 'UserManager':")
        for l in locs:
            print(f"  File: {l.file_path} | Line: {l.line_no} | Kind: {l.kind}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
