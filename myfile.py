#! python2

import sys


class Video:
    def __init__(self, id, size):
        self.id = id
        self.size = size


class Cache:
    def __init__(self, id, size):
        self.size = size
        self.id = id
        self.vids = []

    def add_vid(self, vid):
        self.vids.append[vid]
        self.size -= vid.size


class Endpoint:

    def __init__(self, caches, lat):
        self.caches = caches
        self.requests = dict()
        self.dc_lat = lat

    def add_request(self, id, num_reqs):
        if id is not None and num_reqs is not None:
            self.requests[id] = num_reqs

    def __repr__(self):
        string = str(self.dc_lat) + " " + str(len(self.caches.keys())) + "\n"
        for c in self.caches.keys():
            string += str(c) + " " + str(self.caches[c]) + "\n"
        return string


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


videos = dict()
endpointsDict = dict()
nVideos = 0
nEndpoints = 0
nRequests = 0
nCaches = 0
cacheSize = 0


def init_data(fname):
    global nVideos, nEndpoints, nRequests, nCaches, cacheSize, videos, endpointsDict
    try:
        with open(fname, 'r') as fhanlder:
            initline = fhanlder.readline().split()
            nVideos = int(initline[0])
            nEndpoints = int(initline[1])
            nRequests = int(initline[2])
            nCaches = int(initline[3])
            cacheSize = int(initline[4])
            for i, size in enumerate(fhanlder.readline().split()):
                videos[i] = Video(i, int(size))
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
                endpointsDict[int(request_line[1])].add_request(int(request_line[0]), int(request_line[2]))
    except IOError:
        print "Couldn't find ", fname
        raise


def main():
    fname = sys.argv[1]
    init_data(fname)

if __name__ == '__main__':
    main()
