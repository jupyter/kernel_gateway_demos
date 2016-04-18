import pyspark
sc = pyspark.SparkContext()
rdd = sc.parallelize(range(1000))
sample = rdd.takeSample(False, 5)
print(sample)