+++
title= "XGBoost Deployment"
date= 2018-03-12T17:08:30-07:00
description = "Guide to deploy XGBoost Models."
draft= false
+++
## A guide to installing packages to model containers
{{% notice warning %}}
This tutorial will assume that you have already installed `clipper_admin` and its dependencies.
{{% /notice %}}

In order to keep the base image's light, containers limit the packages they come with default; however, Clipper also supports the installation of additional packages onto model containers using pip. Packages such as XGBoost can be installed and deployed in this way.

First, we open a python interactive shell.
```sh
$ python
# Now, we start clipper.
>>> import logging, xgboost as xgb, numpy as np
>>> from clipper_admin import ClipperConnection, DockerContainerManager
>>> cl = ClipperConnection(DockerContainerManager())
>>> logging.info("Starting Clipper")
18-03-15:11:20:54 INFO     [<stdin>:1] Starting Clipper
>>> cl.start_clipper()
18-03-15:11:21:00 INFO     [docker_container_manager.py:96] Starting managed Redis instance in Docker
18-03-15:11:22:07 INFO     [clipper_admin.py:109] Clipper still initializing.
18-03-15:11:22:08 INFO     [clipper_admin.py:111] Clipper is running
# Next, we must register our application
# We will register it to deploy an xgboost model.
>>> cl.register_application('xgboost-test', 'integers', 'default_pred', 100000)
18-03-15:11:23:17 INFO     [clipper_admin.py:186] Application xgboost-test was successfully registered
# Now, we define a function to generate test points.
>>> def get_test_point():
...     return [np.random.randint(255) for _ in range(784)]
...
# And create a training matrix
>>> dtrain = xgb.DMatrix(get_test_point(), label=[0])
# We then create parameters, watchlist, and specify the number of rounds
# This is code that we use to build our XGBoost Model, and your code may differ.
>>> param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
>>> watchlist = [(dtrain, 'train')]
>>> num_round = 2
>>> bst = xgb.train(param, dtrain, num_round, watchlist)
[0]    train-error:0
[1]    train-error:0
# Now, we define our predict function for our model.
>>> def predict(xs):
...     return [str(bst.predict(xgb.DMatrix(xs)))]
...
>>>
```
Now that we have a model, as well as a predict function, we must deploy our model container. We will use a `python_closure_container`, and install the `xgboost` module using `pip`.
```sh
>>> from clipper_admin.deployers import python as python_deployer
# We specify which packages to install in the pkgs_to_install arg.
# For example, if we wanted to install xgboost and psycopg2, we would use
# pkgs_to_install = ['xgboost', 'psycopg2']
>>> python_deployer.deploy_python_closure(cl, name='xgboost-model', version=1, input_type="integers", func=predict, pkgs_to_install=['xgboost'])
18-03-15:11:37:53 INFO     [deployer_utils.py:58] Anaconda environment found. Verifying packages.
18-03-15:11:38:29 INFO     [deployer_utils.py:158] The following packages in your conda environment are not available in the linux-64 conda channel the container will use:
ca-certificates==2018.1.18=0,...

18-03-15:11:38:29 INFO     [deployer_utils.py:159] Using Anaconda API: https://api.anaconda.org

18-03-15:11:38:29 INFO     [deployer_utils.py:67] Supplied environment details
18-03-15:11:38:37 INFO     [deployer_utils.py:79] Supplied local modules
18-03-15:11:38:37 INFO     [deployer_utils.py:85] Serialized and supplied predict function
18-03-15:11:38:37 INFO     [python.py:192] Python closure saved
18-03-15:11:38:38 INFO     [clipper_admin.py:400] Building model Docker image with model data from /tmp/clipper/tmpcaUamW
18-03-15:11:40:40 INFO     [clipper_admin.py:404] Pushing model Docker image to xgboost-model:1
18-03-15:11:40:42 INFO     [docker_container_manager.py:243] Found 0 replicas for xgboost-model:1. Adding 1
18-03-15:11:40:42 INFO     [clipper_admin.py:578] Successfully registered model xgboost-model:1
18-03-15:11:40:42 INFO     [clipper_admin.py:496] Done deploying model xgboost-model:1.
18-03-15:11:40:48 INFO     [clipper_admin.py:229] Model xgboost-model is now linked to application xgboost-test
18-03-15:11:41:18 INFO     [test_utils.py:64] Creating DockerContainerManager
18-03-15:11:41:52 INFO     [clipper_admin.py:1201] Stopped all Clipper cluster and all model containers
18-03-15:11:41:52 INFO     [clipper_admin.py:123] Successfully connected to Clipper cluster at localhost:36717
# Tell Clipper to route requests for the "xgboost-test" application to the "xgboost-model"
>>> cl.link_model_to_app('xgboost-test', 'xgboost-model')
18-03-15:11:43:02 INFO     [clipper_admin.py:229] Model xgboost-model is now linked to application xgboost-test
```
Now your application is ready to serve predictions. Let's try one!
```sh
>>> import requests, json
# Get Address
>>> addr = cl.get_query_addr()
# Post Query
>>> response = requests.post(
...     "http://%s/%s/predict" % (addr, 'xgboost-test'),
...     headers={"Content-type": "application/json"},
...     data=json.dumps({
...         'input': get_test_point()
...     }))
...
>>> result = response.json()
>>> if response.status_code == requests.codes.ok and result["default"]:
...     print('A default prediction was returned.')
...     elif response.status_code != requests.codes.ok:
...         print(result)
...         raise BenchmarkException(response.text)
...     else:
...         print('Prediction Returned:', result)
...
('Prediction Returned:', {u'default': False, u'output': [0.5], u'query_id': 26})
# And finally, we stop clipper
>>> cl.stop_all()
18-03-15:11:45:42 INFO     [clipper_admin.py:1141] Stopped all Clipper cluster and all model containers
```

