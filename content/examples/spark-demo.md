+++
date = "2017-06-05T17:31:49-07:00"
title = "Deploy a PySpark Model"
toc = true
weight = 5

+++

[Download Jupyter notebook version of this demo](/ipynb/spark_meetup_demo.ipynb)

```python
import sys, os, json, numpy as np, requests
headers = {"Content-type": "application/json"}
```

# Install Clipper Admin

```sh
$ pip install clipper_admin
```


```python
from clipper_admin import Clipper
```


```python
clipper_client  = Clipper("localhost")
```


```python
clipper_client.start()
```


```python
clipper_client.get_all_apps()
```


```python
# An application in Clipper corresponds to a REST prediction endpoint
clipper_client.register_application(
    "digits",
    "pyspark_svm", "ints", "-1.0", 100000)
```


```python
# Send a test prediction
requests.post(
    "http://localhost:1337/digits/predict",
    headers=headers,
    data=json.dumps({"input": [np.random.randint(255) for _ in range(784)]})).json()
```

# Train an SVM with PySpark

> Note that this code uses the `findspark` package to import Spark. You can install it with `pip install findspark`.


```python
import findspark
findspark.init()
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.regression import LabeledPoint
from pyspark.sql import SparkSession
```


```python
spark = SparkSession\
        .builder\
        .appName("clipper-pyspark")\
        .getOrCreate()
sc = spark.sparkContext


```


```python
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
```


```python
model = LogisticRegressionWithLBFGS.train(trainRDD)
```


```python
def simple_predict(spark, model, xs):
    return [str(model.predict(normalize(x))) for x in xs]
```


```python
test_point = np.array([np.random.randint(255) for _ in range(784)])
simple_predict(spark, model, [test_point])
```

{{% notice note %}}
You can find [method documentation](http://docs.clipper.ai/en/latest/#clipper_admin.Clipper.deploy_pyspark_model)
and read more about `clipper_admin` at [docs.clipper.ai](docs.clipper.ai).
{{% /notice %}}

```python
clipper_client.deploy_pyspark_model("pyspark_svm", 1, simple_predict, model, sc, "ints")
```


```python
requests.post(
    "http://localhost:1337/digits/predict",
    headers=headers,
    data=json.dumps({"input": [np.random.randint(255) for _ in range(784)]})).json()
```
