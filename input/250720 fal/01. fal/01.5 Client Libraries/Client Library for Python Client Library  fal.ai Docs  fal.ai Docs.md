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
<div><p><span>import</span><span> fal_client</span></p></div><div><p><span>def</span><span> </span><span>on_queue_update</span><span>(</span><span>update</span><span>)</span><span>:</span></p></div><div><p><span>    </span><span>if</span><span> </span><span>isinstance</span><span>(</span><span>update</span><span>,</span><span> fal_client.InProgress</span><span>):</span></p></div><div><p><span>        </span><span>for</span><span> log </span><span>in</span><span> update.logs:</span></p></div><div><p><span>           </span><span>print</span><span>(</span><span>log</span><span>[</span><span>"</span><span>message</span><span>"</span><span>])</span></p></div><div><p><span>result </span><span>=</span><span> fal_client.</span><span>subscribe</span><span>(</span></p></div><div><p><span>    </span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>arguments</span><span>=</span><span>{</span></p></div><div><p><span>        </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>"</span><span>a cat</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>seed</span><span>"</span><span>: </span><span>6252023</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>image_size</span><span>"</span><span>: </span><span>"</span><span>landscape_4_3</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>num_images</span><span>"</span><span>: </span><span>4</span></p></div><div><p><span><span>    </span></span><span>}</span><span>,</span></p></div><div><p><span>    </span><span>with_logs</span><span>=</span><span>True</span><span>,</span></p></div><div><p><span>    </span><span>on_queue_update</span><span>=</span><span>on_queue_update</span><span>,</span></p></div><div><p><span>)</span></p></div><div><p><span>print</span><span>(</span><span>result</span><span>)</span></p></div>
```

### 2\. Queue Management

You can manage the queue using the following methods:

#### Submit a Request

Submit a request to the queue using the `queue.submit` method.

-   [Python](https://docs.fal.ai/clients/python#tab-panel-10)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-11)

```
<div><p><span>import</span><span> fal_client</span></p></div><div><p><span>handler </span><span>=</span><span> fal_client.</span><span>submit</span><span>(</span></p></div><div><p><span>    </span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>arguments</span><span>=</span><span>{</span></p></div><div><p><span>        </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>"</span><span>a cat</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>seed</span><span>"</span><span>: </span><span>6252023</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>image_size</span><span>"</span><span>: </span><span>"</span><span>landscape_4_3</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>num_images</span><span>"</span><span>: </span><span>4</span></p></div><div><p><span><span>    </span></span><span>}</span><span>,</span></p></div><div><p><span>    </span><span>webhook_url</span><span>=</span><span>"</span><span>https://optional.webhook.url/for/results</span><span>"</span><span>,</span></p></div><div><p><span>)</span></p></div><div><p><span>request_id </span><span>=</span><span> handler.request_id</span></p></div>
```

This is useful when you want to submit a request to the queue and retrieve the result later. You can save the `request_id` and use it to retrieve the result later.

#### Check Request Status

Retrieve the status of a specific request in the queue:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-12)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-13)

```
<div><p><span>status </span><span>=</span><span> fal_client.</span><span>status</span><span>(</span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>,</span><span> request_id</span><span>,</span><span> </span><span>with_logs</span><span>=</span><span>True</span><span>)</span></p></div>
```

#### Retrieve Request Result

Get the result of a specific request from the queue:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-14)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-15)

```
<div><p><span>result </span><span>=</span><span> fal_client.</span><span>result</span><span>(</span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>,</span><span> request_id</span><span>)</span></p></div>
```

### 3\. File Uploads

Some endpoints require files as input. However, since the endpoints run asynchronously, processed by the queue, you will need to provide URLs to the files instead of the actual file content.

Luckily, the client library provides a way to upload files to the server and get a URL to use in the request.

-   [Python](https://docs.fal.ai/clients/python#tab-panel-16)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-17)

```
<div><p><span>url </span><span>=</span><span> fal_client.</span><span>upload_file</span><span>(</span><span>"</span><span>path/to/file</span><span>"</span><span>)</span></p></div>
```

### 4\. Streaming

Some endpoints support streaming:

-   [Python](https://docs.fal.ai/clients/python#tab-panel-18)
-   [Python (async)](https://docs.fal.ai/clients/python#tab-panel-19)

```
<div><p><span>import</span><span> fal_client</span></p></div><div><p><span>def</span><span> </span><span>stream</span><span>()</span><span>:</span></p></div><div><p><span><span>    </span></span><span>stream </span><span>=</span><span> fal_client.</span><span>stream</span><span>(</span></p></div><div><p><span>        </span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>arguments</span><span>=</span><span>{</span></p></div><div><p><span>            </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>"</span><span>a cat</span><span>"</span><span>,</span></p></div><div><p><span>            </span><span>"</span><span>seed</span><span>"</span><span>: </span><span>6252023</span><span>,</span></p></div><div><p><span>            </span><span>"</span><span>image_size</span><span>"</span><span>: </span><span>"</span><span>landscape_4_3</span><span>"</span><span>,</span></p></div><div><p><span>            </span><span>"</span><span>num_images</span><span>"</span><span>: </span><span>4</span></p></div><div><p><span><span>        </span></span><span>}</span><span>,</span></p></div><div><p><span>    </span><span>)</span></p></div><div><p><span>    </span><span>for</span><span> event </span><span>in</span><span> stream:</span></p></div><div><p><span>        </span><span>print</span><span>(</span><span>event</span><span>)</span></p></div><div><p><span>if</span><span> __name__ </span><span>==</span><span> </span><span>"</span><span>__main__</span><span>"</span><span>:</span></p></div><div><p><span>    </span><span>stream</span><span>()</span></p></div>
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
<div><p><span>import</span><span> fal_client</span></p></div><div><p><span>result </span><span>=</span><span> fal_client.</span><span>run</span><span>(</span></p></div><div><p><span>    </span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>arguments</span><span>=</span><span>{</span></p></div><div><p><span>        </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>"</span><span>a cat</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>seed</span><span>"</span><span>: </span><span>6252023</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>image_size</span><span>"</span><span>: </span><span>"</span><span>landscape_4_3</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"</span><span>num_images</span><span>"</span><span>: </span><span>4</span></p></div><div><p><span><span>    </span></span><span>}</span><span>,</span></p></div><div><p><span>)</span></p></div><div><p><span>print</span><span>(</span><span>result</span><span>)</span></p></div>
```

## API Reference

For a complete list of available methods and their parameters, please refer to [Python API Reference documentation](https://fal-ai.github.io/fal/client).

## Support

If you encounter any issues or have questions, please visit the [GitHub repository](https://github.com/fal-ai/fal) or join our [Discord Community](https://discord.gg/fal-ai).