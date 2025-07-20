We believe fal has the fastest FLUX endpoint in the planet. If you can find a faster one, we guarantee to beat it within one week. 🤝

Here is a quick guide on how to use this model from an API in less than 1 minute.

Before we proceed, you need to create an [API key](https://fal.ai/dashboard/keys).

This key secret will be used to authenticate your requests to the fal API.

```
fal.config({ credentials: "PASTE_YOUR_FAL_KEY_HERE",});
```

Now you can call our Model API endpoint using the [fal js client](https://docs.fal.ai/model-endpoints#the-fal-client):

```
import { fal } from "@fal-ai/client";const result = await fal.subscribe("fal-ai/flux/dev", { input: { prompt: "photo of a rhino dressed suit and tie sitting at a table in a bar with a bar stools, award winning photography, Elke vogelsang", },})
;
```