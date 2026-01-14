#!/bin/bash
# Railway startup script
# This ensures the app starts correctly

echo "Starting application..."
echo "PORT: $PORT"
echo "DATABASE_URL: ${DATABASE_URL:0:20}..." # Show first 20 chars only

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT

