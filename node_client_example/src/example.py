# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import pyspark

# In some environments, "sc" is pre-defined.
if not 'sc' in globals():
    sc = pyspark.SparkContext()
rdd = sc.parallelize(range(1000))
sample = rdd.takeSample(False, 5)
print(sample)
