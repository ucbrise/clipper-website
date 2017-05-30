+++
date = "2017-05-23T09:25:27-07:00"
icon = "<b>7. </b>"
title = "Troubleshooting"
weight = 7
chapter = false
draft = true

+++

Here are some common problems users run into when using Clipper and how to solve them.

If you encounter an error not on this list, please file a GitHub issue describing
the problem and how to reproduce it and we will help you diagnose and fix the problem.

## Error


## Docker related errors

+ Docker not installed
+ Docker requires sudo

## Python related errors


## Always seeing default predictions

## Python deployment problems

+ Clipper manager says my model was deployed successfully, but I only see default predictions.



## Diagnosing where the problem occurred


## I started Clipper and registered a model, but when I query the Redis instance with `redis-cli` I don't see anything?

+ Solution: we use multiple redis databases
