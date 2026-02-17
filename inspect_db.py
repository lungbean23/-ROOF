#!/usr/bin/env python3
"""
Inspect Qdrant vector databases to see what memories persist
"""

from qdrant_client import QdrantClient
from pathlib import Path
import sys

def inspect_collection(collection_name: str, collection_path: Path):
    """Inspect a single Qdrant collection"""
    
    print(f"\n{'='*80}")
    print(f"📊 {collection_name.upper()}")
    print(f"{'='*80}")
    print(f"Looking in: {collection_path}")
    
    if not collection_path.exists():
        print(f"❌ Does not exist")
        return
    
    try:
        client = QdrantClient(path=str(collection_path))
        
        # Get collection info
        collection_info = client.get_collection(collection_name)
        point_count = collection_info.points_count
        
        print(f"Total memories: {point_count}")
        
        if point_count == 0:
            print("✅ Empty - no contamination")
            return
        
        # Scroll through all points to see content
        points = client.scroll(
            collection_name=collection_name,
            limit=min(20, point_count),  # Get up to 20 recent memories
            with_payload=True,
            with_vectors=False
        )[0]
        
        print(f"\n📝 Sample memories (showing {len(points)} of {point_count}):\n")
        
        # Track contamination keywords
        contamination_found = []
        keywords = ['kenya', 'm-pesa', 'mpesa', 'epstein', 'maxwell', 'nyc', 'housing', 
                   'roman', 'magistrate', 'inspector general']
        
        for i, point in enumerate(points, 1):
            payload = point.payload
            
            # Extract key info
            message = payload.get('message', 'N/A')[:200]  # First 200 chars
            host = payload.get('host', 'N/A')
            exchange_num = payload.get('exchange_num', 'N/A')
            
            # Check for contamination
            message_lower = message.lower()
            found_keywords = [k for k in keywords if k in message_lower]
            
            if found_keywords:
                contamination_found.extend(found_keywords)
                print(f"🚨 {i}. Exchange #{exchange_num} ({host}) - CONTAMINATION: {found_keywords}")
            else:
                print(f"✓ {i}. Exchange #{exchange_num} ({host})")
            
            print(f"   {message}...")
            print()
        
        if contamination_found:
            print(f"⚠️  CONTAMINATION DETECTED: {set(contamination_found)}")
        else:
            print("✅ No obvious contamination in sample")
            
    except Exception as e:
        print(f"❌ Error reading {collection_name}: {e}")


def main():
    """Inspect all Qdrant collections"""
    
    # Detect project root
    script_dir = Path(__file__).parent
    if script_dir.name == 'db':
        project_root = script_dir.parent.parent
    else:
        project_root = script_dir
    
    print(f"\n🔍 QDRANT DATABASE CONTAMINATION INSPECTOR")
    print("="*80)
    print(f"Project root: {project_root}")
    print("Checking for old topic pollution in vector databases...\n")
    
    data_dir = project_root / "data"
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        print("Run this script from the project root!")
        sys.exit(1)
    
    collections = [
        ("goku_conversation", data_dir / "goku_conversation" / "qdrant_goku"),
        ("homer_conversation", data_dir / "homer_conversation" / "qdrant_homer"),
        ("intern_taco_conversation", data_dir / "intern_taco_conversation" / "qdrant_intern_taco"),
        ("intern_clunt_conversation", data_dir / "intern_clunt_conversation" / "qdrant_intern_clunt"),
        ("director_conversation", data_dir / "director_memory" / "qdrant_director"),
    ]
    
    print("🔎 Searching for contamination keywords:")
    print("   - Kenya, M-Pesa (from payment systems topic)")
    print("   - Epstein, Maxwell (from conspiracy topic)")
    print("   - NYC, housing (from urban planning topic)")
    print("   - Roman, magistrate (from governance topic)")
    print()
    
    for collection_name, collection_path in collections:
        inspect_collection(collection_name, collection_path)
    
    print("\n" + "="*80)
    print("🎯 CONTAMINATION DETECTION COMPLETE")
    print("="*80)
    print("\nTo clear contaminated databases, run:")
    print("  python3 troof.py --fresh \"your new topic\"")
    print()


if __name__ == "__main__":
    main()
