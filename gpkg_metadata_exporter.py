import sqlite3
import csv
import os

def get_table_metadata(cursor, table_name):
    """
    Retrieves and combines structural and GeoPackage-specific metadata for a single table.
    """
    column_metadata = {}

    # 1. Get Structural Metadata (Name, Type, Not Null, Auto Increment)
    # PRAGMA table_info(table_name) returns: cid, name, type, notnull, dflt_value, pk
    try:
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        table_info = cursor.fetchall()
        for col in table_info:
            cid, name, col_type, notnull, dflt_value, pk = col
            column_metadata[name] = {
                'Name': name,
                'Type': col_type,
                'Not Null': 'TRUE' if notnull else 'FALSE',
                'Auto Increment': 'TRUE' if pk and col_type.upper() == 'INTEGER' else 'FALSE',
                'Title': None,
                'Description': None,
                'Enum': None,
                'Reference Table': None,
                'Reference Column': None
            }
    except sqlite3.Error as e:
        print(f"Error querying table_info for {table_name}: {e}")
        return []

    # 2. Get Foreign Key Metadata (Reference Table, Reference Column)
    # PRAGMA foreign_key_list(table_name) returns: id, seq, table, from, to, on_update, on_delete, match
    try:
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
        fk_list = cursor.fetchall()
        # The column names for the FK list are: id, seq, table, from, to, on_update, on_delete, match
        fk_names = ["id", "seq", "table", "from", "to", "on_update", "on_delete", "match"]
        
        for fk in fk_list:
            fk_data = dict(zip(fk_names, fk))
            col_name = fk_data['from']
            if col_name in column_metadata:
                column_metadata[col_name]['Reference Table'] = fk_data['table']
                column_metadata[col_name]['Reference Column'] = fk_data['to']
    except sqlite3.Error as e:
        print(f"Error querying foreign_key_list for {table_name}: {e}")

    # 3. Get GeoPackage Metadata (Title, Description, Enum/Constraint)
    # SELECT column_name, title, description, constraint_name FROM gpkg_data_columns
    try:
        query = f"""
        SELECT column_name, title, description, constraint_name
        FROM gpkg_data_columns
        WHERE table_name = '{table_name}';
        """
        cursor.execute(query)
        gpkg_metadata = cursor.fetchall()
        for col_name, title, description, constraint_name in gpkg_metadata:
            if col_name in column_metadata:
                column_metadata[col_name]['Title'] = title
                column_metadata[col_name]['Description'] = description
                column_metadata[col_name]['Enum'] = constraint_name # GeoPackage uses constraint_name for Enum/Data Constraints
    except sqlite3.Error as e:
        print(f"Error querying gpkg_data_columns for {table_name}: {e}")
        # Note: If gpkg_data_columns is missing or the table is not registered, Title/Description/Enum will be NULL.

    # Convert dictionary values to a list of structured dictionaries for CSV
    return list(column_metadata.values())


def export_metadata_to_csv(gpkg_path, output_dir="metadata_reports"):
    """
    Main function to connect to the GeoPackage and manage the export process.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Connecting to GeoPackage: {gpkg_path}")
    
    try:
        conn = sqlite3.connect(gpkg_path)
        cursor = conn.cursor()

        # 1. Identify tables (data_type 'features' or 'attributes') from gpkg_contents
        cursor.execute("SELECT table_name FROM gpkg_contents WHERE data_type IN ('features', 'attributes');")
        table_names = [row[0] for row in cursor.fetchall()]

        if not table_names:
            print("No feature or attribute tables found in gpkg_contents.")
            return

        print(f"Found {len(table_names)} tables to process: {', '.join(table_names)}")
        
        # Define the final CSV columns (order matters)
        fieldnames = [
            'Name', 'Type', 'Not Null', 'Auto Increment', 
            'Title', 'Description', 'Enum', 
            'Reference Table', 'Reference Column'
        ]

        # 2. Process each table
        for table_name in table_names:
            metadata_rows = get_table_metadata(cursor, table_name)
            
            if not metadata_rows:
                print(f"Skipping empty or error table: {table_name}")
                continue

            # 3. Write output to CSV file
            output_file = os.path.join(output_dir, f"{table_name}.csv")
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(metadata_rows)
            
            print(f"Successfully exported metadata for '{table_name}' to '{output_file}'")

        conn.close()
        print("\nProcessing complete.")

    except sqlite3.Error as e:
        print(f"An SQLite error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    GEOPACKAGE_FILE = "schema/template.gpkg"

    export_metadata_to_csv(GEOPACKAGE_FILE)