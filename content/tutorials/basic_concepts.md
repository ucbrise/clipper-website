+++
title= "Basic Concepts"
date= 2017-09-13T10:22:11-07:00
description = ""
draft = false
weight = 1
toc = true
+++

This tutorial is organized as a tour of the Clipper Admin API. It
will walk you through the key concepts needed to understand how to
create a Clipper cluster and deploy models to it, explaining each
concept as it comes up.

## A Clipper Cluster

A running Clipper cluster consists of a collection of Docker containers communicating with each other over the network.
As you issue commands against Clipper using the Clipper Admin tool, you are communicating with
these containers as well as creating new ones or destroying existing ones. As new commands are introduced 
throughout this guide, we have illustrated how they affect the cluster state.

The core of a Clipper cluster consists of three components: the query frontend, the management frontend,
and the configuration database.

{{< figure src="/images/start_clipper.png" >}}

+ *Query frontend:*
      Listens for incoming prediction requests and schedules and routes them to
      deployed models. When you query Clipper's REST prediction interface, you are sending requests
      to the query frontend.

+ *Management frontend:*
      Manages and updates Clipper's internal configuration state. When you change
      the Clipper cluster's configuration, such as by registering new applications or deploying new models,
      you are issuing commands against the management frontend's admin REST interface.

+ *Configuration database:*
      A Redis instance used to persistently store Clipper's internal
      configuration state. Changes to Clipper's internal configuration are propogated from the management
      frontend to Redis so that they are stored persistently. The query frontend watches for changes to the
      configuration database and updates its state appropriately when a change is detected. By storing all
      configuration state in a persistent database, the query frontend and management frontend can remain
      completely stateless, simplifying their implementations and deferring fault-tolerance to Redis.

#### Creating a Clipper Cluster

Clipper runs on Docker containers managed by a container orchestration framework.
The [Container Orchestration]({{< relref "container_managers.md" >}}) user guide has more information
about picking the right container orchestrator and getting started.

