#!/usr/bin/env python
import re

DIRECTIONS = {'N': (0, 1), 'NE': (1, -1), 'E': (1, 0),
              'SE': (1, 1), 'S': (0, 1), 'SW': (-1, 1),
              'W': (-1, 0), 'NW': (-1, -1)}
    
MAX_ROW = 4
MAX_COLUMN = 4
SMALL_WORD_LOOKUP_MAX = 5


def slurp(file):
    data = []
    with open(file) as f:
        for line in f:
            data.append(line.rstrip())
    return data


def load_word_list():
    return slurp("WORD.LST")


def load_prefix_index():
    return {x:int(y) for x, y in [x.split(" ") for x in slurp("prefix.idx")]}


def move(pos, direction):
    x, y = pos
    incx, inxy = DIRECTIONS[direction]
    return (x + incx, inxy + y)


def get(ruzzle, pos):
    x, y = pos
    return ruzzle[y][x]


def in_range(pos):
    x, y = pos
    return 0 <= x < MAX_COLUMN and 0 <= y < MAX_ROW


def get_prefix_words(word, word_list, prefix_index):
    prefix = word[:SMALL_WORD_LOOKUP_MAX]
    lookup = {}
    if prefix in prefix_index:
        line_number = prefix_index[prefix]
        while (line_number < len(word_list)):
            current_word = word_list[line_number]
            if re.search("^" + prefix + "*", current_word):
                lookup[current_word] = 0
            else:
                return lookup
            line_number = line_number + 1
    else:
        return lookup
    

def find_words(start_pos, ruzzle, history, s, result=None, complete_word_list=[], small_word_lookup={}, prefix_index_lookup={}):
    if 1 < len(s) <= SMALL_WORD_LOOKUP_MAX:
        if s in small_word_lookup:
            result.append(s)
    elif len(s) > SMALL_WORD_LOOKUP_MAX:
        prefix_word_list = get_prefix_words(s, complete_word_list, prefix_index_lookup)
        if s in prefix_word_list:
            result.append(s)
        else:
            return result

    for direction in DIRECTIONS:
        new_pos = move(start_pos, direction)
        if in_range(new_pos) and not new_pos in history:
            result = find_words(new_pos, 
                                ruzzle, history[:] + [new_pos], 
                                s + get(ruzzle, new_pos), 
                                result=result,
                                small_word_lookup=small_word_lookup,
                                complete_word_list=complete_word_list,
                                prefix_index_lookup=prefix_index_lookup)

    return result


def unique_result(result_list, unique=[], history={}):
    for element in result_list:
        if type(element) is list:
            unique = output_result(element, unique, history)
        else:
            if not element in history:
                history[element] = ""
                unique.append(element)
    return unique


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def main():
    print "RUZZLE SOLVER"
    print "Enter each line of the puzzle here"
    print "Do not put any space between the letters"

    words = load_word_list()
    #create a dictionary for words <= 5
    small_word_lookup = {w:0 for w in words if len(w) <= SMALL_WORD_LOOKUP_MAX}

    #load the index for longer words
    indexed_words = load_prefix_index()

    #get the puzzle layout
    ruzzle = []
    for i in range(MAX_ROW):
        s = raw_input("> ")
        ruzzle.append(list(s))

    #solve
    solved_words = []
    for y in range(MAX_ROW):
        for x in range(MAX_COLUMN):
            solved_words = find_words((x,y), 
                                      ruzzle, [(x,y)], 
                                      get(ruzzle, (x, y)),
                                      result = solved_words,
                                      complete_word_list=words,
                                      small_word_lookup=small_word_lookup,
                                      prefix_index_lookup=indexed_words)
    
    output_list = unique_result(solved_words)
    for row in chunks(sorted(output_list), 10):
        print " ".join(row)


if __name__ == '__main__':
    main()
