+++
date = "2017-06-05T17:31:49-07:00"
title = "Deploy a PySpark Model"
toc = true
weight = 5

+++

[Download Jupyter notebook version of this demo](/ipynb/spark_meetup_demo.ipynb)


First, install the Clipper admin tool with pip.

```sh
$ pip install clipper_admin
```

Now from a Python REPL:

First, start a Clipper instance and register an application:

```python
import sys, os, json, numpy as np, requests
headers = {"Content-type": "application/json"}

from clipper_admin import Clipper
clipper_client  = Clipper("localhost")
clipper_client.start()

clipper_client.get_all_apps()

# An application in Clipper corresponds to a REST prediction endpoint
clipper_client.register_application(
    "digits",
    "pyspark_svm", "ints", "-1.0", 100000)

# Send a test prediction
requests.post(
    "http://localhost:1337/digits/predict",
    headers=headers,
    data=json.dumps({"input": [np.random.randint(255) for _ in range(784)]})).json()
```

Now train a logistic regression model with PySpark

> Note that this code uses the `findspark` package to import Spark. You can install it with `pip install findspark`.


```python
import findspark
findspark.init()
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.regression import LabeledPoint
from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("clipper-pyspark")\
        .getOrCreate()
sc = spark.sparkContext

def normalize(x):
    x = x.astype(np.double)
    mu = np.mean(x)
    sigma = np.var(x)
    if sigma > 0:
        return (x - mu) / np.sqrt(sigma)
    else:
        return 1

def obj(y):
    if y == 3:
        return 0
    else:
        return 1

def parse(line):
    fields = line.strip().split(',')
    return LabeledPoint(obj(int(fields[0])), normalize(np.array(fields[1:])))

train_path = "/Users/crankshaw/model-serving/data/mnist_data/train.data"
trainRDD = sc.textFile(train_path).map(
    lambda line: parse(line)).cache()

model = LogisticRegressionWithLBFGS.train(trainRDD)
```

{{% notice note %}}
You can find [method documentation](http://docs.clipper.ai/en/latest/#clipper_admin.Clipper.deploy_pyspark_model)
and read more about `clipper_admin` at [docs.clipper.ai](docs.clipper.ai).
{{% /notice %}}

Finally, define a predict function for the model and deploy
it directly from your Python session to Clipper.

```python
def simple_predict(spark, model, xs):
    return [str(model.predict(normalize(x))) for x in xs]

test_point = np.array([np.random.randint(255) for _ in range(784)])
simple_predict(spark, model, [test_point])

clipper_client.deploy_pyspark_model("pyspark_svm", 1, simple_predict, model, sc, "ints")
```

Now query the application and see your model make predictions.

```python
requests.post(
    "http://localhost:1337/digits/predict",
    headers=headers,
    data=json.dumps({"input": [np.random.randint(255) for _ in range(784)]})).json()
```
