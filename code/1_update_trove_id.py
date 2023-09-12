"""
This program takes in a folder of Excel files and updates the Trove ID column with the new Trove ID. 
This program writes this updated data to a new CSV file in a folder called 'processed_files' in the same directory as the input folder.
TO FOLLOW UP: WHAT HAPPENS TO ROWS WITH TROVE_ID THAT IS NOT UPDATED????!!!!!I NEED TO ACCOUNT FOR THIS
"""

import os
import pandas as pd
import re
import json
import glob

def rename_trove_column(df):
    """
    This function takes a DataFrame and looks for a column named 'Trove ID' or something similar (case-insensitive).
    If such a column is found, it is renamed to 'Old_Trove_ID'. If no such column is found, a message is printed to the console.

    Parameters:
    df (pandas.DataFrame): The DataFrame to modify.

    Returns:
    pandas.DataFrame: The modified DataFrame. If a 'Trove ID' column was found and renamed, the returned DataFrame will have this column renamed to 'Old_Trove_ID'. Otherwise, the DataFrame is returned as is.
    """

    found_column = False
    for column in df.columns:
        if re.search(r'trove[_\s]ID', column, re.IGNORECASE):
            df.rename(columns={column: 'Old_Trove_ID'}, inplace=True)
            found_column = True
            break
    if not found_column:
        print('Column not found')
    return df

def convert_to_int(df):
    """
    This function takes a DataFrame and converts the 'Old_Trove_ID' column to integer type. 
    It first attempts to convert the column to numeric type. Any errors during this conversion (due to non-numeric values) are coerced into NaN.
    Then, it replaces any NaN values with 0 and converts the entire column to integer type.

    Parameters:
    df (pandas.DataFrame): The DataFrame to modify. This DataFrame should have an 'Old_Trove_ID' column.

    Returns:
    pandas.DataFrame: The modified DataFrame with 'Old_Trove_ID' column converted to integer type. 
    If the 'Old_Trove_ID' column did not exist, or contained values that could not be converted to integers, those cells will contain 0.
    """

    # Convert the 'Old_Trove_ID' column to numeric values and replace non-numeric values with NaN
    df['Old_Trove_ID'] = pd.to_numeric(df['Old_Trove_ID'], errors='coerce')
    # Fill NaN values with a default value (0) to skip over empty values
    df['Old_Trove_ID'].fillna(0, inplace=True)
    # Convert the 'Old_Trove_ID' column to integer data type
    df['Old_Trove_ID'] = df['Old_Trove_ID'].astype(int)
    return df  # Return the modified DataFrame

def load_trove_dictionary(file_path: str) -> dict:
    """
    This function reads a JSON file which contains a dictionary of Trove IDs.
    It retrieves the dictionary under the key 'trove' and returns it.
    
    Parameters:
    file_path (str): The path to the JSON file.
    
    Returns:
    dict: The dictionary of Trove IDs.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        trove_dict = data.get("trove", {})
    return trove_dict

def process_directory(input_dir, json_file_path: str) -> None:
    """
    This function processes all Excel files in the given directory. 
    For each Excel file, it reads the data, renames the Trove ID column, 
    converts the Trove ID values to integers, maps the old Trove IDs to new 
    ones using the dictionary from the JSON file, and writes the updated data 
    to a new CSV file in a 'processed_files' subdirectory.

    Parameters:
    input_dir (str): The path to the directory containing the Excel files to process.
    json_file_path (str): The path to the JSON file containing the dictionary of Trove IDs.
    
    Returns:
    None
    """
    trove_dict = load_trove_dictionary(json_file_path)
    # Create 'processed_files' folder in the same directory
    output_dir = os.path.join(input_dir, 'processed_files')
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all Excel files in the directory
    file_list = glob.glob(os.path.join(input_dir, '*.xlsx'))
    for file_path in file_list:
        # Skip temporary files
        if os.path.basename(file_path).startswith('~$'):
            continue
        #print to console to show progress
        print(f"working on {file_path}")

        # Check if file has already been processed
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if os.path.exists(os.path.join(output_dir, f'{base_name}_UPDATED_MAPPING.csv')): 
            print(f"{file_path} has already been processed, skipping...")
            continue

        # Read only up to the 33rd column, this is only for the sheets created prior to June_2022
        df = pd.read_excel(file_path, sheet_name='Sheet1', usecols=range(33))
        #df = pd.read_excel(file_path, sheet_name='Sheet1')
        
        df = rename_trove_column(df)
        df = convert_to_int(df)
        df['title_id'] = df['Old_Trove_ID'].astype(str).map(trove_dict).astype('Int64')
        # Write the DataFrame to a new CSV file in 'processed_files' folder
        output_file_name = os.path.basename(file_path).replace('.xlsx', '_UPDATED_MAPPING.csv')
        output_file_path = os.path.join(output_dir, output_file_name)
        df.to_csv(output_file_path, index=False)

def main():
    json_file_path = '/Volumes/UNTITLED/remote_old_to_new_mappings.json'
    input_dir = "INSERT FOLDER NAME HERE"
    process_directory(input_dir, json_file_path)
    
if __name__ == "__main__":
    main()
