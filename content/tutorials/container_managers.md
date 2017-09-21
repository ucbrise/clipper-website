+++
title= "Container Orchestration"
date= 2017-09-13T10:22:30-07:00
description = ""
draft = false
weight = 2
+++


Clipper is built on top of Docker containers. A running Clipper cluster consists of a collection of Docker containers communicating with each other over the network. As you issue commands against Clipper using the admin tool, you are communicating with these containers as well as creating new ones or destroying existing ones.

The main API for interacting with Clipper is exposed via a [`ClipperConnection`](http://docs.clipper.ai/en/develop/#clipper-connection) object. This is your handle to a Clipper cluster. It can be used to start, stop, inspect, and modify the cluster.

In order to create a `ClipperConnection` object, you must provide it with a [`ContainerManager`](http://docs.clipper.ai/en/develop/#container-managers).
While Docker is becoming an increasingly standard mechanism for deploying applications, there are many different tools for managing Docker containers.
These tools broadly fall into the category of *Container Orchestration frameworks*.
Some popular examples are [Kubernetes](https://kubernetes.io/), [Docker Swarm](https://docs.docker.com/engine/swarm/), and [DC/OS](https://dcos.io/).
One of the reasons Clipper is designed to be fully containerized is to make the system as general as possible and support many different deployment scenarios.
Within the Clipper admin tool, we abstract away all of the Docker container-specific commands behind the `ContainerManager` interface.
The `ClipperConnection` object makes Clipper-specific decisions about how to issue commands, and then makes any changes to the Docker configuration (for example, to launch a container for a newly deployed model) through the `ContainerManager`.
To support different container orchestration frameworks that manage Docker containers in different ways, we create different implementations of the `ContainerManager` interface.

Clipper currently provides two `ContainerManager` implementations: the `DockerContainerManager` and the `KubernetesContainerManager`.

### Docker Container Manager

The Docker container manager runs Clipper on the local Docker daemon directly.
This container manager is useful for development and local experimentation without the need to set up an enterprise-grade container orchestration framework, but is not recommended for production use cases.
In addition, it uses the Python Docker SDK to interface with Docker, and one of the limitations of the library is that it can access the local Docker daemon.
This means that you must issue any Clipper admin commands while logged in to the machine you wish to run Clipper on.

<!-- {{% notice note %}} -->
<!-- If you are upgrading from Clipper 0.1, note that the  -->
<!-- {{% /notice %}} -->


### Kubernetes Container Manager

Credentials

Container registry visible to the K8s cluster

Known limitation: Query scaleout


