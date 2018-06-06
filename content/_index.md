+++
date = "2017-05-20T17:53:26-07:00"
title = "Clipper"
toc = false
weight = 5
chapter = false

+++

## Getting Started

Clipper is a low-latency prediction serving system for machine learning.
Clipper makes it simple to integrate machine learning into user-facing serving systems.

The simplest way to start using Clipper is to use the Clipper Admin Python tool to start a local Clipper cluster using Docker.
Read the [container orchestration guide]({{< relref "tutorials/container_managers.md" >}}) to learn about other ways to run Clipper,
including on Kubernetes.

### Install Clipper

Before starting Clipper, you must have a recent version of [Docker](https://www.docker.com/) and Python installed.
We recommend installing Clipper into an Anaconda environment. Clipper currently supports Python 2, 3.5, 3.6.

```sh
pip install clipper_admin
```

### Quickstart

First start a Python interpreter session.

```sh
# Bare Python interpreter
$ python
```

```
# iPython shell
$ conda install ipython
$ ipython
```

From the Python shell, you can start a new Clipper cluster and deploy a simple Python function as your first model.


```python
from clipper_admin import ClipperConnection, DockerContainerManager
```


```python
clipper_conn = ClipperConnection(DockerContainerManager())
```

Start Clipper. Running this command for the first time will
download several Docker containers, so it may take some time.


```python
clipper_conn.start_clipper()
```

```pycon
18-05-21:12:18:46 INFO     [docker_container_manager.py:109] Starting managed Redis instance in Docker
18-05-21:12:18:50 INFO     [clipper_admin.py:125] Clipper is running
```

Register an application called "hello_world". This will create
a prediction REST endpoint at http://localhost:1337/hello_world/predict


```python
clipper_conn.register_application(name="hello-world", input_type="doubles", default_output="-1.0", slo_micros=100000)
```

```pycon
18-05-21:12:19:02 INFO     [clipper_admin.py:200] Application hello-world was successfully registered
```

Inspect Clipper to see the registered apps


```python
clipper_conn.get_all_apps()
```
```pycon
['hello-world']
```


Define a simple model that just returns the sum of each feature vector.
Note that the prediction function takes a list of feature vectors as
input and returns a list of strings.


```python
def feature_sum(xs):
    return [str(sum(x)) for x in xs]
```

Import the python deployer package


```python
from clipper_admin.deployers import python as python_deployer
```

Deploy the "feature_sum" function as a model. Notice that the application and model
must have the same input type.


```python
python_deployer.deploy_python_closure(clipper_conn, name="sum-model", version=1, input_type="doubles", func=feature_sum)
```
```pycon
18-05-21:12:19:59 INFO     [deployer_utils.py:44] Saving function to /tmp/clipper/tmpx6d_zqeq
18-05-21:12:19:59 INFO     [deployer_utils.py:54] Serialized and supplied predict function
18-05-21:12:19:59 INFO     [python.py:192] Python closure saved
18-05-21:12:19:59 INFO     [python.py:206] Using Python 3.6 base image
18-05-21:12:19:59 INFO     [clipper_admin.py:451] Building model Docker image with model data from /tmp/clipper/tmpx6d_zqeq
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': 'Step 1/2 : FROM clipper/python36-closure-container:develop'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': '\n'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': ' ---> 1aaddfa3945e\n'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': 'Step 2/2 : COPY /tmp/clipper/tmpx6d_zqeq /model/'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': '\n'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': ' ---> b7c29f531d2e\n'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'aux': {'ID': 'sha256:b7c29f531d2eaf59dd39579dbe512538be398dcb5fdd182db14e4d58770d2055'}}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': 'Successfully built b7c29f531d2e\n'}
18-05-21:12:20:00 INFO     [clipper_admin.py:455] {'stream': 'Successfully tagged sum-model:1\n'}
18-05-21:12:20:00 INFO     [clipper_admin.py:457] Pushing model Docker image to sum-model:1
18-05-21:12:20:02 INFO     [docker_container_manager.py:247] Found 0 replicas for sum-model:1. Adding 1
18-05-21:12:20:09 INFO     [clipper_admin.py:634] Successfully registered model sum-model:1
18-05-21:12:20:09 INFO     [clipper_admin.py:552] Done deploying model sum-model:1.
```

Tell Clipper to route requests for the "hello-world" application to the "sum-model"


```python
clipper_conn.link_model_to_app(app_name="hello-world", model_name="sum-model")
```
```pycon
18-05-21:12:20:19 INFO     [clipper_admin.py:262] Model sum-model is now linked to application hello-world
```

Your application is now ready to serve predictions

#### Query Clipper for predictions


Now that you've deployed your first model, you can start requesting predictions with your favorite REST client at the endpoint that Clipper created for your application: `http://localhost:1337/hello-world/predict`

*Directly from the command line with [curl](https://curl.haxx.se/):*

```sh
curl -X POST --header "Content-Type:application/json" -d '{"input": [1.1, 2.2, 3.3]}' 127.0.0.1:1337/hello-world/predict
```

*From a Python interpreter:*

```python
import requests, json, numpy as np
headers = {"Content-type": "application/json"}
requests.post("http://localhost:1337/hello-world/predict", headers=headers, data=json.dumps({"input": list(np.random.random(10))})).json()
```

#### Clean up

If you closed the Python interpreter session that you used to start Clipper, you will need to start a new Python interpreter session and create another connection to the Clipper cluster. If you still have the interpreter session active from earlier, you can re-use your existing `ClipperConnection` object.

If you have still have the Python REPL from earlier,
skip directly to clipper_conn.stop_all()
```python
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.connect()
```

Stop all Clipper docker containers
```python
clipper_conn.stop_all()
```
```pycon
17-08-30:16:15:38 INFO     [clipper_admin.py:1141] Stopped all Clipper cluster and all model containers
```

## Next steps

+ [Browse user guides]({{< relref "tutorials/_index.md" >}})
+ [Fork the code on GitHub](https://github.com/ucbrise/clipper)
