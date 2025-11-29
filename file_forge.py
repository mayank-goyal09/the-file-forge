# file_forge.py
import os
import csv
import json
import pandas as pd

# --- DIRECTORY MANAGEMENT ---
# We will store all files in a "forge_files" folder so we don't mess up your project folder
WORK_DIR = "forge_files"
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)

def get_file_path(filename):
    """Helper to get full path in the work directory."""
    return os.path.join(WORK_DIR, filename)

def list_all_files():
    """Returns a list of all files in the forge."""
    if not os.path.exists(WORK_DIR):
        return []
    return [f for f in os.listdir(WORK_DIR) if os.path.isfile(os.path.join(WORK_DIR, f))]

# --- 1. CREATE ---
def create_file(filename, content, file_type):
    """Creates a file (TXT, CSV, JSON) with initial content."""
    path = get_file_path(filename)
    
    try:
        if file_type == "Text (.txt)":
            if not filename.endswith('.txt'): filename += '.txt'
            path = get_file_path(filename)
            with open(path, 'w') as f:
                f.write(content)
                
        elif file_type == "CSV (.csv)":
            if not filename.endswith('.csv'): filename += '.csv'
            path = get_file_path(filename)
            # Expecting content to be "Name,Age\nAlice,30" format
            lines = content.strip().split('\n')
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                for line in lines:
                    writer.writerow(line.split(','))
                    
        elif file_type == "JSON (.json)":
            if not filename.endswith('.json'): filename += '.json'
            path = get_file_path(filename)
            # Expecting valid JSON string
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                return "Error: Invalid JSON content!", None
            with open(path, 'w') as f:
                json.dump(json_content, f, indent=4)
                
        return f"✅ Success! '{filename}' created.", path
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# --- 2. READ ---
def read_file(filename):
    """Reads file content."""
    path = get_file_path(filename)
    if not os.path.exists(path):
        return "Error: File not found!", None
        
    try:
        if filename.endswith('.txt'):
            with open(path, 'r') as f:
                return f.read(), None
        elif filename.endswith('.csv'):
            df = pd.read_csv(path)
            return "Loaded CSV", df
        elif filename.endswith('.json'):
            with open(path, 'r') as f:
                return "Loaded JSON", json.load(f)
        else:
            with open(path, 'r') as f:
                return f.read(), None
    except Exception as e:
        return f"Error: {str(e)}", None

# --- 3. APPEND ---
def append_to_file(filename, content):
    """Appends text to a TXT file."""
    path = get_file_path(filename)
    if not os.path.exists(path):
        return "Error: File not found!"
    
    try:
        # Only supporting text append for simplicity in this demo
        with open(path, 'a') as f:
            f.write("\n" + content)
        return f"✅ Appended to '{filename}'!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- 4. DELETE ---
def delete_file(filename):
    """Deletes a file."""
    path = get_file_path(filename)
    try:
        if os.path.exists(path):
            os.remove(path)
            return f"🗑️ Deleted '{filename}'."
        else:
            return "Error: File not found!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- 5. CONVERT ---
def convert_csv_json(filename):
    """Converts CSV <-> JSON based on extension."""
    path = get_file_path(filename)
    if not os.path.exists(path):
        return "Error: File not found!", None

    try:
        if filename.endswith('.csv'):
            # CSV -> JSON
            with open(path, 'r') as f:
                data = list(csv.DictReader(f))
            new_name = filename.replace('.csv', '.json')
            new_path = get_file_path(new_name)
            with open(new_path, 'w') as f:
                json.dump(data, f, indent=4)
            return f"✅ Converted to '{new_name}'", new_path
            
        elif filename.endswith('.json'):
            # JSON -> CSV
            with open(path, 'r') as f:
                data = json.load(f)
            if not isinstance(data, list): return "Error: JSON must be a list!", None
            
            new_name = filename.replace('.json', '.csv')
            new_path = get_file_path(new_name)
            with open(new_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return f"✅ Converted to '{new_name}'", new_path
            
        else:
            return "Error: Only CSV or JSON allowed!", None
    except Exception as e:
        return f"❌ Error: {str(e)}", None
