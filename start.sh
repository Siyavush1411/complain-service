#!/bin/bash

echo "Starting FastAPI server..."
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

cleanup() {
    echo "Shutting down..."
    kill $UVICORN_PID
    kill $BOT_PID
}

trap cleanup SIGINT

wait $UVICORN_PID
wait $BOT_PID
