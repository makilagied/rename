import os
import shutil

def rename_and_move_files(file_mapping, source_directory, additional_info, destination_directory):
    """
    Rename specific .xlsx files based on a given mapping and move them to a specified folder if they exist in the directory.
    Allows incorporating additional info into the new file names.

    :param file_mapping: A dictionary where keys are old file names and values are new file names (with placeholders for additional info).
    :param source_directory: Path to the directory containing the files.
    :param additional_info: Dictionary containing variables to be used in the new file names.
    :param destination_directory: Path to the destination directory where files should be moved.
    """
    # Iterate over the mapping dictionary
    for old_name, new_name_template in file_mapping.items():
        # Construct full file paths
        old_file = os.path.join(source_directory, old_name)
        # Format the new file name with additional info
        new_name = new_name_template.format(**additional_info)
        new_file = os.path.join(source_directory, new_name)
        
        # Check if the old file exists
        if os.path.exists(old_file):
            try:
                # Rename the file
                os.rename(old_file, new_file)
                print(f'Renamed: {old_file} -> {new_file}')
                
                # Construct the full destination path
                destination_path = os.path.join(destination_directory, new_name)
                # Move the file to the destination folder
                shutil.move(new_file, destination_path)
                print(f'Moved: {new_file} -> {destination_path}')
            except Exception as e:
                print(f'Error renaming or moving {old_file} to {new_file}: {e}')
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
    'sysdate': '2024-06-13',
    'rptdate': '2024-06-13',
    # Add more variables as needed
}

# Get the path to the user's Downloads directory
downloads_directory = os.path.join(os.path.expanduser('~'), 'Downloads')

# Define the destination directory
destination_directory = r'C:\Users\erick.makilagi\OneDrive - iTrust Finance Limited\itrust'

# Rename and move the files according to the mappings and additional info
rename_and_move_files(file_mapping, downloads_directory, additional_info, destination_directory)
