import ast
from pychronicle.storage import initialize_database, insert_variable_state

class VariableAssignmentFinder(ast.NodeVisitor):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                print(f"Found Variable Assignment: '{target.id}' on Line {node.lineno}")
                # Log to database
                insert_variable_state(self.db_conn, node.lineno, target.id, "Pending value extraction")
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name):
            print(f"Found Annotated Assignment: '{node.target.id}' on Line {node.lineno}")
            insert_variable_state(self.db_conn, node.lineno, node.target.id, "Pending value extraction")
        self.generic_visit(node)

def analyze_assignments(file_path):
    # Initialize connection
    conn = initialize_database()
    if not conn: return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        finder = VariableAssignmentFinder(conn)
        finder.visit(tree)

    except Exception as e:
        print(f"Error analyzing file: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_assignments(__file__)
