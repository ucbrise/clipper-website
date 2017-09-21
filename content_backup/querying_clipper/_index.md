+++
date = "2017-05-23T12:10:39-07:00"
icon = ""
title = "Querying Clipper"
weight = 2
chapter = false

+++

## Sending a Prediction Request

Clipper exposes a REST prediction endpoint for each application you register in Clipper that you
can use to request predictions.

Each application is associated with exactly one model, and any updates to that model (e.g. by
deploying a new version of the model) will automatically be performed and new requests to that
application will query the new version of the model.

The REST endpoint for an application is located at

```
http://<clipper-hostname>:1337/<application-name>/predict
```

This REST endpoint expects HTTP POST requests with the `Content-type` header field
set to `application/json` and the body as a JSON string with the following format

```json
  {
   "input" := [double] | [int] | [byte] | [float] | string 
  }
```


The `"input"` field requires that the type of the value matches the
input type specified when registering the application. If you aren't sure what input
type your application expects, you can use the Clipper manager to inspect the application
from the Python REPL.

```py
# after creating a clipper_manager.Clipper() instance:
print(clipper.get_app_info("my_application_name"))
```

For example, if you registered an application with input type "doubles", prediction
requests must provide a list of doubles as the value associated with the "input" key in
the JSON request object.


{{% notice note %}}
If your application was registered with input type "strings", then the
"input" must be a single string, not a list of "strings".
{{% /notice %}}

You can find examples of querying Clipper in the `examples/` directory of
the Clipper repo.

+ [A simple example](https://github.com/ucbrise/clipper/blob/develop/examples/basic_query/example_client.py)



<!-- ## Parsing the Prediction Response -->
<!--  -->
<!-- If the request was successful, you  -->







