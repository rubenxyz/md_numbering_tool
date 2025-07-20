# gpt-image-1

> OpenAI's latest image generation and editing model: gpt-1-image. Currently powered with bring-your-own-key.


## Overview

- **Endpoint**: `https://fal.run/fal-ai/gpt-image-1/text-to-image/byok`
- **Model ID**: `fal-ai/gpt-image-1/text-to-image/byok`
- **Category**: text-to-image
- **Kind**: inference


## API Information

This model can be used via our HTTP API or more conveniently via our client libraries.
See the input and output schema below, as well as the usage examples.


### Input Schema

The API accepts the following input parameters:


- **`prompt`** (`string`, _required_):
  The prompt to generate the image from.
  - Examples: "A serene cyberpunk cityscape at twilight, with neon signs glowing in vibrant blues and purples, reflecting on rain-slick streets. Sleek futuristic buildings tower above, connected by glowing skybridges. A lone figure in a hooded jacket stands under a streetlamp, backlit by soft mist. The atmosphere is cinematic, moody"

- **`image_size`** (`ImageSizeEnum`, _optional_):
  The size of the image to generate. Default value: `"auto"`
  - Default: `"auto"`
  - Options: `"auto"`, `"1024x1024"`, `"1536x1024"`, `"1024x1536"`

- **`num_images`** (`integer`, _optional_):
  The number of images to generate. Default value: `1`
  - Default: `1`
  - Range: `1` to `4`

- **`quality`** (`QualityEnum`, _optional_):
  The quality of the image to generate. Default value: `"auto"`
  - Default: `"auto"`
  - Options: `"auto"`, `"low"`, `"medium"`, `"high"`

- **`background`** (`BackgroundEnum`, _optional_):
  The background of the image to generate. Default value: `"auto"`
  - Default: `"auto"`
  - Options: `"auto"`, `"transparent"`, `"opaque"`

- **`openai_api_key`** (`string`, _required_):
  The OpenAI API key to use for the image generation. This endpoint is currently powered by bring-your-own-key system.



**Required Parameters Example**:

```json
{
  "prompt": "A serene cyberpunk cityscape at twilight, with neon signs glowing in vibrant blues and purples, reflecting on rain-slick streets. Sleek futuristic buildings tower above, connected by glowing skybridges. A lone figure in a hooded jacket stands under a streetlamp, backlit by soft mist. The atmosphere is cinematic, moody",
  "openai_api_key": ""
}
```

**Full Example**:

```json
{
  "prompt": "A serene cyberpunk cityscape at twilight, with neon signs glowing in vibrant blues and purples, reflecting on rain-slick streets. Sleek futuristic buildings tower above, connected by glowing skybridges. A lone figure in a hooded jacket stands under a streetlamp, backlit by soft mist. The atmosphere is cinematic, moody",
  "image_size": "auto",
  "num_images": 1,
  "quality": "auto",
  "background": "auto",
  "openai_api_key": ""
}
```


### Output Schema

The API returns the following output format:

- **`images`** (`list<Image>`, _required_):
  The generated images.
  - Array of Image
  - Examples: [{"url":"https://storage.googleapis.com/falserverless/model_tests/gpt-image-1/cyberpunk.png"}]



**Example Response**:

```json
{
  "images": [
    {
      "url": "https://storage.googleapis.com/falserverless/model_tests/gpt-image-1/cyberpunk.png"
    }
  ]
}
```


## Usage Examples

### cURL

```bash
curl --request POST \
  --url https://fal.run/fal-ai/gpt-image-1/text-to-image/byok \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
     "prompt": "A serene cyberpunk cityscape at twilight, with neon signs glowing in vibrant blues and purples, reflecting on rain-slick streets. Sleek futuristic buildings tower above, connected by glowing skybridges. A lone figure in a hooded jacket stands under a streetlamp, backlit by soft mist. The atmosphere is cinematic, moody",
     "openai_api_key": ""
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
    "fal-ai/gpt-image-1/text-to-image/byok",
    arguments={
        "prompt": "A serene cyberpunk cityscape at twilight, with neon signs glowing in vibrant blues and purples, reflecting on rain-slick streets. Sleek futuristic buildings tower above, connected by glowing skybridges. A lone figure in a hooded jacket stands under a streetlamp, backlit by soft mist. The atmosphere is cinematic, moody",
        "openai_api_key": ""
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

const result = await fal.subscribe("fal-ai/gpt-image-1/text-to-image/byok", {
  input: {
    prompt: "A serene cyberpunk cityscape at twilight, with neon signs glowing in vibrant blues and purples, reflecting on rain-slick streets. Sleek futuristic buildings tower above, connected by glowing skybridges. A lone figure in a hooded jacket stands under a streetlamp, backlit by soft mist. The atmosphere is cinematic, moody",
    openai_api_key: ""
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

- [Model Playground](https://fal.ai/models/fal-ai/gpt-image-1/text-to-image/byok)
- [API Documentation](https://fal.ai/models/fal-ai/gpt-image-1/text-to-image/byok/api)
- [OpenAPI Schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/gpt-image-1/text-to-image/byok)

### fal.ai Platform

- [Platform Documentation](https://docs.fal.ai)
- [Python Client](https://docs.fal.ai/clients/python)
- [JavaScript Client](https://docs.fal.ai/clients/javascript)
