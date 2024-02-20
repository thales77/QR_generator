import pandas as pd
import qrcode

def generate_qr_codes(csv_file, delimiter=';', box_size=10, border=4, quality=qrcode.constants.ERROR_CORRECT_L):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file, delimiter=delimiter)

    # Iterate through each row
    for index, row in df.iterrows():
        url = row['url']
        filename = row['qr_filename']

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=quality, box_size=box_size, border=border)
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        img.save(filename + ".png")

        print(f"QR code generated for {url} and saved as {filename}.png")

if __name__ == "__main__":
    csv_file = "qr.csv"
    generate_qr_codes(csv_file, delimiter=';')