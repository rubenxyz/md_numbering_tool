## Introduction

The client for Python provides a seamless interface to interact with fal.

## Installation

First, add the client as a dependency in your project:

## Features

### 1\. Call an endpoint

Endpoints requests are managed by a queue system. This allows fal to provide a reliable and scalable service.

The `subscribe` method allows you to submit a request to the queue and wait for the result.

-   [Python](https://docs.fal.ai/clients/python#tab-panel-8)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-9)

```
import fal_clientdef
on_queue_update(update)
: if isinstance(update, fal_client.InProgress)
: for log in update.logs: print(log["message"])
result = fal_client.subscribe( "fal-ai/flux/dev", arguments={ "prompt": "a cat", "seed": 6252023, "image_size": "landscape_4_3", "num_images": 4 }, with_logs=True, on_queue_update=on_queue_update,)
print(result)
```

### 2\. Queue Management

You can manage the queue using the following methods:

#### Submit a Request

Submit a request to the queue using the `queue.submit` method.

-   [Python](https://docs.fal.ai/clients/python#tab-panel-10)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-11)

```
import fal_client

handler = fal_client.submit(
  "fal-ai/flux/dev",
  arguments={
      "prompt": "https://optional.webhook.url/for/results"
  },
)

result = handler.get()
print(result)
```

This is useful when you want to submit a request to the queue and retrieve the result later. You can save the `request_id` and use it to retrieve the result later.

#### Check Request Status

Retrieve the status of a specific request in the queue:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-12)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-13)

```
status = fal_client.status("fal-ai/flux/dev", request_id, with_logs=True)
```

#### Retrieve Request Result

Get the result of a specific request from the queue:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-14)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-15)

```
result = fal_client.result("fal-ai/flux/dev", request_id)
```

### 3\. File Uploads

Some endpoints require files as input. However, since the endpoints run asynchronously, processed by the queue, you will need to provide URLs to the files instead of the actual file content.

Luckily, the client library provides a way to upload files to the server and get a URL to use in the request.

-   [Python](https://docs.fal.ai/clients/python#tab-panel-16)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-17)

```
url = fal_client.upload_file("path/to/file")
```

### 4\. Streaming

Some endpoints support streaming:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-18)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-19)

```
import fal_clientdef
stream()
: stream = fal_client.stream( "fal-ai/flux/dev", arguments={ "prompt": "a cat", "seed": 6252023, "image_size": "landscape_4_3", "num_images": 4 }, ) 
for event in stream: print(event)
if __name__ == "__main__": stream()
```

### 5\. Realtime Communication

For the endpoints that support real-time inference via WebSockets, you can use the realtime client that abstracts the WebSocket connection, re-connection, serialization, and provides a simple interface to interact with the endpoint:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-22)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-23)

### 6\. Run

The endpoints can also be called directly instead of using the queue system.

-   [Python](https://docs.fal.ai/clients/python#tab-panel-20)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-21)

```
import fal_clientresult
= fal_client.run( "fal-ai/flux/dev", arguments={ "prompt": "a cat", "seed": 6252023, "image_size": "landscape_4_3", "num_images": 4 },)
print(result)
```

## API Reference

For a complete list of available methods and their parameters, please refer to [Python API Reference documentation](https://fal-ai.github.io/fal/client).

## Support

If you encounter any issues or have questions, please visit the [GitHub repository](https://github.com/fal-ai/fal) or join our [Discord Community](https://discord.gg/fal-ai).