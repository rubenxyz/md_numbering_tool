# Flux Kontext Trainer

> LoRA trainer for FLUX.1 Kontext [dev]


## Overview

- **Endpoint**: `https://fal.run/fal-ai/flux-kontext-trainer`
- **Model ID**: `fal-ai/flux-kontext-trainer`
- **Category**: training
- **Kind**: training
**Description**: LoRA trainer for FLUX.1 Kontext [dev]. Train custom LoRAs to extend the image editing functionality of FLUX.1 Kontext [dev]



## API Information

This model can be used via our HTTP API or more conveniently via our client libraries.
See the input and output schema below, as well as the usage examples.


### Input Schema

The API accepts the following input parameters:


- **`image_data_url`** (`string`, _required_):
  URL to the input data zip archive.
  
  The zip should contain pairs of images. The images should be named:
  
  ROOT_start.EXT and ROOT_end.EXT
  For example:
  photo_start.jpg and photo_end.jpg
  
  The zip can also contain a text file for each image pair. The text file should be named:
  ROOT.txt
  For example:
  photo.txt
  
  This text file can be used to specify the edit instructions for the image pair.
  
  If no text file is provided, the default_caption will be used.
  
  If no default_caption is provided, the training will fail.

- **`steps`** (`integer`, _optional_):
  Number of steps to train for Default value: `1000`
  - Default: `1000`
  - Range: `2` to `20000`

- **`learning_rate`** (`float`, _optional_):
   Default value: `0.0001`
  - Default: `0.0001`

- **`default_caption`** (`string`, _optional_):
  Default caption to use when caption files are missing. If None, missing captions will cause an error.

- **`output_lora_format`** (`OutputLoraFormatEnum`, _optional_):
  Dictates the naming scheme for the output weights Default value: `"fal"`
  - Default: `"fal"`
  - Options: `"fal"`, `"comfy"`



**Required Parameters Example**:

```json
{
  "image_data_url": ""
}
```

**Full Example**:

```json
{
  "image_data_url": "",
  "steps": 1000,
  "learning_rate": 0.0001,
  "output_lora_format": "fal"
}
```


### Output Schema

The API returns the following output format:

- **`diffusers_lora_file`** (`File`, _required_):
  URL to the trained diffusers lora weights.

- **`config_file`** (`File`, _required_):
  URL to the configuration file for the trained model.



**Example Response**:

```json
{
  "diffusers_lora_file": {
    "url": "",
    "content_type": "image/png",
    "file_name": "z9RV14K95DvU.png",
    "file_size": 4404019
  },
  "config_file": {
    "url": "",
    "content_type": "image/png",
    "file_name": "z9RV14K95DvU.png",
    "file_size": 4404019
  }
}
```


## Usage Examples

### cURL

```bash
curl --request POST \
  --url https://fal.run/fal-ai/flux-kontext-trainer \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
     "image_data_url": ""
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
    "fal-ai/flux-kontext-trainer",
    arguments={
        "image_data_url": ""
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

const result = await fal.subscribe("fal-ai/flux-kontext-trainer", {
  input: {
    image_data_url: ""
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

- [Model Playground](https://fal.ai/models/fal-ai/flux-kontext-trainer)
- [API Documentation](https://fal.ai/models/fal-ai/flux-kontext-trainer/api)
- [OpenAPI Schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/flux-kontext-trainer)

### fal.ai Platform

- [Platform Documentation](https://docs.fal.ai)
- [Python Client](https://docs.fal.ai/clients/python)
- [JavaScript Client](https://docs.fal.ai/clients/javascript)
