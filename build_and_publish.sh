#!/bin/bash

echo "Building FSTDB package..."
python -m build

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo ""
echo "Build successful! Files are in the dist/ folder."
echo ""
echo "To upload to PyPI, run:"
echo "  python -m twine upload dist/*"
echo ""
echo "Or to upload to TestPyPI first:"
echo "  python -m twine upload --repository testpypi dist/*"
echo ""
