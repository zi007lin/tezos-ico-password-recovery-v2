from qtpy import uic
import os


def build_ui():
    """Build UI files from .ui to .py"""
    # Change this line to look in src/ui instead of just ui
    ui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "ui")
    print(f"Building UI files from: {ui_dir}")

    if not os.path.exists(ui_dir):
        print(f"UI directory not found: {ui_dir}")
        return

    # Input and output paths
    ui_file = os.path.join(ui_dir, "passrecoverywindow.ui")
    py_file = os.path.join(ui_dir, "passrecoverywindow.py")

    # Generate Python code
    with open(py_file, "w", encoding="utf-8") as f:
        uic.compileUi(ui_file, f)

    # Read generated file
    with open(py_file, "r", encoding="utf-8") as f:
        py_content = f.read()

    # Replace class name and fix icon path
    py_content = py_content.replace(
        "class Ui_PassRecoveryWindow(object):", "class PassRecoveryWindow(object):"
    )
    py_content = py_content.replace(
        "C:\\\\git\\\\TEZOS_ICO_PASSWORD_RECOVERY_TOOL_V2\\\\ui\\\\assets/tz_recovery.ico",
        "assets/tz_recovery.ico",
    )

    # Write back modified content
    with open(py_file, "w", encoding="utf-8") as f:
        f.write(py_content)

    print("UI build complete!")


if __name__ == "__main__":
    build_ui()
