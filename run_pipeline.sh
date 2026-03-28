#!/bin/bash

echo "🚀 Running Data Pipeline..."

echo "1. Generating Data..."
python generate_data.py

echo "2. Validating Data..."
python data_validation.py

echo "3. Loading into SQLite..."
sqlite3 data/web_traffic.db <<EOF
DELETE FROM web_traffic;
.mode csv
.separator ","
.import data/web_traffic.csv web_traffic
EOF

echo "✅ Pipeline Completed"