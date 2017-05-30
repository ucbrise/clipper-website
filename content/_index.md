+++
date = "2017-05-20T17:53:26-07:00"
title = "Clipper"
toc = false
weight = 5
chapter = false

+++

## What is Clipper?

Clipper is a prediction serving system that sits between user-facing applications and a wide range of commonly used machine learning models and frameworks.

## What does Clipper do?

* Clipper **simplifies integration of machine learning techniques** into user facing applications by providing a simple standard REST interface for prediction and feedback across a wide range of commonly used machine learning frameworks.  *Clipper makes product teams happy.*


* Clipper **simplifies model deployment** and **helps reduce common bugs** by using the same tools and libraries used in model development to render live predictions.  *Clipper makes data scientists happy.*



* Clipper **improves throughput** and ensures **reliable millisecond latencies** by introducing adaptive batching, caching, and straggler mitigation techniques.  *Clipper makes the infra-team less unhappy.*

* Clipper **improves prediction accuracy** by introducing state-of-the-art bandit and ensemble methods to intelligently select and combine predictions and achieve real-time personalization across machine learning frameworks.  *Clipper makes users happy.*


## Why are we building Clipper?

We are group of researchers in the UC Berkeley [RISE Lab](https://rise.cs.berkeley.edu/) studying the fundamental challenges around taking machine learning to production.  In collaboration with leading industrial and research organizations ([sponsors](https://rise.cs.berkeley.edu/sponsors/)), we identified model deployment as one of the next big challenges in the wide-scale adoption of AI technologies.

Deploying trained machine-learning models into production today is an ad-hoc, labor-intensive, and error-prone process. This creates an enormous impediment to building and maintaining user-facing applications that incorporate machine-learning.

Clipper is designed to simplify this process by decoupling applications that
consume predictions from trained models that produce predictions.
Clipper is a robust, high-performance serving system that can scale to thousands of requests per second and provide 
responses that meet latency service level objectives on the order of milliseconds.
As a result, Clipper can be safely incorporated into a production serving stack without negatively
impacting application latencies.

At the same time, Clipper allows data scientists to easily deploy trained models to production.
Data science is an iterative process, and simplifying the model deployment process allows
data scientists to more easily experiment with new features and models to quickly improve
application accuracy. Data scientists deploy models to Clipper with the same code used for
training, eliminating a common class of bugs in machine-learning that arise from code duplication.
And Clipper supports deploying models trained in many machine learning frameworks and implemented
in a variety of programming languages to support the rich ecosystem of data science tools available today.



## Key Features

+ Deploy models trained in your choice of framework to Clipper with a few lines of code by using an existing model container or writing your own
+ Easily update or add models to running applications
+ Use adversarial bandit algorithms to dynamically select best model for prediction at serving time
+ Set latency service level objectives for reliable query latencies
+ Run each model in a separate Docker container for simple cluster management and resource allocation
+ Deploy models running on CPUs, GPUs, or both in the same application
