
def print_output(caches):
    print len(caches)
    for c in caches.keys():
        print c,
        print " ".join([str(v) for v in caches[c].vids])
