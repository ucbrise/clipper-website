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

## Docker Container Manager

The Docker container manager runs Clipper on the local Docker daemon directly.
This container manager is useful for development and local experimentation without the need to set up an enterprise-grade container orchestration framework, but is not recommended for production use cases.
In addition, it uses the Python Docker SDK to interface with Docker, and one of the limitations of the library is that it can access the local Docker daemon.
This means that you must issue any Clipper admin commands while logged in to the machine you wish to run Clipper on.


## Kubernetes Container Manager
<a name="k8s-container-manager"></a>

The Kubernetes container manager runs Clipper on an existing Kubernetes cluster. This container manager
creates a separate deployment for the Query Frontend, the Management Frontend, the Redis configuration
database, and each deployed model (technically, each version of each model).  It will also create a
corresponding [NodePort Service](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)
for the Query Frontend and Management Frontend. You can then query Clipper from any node in the
Kubernetes cluster.

We have strived to make deploying Clipper on Kubernetes as simple as possible. However, Kubernetes
is a complicated, enterprise orchestration framework so there are a few things you need to pay attention to.

### Kubernetes Credentials

In order for Clipper to create and modify Kubernetes objects, it must have the appropriate credentials.
THe Kubernetes container manager expects to read the credentials from `~/.kube/config` or the path set
by the `KUBECONFIG` environment variable. This is the same authentication that the
`kubectl` command-line tool uses. This means that those credentials must be present on any machine
that creates a Kubernetes container manager (e.g your laptop, your staging server).

If you use authenticate your Kubernetes cluster in a different way, please let us know
by filing an issue. We are actively looking to improve our support for Clipper deployments
on Kubernetes.

### Container Registry

When using the Clipper model deployers or calling `ClipperConnection.build_and_deploy_model` directly,
Clipper builds a new Docker image for the model. Each of these methods takes an optional `container_registry`
argument, which is the address of a Docker container registry to push the newly built image to.
When deploying on Kubernetes, you must ensure that this field is set to a valid container registry that you
have already authenticated with (by calling `docker login` from the command line).
Furthermore, you must ensure that both the local machine where you are building the model, and the
Kubernetes cluster, have access to the registry. This ensures that you can push the newly built
image containing the model to the registry, and that Kubernetes can pull the model image onto the
cluster to actually run the Docker container.

### Redis and Persistence

Similar to the Docker container manager, if you do not supply the Kubernetes container manager
with the address of an existing Redis instance, Clipper will create a Redis Kubernetes Deployment
for you. However, this deployment will not be backed by persistent storage, and so the Redis
state will only persist for the lifetime of the pod. If the node dies or the container gets deleted,
you will lose the Redis state containing all of the Clipper configuration data.

For production scenarios, we recommend running your own fault-tolerant Redis cluster (either
within Kubernetes or in a separate service altogether), rather than using the default one
supplied by Clipper.

### Known limitation: Query Frontend Scaleout

Kubernetes makes it simple to horizontally scale a service by increasing or decreasing
the number of replicas of a pod. Clipper uses precisely this mechanism to scale
the number of replicas of a model container. However, scaling the query frontend
service to multiple replicas (e.g. to make it highly available), is significantly
more complicated. The complication arises primarily from the fact that model
containers connect to the query frontend with long-lived RPC connections (over TCP).
These connections last until either the query frontend or the model container dies
and kills the connection. As a result, these long-lived connections must be correctly re-balanced
when query frontend replicas are created or destroyed. Without a re-balancing
mechanism, the query frontend and model container deployments cannot scale independently.

Clipper does not currently provide any support for this re-balancing. The query frontend
is stateless, and so there is no architectural reason why it cannot be replicated, but you
will need to manage this re-balancing yourself. We are currently investigating the best way
to support this use case.


<!-- The problem is that when a model container connects to an instance of the query frontend, -->
<!-- it connects with a long-lived RPC connection (over TCP) that lasts until either the query -->
<!-- frontend or the model container dies, thus killing the connection. Consider the following -->
<!-- example deployment, where you have a model deployed in a pod of size 4 (4 replicas of the -->
<!-- model), all connected to the same query frontend container in a pod of size 1. -->
<!--  -->
<!-- {{< figure src="/images/k8s_query_scaleout_1.png" >}} -->
<!--  -->
<!-- If we then decide to scale out the query frontend pod to have two containers, the expected -->
<!-- behavior would be for the 4 model containers to load balance evenly across the two query -->
<!-- frontend containers like this: -->
<!--  -->
<!-- {{< figure src="/images/k8s_query_scaleout_2.png" >}} -->
<!--  -->
<!--  -->
<!-- Instead, because the connection between a model container and query frontend is long-lived, -->
<!-- the addition of another query frontend container does not trigger the existing model containers -->
<!-- to rebalance. Any new model replicas  -->

