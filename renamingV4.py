import os
import shutil

def get_logged_in_username():
    """
    Get the username of the currently logged-in user on Windows.

    :return: Username of the logged-in user.
    """
    return os.getlogin()

def rename_and_move_files(file_mapping, source_directory, additional_info):
    """
    Rename specific .xlsx files based on a given mapping and move them to a specified folder if they exist in the directory.
    Allows incorporating additional info into the new file names.

    :param file_mapping: A dictionary where keys are old file names and values are new file names (with placeholders for additional info).
    :param source_directory: Path to the directory containing the files.
    :param additional_info: Dictionary containing variables to be used in the new file names.
    """
    # Get the current logged-in username
    username = get_logged_in_username()
    
    # Construct the destination directory path
    destination_directory = os.path.join('C:\\Users', username, 'OneDrive - iTrust Finance Limited', 'itrust')
    
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
    'Profit N Loss 006_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_006_{RPTDATE}{SYSDATE}.xlsx',
    'Profit N Loss 005_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_005_{RPTDATE}{SYSDATE}.xlsx',
    'Profit N Loss 004_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_004_{RPTDATE}{SYSDATE}.xlsx',
    'Profit N Loss 003_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_003_{RPTDATE}{SYSDATE}.xlsx',
    'Profit N Loss 002_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_002_{RPTDATE}{SYSDATE}.xlsx',
    'Profit N Loss 001_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_001_{RPTDATE}{SYSDATE}.xlsx',
    'Loan Report Swalha_Loan Report Swalha Layout.xlsx': 'Loan Report Swalha_{RPTDATE}{SYSDATE}.xlsx',
    'FUND CUSTOMER BALANCE_Reports.xlsx': 'FUND CUSTOMER BALANCE_{RPTDATE}{SYSDATE}.xlsx',
    'Daily Investment Report_Loan Report Swalha Layout.xlsx': 'Daily Investment Report_{RPTDATE}{SYSDATE}.xlsx',
    'Balancesheet_006_Reports.xlsx': 'Balancesheet_consolidated_006_{RPTDATE}{SYSDATE}.xlsx',
    'Balancesheet_005_Reports.xlsx': 'Balancesheet_consolidated_005_{RPTDATE}{SYSDATE}.xlsx',
    'Balancesheet_004_Reports.xlsx': 'Balancesheet_consolidated_004_{RPTDATE}{SYSDATE}.xlsx',
    'Balancesheet_003_Reports.xlsx': 'Balancesheet_consolidated_003_{RPTDATE}{SYSDATE}.xlsx',
    'Balancesheet_002_Reports.xlsx': 'Balancesheet_consolidated_002_{RPTDATE}{SYSDATE}.xlsx',
    'Balancesheet_001_Reports.xlsx': 'Balancesheet_consolidated_001_{RPTDATE}{SYSDATE}.xlsx',
    'SKUK_Reports.xlsx': 'SKUK_Report_{RPTDATE}{SYSDATE}.xlsx',
    'PL_CONSOLIDATED_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_000_{RPTDATE}{SYSDATE}.xlsx',
    'CUSTOMER BALANCE_Reports.xlsx': 'CUSTOMER BALANCE_{RPTDATE}{SYSDATE}.xlsx',
    'Bot_Loan_status_Bot_loan_status.xls': 'Bot_Loan_status_{RPTDATE}{SYSDATE}.xls',
    'Balancesheet_consolidated_new_Reports.xlsx': 'Balancesheet_consolidated_000_{RPTDATE}{SYSDATE}.xlsx',
    'Data Entry Report_Data Entry_Layout.xlsx': 'Data Entry Report_{RPTDATE}{SYSDATE}.xlsx',
     # Add more mappings as needed
}

# Define variables to be used in the new file names
additional_info = {
    'RPTDATE': '13Jun2024',
    'SYSDATE': 'sysdate13Jun2024',
    # Add more variables as needed
}

# Get the path to the user's Downloads directory
downloads_directory = os.path.join(os.path.expanduser('~'), 'Downloads')

# Rename and move the files according to the mappings and additional info
rename_and_move_files(file_mapping, downloads_directory, additional_info)