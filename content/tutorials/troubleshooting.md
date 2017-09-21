+++
title= "Troubleshooting"
date= 2017-09-13T10:22:56-07:00
description = ""
draft= false
weight = 4
+++

Guidance on how to identify and fix some common errors.


### Identifying the cause of default predictions

There are a few reasons why your application may be returning default predictions.
Your first debugging clue is the "default\_explanation" field in the response body.

#### No connected models found for query

This means that Clipper could not find any model containers to route your request to.
Here are some steps to debug this problem.

1. *Is your model linked to your application?*

      Run the following command to see whether your application has a model linked to it:
      ```py
      clipper_conn.get_linked_models(app_name="<your-app-name>")
      ```
      If you forgot to link your model to your application, you can do so with:
      ```py
      clipper_conn.link_model_to_app(app_name="<your-app-name>", model_name="<your-model-name>")
      ```

2. *Is your model container running?*

      As with any code, your model container may have contained
      a bug which caused it to crash or render it unable to initialize correctly.
      For example, if you are using the Python model deployer and your deployed Python model referenced a library
      that the container was unable to resolve, your container will crash due to an uncaught `ImportError` when it tries
      to load your model. You can check the number of live Docker containers for your model with this command:
      ```py
      clipper_conn.cm.get_num_replicas("name"="<your-model-name>", version="<your-model-version>")
      ```
      If this returns 0, your model container crashed for some reason. To identify why the container crashed, inspect the
      container logs for an error message about why the container exited.

      You can fetch the logs for all Docker containers associated with Clipper 
      (including containers that have crashed) with `clipper_conn.get_clipper_logs()`. You will need
      to hunt around in the logs a little bit to identify the right log file, but each log file name includes
      the Docker container ID of the container it was collected from. If you are running Clipper using the
      DockerContainerManager, you can use `docker ps -a --filter label=ai.clipper.container.label` to list
      all of the Docker containers associated with Clipper. This may help you identify the correct log file more easily.

3. *Has your model container finished initializing?*

      Model containers can take a long time to initialize. For large models, it can take tens of seconds
      to load and deserialize the model state, and some machine-learning frameworks have non-trivial initialization
      overheads. If you've determined that your model container is still running (from step 2), inspect the logs again
      to see if it has finished initializing. When the container has fully initialized, it will log "Serving predictions for
      <your-input-type> input type" (where <your-input-type> will be the actual input type of the container). If you do not
      see this message logged yet and your container is still running, it is most likely still initializing and will finish
      soon.


#### Failed to retrieve a prediction response within the specified latency SLO

If you see this message in the "default\_explanation" field, it means that at some point a
model container for your model successfully connected to Clipper, but Clipper did not receive
a prediction from the container in time for the current request. Here are some steps to debug this
problem.

1. *Is your application SLO too low?*

      When you register an application, you set the latency SLO -- the amount of time that Clipper
      will wait for a prediction from the model container before returning the default response.
      If you set this value too low, Clipper will return a response before your model is done 
      rendering a prediction. Each model container logs how long each prediction took, and the Clipper
      metrics track the latency distribution of each model container. Run the following command to inspect
      the Clipper metrics:

      ```py
      clipper_conn.inspect_instance()
      ```
      
      This command will return a JSON object. The "histograms" field includes latency histograms
      for every application and every model registered in Clipper. Find the relevant histograms for your
      model and application. If the mean prediction latency for your model is higher than the latency SLO you
      set, your model is too slow. You can fix this by creating a new application with a higher SLO and
      linking your model to that application.

2. *Did your model container crash?*

      It's possible that your model container initialized without problems and connected to Clipper,
      but then crashed during actual prediction processing. To determine whether your model container
      has crashed, repeat step 2 from the previous section to get the number of replicas for a model
      and inspect the container logs.

      If you determine that your model container has crashed, the container log should have a stack trace
      that will help you identify the problem. One common reason that model containers crash, especially
      when deploying using one of the provided [model deployers](http://docs.clipper.ai/en/develop/#model-deployers),
      is that the prediction function has the wrong interface. Remember, the function must accept a
      *list of inputs* of the specified input type. And it must return a *list of strings*. A common
      mistake is to deploy a prediction function that operates on a single input at a time,
      rather than processsing a list of inputs at a time as a batch.


{{% notice info %}}
The commands to inspect the number of model containers and fetch container logs are just convenience
wrappers around Docker or Kubernetes commands. If you are comfortable with the `docker` or `kubectl`
command line tools, you can just inspect the containers directly.
{{% /notice %}}