Once you've selected your container orchestration framework by deciding which `ContainerManager` implementation to
use, you can create a new [`ClipperConnection`](http://docs.clipper.ai/en/release-0.2/#clipper-connection) object.

The `ClipperConnection` object is your handle to starting and managing a Clipper cluster.

The first thing to do with your connection is use it to start Clipper:
[`ClipperConnection.start_clipper()`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.start_clipper)

#### Connecting to a Clipper Cluster

If instead of creating a cluster, you want to connect to an existing one, you can do this with the
`ClipperConnection.connect()` method. When you start a new cluster, your connection object connects automatically.

Your connection object must be connected to a cluster to execute the remainder of the commands in this guide.


## Model Deployment

### Defining a model

At its most basic, a trained model is just a function that takes some input and produces some output. As a result, one way to think about Clipper is as a function server. While these functions are often complex models, Clipper is not restricted to serving machine learning models.

To improve performance during inference, many machine learning models exploit opportunities for data parallelism in the inference process. Because of this, Clipper tries to provide multiple inputs at once to a deployed model. Therefore, models deployed to Clipper *must have a function interface that takes a list of inputs as an argument and returns a list of predictions as strings*. Returning predictions as strings provides significant flexibility over what your models can return. Commonly, models in Clipper will return either a single number (such as a label or score) or JSON containing a richer representation of the model output (for example, by including confidence estimates of predicted labels).


### Deploying a Model

One of the goals of Clipper is to make it simple to deploy and maintain machine-learning models in production. The prediction interface that models must implement is very simple, consisting of a single function. And the use of Docker makes it easy to include all of a model's dependencies in a self-contained environment. However, deploying a new type of model still entails writing and debugging a new model container and creating a Docker image.

To make the model deployment process even simpler, Clipper provides a library of *model deployers* for common types of models. If your model can be deployed with one of these deployers, you no longer need to write a model container, create a Docker image, or even figure out how to save a model. Instead, you provide your trained model directly to the model deployer function. The model deployer takes care of saving the model and building a Docker image that is compatible with your model type.

Currently, Clipper provides three model deployers for three common types of models:

+ One to deploy arbitrary Python functions (within some constraints): [[Docs]](http://docs.clipper.ai/en/release-0.2/#pure-python-functions)
+ One to deploy PySpark models along with pre- and post-processing logic: [[Docs]](http://docs.clipper.ai/en/release-0.2/#pyspark-models)
+ One to deploy R models: [[Install]](https://github.com/ucbrise/clipper/tree/develop/containers/R) [[Docs]](https://github.com/ucbrise/clipper/blob/develop/containers/R/rclipper_user/vignettes/Rclipper.Rmd)

If you are using a model deployer, consult the deployer's documentation on how to deploy a model.

If the model you are hoping to deploy cannot use one of these model deployers, you will have to write your own model container. The Clipper GitHub repository contains several [example model container implementations](https://github.com/ucbrise/clipper/tree/develop/containers/python) that you can base your own implementation on.

Once you've written a model container and packaged it into a Docker image along with any dependencies, you can
deploy it with: [`ClipperConnection.deploy_model`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.deploy_model).


Clipper deploys each model in its own Docker container. After deploying the model, Clipper uses the
container manager you provided to start a container for this model and create an RPC connection with the Clipper query frontend, as illustrated below (the changes to the cluster state are highlighted in red).

{{< figure src="/images/deploy_model.png" >}}

#### Input Types

When you deploy models and register applications, you must specify the input type that the model or application expects. The type that you specify has implications for how Clipper manages input serialization and deserialization. From the user's perspective, the input type affects the behavior of Clipper in two places. In the "input" field of the request JSON body, applications will reject requests where the value of that field is the wrong type. And the deployed model function will be called with a list of inputs of the specified type.

The input type can be one of the following types:
+ *"ints"*: The value of the "input" field in a request must be a JSON list of ints. The model function will be called with a list of numpy arrays of type `numpy.int`.
+ *"floats"*: The value of the "input" field in a request must be a JSON list of doubles. The model function will be called with a list of numpy arrays of type `numpy.float32`.
+ *"doubles"*: The value of the "input" field in a request must be a JSON list of doubles. The model function will be called with a list of numpy arrays of type `numpy.float64`.
+ *"bytes"*: The value of the "input" field in a request must be a Base64 encoded string. The model function will be called with a list of numpy arrays of type `numpy.int8`.
+ *"strings"*: The value of the "input" field in a request must be a string. The model function will be called with a list of strings.


### Applications

Instead of automatically creating a REST endpoint when you deploy a model, Clipper introduces a layer of indirection: the application. Clients query a specific application in Clipper, and the application routes the query to the correct model. This allows multiple applications to route queries to the same model, and in the future will allow a single application to route queries to multiple models. A single Clipper cluster can have many applications registered and many models deployed at once.

When you register an application you configure certain elements of the application's behavior. These include:
+ The name to give the REST endpoint.
+ The input type that the application expects (Clipper will ensure applications only route requests to models with matching input types).
+ The latency service level objective (SLO) specified in microseconds. Clipper will manage how it schedules and routes queries for an application based on the specified service level objective. For example, Clipper will set the amount of time it allows requests to spend queued before being sent to the model based on the service level objective for the application requesting the prediction. In addition, Clipper will respond to requests by the end of the specified SLO, even if it has not received a prediction back from the model.
+ The default output: Clipper will respond with the default output to requests if a real prediction isn't available by the end of the service level objective.

You can register an application with
[`ClipperConnection.register_application`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.register_application).


When you register an application with Clipper, it creates a REST endpoint for that application:

```
URL: /<app_name>/predict
Method: POST
Data Params: {"input": <input>}
```

{{< figure src="/images/register_app.png" >}}

#### Linking a Model

After you register an application and deploy a model,  you must link an application to a model. This linking step tells Clipper to route requests received by that application's REST endpoint to the specified model for predictions.

You can link a model to an application with [`ClipperConnection.link_model_to_app`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.link_model_to_app).

{{< figure src="/images/link_model.png" >}}

### Model Versioning

Machine learning models are rarely static. Instead, data science tends to be an iterative process, with new and improved models being developed over time. Clipper supports this workflow by letting you deploy new versions of models. When you link an application to a model, you do not specify which version of the model the application links to. Instead,
an application always routes queries to the current version of its linked model.

Every model deployed to Clipper must have a version. A given version of a model is immutable, and once deployed
to Clipper cannot be updated or changed. Clipper just treats versions as unique string identifiers, so you have significant flexibility over your versioning scheme. Common choices include numeric versioning, Git hashes (e.g. of the model code), or semantic versioning. Versions in Clipper are not inherently ordered, Clipper just tracks which of the deployed versions is the currently active one for each model.

#### Model Updates

When a new version of a model is deployed (through a call to `deploy_model` or via using one of the model deployers), Clipper will automatically start routing requests to the new version.

{{< figure src="/images/update_model.png" >}}

#### Model Rollbacks

Sometimes the "new and improved" model is not actually improved. If you deploy a model that isn't working well, you can roll back to any previous version: [`ClipperConnection.set_model_version`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.set_model_version).

This just changes which version of the model the application's routes requests to.

{{< figure src="/images/rollback_version.png" >}}


### Replicating a Model

Many machine learning models are computationally expensive and a single instance of the model may not meet the throughput demands of a serving workload. To increase prediction throughput, you can add additional replicas of a model. This creates additional Docker containers running the same model. Clipper will act as a load-balancer and distribute incoming requests across the set of available model replicas to provide higher throughput.

You can set the number of replicas of a model with: [`ClipperConnection.set_num_replicas()`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.set_num_replicas).

If there are currently less than the specified number of replicas active, Clipper will launch more. If there are more than the specified number of replicas, Clipper will stop some.

{{< figure src="/images/add_replicas.png" >}}


## Querying Clipper

Clipper exposes a REST prediction endpoint for each application you register in Clipper that you
can use to request predictions.

The REST endpoint for an application is located at

```
http://<query_address>/<application-name>/predict
```

You can use the `ClipperConnection` object to get the query address:

```py
query_addr = clipper_conn.get_query_addr()
```

This REST endpoint expects HTTP POST requests with the `Content-type` header field
set to `application/json` and the body as a JSON string with the following format

```json
  {
   "input" := [double] | [int] | [byte] | [float] | string 
  }
```

The "input" field requires that the type of the value matches the
input type specified when registering the application.

For example, if you set the input type of your application to "doubles", the following would be a valid
request body:

```json
  {
   "input": [1.1, 2.2, 3.3]
  }
```

If the input type of your application is "strings", you must supply a single string as the value for the
"input" key. This string may itself be JSON, and Clipper will ensure that it is properly escaped and propagated
to the model.

```json
  {
   "input": "Hello world. This is a string."
  }
```

You can find examples of querying Clipper in the `examples/` directory of
the Clipper repo.

+ [A simple example](https://github.com/ucbrise/clipper/blob/develop/examples/basic_query/example_client.py)

## Inspecting Cluster Configuration

The `ClipperConnection` object has several methods to inspect various aspects of the Clipper cluster.

+ [`ClipperConnection.get_all_apps()`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.get_all_apps): List all of the applications.
+ [`ClipperConnection.get_all_models()`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.get_all_models): List all of the models.
+ [`ClipperConnection.inspect_instance()`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.inspect_instance): Clipper tracks several performance metrics that you can inspect at any time.
+ [`ClipperConnection.get_clipper_logs()`](http://docs.clipper.ai/en/release-0.2/#clipper_admin.ClipperConnection.get_clipper_logs): You can fetch the raw container logs from all of the Clipper docker containers. The command will print the paths to the log files for further examination. You can figure out which logs belong to which container based on the unique Docker container ID in the log filename.



{{% notice info %}}
See the [Troubleshooting user guide]({{< relref "troubleshooting.md" >}}) for specific help on debugging
some common problems.
{{% /notice %}}

## Stopping Clipper

If you run into issues and want to completely stop Clipper, you can do this by calling [`ClipperConnection.stop_all()`](http://docs.clipper.ai/en/latest/#clipper_admin.ClipperConnection.stop_all). This will stop all Clipper processes and any Docker containers that were started via the Clipper admin API.


{{% notice note %}}
This guide is based on a [Clipper tutorial](https://github.com/ucbrise/risecamp/blob/master/clipper/clipper_exercises.ipynb) presented at [RISE Camp 2017](https://risecamp.berkeley.edu/).
{{% /notice %}}
