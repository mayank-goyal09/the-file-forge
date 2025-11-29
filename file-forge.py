import os
import csv
import json
import time

# ========== TEXT FILE OPERATIONS ==========
def create_text_file(filename, content):
    """Creates a text file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Text file '{filename}' forged successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

def read_text_file(filename):
    """Reads a text file."""
    try:
        with open(filename, 'r') as f:
            print(f"\n📜 --- Content of {filename} ---")
            print(f.read())
            print("----------------------------------")
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found!")

def append_text_file(filename, content):
    """Appends to a text file."""
    try:
        with open(filename, 'a') as f:
            f.write("\n" + content)
        print(f"✅ Data added to '{filename}'!")
    except Exception as e:
        print(f"❌ Error: {e}")

# ========== CSV OPERATIONS ==========
def create_csv_file(filename):
    """Creates a CSV file with user-defined headers and rows."""
    try:
        headers = input("Enter column names (comma-separated, e.g., Name,Age,City): ").split(',')
        headers = [h.strip() for h in headers]
        
        rows = []
        print("Enter rows one by one. Type 'done' when finished.")
        while True:
            print(f"Enter values for {headers} (comma-separated):")
            user_input = input("👉 ")
            if user_input.lower() == 'done':
                break
            values = user_input.split(',')
            values = [v.strip() for v in values]
            
            if len(values) != len(headers):
                print(f"⚠️ Expected {len(headers)} values, got {len(values)}. Try again.")
                continue
            
            row_dict = dict(zip(headers, values))
            rows.append(row_dict)
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✅ CSV file '{filename}' created with {len(rows)} rows! 📊")
    except Exception as e:
        print(f"❌ Error: {e}")

def read_csv_file(filename):
    """Reads and displays a CSV file."""
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            print(f"\n📊 --- CSV Content of {filename} ---")
            for row in reader:
                print(row)
            print("---------------------------------------")
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found!")
    except Exception as e:
        print(f"❌ Error: {e}")

# ========== JSON OPERATIONS ==========
def create_json_file(filename):
    """Creates a JSON file from user input."""
    try:
        print("Let's build a JSON object!")
        data = {}
        
        while True:
            key = input("Enter a key (or 'done' to finish): ")
            if key.lower() == 'done':
                break
            value = input(f"Enter value for '{key}': ")
            
            # Try to convert to number if possible
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep as string
            
            data[key] = value
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"✅ JSON file '{filename}' created! 🌐")
    except Exception as e:
        print(f"❌ Error: {e}")

def read_json_file(filename):
    """Reads and displays a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            print(f"\n🌐 --- JSON Content of {filename} ---")
            print(json.dumps(data, indent=4))
            print("----------------------------------------")
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found!")
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON format in '{filename}'!")
    except Exception as e:
        print(f"❌ Error: {e}")

# ========== CONVERSION OPERATIONS ==========
def csv_to_json(csv_filename, json_filename):
    """Converts a CSV file to JSON format."""
    try:
        with open(csv_filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)
        
        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"✅ Successfully converted '{csv_filename}' → '{json_filename}'! 🔄")
        print(f"📊 Converted {len(data)} rows.")
        
    except FileNotFoundError:
        print(f"❌ Error: '{csv_filename}' not found!")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

def json_to_csv(json_filename, csv_filename):
    """Converts a JSON file (list of dictionaries) to CSV format."""
    try:
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
        
        if not isinstance(data, list):
            print("❌ Error: JSON must be an array (list) of objects!")
            return
        
        if len(data) == 0:
            print("❌ Error: JSON file is empty!")
            return
        
        headers = data[0].keys()
        
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Successfully converted '{json_filename}' → '{csv_filename}'! 🔄")
        print(f"📊 Converted {len(data)} rows with {len(headers)} columns.")
        
    except FileNotFoundError:
        print(f"❌ Error: '{json_filename}' not found!")
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in '{json_filename}'!")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

# ========== FILE UTILITIES ==========
def delete_file(filename):
    """Deletes any file."""
    try:
        os.remove(filename)
        print(f"🗑️ File '{filename}' melted down (deleted)!")
    except FileNotFoundError:
        print(f"❌ Can't delete what doesn't exist!")

def list_files():
    """Lists all files in the current directory."""
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print("\n📂 Files in current directory:")
    for f in files:
        print(f"  • {f}")

# ========== MAIN MENU ==========
def main():
    print("⚔️⚔️⚔️  THE FILE FORGE 3.0 - ALCHEMIST EDITION  ⚔️⚔️⚔️")
    print("Now with FORMAT CONVERSION MAGIC! 🔄✨\n")
    
    # ========== MAIN MENU ==========
def main():
    print("⚔️⚔️⚔️  THE FILE FORGE 3.0 - ALCHEMIST EDITION  ⚔️⚔️⚔️")
    print("Now with FORMAT CONVERSION MAGIC! 🔄✨\n")
    
    while True:
        print("\n" + "="*55)
        print("📋 MAIN MENU")
        print("="*55)
        print(" 1.  Create TEXT File")
        print(" 2.  Read TEXT File")
        print(" 3.  Append to TEXT File")
        print(" 4.  Create CSV File 📊")
        print(" 5.  Read CSV File 📊")
        print(" 6.  Create JSON File 🌐")
        print(" 7.  Read JSON File 🌐")
        print(" 8.  Convert CSV → JSON 🔄")
        print(" 9.  Convert JSON → CSV 🔄")
        print("10.  Delete ANY File 🗑️")
        print("11.  List All Files 📂")
        print(" 0.  Exit Forge")
        
        choice = input("\n👉 Your command, Alchemist: ")
        
        # Rest of your code stays the same...

        
        if choice == '1':
            name = input("Filename (e.g., story.txt): ")
            text = input("Initial content: ")
            create_text_file(name, text)
            
        elif choice == '2':
            name = input("Filename to read: ")
            read_text_file(name)
            
        elif choice == '3':
            name = input("Filename to append: ")
            text = input("Text to add: ")
            append_text_file(name, text)
            
        elif choice == '4':
            name = input("CSV filename (e.g., data.csv): ")
            create_csv_file(name)
            
        elif choice == '5':
            name = input("CSV filename to read: ")
            read_csv_file(name)
            
        elif choice == '6':
            name = input("JSON filename (e.g., config.json): ")
            create_json_file(name)
            
        elif choice == '7':
            name = input("JSON filename to read: ")
            read_json_file(name)
            
        elif choice == '8':
            csv_name = input("Enter CSV filename to convert: ")
            json_name = input("Enter output JSON filename: ")
            csv_to_json(csv_name, json_name)
            
        elif choice == '9':
            json_name = input("Enter JSON filename to convert: ")
            csv_name = input("Enter output CSV filename: ")
            json_to_csv(json_name, csv_name)
            
        elif choice == '10':
            name = input("Filename to delete: ")
            confirm = input(f"⚠️ Are you SURE you want to delete '{name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                delete_file(name)
            else:
                print("Deletion cancelled.")
                
        elif choice == '11':
            list_files()
            
        elif choice == '0':
            print("\n👋 The Forge grows cold. Farewell, Master Alchemist!")
            break
            
        else:
            print("⚠️ Invalid command. Try again.")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
 

