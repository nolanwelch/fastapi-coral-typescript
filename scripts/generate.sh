#!/usr/bin/env bash
set -euo pipefail

echo "→ Exporting OpenAPI schema from backend..."
cd backend && python -m scripts.export_openapi && cd ..

echo "→ Generating frontend client from openapi.json..."
cd frontend && npx @hey-api/openapi-ts \
  --input ../openapi.json \
  --output src/api \
  --client axios && cd ..

echo "✓ Done. Commit openapi.json and src/api/ together."
