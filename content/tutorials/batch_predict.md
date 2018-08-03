+++
title= "Batch Predict"
date= 2017-09-12T23:45:24-07:00
description = ""
toc = false
weight = 13
+++

## Batch Prediction Interface

### Request
Since release 0.3.0, Clipper has a batch prediction inferface for query. Instead of sending: 
```json
{ "input" := [double] | [int] | [byte] | [float] | string }
```
You can now send:
```json
{ "input_batch" := [[double] | [int] | [byte] | [float] | string] }
```
Clipper will return prediction for the batch in the original order. 

### Response
Instead of returning:
```json
{"query_id":1,"output":4.0,"default":false}
```
Clipper will now return:
```json
{
	"batch_predictions":
	[
		{"query_id":2,"output":4.0,"default":false},
		{"query_id":3,"output":5.0,"default":false}
	]
}
```

### Note
If a request contain both `input` and `input_batch`, `input` will take precedence and `input_batch` will be ignored. 