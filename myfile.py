import sys

class Video:
    def __init__(self, id, size):
        id = id
        size = size


class Cache:
    def __init__(self, id, size):
        size = size
        id = id
        vids = []

    def add_vid(self, vid):
        self.vids.append[vid]
        self.size -= vid.size


class Endpoint:

    def __init__(self, caches, lat):
        caches = caches
        requests = dict()
        dc_lat = lat

    def add_request(self, id, num_reqs):
        self.requests[id] = num_reqs


def calc_endpoint_score(caches, endpoint):
    score = 0
    # calculate score from each request
    for req in endpoint.requests.keys():
        min_lat = endpoint.dc_lat
        for c in caches:
            # requested video is in cache and cache is connected to endpoint
            if req in caches.vids and c in endpoint.caches.keys():
                if endpoint.caches[c] < min_lat:
                    min_lat = endpoint.caches[c]
        score += min_lat * endpoint.requests[req]


videoSizes = dict()
endpointsDict = dict()
nVideos = 0
nEndpoints = 0
nRequests = 0
nCaches = 0
cacheSize = 0


def init_data(fname):
    global nVideos, nEndpoints, nRequests, nCaches, cacheSize, videoSizes, endpointsDict
    try:
        with open(fname, 'r') as fhanlder:
            initline = fhanlder.readline().split()
            nVideos = int(initline[0])
            nEndpoints = int(initline[1])
            nRequests = int(initline[2])
            nCaches = int(initline[3])
            cacheSize = int(initline[4])
            for i, size in enumerate(fhanlder.readline().split()):
                videoSizes[i] = Video(i, int(size))
            for i in range(0, nEndpoints):
                endpoint_line = fhanlder.readline().split()
                latency = int(endpoint_line[0])
                connection_latencies = dict()
                for j in range(0, int(endpoint_line[1])):
                    line = fhanlder.readline().split()
                    connection_latencies[int(line[0])] = int(line[1])
                endpointsDict[i] = Endpoint(connection_latencies, latency)
            for i in range(0, nRequests):
                request_line = fhanlder.readline().split()
                print " ".join(request_line)
                endpointsDict[int(request_line[1])].add_request(int(request_line[0]), int(request_line[2]))
    except IOError:
        print "Couldn't find ", fname
        raise


def selfcheck():
    print "nVideos", nVideos
    print "nEndpoints", nEndpoints
    print "nRequests", nRequests
    print "nCaches", nCaches
    print "cacheSize", cacheSize
    for k in videoSizes.keys():
        print videoSizes[k] + " ",
    print

def main():
    fname = sys.argv[1]
    init_data(fname)
    selfcheck()

if __name__ == '__main__':
    main()
