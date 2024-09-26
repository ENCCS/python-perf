# pythran export update_word_counts(str, str:int dict)
def update_word_counts(line, counts):
    """
    Given a string, parse the string and update a dictionary of word
    counts (mapping words to counts of their frequencies). DELIMITERS are
    removed before the string is parsed. The function is case-insensitive
    and words in the dictionary are in lower-case.
    """
    DELIMITERS = '. , ; : ? $ @ ^ < > # % ` ! * - = ( ) [ ] { } / " \''.split()
    for purge in DELIMITERS:
        line = line.replace(purge, ' ')
    words = line.split()
    for word in words:
        word = word.lower().strip()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


# pythran export calculate_word_counts(str list)
def calculate_word_counts(lines):
    """
    Given a list of strings, parse each string and create a dictionary of
    word counts (mapping words to counts of their frequencies). DELIMITERS
    are removed before the string is parsed. The function is
    case-insensitive and words in the dictionary are in lower-case.
    """
    counts = {}
    for line in lines:
        counts = update_word_counts(line, counts)
    return counts