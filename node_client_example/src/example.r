library(SparkR)

sc <- sparkR.init("local[*]")
sqlContext <- sparkRSQL.init(sc)

# do something to prove it works
data(iris)
df <- createDataFrame(sqlContext, iris)
head(filter(df, df$Petal_Width > 0.2))