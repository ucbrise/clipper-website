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


The [Container Orchestration]({{< relref "container_managers.md" >}}) user guide has more information
about picking a container manager.

#### Connecting to a Clipper Cluster



## Model Deployment

Once

A model deployment in Clipper has three elements:

1. *An application*
2. *A model*
3. *Model containers*

### Application

#### Registering an application

#### Input Types

### Model

#### Deploying a model

### Model Containers

## Querying Clipper

## Inspecting Cluster Configuration

{{% notice note %}}
See the [Troubleshooting user guide]({{< relref "troubleshooting.md" >}}) for specific help on debugging
some common problems.
{{% /notice %}}


