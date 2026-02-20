#!/bin/bash
# Deployment script for Hugging Face Spaces

echo "Preparing backend for Hugging Face deployment..."

# Check if required environment variables are set
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL environment variable is not set"
    exit 1
fi

if [ -z "$JWT_SECRET" ]; then
    echo "Error: JWT_SECRET environment variable is not set"
    exit 1
fi

echo "Environment variables are properly set."

# Install dependencies
pip install -r requirements.txt

echo "Dependencies installed successfully."

# Run database migrations if needed
# alembic upgrade head

echo "Deployment preparation completed successfully."
echo "Application is ready to run on Hugging Face Spaces."