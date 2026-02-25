import json
from pathlib import Path

from app.main import app


def main() -> None:
    schema = app.openapi()
    output_path = Path(__file__).resolve().parent.parent.parent / "openapi.json"
    output_path.write_text(json.dumps(schema, indent=2) + "\n")
    print(f"OpenAPI schema written to {output_path}")


if __name__ == "__main__":
    main()
