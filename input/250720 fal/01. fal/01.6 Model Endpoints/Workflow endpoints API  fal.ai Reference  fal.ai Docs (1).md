Workflows are a way to chain multiple models together to create a more complex pipeline. This allows you to create a single endpoint that can take an input and pass it through multiple models in sequence. This is useful for creating more complex models that require multiple steps, or for creating a single endpoint that can handle multiple tasks.

### Workflow as an API

Workflow APIs work the same way as other model endpoints, you can simply send a request and get a response back. However, it is common for workflows to contain multiple steps and produce intermediate results, as each step contains their own response that could be relevant in your use-case.

Therefore, workflows benefit from the **streaming** feature, which allows you to get partial results as they are being generated.

### Workflow events

The workflow API will trigger a few events during its execution, these events can be used to monitor the progress of the workflow and get intermediate results. Below are the events that you can expect from a workflow stream:

#### The `submit` event

This events is triggered every time a new step has been submitted to execution. It contains the `app_id`, `request_id` and the `node_id`.

```
{ "type": "submit", "node_id": "stable_diffusion_xl", "app_id": "fal-ai/fast-sdxl", "request_id": "d778bdf4-0275-47c2-9f23-16c27041cbeb"}
```

#### The `completion` event

This event is triggered upon the completion of a specific step.

```
{ "type": "completion", "node_id": "stable_diffusion_xl", "output": { "images": [ { "url": "https://fal.media/result.jpeg", "width": 1024, "height": 1024, "content_type": "image/jpeg" } ], "timings": { "inference": 2.1733 }, "seed": 6252023, "has_nsfw_concepts": [false], "prompt": "a cute puppy" }}
```

#### The `output` event

The `output` event means that the workflow has completed and the final result is ready.

```
{ "type": "output", "output": { "images": [ { "url": "https://fal.media/result.jpeg", "width": 1024, "height": 1024, "content_type": "image/jpeg" } ] }}
```

#### The `error` event

The `error` event is triggered when an error occurs during the execution of a step. The `error` object contains the `error.status` with the HTTP status code, an error `message` as well as `error.body` with the underlying error serialized.

```
{ "type": "error", "node_id": "stable_diffusion_xl", "message": "Error while fetching the result of the request d778bdf4-0275-47c2-9f23-16c27041cbeb", "error": { "status": 422, "body": { "detail": [ { "loc": ["body", "num_images"], "msg": "ensure this value is less than or equal to 8", "type": "value_error.number.not_le", "ctx": { "limit_value": 8 } } ] } }}
```

### Example

A cool and simple example of the power of workflows is `workflows/fal-ai/sdxl-sticker`, which consists of three steps:

1.  Generates an image using `fal-ai/fast-sdxl`.
2.  Remove the background of the image using `fal-ai/imageutils/rembg`.
3.  Converts the image to a sticker using `fal-ai/face-to-sticker`.

What could be a tedious process of running and coordinating three different models is now a single endpoint that you can call with a single request.

-   [Javascript](https://docs.fal.ai/model-endpoints/workflows#tab-panel-29)
-   [python](https://docs.fal.ai/model-endpoints/workflows#tab-panel-30)
-   [python (async)](https://docs.fal.ai/model-endpoints/workflows#tab-panel-31)
-   [Swift](https://docs.fal.ai/model-endpoints/workflows#tab-panel-32)

```
import fal_clientstream
= fal_client.stream( "workflows/fal-ai/sdxl-sticker", arguments={ "prompt": "a face of a cute puppy, in the style of pixar animation", },)
for event in stream: print(event)
```

### Type definitions

Below are the type definition in TypeScript of events that you can expect from a workflow stream:

```
type WorkflowBaseEvent = { type: "submit" | "completion" | "error" | "output"; node_id: string;};export type WorkflowSubmitEvent = WorkflowBaseEvent &amp; { type: "submit"; app_id: string; request_id: string;};export type WorkflowCompletionEvent&lt;Output = any&gt; = WorkflowBaseEvent &amp; { type: "completion"; app_id: string; output: Output;};export type WorkflowDoneEvent&lt;Output = any&gt; = WorkflowBaseEvent &amp; { type: "output"; output: Output;};export type WorkflowErrorEvent = WorkflowBaseEvent &amp; { type: "error"; message: string; error: any;};
```