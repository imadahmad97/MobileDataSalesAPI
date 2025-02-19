import csv
import base64


# Example usage
file_path = r"C:\Users\t767284\Documents\repos\MobileDataSalesAPI\appdata\bulk_upload_data\bulk_upload_data.csv"  # Replace with your actual CSV file path
decoded_data = parse_csv_to_dicts(file_path)
print(decoded_data)
