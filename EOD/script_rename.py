from flask import Flask, request, jsonify, render_template
import os
import shutil
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xls', 'xlsx'}

def allowed_file(filename):
    """
    Check if the uploaded file is allowed based on its extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def format_date(date_str):
    """
    Convert a date string from YYYY-MM-DD format to DDMonYYYY format.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%d%b%Y')

class FileRenamerMover:
    def __init__(self, file_mapping, additional_info):
        """
        Initialize the FileRenamerMover with file mapping, additional information, 
        and destination directories based on the logged-in user.
        """
        self.file_mapping = file_mapping
        self.additional_info = additional_info
        self.username = self.get_logged_in_username()
        self.base_destination_directory = os.path.join('C:\\Users', self.username, 'OneDrive - iTrust Finance Limited', 'itrust')
        self.finance_folder = os.path.join(self.base_destination_directory, 'FINANCE')
        self.credit_folder = os.path.join(self.base_destination_directory, 'CREDIT')
        self.investment_folder = os.path.join(self.base_destination_directory, 'INVESTMENT')

    def get_logged_in_username(self):
        """
        Retrieve the username of the currently logged-in user.
        """
        return os.getlogin()

    def determine_destination_folder(self, new_name):
        """
        Determine the appropriate destination folder for a renamed file based on its new name.
        """
        if new_name.startswith('P&L_CONSOLIDATED_'):
            suffix = new_name.split('_')[2]
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'P&L', suffix)
        elif new_name.startswith('SKUK_Report_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'SUKUK')
        elif new_name.startswith('Daily Investment Report_'):
            return os.path.join(self.investment_folder, '2024', 'JUNE')
        elif new_name.startswith('FUND CUSTOMER BALANCE_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'FUND CUSTOMER BALANCE')
        elif new_name.startswith('Data Entry Report_'):
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'DATA ENTRY')
        elif new_name.startswith('Balancesheet_consolidated_'):
            suffix = new_name.split('_')[2]
            return os.path.join(self.finance_folder, '2024', 'JUNE', 'BALANCE SHEET', suffix)
        elif new_name.startswith('CUSTOMER BALANCE_'):
            return os.path.join(self.credit_folder, '2024', 'JUNE', 'CUSTOMER BALANCE')
        elif new_name.startswith('Bot_Loan_status_'):
            return os.path.join(self.credit_folder, '2024', 'JUNE', 'BOT LOAN STATUS')
        elif new_name.startswith('Loan Report Swalha_'):
            return os.path.join(self.credit_folder, '2024', 'JUNE', 'BOT LOAN STATUS')
        else:
            return os.path.join(self.base_destination_directory)

    def rename_and_move_files(self, uploaded_files):
        """
        Rename and move uploaded files to their appropriate destination folders based on the mapping.
        """
        results = []
        for uploaded_file in uploaded_files:
            old_name = uploaded_file.filename
            if old_name in self.file_mapping:
                new_name_template = self.file_mapping[old_name]
                new_name = new_name_template.format(**self.additional_info)
                new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)

                try:
                    uploaded_file.save(new_file_path)
                    destination_folder = self.determine_destination_folder(new_name)
                    destination_path = os.path.join(destination_folder, new_name)
                    
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)

                    shutil.move(new_file_path, destination_path)
                    results.append({'old': old_name, 'new': new_name, 'moved_to': destination_path})
                except Exception as e:
                    results.append({'error': str(e), 'file': old_name})
            else:
                results.append({'error': 'File not found in mapping', 'file': old_name})
        return results

@app.route('/')
def index():
    """
    Render the index HTML template for file uploading.
    """
    return render_template('index.html')

@app.route('/process_files', methods=['POST'])
def process_files():
    """
    Process uploaded files: rename and move them based on the provided RPTDATE and SYSDATE.
    """
    rpt_date_raw = request.form['rptdate']
    sys_date_raw = request.form['sysdate']

    rpt_date = format_date(rpt_date_raw)
    sys_date = format_date(sys_date_raw)
    
    uploaded_files = request.files.getlist('files')

    if not all(allowed_file(file.filename) for file in uploaded_files):
        return jsonify({'error': 'Only .xls and .xlsx files are allowed'}), 400

    file_mapping = {
        'Profit N Loss 006_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_006_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Profit N Loss 005_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_005_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Profit N Loss 004_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_004_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Profit N Loss 003_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_003_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Profit N Loss 002_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_002_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Profit N Loss 001_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_001_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Loan Report Swalha_Loan Report Swalha Layout.xlsx': 'Loan Report Swalha_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'FUND CUSTOMER BALANCE_Reports.xlsx': 'FUND CUSTOMER BALANCE_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Daily Investment Report_Loan Report Swalha Layout.xlsx': 'Daily Investment Report_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Balancesheet_006_Reports.xlsx': 'Balancesheet_consolidated_006_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Balancesheet_005_Reports.xlsx': 'Balancesheet_consolidated_005_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Balancesheet_004_Reports.xlsx': 'Balancesheet_consolidated_004_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Balancesheet_003_Reports.xlsx': 'Balancesheet_consolidated_003_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Balancesheet_002_Reports.xlsx': 'Balancesheet_consolidated_002_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Balancesheet_001_Reports.xlsx': 'Balancesheet_consolidated_001_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'SKUK_Reports.xlsx': 'SKUK_Report_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'PL_CONSOLIDATED_PL_CONSOLIDATED.xlsx': 'P&L_CONSOLIDATED_000_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'CUSTOMER BALANCE_Reports.xlsx': 'CUSTOMER BALANCE_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Bot_Loan_status_Bot_loan_status.xls': 'Bot_Loan_status_{RPTDATE}sysdate{SYSDATE}.xls',
        'Balancesheet_consolidated_new_Reports.xlsx': 'Balancesheet_consolidated_000_{RPTDATE}sysdate{SYSDATE}.xlsx',
        'Data Entry Report_Data Entry_Layout.xlsx': 'Data Entry Report_{RPTDATE}sysdate{SYSDATE}.xlsx',
    }

    additional_info = {
        'RPTDATE': rpt_date,
        'SYSDATE': sys_date,
    }

    renamer_mover = FileRenamerMover(file_mapping, additional_info)
    result = renamer_mover.rename_and_move_files(uploaded_files)
    
    return jsonify(result)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', debug=True)
