+++
date = "2017-05-20T19:16:04-07:00"
title = "Image Classification Tutorial"
toc = true
weight = 3

+++


This tutorial will walk you through the process of starting Clipper,
creating an application, querying the application, and deploying models
to improve application accuracy.

The tutorial uses the Clipper client management Python library for controlling
Clipper. While this is the simplest way to manage Clipper, the client library
is simply a convenience wrapper around a standardized management REST interface
which can be queried with any REST client.


## Setup

The tutorial runs Clipper in Docker containers and orchestrates
them with Docker-Compose, so you must have Docker and Docker-Compose
installed. The tutorial can be run in two modes, local or remote.

Running in local mode will start Clipper locally on your laptop. Running
in remote mode will start Clipper on the machine you specify. When
running the tutorial remotely, you must have SSH access to the machine.
If running on EC2, you can use AMI `ami-3ba0f05b`,
an Ubuntu image that has Docker and Docker-Compose installed.

The tutorial uses Python and Jupyter notebooks to interact with Clipper and
train models. You can install the Python dependencies needed to run
the tutorial with:

```
pip install -r requirements.txt
```

Note these dependencies must be installed for both the local and remote
versions of the tutorial.

You must also clone or download the [Clipper repo](https://github.com/ucbrise/clipper).

```sh
git clone --recursive https://github.com/ucbrise/clipper.git
```

## Running the tutorial

To start the tutorial, go to the tutorial directory
([`examples/tutorial`](https://github.com/ucbrise/clipper/tree/release-0.1/examples/tutorial)) and start the Jupyter server.

```
$ jupyter notebook
```
and open the `tutorial_part_one.ipynb` notebook. The tutorial is self-guided
from there.

Happy serving!

{{% notice info %}}
If you run into any problems or find anything unclear while doing the tutorial,
please file a [GitHub issue](https://github.com/ucbrise/clipper/issues/new)
or contact us through the Clipper mailing list (<clipper-dev@googlegroups.com>) so we
can improve it.
{{% /notice %}}
