+++
title= "Metric Monitoring"
date= 2018-03-13T10:23:10-07:00
description = ""
draft= false
weight = 10
+++

In starting Clipper v0.3.x, Clipper reports metrics to a [Prometheus](https://prometheus.io/) server

## Prometheus Server
We use prometheus as the metric tracking system. Once you spin up a clipper query frontend and a model containers.
If you are using `DockerContainerManager`, You can view prometheus UI at: [`http://localhost:9090`](http://localhost:9090).
If you are using `KubernetesContainerManager`, You can query the metric address by calling `get_metric_addr()`.

Please note that Prometheus UI is for debug purpose only. You can view certain metric and graph the timeseries. But for better visualization, we recommend [Grafana](https://grafana.com/). Grafana has default support for Prometheus Client. Feel free to checkout [examples/monitoring](https://github.com/ucbrise/clipper/tree/develop/examples/monitoring) for example of displaying Clipper metrics in Grafana.

## Available Metrics
So far, you will be able to view latency metrics for each model container as well as overall latency and throughput broken down by applications. 
