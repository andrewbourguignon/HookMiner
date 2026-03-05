import pandas as pd
import os

def export_to_csv(hooks, filename="proven_hooks.csv"):
    """
    Exports new hooks to the specified CSV file in the Downloads folder.
    Hooks is a list of dictionaries with metadata and the extracted hook.
    """
    # High-access storage: Downloads (For easy user selection and prompting)
    downloads_dir = os.path.expanduser("~/Downloads")
    downloads_path = os.path.join(downloads_dir, f"HookMiner_{filename}")
    
    df = pd.DataFrame(hooks)
    
    # Export to Downloads (Overwrite/Refresh mode for the latest batch)
    df.to_csv(downloads_path, index=False)
    
    print(f"Successfully exported {len(hooks)} hooks to:")
    print(f"  - {downloads_path}")
