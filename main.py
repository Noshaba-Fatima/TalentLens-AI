import subprocess
import sys
from pathlib import Path


def main() -> None:
    app_path = Path(__file__).resolve().parent / "streamlit_app.py"

    if not app_path.exists():
        print(f"Error: Could not find {app_path}")
        sys.exit(1)

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path)],
            check=True,
        )
    except KeyboardInterrupt:
        print("\nShutting down TalentLens AI...")


if __name__ == "__main__":
    main()