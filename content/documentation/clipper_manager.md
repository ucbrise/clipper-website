+++
date = "2017-05-23T09:08:41-07:00"
title = "User Guide"
toc = true
weight = 1

+++

## Getting Started

You can use the Clipper Admin Python tool to programatically start and manage a Clipper cluster.
If you want to manage the cluster interactively, you can import the tool into an interactive Python
session or Jupyter notebook and issue commands one at a time.

The Clipper Admin tool can be installed with Pip. We recommend
using [Anaconda](https://www.continuum.io/downloads) as your Python
installation.

```
pip install clipper_admin
```

## Key Concepts

A model deployment in Clipper has three elements:

1. *An application*
2. *A model*
3. *Model containers*


### Applications

An application in Clipper corresponds to a REST endpoint that can be queried to get predictions.
A general guideline is that each client application that wants to consume predictions from Clipper
should register its own application. So for example, if you wanted to use Clipper to recommend music
and to predict sound quality, you would register two applications with Clipper.

When registering an application, a client specifies some additional information that governs how Clipper
will handle incoming requests. In particular, the client specifies an input type for the application,


     TODO: picking a default output
     TODO: picking an application slo

A Clipper application is the client-facing part of Clipper. Each application exposes
a REST endpoint that can be queried to get predictions from a model. When an application
is registered, the person

Client's that consume
applicat

### Models

### Model Containers

## Other topics

### Input types

A user guide is coming soon.
In the meantime, you can check out the [API Documentation](http://docs.clipper.ai).

## Deploying a Model


## Container Managers



## Changes

### 0.2.0
The 0.2 release of Clipper introduced a significant breaking change in the Clipper admin API.
