from pyspark import SparkContext
import sys

# Square distance between two (lat, long) points
def findDistance(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

# Find index of cluster point should be in
def findCluster(p1, centers):
    minDistance = float("inf")
    minCenter = -1
    # Compare distance between point and all centers to find closest one
    for i in range(len(centers)):
        dist = findDistance(p1, centers[i])
        if dist < minDistance:
            minDistance = dist
            minCenter = i
    return minCenter

# Find distance between old and new centers
# Centers are stored in lists [(lat, long), (lat, long) ... ]
def centerDist(oldCenters, newCenters):
    convergeDist = 0.1
    tempDist = (oldCenters[0][0] - newCenters[0][0]) ** 2 + \
                (oldCenters[0][1] - newCenters[0][1]) ** 2 + \
                (oldCenters[1][0] - newCenters[1][0]) ** 2 + \
                (oldCenters[1][1] - newCenters[1][1]) ** 2 + \
                (oldCenters[2][0] - newCenters[2][0]) ** 2 + \
                (oldCenters[2][1] - newCenters[2][1]) ** 2 + \
                (oldCenters[3][0] - newCenters[3][0]) ** 2 + \
                (oldCenters[3][1] - newCenters[3][1]) ** 2 + \
                (oldCenters[4][0] - newCenters[4][0]) ** 2 + \
                (oldCenters[4][1] - newCenters[4][1]) ** 2

    # False to continue, True to end
    return tempDist <= convergeDist

# Recalculate one center at a time
# cluster is a list of all points
# Each point is ((lat, long), index)
def newCenter(cluster, index):
    count = 0
    sumX = 0
    sumY = 0

    for point in cluster:
        if point[1] == index:
            count += 1
            sumX += point[0][0]
            sumY += point[0][1]
    
    avg = (sumX / count, sumY / count)

    return avg

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hw4.py <input>")
        sys.exit(1)
    
    sc = SparkContext()
    # Split file, remove zeroes, convert to (lat, long) pairs
    data = sc.textFile(sys.argv[1]) \
            .map(lambda line: line.split(",")) \
            .filter(lambda line: line[3] != '0' and line[4] != '0') \
            .map(lambda line: (float(line[3]), float(line[4]))) \
            .persist()

    # Get starting centers
    centers = data.takeSample(False, 5, 34)
    points = data.collect()

    # Make clusters
    clusters = []
    for point in points:
        index = findCluster(point, centers)
        clusters.append((point, index))

    # Calculate first new centers
    newCenters = []
    for i in range(len(centers)):
        newCenters.append(newCenter(clusters, i))
    
    # Repeat until distance between centers < 0.1
    while not centerDist(centers, newCenters):
        clusters = []
        centers = newCenters
        for point in points:
            index = findCluster(point, centers)
            clusters.append((point, index))
        newCenters = []
        for i in range(len(centers)):
            newCenters.append(newCenter(clusters, i))

    # Final output
    for center in newCenters:
        print(center)

    sc.stop()