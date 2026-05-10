You can use Imagen on Vertex AI's upscaling feature to increase the size of an image without losing quality.

## Model versions

Upscaling availability is based on model version:

| Feature | Imagen (v.002) | Imagen 2 (v.005) | Imagen 2 (v.006) |
| --- | --- | --- | --- |
| Upscaling | ✔ | Not supported | Not supported |

Use the following code samples to upscale an existing, generated, or edited image.

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

For more information about `imagegeneration` model requests, see the [`imagegeneration` model API reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/image-generation).

Upscaling mode is an optional field in the `parameters` object of a JSON request body. When you upscale an image using the API, specify `"mode": "upscale"` and `upscaleConfig`.

Before using any of the request data, make the following replacements:

-   LOCATION: Your project's region. For example, `us-central1`, `europe-west2`, or `asia-northeast3`. For a list of available regions, see [Generative AI on Vertex AI locations](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations-genai).
-   PROJECT\_ID: Your Google Cloud [project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifiers).
-   B64\_BASE\_IMAGE: The base image to edit or upscale. The image must be specified as a [base64-encoded](https://cloud.google.com/vertex-ai/generative-ai/docs/image/base64-encode) byte string. Size limit: 10 MB.
-   IMAGE\_SOURCE: The Cloud Storage location of the image you want to edit or upscale. For example: `gs://output-bucket/source-photos/photo.png`.
-   UPSCALE\_FACTOR: Optional. The factor to which the image will be upscaled. If not specified, the upscale factor will be determined from the longer side of the input image and `sampleImageSize`. Available values: `x2` or `x4` .

HTTP method and URL:

```
POST https://<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>/publishers/google/models/imagegeneration@002:predict
```

Request JSON body:

```
{
  "instances": [
    {
      "prompt": "",
      "image": {
        // use one of the following to specify the image to upscale
        "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="B64_BASE_IMAGE" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit B64_BASE_IMAGE" aria-label="Edit B64_BASE_IMAGE">B64_BASE_IMAGE</var></span></devsite-var>"
        "gcsUri": "<devsite-var rendered="" translate="no" is-upgraded="" scope="IMAGE_SOURCE" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit IMAGE_SOURCE" aria-label="Edit IMAGE_SOURCE">IMAGE_SOURCE</var></span></devsite-var>"
        // end of base image input options
      },
    }
  ],
  "parameters": {
    "sampleCount": 1,
    "mode": "<devsite-var rendered="" translate="no" is-upgraded="" scope="upscale" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit upscale" aria-label="Edit upscale">upscale</var></span></devsite-var>",
    "upscaleConfig": {
      "upscaleFactor": "<devsite-var rendered="" translate="no" is-upgraded="" scope="UPSCALE_FACTOR" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit UPSCALE_FACTOR" aria-label="Edit UPSCALE_FACTOR">UPSCALE_FACTOR</var></span></devsite-var>"
    }
  }
}
```

To send your request, choose one of these options:

[curl](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#curl)[PowerShell](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#powershell)

Save the request body in a file named `request.json`, and execute the following command:

```
curl -X POST \<br>     -H "Authorization: Bearer $(gcloud auth print-access-token)" \<br>     -H "Content-Type: application/json; charset=utf-8" \<br>     -d @request.json \<br>     "https://<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>/publishers/google/models/imagegeneration@002:predict"
```

You should receive a JSON response similar to the following:

```
{
  "predictions": [
    {
      "mimeType": "image/png",
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="iVBOR..[base64-encoded-upscaled-image]...YII="><span><var spellcheck="false" is-upgraded="">iVBOR..[base64-encoded-upscaled-image]...YII=</var></span></devsite-var>"
    }
  ]
}
```

## What's next

Read articles about Imagen and other Generative AI on Vertex AI products:

-   [A developer's guide to getting started with Imagen 3 on Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/a-developers-guide-to-imagen-3-on-vertex-ai?e=0?utm_source%3Dlinkedin)
-   [New generative media models and tools, built with and for creators](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/#veo)
-   [New in Gemini: Custom Gems and improved image generation with Imagen 3](https://blog.google/products/gemini/google-gemini-update-august-2024/)
-   [Google DeepMind: Imagen 3 - Our highest quality text-to-image model](https://deepmind.google/technologies/imagen-3/)