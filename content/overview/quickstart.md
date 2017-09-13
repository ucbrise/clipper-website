+++
date = "2017-05-20T18:01:34-07:00"
icon = "<b>1. </b>"
title = "Quickstart"
weight = 1
+++

The easiest way to get started using Clipper is to install the `clipper_admin` pip package and use it interactively from a Python
REPL.



> This quickstart requires [Docker](https://www.docker.com/) and only supports Python2.


#### Start a Clipper Instance and Deploy a Model

__Install Clipper__

You can either install Clipper directly from GitHub:
```sh
pip install git+https://github.com/ucbrise/clipper.git@release-0.2#subdirectory=clipper_admin
```
or by cloning Clipper and installing directly from the file system:
```sh
pip install -e </path/to/clipper_repo>/clipper_admin
```


__Start a local Clipper cluster__

First start a Python interpreter session.

```sh
$ python

# Or start one with iPython
$ conda install ipython
$ ipython
```

```py
>>> from clipper_admin import ClipperConnection, DockerContainerManager
>>> clipper_conn = ClipperConnection(DockerContainerManager())

# Start Clipper. Running this command for the first time will
# download several Docker containers, so it may take some time.
>>> clipper_conn.start_clipper()
17-08-30:15:48:41 INFO     [docker_container_manager.py:95] Starting managed Redis instance in Docker
17-08-30:15:48:43 INFO     [clipper_admin.py:105] Clipper still initializing.
17-08-30:15:48:44 INFO     [clipper_admin.py:107] Clipper is running

# Register an application called "hello_world". This will create
# a prediction REST endpoint at http://localhost:1337/hello_world/predict
>>> clipper_conn.register_application(name="hello-world", input_type="doubles", default_output="-1.0", slo_micros=100000)
17-08-30:15:51:42 INFO     [clipper_admin.py:182] Application hello-world was successfully registered

# Inspect Clipper to see the registered apps
>>> clipper_conn.get_all_apps()
[u'hello_world']

# Define a simple model that just returns the sum of each feature vector.
# Note that the prediction function takes a list of feature vectors as
# input and returns a list of strings.
>>> def feature_sum(xs):
      return [str(sum(x)) for x in xs]

# Import the python deployer package
>>> from clipper_admin.deployers import python as python_deployer

# Deploy the "feature_sum" function as a model. Notice that the application and model
# must have the same input type.
>>> python_deployer.deploy_python_closure(clipper_conn, name="sum-model", version=1, input_type="doubles", func=feature_sum)
17-08-30:15:59:56 INFO     [deployer_utils.py:50] Anaconda environment found. Verifying packages.
17-08-30:16:00:04 INFO     [deployer_utils.py:150] Fetching package metadata .........
Solving package specifications: .

17-08-30:16:00:04 INFO     [deployer_utils.py:151]
17-08-30:16:00:04 INFO     [deployer_utils.py:59] Supplied environment details
17-08-30:16:00:04 INFO     [deployer_utils.py:71] Supplied local modules
17-08-30:16:00:04 INFO     [deployer_utils.py:77] Serialized and supplied predict function
17-08-30:16:00:04 INFO     [python.py:127] Python closure saved
17-08-30:16:00:04 INFO     [clipper_admin.py:375] Building model Docker image with model data from /tmp/python_func_serializations/sum-model
17-08-30:16:00:05 INFO     [clipper_admin.py:378] Pushing model Docker image to sum-model:1
17-08-30:16:00:07 INFO     [docker_container_manager.py:204] Found 0 replicas for sum-model:1. Adding 1
17-08-30:16:00:07 INFO     [clipper_admin.py:519] Successfully registered model sum-model:1
17-08-30:16:00:07 INFO     [clipper_admin.py:447] Done deploying model sum-model:1.

# Tell Clipper to route requests for the "hello-world" application to the "sum-model"
>>> clipper_conn.link_model_to_app(app_name="hello-world", model_name="sum-model")
17-08-30:16:08:50 INFO     [clipper_admin.py:224] Model sum-model is now linked to application hello-world

# Your application is now ready to serve predictions
```

#### Query Clipper for predictions


Now that you've deployed your first model, you can start requesting predictions at the REST endpoint that clipper created for your application: `http://localhost:1337/hello-world/predict`

With cURL:


```sh
$ curl -X POST --header "Content-Type:application/json" -d '{"input": [1.1, 2.2, 3.3]}' 127.0.0.1:1337/hello-world/predict
```

From a Python REPL:

```py
>>> import requests, json, numpy as np
>>> headers = {"Content-type": "application/json"}
>>> requests.post("http://localhost:1337/hello-world/predict", headers=headers, data=json.dumps({"input": list(np.random.random(10))})).json()
```

#### Clean up

If you closed the Python REPL you were using to start Clipper, you will need to start a new Python REPL and create another connection to the Clipper cluster. If you still have the Python REPL session active from earlier, you can re-use your existing `ClipperConnection` object.

```py
# If you have still have the Python REPL from earlier, skip directly
# to clipper_conn.stop_all()
>>> from clipper_admin import ClipperConnection, DockerContainerManager
>>> clipper_conn = ClipperConnection(DockerContainerManager())
>>> clipper_conn.connect()

# Stop all Clipper docker containers
>>> clipper_conn.stop_all()
17-08-30:16:15:38 INFO     [clipper_admin.py:1141] Stopped all Clipper cluster and all model containers
```



























The clipper-admin package contains the [Clipper manager]({{< relref "documentation/clipper_manager.md" >}}) which can be used to start and manage a Clipper instance.

{{% notice note %}}
**Dependencies:** Before using Clipper, you must install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) and the [Anaconda Python](https://www.continuum.io/downloads) distribution.
{{% /notice %}}

```
$ pip install clipper_admin
$ python
```

Once you have the `clipper_admin` package installed, you can use it to start a Clipper instance and deploy your first model.
When you use the Clipper manager to start a Clipper instance, it will run Clipper in [Docker](https://www.docker.com/) containers using [Docker Compose](https://docs.docker.com/compose/).


From the Python REPL:

```py
>>> from clipper_admin import Clipper
# Start a Clipper instance on localhost
>>> clipper_conn = Clipper("localhost")
Checking if Docker is running...
>>> clipper_conn.start()
Clipper is running

# Register an application called "hello_world" that will query a model
# called "feature_sum_model". This will create a prediction REST endpoint
# at http://localhost:1337/hello_world/predict
>>> clipper_conn.register_application("hello_world", "feature_sum_model", "doubles", "-1.0", 100000)
Success!

# Inspect Clipper to see the registered apps
>>> clipper_conn.get_all_apps()
[u'test']

# Define a simple model that just returns the sum of each feature vector.
# Note that the prediction function takes a list of feature vectors as
# input and returns a list of strings.
>>> def pred(xs):
      return [str(np.sum(x)) for x in xs]

# Deploy the model, naming it "feature_sum_model" and giving it version 1
>>> clipper_conn.deploy_predict_function("feature_sum_model", 1, pred, "doubles")
```

{{% notice note %}}
If your Docker installation requires root access, you can pass
the keyword argument `sudo=True` when constructing a `clipper_manager.Clipper()`
instance to tell the Clipper manager to execute Docker commands as root.
{{% /notice %}}

Now that you've deployed your first model, you can start requesting predictions at the
REST endpoint that clipper created for your application:
`http://localhost:1337/hello_world/predict`

With curl:

```sh
$ curl -X POST --header "Content-Type:application/json" -d '{"input": [1.1, 2.2, 3.3]}' 127.0.0.1:1337/hello_world/predict

{"query_id":0,"output":6.6,"default":false}
```

From a Python REPL:

```py
>>> import requests, json, numpy as np
>>> headers = {"Content-type": "application/json"}
>>> requests.post("http://localhost:1337/hello_world/predict", headers=headers, data=json.dumps({"input": list(np.random.random(10))})).json()
```



