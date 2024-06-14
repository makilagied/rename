import os

def rename_specific_xlsx_files(file_mapping, directory, additional_info):
    """
    Rename specific .xlsx files based on a given mapping if they exist in the directory.
    Allows incorporating additional info into the new file names.

    :param file_mapping: A dictionary where keys are old file names and values are new file names (with placeholders for additional info).
    :param directory: Path to the directory containing the files.
    :param additional_info: Dictionary containing variables to be used in the new file names.
    """
    # Iterate over the mapping dictionary
    for old_name, new_name_template in file_mapping.items():
        # Construct full file paths
        old_file = os.path.join(directory, old_name)
        # Format the new file name with additional info
        new_name = new_name_template.format(**additional_info)
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
    'old_file1.xlsx': 'new_file1_{sysdate}_{rptdate}.xlsx',
    'old_file2.xlsx': 'new_file2_{sysdate}_{rptdate}.xlsx',
    'old_file3.xlsx': 'new_file3_{sysdate}_{rptdate}.xlsx',
    # Add more mappings as needed
}

# Define variables to be used in the new file names
additional_info = {
    'sysdate': 'sysdate13',
    'rptdate': 'rptdate13',
    # Add more variables as needed
}

# Get the path to the user's Downloads directory
downloads_directory = os.path.join(os.path.expanduser('~'), 'Downloads')

# Rename the files according to the mapping and additional info
rename_specific_xlsx_files(file_mapping, downloads_directory, additional_info)
