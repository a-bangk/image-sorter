import os
import csv
import sys
from collections import defaultdict
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        info = image._getexif()
        if info is not None:
            exif_data = {TAGS.get(tag): value for tag, value in info.items() if tag in TAGS}
            if 'DateTimeOriginal' in exif_data:
                return exif_data['DateTimeOriginal']
    except Exception as e:
        print(f"Error getting EXIF data for {image_path}: {e}")
    return None

def get_image_info(root_dir):
    file_dict = defaultdict(list)
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png', 'tiff', 'bmp', 'gif')):
                full_path = os.path.join(root, file)
                file_size = os.path.getsize(full_path)
                date_taken = get_exif_data(full_path)
                file_dict[file].append((full_path, date_taken, file_size))
    return file_dict

def write_to_csv(file_dict, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['File Name', 'Full Path', 'Date Taken', 'File Size'])
        for file_name, file_info_list in file_dict.items():
            for file_info in file_info_list:
                csv_writer.writerow([file_name, file_info[0], file_info[1], file_info[2]])

def main(root_dir):
    output_csv = 'output.csv'
    file_dict = get_image_info(root_dir)
    write_to_csv(file_dict, output_csv)
    print(f"CSV file has been created at {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <directory_path>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"The provided path '{root_dir}' is not a valid directory.")
        sys.exit(1)
    
    main(root_dir)

