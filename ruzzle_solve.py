#!/usr/bin/env python

DIRECTIONS = {'N': (0, 1), 'NE': (1, -1), 'E': (1, 0),
              'SE': (1, 1), 'S': (0, 1), 'SW': (-1, 1),
              'W': (-1, 0), 'NW': (-1, -1)}
    
MAX_ROW = 4
MAX_COLUMN = 4
SMALL_WORD_LOOKUP_MAX = 6

word = []
small_word_lookup = {}
word_prefix_index = {}
solved_words = {}

def load_word_list():
    word_list = []
    with open("WORD.LST") as f:
        for line in f:
            word_list.append(line.rstrip())
    return word_list
        

def move(pos, direction):
    x, y = pos
    incx, inxy = DIRECTIONS[direction]
    return (x + incx, inxy + y)


def get(ruzzle, pos):
    x, y = pos
    return ruzzle[y][x]

def get_prefix_words(prefix):
    results = []
    for w in words:
        if re.search(prefix + "*", w):
            results.append(w)
    return results


def in_range(pos):
    x, y = pos
    return 0 <= x < MAX_COLUMN and 0 <= y < MAX_ROW


def find_words(start_pos, ruzzle, history, s):
    #word_list = get_prefix_words(s)

    global small_word_lookup
    global solved_words
    if 1 < len(s) <= SMALL_WORD_LOOKUP_MAX:
        if s in small_word_lookup:
            if not s in solved_words:
                #print s, history, [get(ruzzle, p) for p in history]
                solved_words[s] = ""
    elif len(s) > SMALL_WORD_LOOKUP_MAX:
        return

    for direction in DIRECTIONS:
        new_pos = move(start_pos, direction)
        if in_range(new_pos) and not new_pos in history:
            find_words(new_pos, ruzzle, history[:] + [new_pos], s + get(ruzzle, new_pos))


def main():
    print "RUZZLE SOLVER"
    print "Enter each line of the puzzle here"
    print "Do not put any space between the letters"

    ruzzle = []
        
    global words
    words = load_word_list()

    #create a dictionary for words <= 5
    global small_word_lookup
    for w in words:
        if len(w) <= 6:
            small_word_lookup[w] = ""

    #load the index for longer words
    global index_word

    #get the puzzle layout
    for i in range(MAX_ROW):
        s = raw_input("> ")
        ruzzle.append(list(s))

    #solve
    global solved_words
    solved_words = {}
    for y in range(MAX_ROW):
        for x in range(MAX_COLUMN):
            find_words((x,y), ruzzle, [(x,y)], get(ruzzle, (x, y)))
    
    output_list = []
    for word in solved_words:
        output_list.append(word)
        if len(output_list) > 9:
            print " ".join(output_list)
            output_list = []
            
    print " ".join(output_list)
    

if __name__ == '__main__':
    main()
