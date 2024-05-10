import pytest
from pyspark.sql import SparkSession
import unix_timestamp


@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("PySparkTests") \
        .getOrCreate()
    yield spark
    spark.stop()


def test_feature_assembly(spark):
    from pyspark.ml.feature import VectorAssembler

    # Example DataFrame
    data = [("Type1", "2021-01-01 12:00:00", "Location1", "high"),
            ("Type2", "2021-01-02 13:00:00", "Location2", "medium")]
    df = spark.createDataFrame(
        data, ["EventType", "Timestamp", "Location", "Severity"])

    # Convert Timestamp to numeric
    df = df.withColumn("Timestamp_numeric", unix_timestamp("Timestamp"))

    # Assemble features
    assembler = VectorAssembler(
        inputCols=["EventType_index", "Location_index",
                   "Severity_index", "Timestamp_numeric"],
        outputCol="features"
    )
    output_df = assembler.transform(df)

    # Check if the features column exists
    assert "features" in output_df.columns


def test_anomaly_detection(spark):
    from pyspark.sql.window import Window
    from pyspark.sql.functions import lag, col, when

    # Setup test data
    data = [("Location1", "high", "2021-01-01 12:00:00"),
            ("Location1", "medium", "2021-01-02 13:00:00")]
    df = spark.createDataFrame(data, ["Location", "Severity", "Timestamp"])

    # Calculate severity change
    windowSpec = Window.partitionBy("Location").orderBy("Timestamp")
    df = df.withColumn("prev_severity", lag("Severity", 1).over(windowSpec))
    df = df.withColumn("severity_change", when(
        col("Severity") == "high", 2).otherwise(0))

    # Assert conditions
    results = df.collect()
    # First entry has no previous severity
    assert results[0]["severity_change"] == 0
    assert results[1]["severity_change"] == 2  # Change from None to high
