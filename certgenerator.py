import argparse
import os
import uuid

import gspread
import jinja2
import pdfkit
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def parse_arguments():
    parser = argparse.ArgumentParser(description='-t <path_to_template_file> -d <date> -f <folder_id>')
    parser.add_argument('-t', '--template', help='path_to_template_file', required=True)
    parser.add_argument('-d', '--date', help='date', required=True)
    parser.add_argument('-f', '--folder_id', help='folder_id', required=True)

    return parser.parse_args()


def get_google_sheets_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('venv/service_account.json', scope)
    return gspread.authorize(creds)


def get_students_list(sheet):
    students_list = sheet.get_all_values()

    for i, row in enumerate(students_list):
        for j, cell in enumerate(row):
            if j == 0:
                students_list[i] = {'name': cell, 'surname': row[j + 1], 'coordinates': (i + 1, j + 3)}

    return students_list


def generate_certificate(template, student, date):
    context = {
        "student_surname": student.get('surname'),
        "student_name": student.get('name'),
        "date": date,
        "image_folder": os.path.join(os.path.abspath(os.path.dirname(__name__)), 'templates', 'screens'),
        "css_folder": os.path.join(os.path.abspath(os.path.dirname(__name__)), 'templates', 'css'),
    }

    rendered_template = template.render(context)
    file_name = f"certificate-{uuid.uuid4()}"
    options = {
        "enable-local-file-access": None,
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm'
    }
    path = "Certificates/"
    if not os.path.exists(path):
        os.makedirs(path)
    pdfkit.from_string(rendered_template, f"Certificates/{file_name}.pdf", options=options)
    return file_name


def upload_certificate_to_drive(drive, folder_id, file_name):
    file = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file.SetContentFile(f'Certificates/{file_name}.pdf')
    file.Upload()

    permission = file.InsertPermission({
        'type': 'anyone',
        'value': None,
        'role': 'reader',
        'withLink': True
    })

    return file['alternateLink']


def update_google_sheet(sheet, student, link):
    sheet.update_cell(student.get('coordinates')[0], student.get('coordinates')[1], link)


def main():
    args = parse_arguments()

    # Authenticate Google API
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Get Google Sheets client
    sheets_client = get_google_sheets_client()

    # Get template
    with open(args.template, 'r') as f:
        template_string = f.read()

    template = jinja2.Template(template_string)

    # Open spreadsheet
    sheet = sheets_client.open('Students').sheet1

    # Get students list
    students_list = get_students_list(sheet)

    date = args.date

    # Generate and upload certificates
    for student in students_list:
        file_name = generate_certificate(template, student, date)
        link = upload_certificate_to_drive(drive, args.folder_id, file_name)
        update_google_sheet(sheet, student, link)

    print('Certificates generation and upload to Google Drive completed successfully!')


if __name__ == '__main__':
    main()
