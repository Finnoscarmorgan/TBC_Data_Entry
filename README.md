# TBC_Data_Entry
This repository contains code that has been used to clean and standardise data for the To Be Continued (Read All About) Project.

The data folder contains a pickle file of a json file of data from all processed sheets (up until July 1) at time of harvest (27 July 2023)

## Remaining Tasks
1. Manually correcting files that were flagged for checking (see below)
2. Processing sheets post July 1 (see below) from One Drive

## Documentation for Sheet Data-Cleaning
This folder contains code for processing of the spreadsheets downloaded from Cloudstor (27 July 2023).
The content of Cloudstor was downloaded onto an External Hardrive and some manual processing of the sheets has been required because of different file formats from earlier documents. 

Following the download of the sheets from Cloudstor (27 July 2023), the following steps were taken:
1. The folder ```'done_after_migration'``` was created and any sheets that were created/uploaded after the 1 July 2023 have been moved into this folder (these sheets will not require the title_id to be updated)
2. The folder ```'done_prior_to_June_2022'``` was created. This folder includes sheets uploaded prior to 23 June 2022. There appears to be an issue with sheets generated prior to 23_June_2022. I have moved these into another folder to process seperately titled 'done_prior_to_23_June_2022' (this is 160 sheets)
3. The sheets that were generated and uploaded prior to migration (1 July 2023) have been moved into the folder ```'done'```

## Code Explanation

### 1.  update_trove_id.py
This program takes in a folder of Excel files and updates the Trove ID column with the new Trove ID from the mappings files.

The output is the 'UPDATED_MAPPING.csv' file. If there is not mapping to update, the row is retianed as is, and nothing is recorded in the column. 

This code is run first but does not need to be run on the sheets produced after the migration

### 2.  clean_and_check_data.py
This program takes in the ```'...UPDATED_MAPPING.csv'``` files. 

This program checks to see if the article_id exists in the the uploaded_chapters array from the mappings file and writes two csv files titled ```'...sheet_to_check.csv'``` and ```'...sheet_to_upload.csv'```. 

The ```'...sheet_to_check.csv'``` file contains the sheets that need to be checked manually. The ```'...sheet_to_upload.csv'``` file contains the sheets that can continue to the next stage to check the API and title infornation. 

The ```'...sheet_to_check.csv'``` file will contain the following entry errors:
1. entries that are 'non-fiction' and may or may not be marked as such
2. entries that have already been added (article_ids) that are already in the database (from mappings file)
3. entries in which the article_id is not found in the mappings file (database) but there is a missing updated trove_id. 

Theoretically, if there is not an updated Trove ID and the row is added to the ```'...sheet_to_upload.csv'``` file, this error will be caight at the next stage when the title is processed against the Trove API.

**Some Notes on this Process**
Some of the sheets could not be processed because of incorrect column names. These have been removed from the 'processed_files' (both the 'sheet_to_check.csv' file and 'sheet_to_upload.csv' file) folder as the data formats will not be correct. 
    
These files have also been removed from the 'Updated_Mappings' folder. The sheets that could not be processed are listed in the 'column_not_found.txt' file.
1. Remove problem files from Updated_Mappings folder
2. Remove problem files from processed_files folder (update sheet_to_check.csv and sheet_to_upload.csv)
3. The problem files were manually altered and moved into the folder 'Updated_Mappings_to_Reprocess' , this is located in the 'processed_files' folder. clean_and_check_data.py was run on this folder and the results were moved into the 'done_August_4/processed_files_output' folder. 

This program writes this updated data to a new CSV file in a folder called 'processed_files' in the same directory as the input folder.

#### Additional Code
- **move_files.py**: 
This program processes all the files in a given directory and moves the files that end with the string '_sheet_to_check.csv' to a new directory called 'files_to_check'. 
    
These are located: **.../2023/TBC_Data_Entry/data_cleaning/done_August_4/processed_files_output/files_to_check**

### 3.  check_title_id_query_API.py
This program gets a title record from the readallaboutit api given a title_id. Request a title record for a given title_id and check that the given title string is a perfect match (in either the 'publication_title' or 'common_title'). It returns two csv files:
- 'safe_upload.csv'
- 'not_safe_upload.csv'

**Additional Code to run**
- 1. 'combine_safe_files.py' : this just concatenates all the safe files together into one json file
- 2. 'convert_json.py' : this program ensures that the json file is in the correct format for the API ingest, that is, removing null values and convertin trove_id to integer. 

### Other Additional Code
- **'rename_column.py'**
this program renames the first column of all csv files in a sub-directory as 'article_id' (this was run on sheets produced prior to June 2022). 
- **`exclude_harvested_article_id.py`** this program takes in the results of a given trove harvest and removes all article_ids that have been added to the database or are still in the process of being corrected.
- `remove_chapter_title.py`this program removes the chapter title from the title string and breaks the input csv file into incremented files of 800 entries each.    

