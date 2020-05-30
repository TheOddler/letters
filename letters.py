import os
from tqdm import tqdm
from helpers import file_name
from collections import defaultdict
import jellyfish
from multiprocessing import Pool, cpu_count
from functools import partial

# Settings
vowels_folder = "alfabe/vowels"
consonant_folder = "alfabe/consonant"
max_distance = 4
out_path = "out"


# Make sure the output folder exists
if not os.path.exists(out_path):
    os.makedirs(out_path)


# The function that compares the words
def process_word(word, other_words):
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
    
    return word, distance_groups


def write_info(word, distance_groups, out):
    out.write(word)
    out.write(" -->\n")
    for distance, words in sorted(distance_groups.items(), key=lambda i: i[0]):
        out.write("\t")
        out.write(str(distance))
        out.write(": ")
        out.write(", ".join(words))
        out.write("\n")





def process_files(letter_files):
    for letter_file in letter_files:
        letter = file_name(letter_file)
        words = open(letter_file, "r").readlines()
        words_count = len(words)

        def other_filter(fn): return file_name(fn) != letter
        other_letter_files = filter(other_filter, letter_files)
        for other_letter_file in other_letter_files:
            other_letter = file_name(other_letter_file)
            other_words = open(other_letter_file, "r").readlines()

            label = f"{letter}-{other_letter}"
            out = open(f"{out_path}/{label}.txt", "w")

            with Pool(cpu_count() - 1) as pool:
                infos = tqdm(pool.imap(partial(process_word, other_words=other_words), words), total=words_count, desc=label)

                for (word, distance_groups) in tqdm(infos, desc="Writing"):
                    write_info(word, distance_groups, out)


def process_folder(folder_path):
    # Get all the letter files
    letter_files = []
    for root, _, files in os.walk(folder_path, topdown=False):
        for name in files:
            letter_files.append(os.path.join(root, name))

    # Sort them because then I can print and they are alphabetically
    letter_files.sort(key=file_name)

    # Process the files
    process_files(letter_files)


process_folder(vowels_folder)
process_folder(consonant_folder)
