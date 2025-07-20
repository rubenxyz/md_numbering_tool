# Bytedance

> Seedream 3.0 is a bilingual (Chinese and English) text-to-image model that excels at text-to-image generation.


## Overview

- **Endpoint**: `https://fal.run/fal-ai/bytedance/seedream/v3/text-to-image`
- **Model ID**: `fal-ai/bytedance/seedream/v3/text-to-image`
- **Category**: text-to-image
- **Kind**: inference


## API Information

This model can be used via our HTTP API or more conveniently via our client libraries.
See the input and output schema below, as well as the usage examples.


### Input Schema

The API accepts the following input parameters:


- **`prompt`** (`string`, _required_):
  The text prompt used to generate the image
  - Examples: "Fisheye lens, the head of a cat, the image shows the effect that the facial features of the cat are distorted due to the shooting method."

- **`image_size`** (`ImageSize | Enum`, _optional_):
  Use for finer control over the output image size. Will be used over aspect_ratio, if both are provided. Width and height must be between 512 and 2048.
  - One of: ImageSize | Enum

- **`guidance_scale`** (`float`, _optional_):
  Controls how closely the output image aligns with the input prompt. Higher values mean stronger prompt correlation. Default value: `2.5`
  - Default: `2.5`
  - Range: `1` to `10`

- **`num_images`** (`integer`, _optional_):
  Number of images to generate Default value: `1`
  - Default: `1`
  - Range: `1` to `4`

- **`seed`** (`integer`, _optional_):
  Random seed to control the stochasticity of image generation.



**Required Parameters Example**:

```json
{
  "prompt": "Fisheye lens, the head of a cat, the image shows the effect that the facial features of the cat are distorted due to the shooting method."
}
```

**Full Example**:

```json
{
  "prompt": "Fisheye lens, the head of a cat, the image shows the effect that the facial features of the cat are distorted due to the shooting method.",
  "guidance_scale": 2.5,
  "num_images": 1
}
```


### Output Schema

The API returns the following output format:

- **`images`** (`list<Image>`, _required_):
  Generated images
  - Array of Image
  - Examples: [{"url":"https://v3.fal.media/files/rabbit/EJqemc4hQlHKAtkkfTJqB_a2aaccab7ff84740b6323da580146087.png"}]

- **`seed`** (`integer`, _required_):
  Seed used for generation
  - Examples: 42



**Example Response**:

```json
{
  "images": [
    {
      "url": "https://v3.fal.media/files/rabbit/EJqemc4hQlHKAtkkfTJqB_a2aaccab7ff84740b6323da580146087.png"
    }
  ],
  "seed": 42
}
```


## Usage Examples

### cURL

```bash
curl --request POST \
  --url https://fal.run/fal-ai/bytedance/seedream/v3/text-to-image \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
     "prompt": "Fisheye lens, the head of a cat, the image shows the effect that the facial features of the cat are distorted due to the shooting method."
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
    "fal-ai/bytedance/seedream/v3/text-to-image",
    arguments={
        "prompt": "Fisheye lens, the head of a cat, the image shows the effect that the facial features of the cat are distorted due to the shooting method."
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

const result = await fal.subscribe("fal-ai/bytedance/seedream/v3/text-to-image", {
  input: {
    prompt: "Fisheye lens, the head of a cat, the image shows the effect that the facial features of the cat are distorted due to the shooting method."
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

- [Model Playground](https://fal.ai/models/fal-ai/bytedance/seedream/v3/text-to-image)
- [API Documentation](https://fal.ai/models/fal-ai/bytedance/seedream/v3/text-to-image/api)
- [OpenAPI Schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/bytedance/seedream/v3/text-to-image)

### fal.ai Platform

- [Platform Documentation](https://docs.fal.ai)
- [Python Client](https://docs.fal.ai/clients/python)
- [JavaScript Client](https://docs.fal.ai/clients/javascript)
