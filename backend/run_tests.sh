#!/bin/bash

# Simple script to run backend tests
# Usage: ./run_tests.sh

echo "🧪 Running Mistral Fact Checker Backend Tests..."
echo "================================================"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    source venv/bin/activate
fi

# Install test dependencies if needed
echo "📦 Checking dependencies..."
pip install -q pytest pytest-asyncio

echo ""
echo "🚀 Running tests..."
echo ""

# Run pytest with verbose output
pytest test_main.py -v --tb=short

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed. Please check the output above."
fi

exit $TEST_EXIT_CODE

