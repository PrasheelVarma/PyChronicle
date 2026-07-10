import ast
import sys

from pychronicle.storage import (
    initialize_database,
    insert_variable_state
)


class VariableAssignmentFinder(ast.NodeVisitor):
    """
    Traverses the AST and records every variable assignment.
    """

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def visit_Assign(self, node):
        """
        Handles normal assignments.

        Example:
            x = 10
            a = b = 5
        """
        for target in node.targets:
            if isinstance(target, ast.Name):
                print(
                    f"Found Variable Assignment: "
                    f"'{target.id}' on Line {node.lineno}"
                )

                insert_variable_state(
                    self.db_conn,
                    node.lineno,
                    target.id,
                    "Pending value extraction"
                )

        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        """
        Handles annotated assignments.

        Example:
            age: int = 20
        """
        if isinstance(node.target, ast.Name):
            print(
                f"Found Annotated Assignment: "
                f"'{node.target.id}' on Line {node.lineno}"
            )

            insert_variable_state(
                self.db_conn,
                node.lineno,
                node.target.id,
                "Pending value extraction"
            )

        self.generic_visit(node)


def analyze_assignments(file_path: str) -> None:
    """
    Parse a Python source file and log all variable assignments.
    """

    conn = initialize_database()

    if conn is None:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)

        finder = VariableAssignmentFinder(conn)
        finder.visit(tree)

        print("\nAnalysis completed successfully.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' was not found.")

    except SyntaxError as e:
        print(
            f"Syntax Error in '{file_path}' "
            f"at line {e.lineno}: {e.msg}"
        )

    except Exception as e:
        print(f"Unexpected Error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("\nUsage:")
        print("python -m pychronicle.parser <python_file>\n")
        sys.exit(1)

    analyze_assignments(sys.argv[1])
