import os
from tqdm import tqdm
from helpers import file_name
import jellyfish

# Settings
folder = "alfabe"
max_distance = 2


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
    # Filter other words that are too long out for performance
    word_length = len(word)
    other_words = [other_word.strip() for other_word in other_words if abs(len(other_word)-word_length) <= max_distance]

    # Calculate word similarities (and keep only the ones similar enough)
    other_words = [(other_word, jellyfish.levenshtein_distance(other_word, word)) for other_word in other_words]
    
    # Only keep the similar enough words
    other_words = [(other_word, similarity) for (other_word, similarity) in other_words if similarity <= max_distance]

    # Sort them by similarity
    other_words.sort(key=lambda tup: tup[1])

    # Keep only the words
    other_words = [other_word for (other_word, _) in other_words]

    # Write
    out.write(word)
    out.write(" --> ")
    out.write(", ".join(other_words))
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
            word = word.strip()
            compare(word, other_words, out)
