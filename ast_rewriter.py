import ast

class VariableAssignmentFinder(ast.NodeVisitor):

    def visit_Assign(self, node):
        # Handle standard assignments
        for target in node.targets:
            if isinstance(target, ast.Name):
                print(f"Found Variable Assignment: '{target.id}' on Line {node.lineno}")


        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        # Handle type-annotated assignments
        if isinstance(node.target, ast.Name):
            print(f"Found Annotated Assignment: '{node.target.id}' on Line {node.lineno}")
        self.generic_visit(node)

def analyze_assignments(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        print(f"--- Analyzing AST Nodes for: {file_path} ---")

        # Initialize
        finder = VariableAssignmentFinder()
        finder.visit(tree)

    except Exception as e:
        print(f"Error analyzing file: {e}")

if __name__ == "__main__":
    # script scan - finds 'source', 'tree', or 'finder'
    analyze_assignments(__file__)
