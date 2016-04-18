import org.apache.spark.sql.SQLContext

case class custTab(col0: Integer, col1: String, col2: String, col3: String)

// explicitly create a sqlcontext
val sqlC = new SQLContext(sc)

// to get the toDF method
import sqlC.implicits._

val custDataTs = Seq(
     custTab(1, "14/Jul/2012:15:58:12 +0000", "ABC", "Error in transaction processing"),
     custTab(2, "10/14/12 03:34:39", "OR", "Warning systems down"),
     custTab(3, "NA", "DEF", "Normal"),
     custTab(4, "2014.06.09 06:30PM", "CA", "Emergency shutdown alert"),
     custTab(5, "None", "MA", "")
   )
val custTableTs = sc.parallelize(custDataTs, 4).toDF()
custTableTs.show()