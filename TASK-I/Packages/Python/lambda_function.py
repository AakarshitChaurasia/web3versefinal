import os
import boto3
import comtypes

s3 = boto3.client('s3')

def docx_to_pdf(file_path):
    # Create COM object
    word = comtypes.client.CreateObject('Word.Application')
    # Set visible to False to avoid opening Word window
    word.Visible = False
    # Open the document
    doc = word.Documents.Open(file_path)
    # Get the PDF format constant value
    wdFormatPDF = 17
    # Change the extension of the file name
    pdf_path = os.path.splitext(file_path)[0] + '.pdf'
    # Save the file in PDF format
    doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
    # Close the document and the Word application
    doc.Close()
    word.Quit()

def lambda_handler(event, context):
    # Get the uploaded file from the request
    file_content = event['body']
    file_name = event['file_name']

    # Validate file type and size
    if not file_name.endswith('.docx'):
        return {'statusCode': 400, 'body': 'Invalid file type'}

    if len(file_content) > (5 * 1024 * 1024):
        return {'statusCode': 400, 'body': 'File too large'}

    # Save the file locally
    with open('/tmp/' + file_name, 'wb') as f:
        f.write(file_content)

    # Convert the file to PDF
    docx_to_pdf('/tmp/' + file_name)

    # Read the contents of the generated PDF file
    with open('/tmp/' + os.path.splitext(file_name)[0] + '.pdf', 'rb') as f:
        pdf_file_content = f.read()

    # Upload the PDF file to S3
    s3.put_object(Bucket=os.environ['BUCKET_NAME'], Key=file_name + '.pdf', Body=pdf_file_content)

    return {'statusCode': 200, 'body': 'Conversion successful'}
