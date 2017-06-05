+++
date = "2017-05-20T18:01:34-07:00"
icon = "<b>1. </b>"
title = "Quickstart"
weight = 1
+++

The easiest way to get started using Clipper is to install the `clipper_admin` pip package and use it interactively from a Python
REPL.
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



