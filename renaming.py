import os

def rename_specific_xlsx_files(file_mapping, directory):
    """
    Rename specific .xlsx files based on a given mapping if they exist in the directory.

    :param file_mapping: A dictionary where keys are old file names and values are new file names.
    :param directory: Path to the directory containing the files.
    """
    # Iterate over the mapping dictionary
    for old_name, new_name in file_mapping.items():
        # Construct full file paths
        old_file = os.path.join(directory, old_name)
        new_file = os.path.join(directory, new_name)
        
        # Check if the old file exists
        if os.path.exists(old_file):
            try:
                # Rename the file
                os.rename(old_file, new_file)
                print(f'Renamed: {old_file} -> {new_file}')
            except Exception as e:
                print(f'Error renaming {old_file} to {new_file}: {e}')
        else:
            print(f'File not found: {old_file}')

# Example usage
file_mapping = {
    'PL_CONSOLIDATED_PL_CONSOLIDATED (2).xlsx': 'were.xlsx',
    'Data Entry Report_Data Entry_Layout.xlsx': 'new_file2.xlsx',
    'Balancesheet_consolidated_new_Reports (2).xlsx': 'new_file3.xlsx',
    # Add more mappings as needed
}

# Get the path to the user's Downloads directory
downloads_directory = os.path.join(os.path.expanduser('~'), 'Downloads')

# Rename the files according to the mapping
rename_specific_xlsx_files(file_mapping, downloads_directory)
