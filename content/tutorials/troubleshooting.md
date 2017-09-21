+++
title= "Troubleshooting"
date= 2017-09-13T10:22:56-07:00
description = ""
draft= false
weight = 4
+++

Guidance on how to identify and fix some common errors.


## Always get default predictions

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

This means that at some point a model container for the specified model successfully
connected to Clipper, but Clipper cannot get any predictions.

1. *Is your application SLO too low?*

2. *Did your model container crash?*
Wrong output type, wrong output length, errors


3. *

First

If you are able to get Clipper running



{{% notice info %}}
The commands to inspect the number of model containers and fetch container logs are just convenience
wrappers around Docker or Kubernetes commands. If you are comfortable with the `docker` or `kubectl`
command line tools, you can just inspect the containers directly.
{{% /notice %}}
