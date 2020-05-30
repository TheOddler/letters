import os
from tqdm import tqdm
from helpers import file_name
from collections import defaultdict
import jellyfish

# Settings
folder = "alfabe"
max_distance = 4


# Get all the letter files
letter_files = []
for root, dirs, files in os.walk("alfabe/vowels", topdown=False):
    for name in files:
        letter_files.append(os.path.join(root, name))

# Sort them because then I can print and they are alphabetically
letter_files.sort(key=file_name)

# Make sure the output folder exists
out_path = "out"
if not os.path.exists(out_path):
    os.makedirs(out_path)

# The function that compares the words
def compare(word, other_words, out):
    # Clean the word
    word = word.strip()

    # Helper value
    word_length = len(word)
    
    # Group the other words on distance
    distance_groups = defaultdict(list)
    for other_word in other_words:
        other_word = other_word.strip()

        # Remove words too diffent in length, faster than calculating the levenstein distance, so should improve performance
        len_diff = abs(len(other_word) - word_length)
        if len_diff > max_distance: continue

        # Only keep the similar enough words
        distance = jellyfish.levenshtein_distance(other_word, word)
        if distance > max_distance: continue

        # Group the words we keep
        distance_groups[distance].append(other_word)

    # Write
    out.write(word)
    out.write(" -->\n")
    for distance, words in sorted(distance_groups.items(), key=lambda i: i[0]):
        out.write("\t")
        out.write(str(distance))
        out.write(": ")
        out.write(", ".join(words))
        out.write("\n")


# Do the actual calculation
for f in letter_files:
    letter = file_name(f)
    words = open(f, "r").readlines()

    def other_filter(fn): return file_name(fn) != letter
    other_letter_files = filter(other_filter, letter_files)
    for f in other_letter_files:
        other_letter = file_name(f)
        other_words = open(f, "r").readlines()

        print(f"{letter}-{other_letter}")

        out = open(f"{out_path}/{letter}-{other_letter}.txt", "w")

        for word in tqdm(words):
            compare(word, other_words, out)
