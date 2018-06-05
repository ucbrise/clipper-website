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
If you are using `KubernetesContainerManager`, You can query the metric address by calling `clipper_conn.get_metric_addr()`.

Please note that Prometheus UI is for debug purpose only. You can view certain metric and plot the timeseries. But for better visualization, we recommend [Grafana](https://grafana.com/). Grafana has default support for Prometheus Client. Feel free to checkout [examples/monitoring](https://github.com/ucbrise/clipper/tree/develop/examples/monitoring) for example of displaying Clipper metrics in Grafana dashboard.

## Available Metrics
Clipper provides series of latency and throughput metrics by default. In particular, we provide latency and throughput metrics for different granularity: from metric on each prediction call in model container to an application. 

To see it in detail, feel free to run the example and browse the Prometheus server.

## User Defined Metrics
You can also add user defined metrics in your application. The API is simple. When you write your predict function, just add the following:

-  `import clipper_admin.metric as metric` to import the clipper.metric sub-package
-  `metric.add(metric_name, metric_type, metric_description, optional_histogram_bucket)` to add a metric.  The metric type is defined in [Prometheus Data Types](https://prometheus.io/docs/concepts/metric_types/)
- `metric.report(metric_name, metric_data)` to report a metric. 

Please checkout a detailed [example/user_defined_metric](https://github.com/ucbrise/clipper/tree/develop/examples/user_defined_metric) with user defined metric. In the example, we will add metrics for a sklearn spam prediction model. 


## [WIP] System Metrics
Clipper does not collect physical system metrics like the CPU or memory usage. Please follow the progress [here](https://github.com/ucbrise/clipper/issues/421) and feel free to [contribute](/contributing)!
