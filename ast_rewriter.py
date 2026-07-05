import ast

def load_and_parse_file(file_path):
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        print(f"AST successfully generated for: {file_path}")
        return tree
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

if __name__ == "__main__":
    # Test execution on itself to confirm it works
    load_and_parse_file(__file__)
