"""
This program takes in a folder of CSV files and performs the following operations on each file if there is 
an entry in the column called 'title_id':
1. checks that all the data in the 'chapter number' column is a string. If the row is empty, it is filled with an empty string ('').
2. checks that all the data in the 'chapter title' column is a string. If the row is empty, it is filled with an empty string ('').
3. Reads in the 'article_id' column as an integer, and reads in reads a JSON file which contains a dictionary of article_ids.
4. Checks if the article_id is in the dictionary. 
If it is not in the dictionary, the row is written to a new CSV file with an updated filename that ends 'sheet_to_upload.csv'.
If the article_id is in the dictionary, the row is written to a new CSV file with an updated filename that ends 'sheet_to_check.csv'.
5. The new CSV files are saved in a folder called 'processed_files' in the same directory as the input folder.
"""

import os
import pandas as pd
import re
import json
import glob
import datetime

def check_chapter_number(df):
    """
    This function checks that all the data in the 'chapter number' column is a string.
    If the row is empty, it is filled with an empty string ('').
    If the row is not empty, it is converted to a string.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to modify.

    Returns:
    pandas.DataFrame: The modified DataFrame. If a 'chapter number' column was found and converted, the returned DataFrame will have this column converted to string type. Otherwise, the DataFrame is returned as is.
    """

    #check if chapter number column exists
    found_column = False
    for column in df.columns:
        if re.search(r'chapter[_\s]number', column, re.IGNORECASE):
            found_column = True
            # change column name to 'chapter_number'
            df.rename(columns={column: 'chapter_number'}, inplace=True)
            #replace all nan values with empty string
            df['chapter_number'] = df['chapter_number'].astype(str).replace('nan', '', regex=False)
            #convert column to string
            df['chapter_number'] = df['chapter_number'].astype(str)
            break
    if not found_column:
        print("No 'chapter number' column found.")
    return df

def check_chapter_title(df):
    """
    This function checks that all the data in the 'chapter title' column is a string.
    If the row is empty, it is filled with an empty string ('').
    If the row is not empty, it is converted to a string.

    Parameters:
    df (pandas.DataFrame): The DataFrame to modify.

    Returns:
    pandas.DataFrame: The modified DataFrame. If a 'chapter title' column was found and converted, the returned DataFrame will have this column converted to string type. Otherwise, the DataFrame is returned as is.
    """
    
    #check if chapter title column exists
    found_column = False
    for column in df.columns:
        if re.search(r'chapter[_\s]title', column, re.IGNORECASE):
            found_column = True
            # change column name to 'chapter_title'
            df.rename(columns={column: 'chapter_title'}, inplace=True)
         # Convert column to string and replace 'nan' with empty string
            df['chapter_title'] = df['chapter_title'].astype(str).replace('nan', '', regex=False)
            break
    if not found_column:
        print("No 'chapter title' column found.")
    return df

def load_article_dictionary(file_path: str) -> list:
    """
    This function reads a JSON file which contains an array of article_ids.
    
    Parameters:
    file_path (str): The path to the JSON file to read.
    
    Returns:
    list: The array of article_ids.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        article_ids = data.get("uploaded_chapters", [])
    return article_ids

def process_directory(input_dir, json_file_path: str) -> None:
    """
    This function processes all the csv files in the given directory.
    For each csv file, it reads the data, checks that the article_id is in the dictionary,
    if it is not in the dictionary, the row is written to a new CSV file with an updated filename that ends 'sheet_to_upload.csv'.
    If the article_id is in the dictionary, the row is written to a new CSV file with an updated filename that ends 'sheet_to_check.csv'.
    The new CSV files are saved in a folder called 'processed_files' in the same directory as the input folder.

    Parameters:
    input_dir (str): The path to the directory containing the CSV files to process.
    json_file_path (str): The path to the JSON file containing the array of article_ids.

    Returns:
    None

    """
    article_ids = load_article_dictionary(json_file_path)

    # Create 'processed_files' folder in the same directory
    output_dir = os.path.join(input_dir, 'clean_and_check_processed_files')
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all CSV files in the directory
    file_list = glob.glob(os.path.join(input_dir, '*.csv'))
    for file_path in file_list:
        # Skip temporary files
        if os.path.basename(file_path).startswith('~$'):
            continue
        #print to console to show progress
        print(f"working on {file_path}")
        # print timestamp to console to show progress
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        df = pd.read_csv(file_path)
        #call function to check chapter number
        df = check_chapter_number(df)
        #call function to check chapter title
        df = check_chapter_title(df)


        #Check if article_id is in array article_ids, if not, write to sheet_to_upload.csv
        for index, row in df.iterrows():
            #check if value in title_id is a NaN value
            if pd.isna(row['title_id']):
                #write this row to '_sheet_to_check.csv'
                output_file_name = os.path.basename(file_path).replace('.csv', '_sheet_to_check.csv')
            elif 'article_id' in row:
            # Convert the article_id to str, handling any conversion errors
                try:
                    article_id = str(row['article_id'])
                    #article_id = int(row['article_id'])
                    if article_id not in article_ids:
                        output_file_name = os.path.basename(file_path).replace('.csv', '_sheet_to_upload.csv')
                    else:
                        output_file_name = os.path.basename(file_path).replace('.csv', '_sheet_to_check.csv')
                except ValueError:
                    print(f"Error converting article_id for row {index}: {row['article_id']}")
                    continue # Skip this row if conversion fails
            else:
                print(f"No article_id found for row {index}")
                continue # Skip this row if no article_id found

            output_file_path = os.path.join(output_dir, output_file_name)
            row.to_frame().T.to_csv(output_file_path, index=False, mode='a', header=not os.path.exists(output_file_path))
            

def main():
    json_file_path = '/Volumes/UNTITLED/remote_old_to_new_mappings.json'
    input_dir = "INSERT FOLDER NAME HERE"
    process_directory(input_dir, json_file_path)
   
if __name__ == "__main__":
    main()