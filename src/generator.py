import pandas as pd
import os

def export_to_csv(hooks, filename="proven_hooks.csv"):
    """
    Appends new hooks to the specified CSV file in Documents and creates a copy in Downloads.
    Hooks is a list of dictionaries with metadata and the extracted hook.
    """
    # 1. Primary storage: Documents (Persistent Database)
    documents_dir = os.path.expanduser("~/Documents/HookMiner/data")
    os.makedirs(documents_dir, exist_ok=True)
    filepath = os.path.join(documents_dir, filename)
    
    # 2. Secondary storage: Downloads (For easy user access)
    downloads_dir = os.path.expanduser("~/Downloads")
    downloads_path = os.path.join(downloads_dir, f"HookMiner_{filename}")
    
    df = pd.DataFrame(hooks)
    
    # Export to Documents (Append mode)
    file_exists = os.path.isfile(filepath)
    df.to_csv(filepath, mode='a', index=False, header=not file_exists)
    
    # Export to Downloads (Overwrite/Refresh mode for the latest batch)
    df.to_csv(downloads_path, index=False)
    
    print(f"Successfully exported {len(hooks)} hooks to:")
    print(f"  - {filepath} (Aggregated)")
    print(f"  - {downloads_path} (Latest Run)")
