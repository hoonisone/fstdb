#!/bin/bash
echo "Installing build package..."
python -m pip install --upgrade build
if [ $? -ne 0 ]; then
    echo "Failed to install build package!"
    exit 1
fi

echo "Building package..."
python -m build
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi
echo "Build successful! Files are in the dist/ folder."
