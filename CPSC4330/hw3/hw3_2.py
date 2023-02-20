import sys
import re
import os.path
from pyspark import SparkContext

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hw3_2.py <input>")
        sys.exit(1)
    if not os.path.isfile("stopwords.txt"):
        print("stopwords.txt could not be found")
        sys.exit(1)
    stopFile = open("stopwords.txt")
    stopWords = stopFile.read()
    sc = SparkContext()
    shakespeare = sc.textFile(sys.argv[1]) \
        .flatMap(lambda line: line.split(" ")) \
        .map(lambda word: re.sub('[,.?!;:|"\[\]\-\\t]+', '', word)) \
        .filter(lambda word: word != ' ' and word != '') \
        .map(lambda word: word.lower()) \
        .filter(lambda word: word not in stopWords) \
        .map(lambda word: (word, 1)) \
        .groupByKey(1) \
        .map(lambda count: (count[0], sum(count[1]))) \
        .sortBy(lambda x: x[1], False) \

    for (word, count) in shakespeare.take(10):
        print(word, count)

