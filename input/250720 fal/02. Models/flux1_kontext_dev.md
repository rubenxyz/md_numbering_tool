# FLUX.1 Kontext [dev]

> Frontier image editing model.


## Overview

- **Endpoint**: `https://fal.run/fal-ai/flux-kontext/dev`
- **Model ID**: `fal-ai/flux-kontext/dev`
- **Category**: image-to-image
- **Kind**: inference


## API Information

This model can be used via our HTTP API or more conveniently via our client libraries.
See the input and output schema below, as well as the usage examples.


### Input Schema

The API accepts the following input parameters:


- **`prompt`** (`string`, _required_):
  The prompt to edit the image.
  - Examples: "Change the setting to a day time, add a lot of people walking the sidewalk while maintaining the same style of the painting"

- **`image_url`** (`string`, _required_):
  The URL of the image to edit.
  - Examples: "https://storage.googleapis.com/falserverless/example_inputs/kontext_example_input.webp"

- **`num_inference_steps`** (`integer`, _optional_):
  The number of inference steps to perform. Default value: `28`
  - Default: `28`
  - Range: `10` to `50`

- **`seed`** (`integer`, _optional_):
  The same seed and the same prompt given to the same version of the model
  will output the same image every time.

- **`guidance_scale`** (`float`, _optional_):
  The CFG (Classifier Free Guidance) scale is a measure of how close you want
  the model to stick to your prompt when looking for a related image to show you. Default value: `2.5`
  - Default: `2.5`
  - Range: `1` to `20`

- **`sync_mode`** (`boolean`, _optional_):
  If set to true, the function will wait for the image to be generated and uploaded
  before returning the response. This will increase the latency of the function but
  it allows you to get the image directly in the response without going through the CDN.
  - Default: `false`

- **`num_images`** (`integer`, _optional_):
  The number of images to generate. Default value: `1`
  - Default: `1`
  - Range: `1` to `4`

- **`enable_safety_checker`** (`boolean`, _optional_):
  If set to true, the safety checker will be enabled. Default value: `true`
  - Default: `true`

- **`output_format`** (`OutputFormatEnum`, _optional_):
  Output format Default value: `"jpeg"`
  - Default: `"jpeg"`
  - Options: `"jpeg"`, `"png"`

- **`acceleration`** (`AccelerationEnum`, _optional_):
  The speed of the generation. The higher the speed, the faster the generation. Default value: `"none"`
  - Default: `"none"`
  - Options: `"none"`, `"regular"`, `"high"`

- **`resolution_mode`** (`ResolutionModeEnum`, _optional_):
  Determines how the output resolution is set for image editing.
  - `auto`: The model selects an optimal resolution from a predefined set that best matches the input image's aspect ratio. This is the recommended setting for most use cases as it's what the model was trained on.
  - `match_input`: The model will attempt to use the same resolution as the input image. The resolution will be adjusted to be compatible with the model's requirements (e.g. dimensions must be multiples of 16 and within supported limits).
  Apart from these, a few aspect ratios are also supported. Default value: `"match_input"`
  - Default: `"match_input"`
  - Options: `"auto"`, `"match_input"`, `"1:1"`, `"16:9"`, `"21:9"`, `"3:2"`, `"2:3"`, `"4:5"`, `"5:4"`, `"3:4"`, `"4:3"`, `"9:16"`, `"9:21"`



**Required Parameters Example**:

```json
{
  "prompt": "Change the setting to a day time, add a lot of people walking the sidewalk while maintaining the same style of the painting",
  "image_url": "https://storage.googleapis.com/falserverless/example_inputs/kontext_example_input.webp"
}
```

**Full Example**:

```json
{
  "prompt": "Change the setting to a day time, add a lot of people walking the sidewalk while maintaining the same style of the painting",
  "image_url": "https://storage.googleapis.com/falserverless/example_inputs/kontext_example_input.webp",
  "num_inference_steps": 28,
  "guidance_scale": 2.5,
  "num_images": 1,
  "enable_safety_checker": true,
  "output_format": "jpeg",
  "acceleration": "none",
  "resolution_mode": "match_input"
}
```


### Output Schema

The API returns the following output format:

- **`images`** (`list<Image>`, _required_):
  The generated image files info.
  - Array of Image
  - Examples: [{"height":768,"content_type":"image/jpeg","url":"https://storage.googleapis.com/falserverless/example_outputs/kontext_example_output.jpeg","width":1024}]

- **`timings`** (`Timings`, _required_)

- **`seed`** (`integer`, _required_):
  Seed of the generated Image. It will be the same value of the one passed in the
  input or the randomly generated that was used in case none was passed.

- **`has_nsfw_concepts`** (`list<boolean>`, _required_):
  Whether the generated images contain NSFW concepts.
  - Array of boolean

- **`prompt`** (`string`, _required_):
  The prompt used for generating the image.



**Example Response**:

```json
{
  "images": [
    {
      "height": 768,
      "content_type": "image/jpeg",
      "url": "https://storage.googleapis.com/falserverless/example_outputs/kontext_example_output.jpeg",
      "width": 1024
    }
  ],
  "prompt": ""
}
```


## Usage Examples

### cURL

```bash
curl --request POST \
  --url https://fal.run/fal-ai/flux-kontext/dev \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
     "prompt": "Change the setting to a day time, add a lot of people walking the sidewalk while maintaining the same style of the painting",
     "image_url": "https://storage.googleapis.com/falserverless/example_inputs/kontext_example_input.webp"
   }'
```

### Python

Ensure you have the Python client installed:

```bash
pip install fal-client
```

Then use the API client to make requests:

```python
import fal_client

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

result = fal_client.subscribe(
    "fal-ai/flux-kontext/dev",
    arguments={
        "prompt": "Change the setting to a day time, add a lot of people walking the sidewalk while maintaining the same style of the painting",
        "image_url": "https://storage.googleapis.com/falserverless/example_inputs/kontext_example_input.webp"
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)
print(result)
```

### JavaScript

Ensure you have the JavaScript client installed:

```bash
npm install --save @fal-ai/client
```

Then use the API client to make requests:

```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-kontext/dev", {
  input: {
    prompt: "Change the setting to a day time, add a lot of people walking the sidewalk while maintaining the same style of the painting",
    image_url: "https://storage.googleapis.com/falserverless/example_inputs/kontext_example_input.webp"
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});
console.log(result.data);
console.log(result.requestId);
```


## Additional Resources

### Documentation

- [Model Playground](https://fal.ai/models/fal-ai/flux-kontext/dev)
- [API Documentation](https://fal.ai/models/fal-ai/flux-kontext/dev/api)
- [OpenAPI Schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/flux-kontext/dev)

### fal.ai Platform

- [Platform Documentation](https://docs.fal.ai)
- [Python Client](https://docs.fal.ai/clients/python)
- [JavaScript Client](https://docs.fal.ai/clients/javascript)
