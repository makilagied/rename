import os
import shutil

class FileRenamerMover:
    def __init__(self, file_mapping, source_directory, additional_info):
        """
        Initialize the FileRenamerMover with the necessary parameters.
        
        :param file_mapping: A dictionary where keys are old file names and values are new file names (with placeholders for additional info).
        :param source_directory: Path to the directory containing the files.
        :param additional_info: Dictionary containing variables to be used in the new file names.
        """
        self.file_mapping = file_mapping
        self.source_directory = source_directory
        self.additional_info = additional_info
        self.username = self.get_logged_in_username()
        self.base_destination_directory = os.path.join('C:\\Users', self.username, 'OneDrive - iTrust Finance Limited', 'itrust')
        self.finance_folder = os.path.join(self.base_destination_directory, 'FINANCE')
        self.credit_folder = os.path.join(self.base_destination_directory, 'CREDIT')
        self.investment_folder = os.path.join(self.base_destination_directory, 'INVESTMENT')

    def get_logged_in_username(self):
        """
        Get the username of the currently logged-in user on Windows.

        :return: Username of the logged-in user.
        """
        return os.getlogin()

    def determine_destination_folder(self, new_name):
        """
        Determine the destination folder based on the new file name.
        
        :param new_name: The new name of the file.
        :return: The path to the destination folder.
        """
        if new_name.startswith('P&L_CONSOLIDATED_'):
            suffix = new_name.split('_')[2]
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'P&L', suffix)
        elif new_name.startswith('SKUK_Report_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'SUKUK')
        elif new_name.startswith('Daily Investment Report_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'INVESTMENT FUND REPORT')
        elif new_name.startswith('FUND CUSTOMER BALANCE_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'FUND CUSTOMER BALANCE')
        elif new_name.startswith('Data Entry Report_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'DATA ENTRY')
        elif new_name.startswith('Balancesheet_consolidated_'):
            suffix = new_name.split('_')[2]
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'BALANCESHEET', suffix)
        elif new_name.startswith('CUSTOMER BALANCE_'):
            return os.path.join(self.credit_folder, '2024', 'JUNE', 'CUSTOMER BALANCE')
        elif new_name.startswith('Bot_Loan_status_'):
            return os.path.join(self.credit_folder, '2024', 'JUNE', 'BOT LOAN STATUS')
        else:
            return os.path.join(self.investment_folder, '2024', 'JUNE')

    def rename_and_move_files(self):
        """
        Rename specific .xlsx files based on a given mapping and move them to a specified folder if they exist in the directory.
        """
        # Iterate over the mapping dictionary
        for old_name, new_name_template in self.file_mapping.items():
            # Construct full file paths
            old_file = os.path.join(self.source_directory, old_name)
            # Format the new file name with additional info
            new_name = new_name_template.format(**self.additional_info)
            new_file = os.path.join(self.source_directory, new_name)
            
            # Check if the old file exists
            if os.path.exists(old_file):
                try:
                    # Rename the file
                    os.rename(old_file, new_file)
                    print(f'Renamed: {old_file} -> {new_file}')
                    
                    # Determine the destination folder
                    destination_folder = self.determine_destination_folder(new_name)
                    # Construct the full destination path
                    destination_path = os.path.join(destination_folder, new_name)
                    
                    # Create the destination directory if it doesn't exist
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    
                    # Move the file to the destination folder
                    shutil.move(new_file, destination_path)
                    print(f'Moved: {new_file} -> {destination_path}')
                except Exception as e:
                    print(f'Error renaming or moving {old_file} to {new_file}: {e}')
            else:
                print(f'File not found: {old_file}')

# Example usage
if __name__ == "__main__":
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
    }

    # Define variables to be used in the new file names
    additional_info = {
        'RPTDATE': '14Jun2030',
        'SYSDATE': 'sysdate14Jun2030',
        # Add more variables as needed
    }

    # Get the path to the user's Downloads directory
    downloads_directory = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Create an instance of the FileRenamerMover class and rename and move the files
    renamer_mover = FileRenamerMover(file_mapping, downloads_directory, additional_info)
    renamer_mover.rename_and_move_files()
