#!/bin/bash

echo "🐳 Testing Docker Setup"
echo "======================"

echo ""
echo "1. 🏗️  Building Docker image..."
docker build -t credit-approval-api .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

echo ""
echo "2. 🧪 Testing with external database..."
echo "   (Make sure your .env file has the correct database credentials)"

# Test with external database
docker run --rm \
    --env-file .env \
    -p 8000:8000 \
    credit-approval-api

echo ""
echo "✅ Docker test completed!"