# Find similar words

This program looks for similar words given lists of words.

Each list contains words with a specific sound/letter.
Similar words (a.k.a. minimal pairs in linguistics terms) can be used in speech-language therapy when clients need to learn how to differentiate two sounds.
Moreover, these lists of similar words might come in handy in research as well.
For example, educational research might use these for a spelling task or lingusitc research might use these in a speech production task.

# Usage

Simply run `py letter.py` (or `python3 letter.py`)

# Requirements

* Python 3
* tqmd: `pip install tqdm` (used for the progress bar)
* jellyfish: `pip install jellyfish` (used to calculate the levenshtein distance between words)

# References

Word lists from: https://kelimeler.net/
