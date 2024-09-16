import os
import qrcode
import zipfile

def generate_qr_codes(pdf_folder, isbn, box_size=10, border=4, quality=qrcode.constants.ERROR_CORRECT_L):
    # List all PDF files in the specified folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    # Create output directory for QR codes
    output_folder = 'qr'
    os.makedirs(output_folder, exist_ok=True)

    # List to keep track of QR code filenames
    qr_filenames = []

    # Iterate through each PDF file
    for pdf_file in pdf_files:
        # Extract 'contenuto' from the filename (without the '.pdf' extension)
        contenuto = os.path.splitext(pdf_file)[0]

        # Build the URL
        url = f"https://contenuti.edises.it/?isbn={isbn}&contenuto={contenuto}&tipo=pdf"

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=quality, box_size=box_size, border=border)
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image with a name based on the 'contenuto'
        qr_filename = os.path.join(output_folder, f"{contenuto}.png")
        img.save(qr_filename)
        qr_filenames.append(qr_filename)

        print(f"QR code generated for {url} and saved as {qr_filename}")

    # Zip all the QR code images into a single zip file within the 'qr' directory
    zip_filename = os.path.join(output_folder, 'qr_codes.zip')
    with zipfile.ZipFile(zip_filename, 'w') as qr_zip:
        for qr_file in qr_filenames:
            # Add the QR code image to the ZIP file
            qr_zip.write(qr_file, arcname=os.path.basename(qr_file))

    # Remove the individual QR code image files, leaving only the ZIP file
    for qr_file in qr_filenames:
        os.remove(qr_file)

    print(f"All QR codes have been zipped into {zip_filename} and individual QR code images have been removed.")

if __name__ == "__main__":
    isbn = input("Please enter the ISBN number: ")
    pdf_folder = 'pdf'  # Ensure this folder exists and contains your PDF files
    generate_qr_codes(pdf_folder, isbn)
