[Try image generation (Vertex AI Studio)](https://console.cloud.google.com/vertex-ai/studio/media/generate;tab=image)

[Try Imagen in a Colab](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen4_image_generation.ipynb)

This page describes using a seed number in Imagen on Vertex AI to generate deterministic images.

A seed number is a number that you add to a request to make non-deterministic generated images deterministic. _Deterministic_ means that each time you generate an image with Imagen, you receive the same generated output each time.

For example, you can provide a prompt, set the number of results to 1, and use a seed number to get the same image each time you use the same input values. If you send the same request with the number of results set to 8, you will get the same eight images.

## Use a seed to generate images

Do the following:

[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Seed number is an optional field in the `parameters` object of a JSON request body.

Before using any of the request data, make the following replacements:

-   PROJECT\_ID: Your Google Cloud [project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifiers).
-   MODEL\_VERSION: The Imagen model version to use. For more information about available models, see [Imagen models](https://cloud.google.com/vertex-ai/generative-ai/docs/models#imagen-models).
    
-   LOCATION: Your project's region. For example, `us-central1`, `europe-west2`, or `asia-northeast3`. For a list of available regions, see [Generative AI on Vertex AI locations](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations-genai).
-   TEXT\_PROMPT: The text prompt that guides what images the model generates. This field is required for both generation and editing.
-   IMAGE\_COUNT: The number of generated images. Accepted integer values: 1-8 (`imagegeneration@002`), 1-4 (all other model versions). Default value: 4.

**Additional optional parameters**

HTTP method and URL:

```
POST https://<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>/publishers/google/models/<devsite-var rendered="" translate="no" is-upgraded="" scope="MODEL_VERSION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit MODEL_VERSION" aria-label="Edit MODEL_VERSION">MODEL_VERSION</var></span></devsite-var>:predict
```

Request JSON body:

```
{
  "instances": [
    {
      "prompt": "<devsite-var rendered="" translate="no" is-upgraded="" scope="TEXT_PROMPT" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit TEXT_PROMPT" aria-label="Edit TEXT_PROMPT">TEXT_PROMPT</var></span></devsite-var>"
    }
  ],
  "parameters": {
    "sampleCount": <devsite-var rendered="" translate="no" is-upgraded="" scope="IMAGE_COUNT" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit IMAGE_COUNT" aria-label="Edit IMAGE_COUNT">IMAGE_COUNT</var></span></devsite-var>
  }
}
```

To send your request, choose one of these options:

[curl](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#curl)[PowerShell](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#powershell)

Save the request body in a file named `request.json`, and execute the following command:

```
curl -X POST \<br>     -H "Authorization: Bearer $(gcloud auth print-access-token)" \<br>     -H "Content-Type: application/json; charset=utf-8" \<br>     -d @request.json \<br>     "https://<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>/publishers/google/models/<devsite-var rendered="" translate="no" is-upgraded="" scope="MODEL_VERSION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit MODEL_VERSION" aria-label="Edit MODEL_VERSION">MODEL_VERSION</var></span></devsite-var>:predict"
```

The following sample response is for a request with `"sampleCount": 2`. The response returns two prediction objects, with the generated image bytes base64-encoded.

```
<span>{</span>
<span>  </span><span>"predictions"</span><span>:</span><span> </span><span>[</span>
<span>    </span><span>{</span>
<span>      </span><span>"bytesBase64Encoded"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES</var></span></devsite-var>"</span><span>,</span>
<span>      </span><span>"mimeType"</span><span>:</span><span> </span><span>"image/png"</span>
<span>    </span><span>},</span>
<span>    </span><span>{</span>
<span>      </span><span>"mimeType"</span><span>:</span><span> </span><span>"image/png"</span><span>,</span>
<span>      </span><span>"bytesBase64Encoded"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES</var></span></devsite-var>"</span>
<span>    </span><span>}</span>
<span>  </span><span>]</span>
<span>}</span>
```

If you use a model that supports prompt enhancement, the response includes an additional `prompt` field with the enhanced prompt used for generation:

```
{
  "predictions": [
    {
      "mimeType": "<devsite-var rendered="" translate="no" is-upgraded="" scope="MIME_TYPE"><span><var spellcheck="false" is-upgraded="">MIME_TYPE</var></span></devsite-var>",<strong>
      "prompt": "<devsite-var rendered="" translate="no" is-upgraded="" scope="ENHANCED_PROMPT_1"><span><var spellcheck="false" is-upgraded="">ENHANCED_PROMPT_1</var></span></devsite-var>",</strong>
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES_1"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES_1</var></span></devsite-var>"
    },
    {
      "mimeType": "<devsite-var rendered="" translate="no" is-upgraded="" scope="MIME_TYPE"><span><var spellcheck="false" is-upgraded="">MIME_TYPE</var></span></devsite-var>",<strong>
      "prompt": "<devsite-var rendered="" translate="no" is-upgraded="" scope="ENHANCED_PROMPT_2"><span><var spellcheck="false" is-upgraded="">ENHANCED_PROMPT_2</var></span></devsite-var>",</strong>
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES_2"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES_2</var></span></devsite-var>"
    }
  ]
}
```

1.  Replace the following:
    
    -   SEED\_NUMBER: integer. Optional. Any non-negative integer you provide to make output images deterministic. Providing the same seed number always results in the same output images. If the model you're using supports digital watermarking, you must set `"addWatermark": false` to use this field. Accepted integer values: `1` - `2147483647`.

```
<span>{</span>
<span>  </span><span>"instances"</span><span>:</span><span> </span><span>[</span>
<span>    </span><devsite-var rendered="" translate="no" is-upgraded="" scope="..." tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit ..." aria-label="Edit ...">...</var></span></devsite-var>
<span>  </span><span>],</span>
<span>  </span><span>"parameters"</span><span>:</span><span> </span><span>{</span>
<span>    </span><span>"sampleCount"</span><span>:</span><span> </span><span>IMAGE_COUNT</span><span>,</span><strong>
<span>    </span><span>"seed"</span><span>:</span><span> </span><devsite-var rendered="" translate="no" is-upgraded="" scope="SEED_NUMBER" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit SEED_NUMBER" aria-label="Edit SEED_NUMBER">SEED_NUMBER</var></span></devsite-var><span>,</span></strong>
<span>    </span><span>// required for model version 006 and greater only when using a seed number</span>
<span>    </span><span>"addWatermark"</span><span>:</span><span> </span><span>false</span>
<span>  </span><span>}</span>
<span>}</span>
```

## What's next

-   [Use prompt rewriter](https://cloud.google.com/vertex-ai/generative-ai/docs/image/use-prompt-rewriter)
-   [Set text prompt language](https://cloud.google.com/vertex-ai/generative-ai/docs/image/set-text-prompt-language)
-   [Configure aspect ratio](https://cloud.google.com/vertex-ai/generative-ai/docs/image/configure-aspect-ratio)
-   [Omit content using a negative prompt](https://cloud.google.com/vertex-ai/generative-ai/docs/image/omit-content-using-a-negative-prompt)