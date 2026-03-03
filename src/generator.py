import pandas as pd
import os

def export_to_csv(hooks, filename="proven_hooks.csv"):
    """
    Appends new hooks to the specified CSV file.
    Hooks is a list of dictionaries with metadata and the extracted hook.
    """
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join("data", filename)
    
    df = pd.DataFrame(hooks)
    
    # If file exists, append without header. Else, write with header.
    file_exists = os.path.isfile(filepath)
    df.to_csv(filepath, mode='a', index=False, header=not file_exists)
    
    print(f"Successfully exported {len(hooks)} hooks to {filepath}")
