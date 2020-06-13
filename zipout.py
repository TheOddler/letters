import os
from helpers import file_name
from collections import defaultdict
from zipfile import ZipFile, ZIP_BZIP2
from tqdm import tqdm

out_path = "out"

out_files = []
for root, _, files in os.walk(out_path, topdown=False):
    for name in files:
        out_files.append(os.path.join(root, name))

groups = defaultdict(list)
for out_file in out_files:
    name = file_name(out_file)
    first_letter = name[0] # I assume the file name has a structure of letter-letter
    groups[first_letter].append(out_file)

for first_letter, files in tqdm(groups.items(), desc="All"):
    with ZipFile(f'{first_letter}.zip', 'w', ZIP_BZIP2) as zipObj:
        for file_path in tqdm(files, desc=first_letter):
            # Add file to zip
            zipObj.write(file_path)
