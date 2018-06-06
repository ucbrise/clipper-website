+++
title= "Creating a Custom Model Container"
date= 2018-03-13T10:23:10-07:00
description = ""
draft= false
weight = 12
+++

If none of the provided [model deployers](http://docs.clipper.ai/en/latest/#model-deployers) meet your needs, you will need to create your own model container. In this tutorial, we will walk through two common use cases for creating your own model containers.

1. Your prediction function can still be pickled (see the [cloudpickle documentation](https://github.com/cloudpipe/cloudpickle) to determine whether your function can be pickled), but requires custom packages
that are not available via Pip.
2. Your prediction function cannot be pickled, and you want to hardcode the model inside the container.

## Installing Custom Python Packages

If the only reason you cannot use one of the pre-existing model deployers is because your function relies
on custom Python packages that cannot be installed via pip, creating a custom model container is straightforward. You will create a new Docker image to serve as the base image for the Python closure
deployer. To create this image, create a Dockerfile with the following contents.

First, start with the Python deployers base image as the base image for your new Docker image:

+ Python 2.7: `FROM clipper/python-closure-container:0.3`
+ Python 3.5: `FROM clipper/python35-closure-container:0.3`
+ Python 3.6: `FROM clipper/python36-closure-container:0.3`

Next, install the custom Python packages into the Docker container.
If they are local modules that need to be copied, use the [COPY](https://docs.docker.com/engine/reference/builder/#copy) command. If you need to download or compile anything, use the [RUN](https://docs.docker.com/engine/reference/builder/#run) command.

For example, to create a custom model container for Python 3.6 that includes some local Python modules,
you would write the following Dockerfile:

```docker
FROM clipper/python36-closure-container:0.3

# Create a directory to copy the local module into
RUN mkdir -p /python-deps

# Copy the module from your local filesystem into the Docker image
COPY /path/to/local/module /python-deps/

# Add the module to your PYTHONPATH so the Python interpreter
# can find it
ENV PYTHONPATH="$PYTHONPATH:/python-deps/
```

Once you have create the Dockerfile, you must build it to create a Docker image. From the
directory where the Dockerfile is saved, run the following command:

```console
docker build -t custom-model-image .
```

{{% notice note %}}
All files referenced in COPY or ADD commands must be inside the *context* of the build command,
and that it will recursively copy entire directory trees.
{{% /notice %}}


Once you've successfully built your custom base image, specify it as the base image in
the Python closure deployer. For example, to use your custom base image to deploy a
Python function called `myfunc` as a model
named "custom-model" with version 1 that takes strings as input, you would issue the following command:

```python
deploy_python_closure(clipper_conn, "custom-model", 1,
            "strings", myfunc, base_image='custom-model-image')
```

### Optional: Push the image to a Docker registry
If you want to be able to use the Docker image on other machines, push it to a Docker registry
using the [`docker push`](https://docs.docker.com/engine/reference/commandline/push/) command.


## Writing your own container implementation

If your prediction function cannot be pickled, you will need to explicitly package the function in the container.

A more complete guide will be coming soon. In the meantime, you can look at the model deployer [container implementations](https://github.com/ucbrise/clipper/tree/develop/containers/python) and [Dockerfiles](https://github.com/ucbrise/clipper/tree/develop/dockerfiles) to see some examples of implementing your own model container.
