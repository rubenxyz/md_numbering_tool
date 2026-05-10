[Try Imagen in a Colab](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen3_image_generation.ipynb)

This page describes how to omit content from Imagen on Vertex AI generated images.

A negative prompt is a description of what you want to omit in generated images. For example, consider the prompt _"a rainy city street at night with no people"_. The model may interpret "people" as a directive of what include instead of omit. To generate better results, you could use the prompt _"a rainy city street at night"_ with a negative prompt _"people"_.

Imagen generates these images with and without a negative prompt:

**Text prompt only**

-   Text prompt: "_a pizza_"

![three sample pizza images](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/pizza.png)

**Text prompt and negative prompt**

-   Text prompt: "_a pizza_"
-   Negative prompt: "_pepperoni_"

![three sample pizza images without pepperoni](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/pizza_neg-prompt.png)

The following models support negative prompts:

-   `imagen-3.0-capability-001`
-   `imagen-3.0-fast-generate-001`
-   `imagen-3.0-generate-001`

To omit content from generated images, do the following:

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Negative prompt is an optional field in the `parameters` object of a JSON request body.

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
    
    -   NEGATIVE\_PROMPT: A negative prompt to help generate the images. For example: "animals" (removes animals), "blurry" (makes the image clearer), "text" (removes text), or "cropped" (removes cropped images).
    
    ```
    <span>{</span>
    <span>  </span><span>"instances"</span><span>:</span><span> </span><span>[</span>
    <span>    </span><devsite-var rendered="" translate="no" is-upgraded="" scope="..." tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit ..." aria-label="Edit ...">...</var></span></devsite-var>
    <span>  </span><span>],</span>
    <span>  </span><span>"parameters"</span><span>:</span><span> </span><span>{</span>
    <span>    </span><span>"sampleCount"</span><span>:</span><span> </span><span>IMAGE_COUNT</span><span>,</span><strong>
    <span>    </span><span>"negativePrompt"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="NEGATIVE_PROMPT" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit NEGATIVE_PROMPT" aria-label="Edit NEGATIVE_PROMPT">NEGATIVE_PROMPT</var></span></devsite-var>"</span></strong>
    <span>  </span><span>}</span>
    <span>}</span>
    ```

## What's next

-   [Use prompt rewriter](https://cloud.google.com/vertex-ai/generative-ai/docs/image/use-prompt-rewriter)
-   [Set text prompt language](https://cloud.google.com/vertex-ai/generative-ai/docs/image/set-text-prompt-language)
-   [Configure aspect ratio](https://cloud.google.com/vertex-ai/generative-ai/docs/image/configure-aspect-ratio)
-   [Generate deterministic images](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-deterministic-images)