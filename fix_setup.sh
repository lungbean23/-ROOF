#!/bin/bash
# Quick fix script for ┴ROOF Radio vector memory setup

echo "🔧 Fixing ┴ROOF Radio Setup..."

# Step 1: Move vector_memory.py to correct location
if [ -f "hosts/ventor_memory.py" ]; then
    echo "❌ Found misnamed file: hosts/ventor_memory.py"
    echo "   Moving to correct location: vector_memory.py"
    mv hosts/ventor_memory.py vector_memory.py
    echo "✓ File relocated"
fi

# Step 2: Remove duplicate if exists
if [ -f "hosts/vector_memory.py" ]; then
    echo "⚠️  Removing duplicate hosts/vector_memory.py"
    rm hosts/vector_memory.py
fi

# Step 3: Install ChromaDB (background process to avoid hanging)
echo ""
echo "📦 Installing ChromaDB..."
echo "   This may take 2-3 minutes..."

# Install in background, show progress
pip install --user chromadb>=0.4.0 --quiet &
PID=$!

# Show spinner while installing
spin='-\|/'
i=0
while kill -0 $PID 2>/dev/null; do
    i=$(( (i+1) %4 ))
    printf "\r   Installing... ${spin:$i:1}"
    sleep 0.1
done

wait $PID
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\r✓ ChromaDB installed successfully!        "
else
    echo -e "\r❌ Installation failed. Try manually:      "
    echo "   pip install --user chromadb"
    exit 1
fi

# Step 4: Verify installation
echo ""
echo "🔍 Verifying installation..."
python3 -c "import chromadb; print('✓ ChromaDB imported successfully')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete! You can now run:"
    echo "   python3 troof.py \"your topic here\""
else
    echo ""
    echo "⚠️  Import verification failed. Check Python path."
fi

echo ""
echo "📁 File structure verified:"
tree -L 2 --filesfirst | grep -E "(vector|host|intern)" || find . -name "*vector*" -o -name "smart_host.py"
