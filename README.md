## Certificate Generator

<!---Пример кода-->

This is a simple script that generates certificates of completion based on a given template for each student in a `Google Sheets` spreadsheet. The generated certificates are then uploaded to `Google Drive` and their links are added to the spreadsheet.

### Installation
1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Set up the necessary authentication files:
   * Create a `env` directory in the project root.
   * Download the service account JSON file and save it as `service_account.json` in the `env` directory.
   * Download the `client_secrets.json` file for Google Drive API authentication and save it in the `env` directory.
4. Set up the `Google Sheets` document:
   * Create a new `Google Sheets` document.
   * Add a sheet to the document.
   * In the first row of the sheet, add the following column headers: `Name`, `Surname`, `Certificate Link`, and `Referer`.
5. Customize the certificate template:
   * Create a new HTML file in the `templates` directory.
   * Use Jinja2 templating syntax to customize the certificate template.
6. Update the `folder_id` in the `upload_certificate_to_drive` function to match the ID of the folder in your Google Drive where you want the generated certificates to be uploaded.
### Usage
#### To run the script, execute the following command:
>bash
```
python certificate_generator.py -t <path_to_template_file> -r <referer> -d <date>
```
Where `<path_to_template_file>` is the path to the HTML file containing the certificate template, and `<referer>` is the name of the person or organization issuing the certificates.

The script will generate a certificate for each student in the `Google Sheets` document, upload the certificate to `Google Drive`, and add the link to the `Certificate Link` column of the corresponding row in the spreadsheet. The Referer column will also be updated with the name of the person or organization issuing the certificates.

### License
This project is licensed under the terms of the MIT license.
