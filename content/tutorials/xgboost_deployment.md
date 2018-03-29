+++
title= "XGBoost Deployment"
date= 2018-03-12T17:08:30-07:00
description = "Guide to deploy XGBoost Models."
draft= false
+++
## A guide to deploy XGBoost Models
{{% notice warning %}}
This tutorial will assume that you have already installed `clipper_admin` and its dependencies.
{{% /notice %}}

In order to keep the base images small, containers limit the packages they come with default; however, Clipper also supports the installation of additional packages onto model containers using pip. Packages such as XGBoost can be installed and deployed in this way.

The following tutorial is written in Python. First, we start Clipper.
```python
import logging, xgboost as xgb, numpy as np
from clipper_admin import ClipperConnection, DockerContainerManager
cl = ClipperConnection(DockerContainerManager())
```
Next, we must register our application
```python
# We will register it to deploy an xgboost model.
cl.register_application('xgboost-test', 'integers', 'default_pred', 100000)
```
Now we need to get some training data. For the purposes of this example, we will just use randomly generated data.
```python
def get_test_point():
    return [np.random.randint(255) for _ in range(784)]
```
We then create an XGBoost model. (These steps will guide you to create a generic model).
```python
# Create a training matrix.
dtrain = xgb.DMatrix(get_test_point(), label=[0])
# We then create parameters, watchlist, and specify the number of rounds
# This is code that we use to build our XGBoost Model, and your code may differ.
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
watchlist = [(dtrain, 'train')]
num_round = 2
bst = xgb.train(param, dtrain, num_round, watchlist)
```
We also must define our predict function for our model. In order to deploy the XGBoost model to Clipper, we define a closure that references the XGBoost model. Clipper's model deployer will automatically track down everything that is referenced in the closure (including the XGBoost model), and include it in the model container.
```python
def predict(xs):
    return [str(bst.predict(xgb.DMatrix(xs)))]
```
Now that we have a model, as well as a predict function, we must deploy our model container. We will use a `python_closure_container`, and install the `xgboost` module using `pip`.
```python
from clipper_admin.deployers import python as python_deployer
# We specify which packages to install in the pkgs_to_install arg.
# For example, if we wanted to install xgboost and psycopg2, we would use
# pkgs_to_install = ['xgboost', 'psycopg2']
python_deployer.deploy_python_closure(cl, name='xgboost-model', version=1,
     input_type="integers", func=predict, pkgs_to_install=['xgboost'])
```
The next step is to link the model container to our app, so that Clipper can route requests for the "xgboost-test" application to the "xgboost-model" container.
```python
cl.link_model_to_app('xgboost-test', 'xgboost-model')
```
Now your application is ready to serve predictions. Let's try one!
```python
import requests, json
# Get Address
addr = cl.get_query_addr()
# Post Query
response = requests.post(
     "http://%s/%s/predict" % (addr, 'xgboost-test'),
     headers={"Content-type": "application/json"},
     data=json.dumps({
         'input': get_test_point()
     }))
result = response.json()
if response.status_code == requests.codes.ok and result["default"]:
     print('A default prediction was returned.')
     elif response.status_code != requests.codes.ok:
         print(result)
         raise BenchmarkException(response.text)
     else:
         print('Prediction Returned:', result)
```
You should see something like the following output:
```python
('Prediction Returned:', {u'default': False, u'output': [0.5], u'query_id': 26})
```
And finally, we stop Clipper
```python
cl.stop_all()
```
