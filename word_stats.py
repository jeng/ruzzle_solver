#!/usr/bin/env python

from ruzzle_solve import load_word_list

def main():
    words = load_word_list()
    desc = {2:"Two", 3:"Three", 4:"Four", 5:"Five"}
    stats = {2:0, 3:0, 4:0, 5:0}
    total_word_count = 0
    for w in words:
        total_word_count += 1
        n = len(w)
        if n in stats:
            stats[n] = stats[n] + 1

    print "STATS"
    print "-" * 20
    for i in stats:
        print "%5s %s" % (desc[i], stats[i])
    print "-" * 20
    stat_total = sum([stats[i] for i in stats])
    print "TOTAL > ", stat_total
    print "TOTAL WORDS > ", total_word_count
    print "PERCENT > ", round ( ( stat_total/(1.0 *total_word_count)) * 100)
    print "\n\n"
    
    #compute the word prefix indexes over 5
    index_dict = {}
    index = 0
    for line in words:
        if len(line) > 5:
            prefix = line[:5]
            if not prefix in index_dict:
                index_dict[prefix] = index
        index += 1

    print "PREFIX INDEX"
    print "-" * 20

    # for prefix in index_dict:
    #     print "%30s %d" % (prefix, index_dict[prefix])


    index_size = len(index_dict)
    print "INDEX LIST SIZE > ", index_size
    print "PRECENT > ", round((index_size / (total_word_count * 1.0)) * 100)
    print "\n\n"
    print "DUMPING INDEXES TO PREFIX.IDX"
    print "-" * 20
    with open("prefix.idx", "w") as index_file:
        for prefix in index_dict:
            index_file.write("%s %d\n" % (prefix, index_dict[prefix]))
    print "DONE"

main()
