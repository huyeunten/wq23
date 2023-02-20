import sys
from pyspark import SparkContext

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: hw3_1.py <input> <output>")
        sys.exit(1)
    sc = SparkContext()
    rdd = sc.textFile(sys.argv[1]) \
        .map(lambda line: line.split("\t")) \
        .filter(lambda line: line[7].isnumeric()) \
        .map(lambda fields: (fields[3], int(fields[7]))) \
        .groupByKey(1).sortByKey() \
        .map(lambda line: (line[0], sum(line[1])/len(line[1]), len(line[1])))
    rdd.saveAsTextFile(sys.argv[2])
    sc.stop()