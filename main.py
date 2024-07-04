import os
import csv
from PIL import Image
from collections import defaultdict

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        image.verify()  # Verify that it is, in fact, an image
        image = Image.open(image_path)
        exif = image._getexif()
        if not exif:
            return None, None
        exif_date = exif.get(36867)  # DateTimeOriginal tag
        return exif_date, os.path.getsize(image_path) / (1024 * 1024)  # File size in MB
    except Exception as e:
        return None, None

def find_duplicates(root_dir):
    files_by_name = defaultdict(list)

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            files_by_name[file].append(file_path)

    duplicates = {k: v for k, v in files_by_name.items() if len(v) > 1}
    return duplicates

def save_duplicates_to_csv(duplicates, root_dir):
    batch_size = 50
    file_index = 1
    count = 0

    csvfile = open(f'output_{file_index}.csv', 'w', newline='')
    fieldnames = ['FileName', 'RelativePath', 'Path1', 'Path2', 'DateTaken', 'FileSizeMB']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for filename, paths in duplicates.items():
        if len(paths) < 2:
            continue

        for i in range(len(paths) - 1):
            relative_path = os.path.relpath(os.path.commonpath([paths[i], paths[i + 1]]), start=root_dir)
            date_taken, file_size = get_exif_data(paths[i])
            row = {
                'FileName': filename,
                'RelativePath': relative_path,
                'Path1': paths[i],
                'Path2': paths[i + 1],
                'DateTaken': date_taken if date_taken else 'N/A',
                'FileSizeMB': file_size if file_size else 'N/A'
            }
            writer.writerow(row)
            count += 1

            if count % batch_size == 0:
                csvfile.flush()
                csvfile.close()
                file_index += 1
                csvfile = open(f'output_{file_index}.csv', 'w', newline='')
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    if count % batch_size != 0:
        csvfile.flush()
        csvfile.close()

def main(root_dir):
    duplicates = find_duplicates(root_dir)
    save_duplicates_to_csv(duplicates, root_dir)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <root_directory>")
        sys.exit(1)
    root_directory = sys.argv[1]
    main(root_directory)
