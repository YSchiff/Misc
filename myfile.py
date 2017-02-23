

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
        requests = {}
        dc_lat = lat

    def add_request(self, id, num_reqs):
        self.requests[id] = num_reqs


def calc_score(caches, endpoint):
    for req in endpoint.requests.keys():
        min_lat = endpoint.dc_lat
        for c in caches:
            if req in caches.vids and c in :


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
        with open(fname) as fhanlder:
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
                endpointsDict[int(request_line[1])].add_request(int(request_line[0]), int(request_line[2]))
    except IOError:
        print "Couldn't find ", fname
        raise


def main():
    fname = sys.argv[1]


if __name__ == '__main__':
    main()
