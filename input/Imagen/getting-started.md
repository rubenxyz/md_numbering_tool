<iframe frameborder="0" allowfullscreen="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" width="640" height="360" src="https://www.youtube.com/embed/6n5ngB88DHU?origin=https%3A%2F%2Fcloud.google.com&amp;autoplay&amp;controls&amp;embed_domain&amp;enablejsapi=1&amp;end&amp;hl&amp;showinfo&amp;start&amp;video-id=6n5ngB88DHU&amp;widgetid=7&amp;forigin=https%3A%2F%2Fcloud.google.com%2Fvertex-ai%2Fgenerative-ai%2Fdocs%2Fimage%2Fgenerate-images&amp;aoriginsup=1&amp;vf=1" id="widget8" data-title="YouTube video player" title="Generate and edit images with Generative AI Studio"></iframe>

You can use Imagen on Vertex AI to generate new images from a text prompt. Supported interfaces include the Google Cloud console and the Vertex AI API.

For more information about writing text prompts for image generation and editing, see the [prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide).

[View Imagen for Generation model card](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/imagen-4.0-generate-preview-06-06)

[Try image generation (Vertex AI Studio)](https://console.cloud.google.com/vertex-ai/studio/media/generate;tab=image)

[Try Imagen in a Colab](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen4_image_generation.ipynb)

## Before you begin

2.  Set up authentication for your environment.
    
    Select the tab for how you plan to use the samples on this page:
    
    [Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)
    
    To use the REST API samples on this page in a local development environment, you use the credentials you provide to the gcloud CLI.
    
    After [installing](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI, [initialize](https://cloud.google.com/sdk/docs/initializing) it by running the following command:
    
    ```
    gcloud<span> </span>init
    ```
    
    If you're using an external identity provider (IdP), you must first [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
    
    For more information, see [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest) in the Google Cloud authentication documentation.
    

You can generate novel images using only descriptive text as an input. The following samples show you basic instructions to generate images.

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python-gen-ai-sdk)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

For more information about `imagegeneration` model requests, see the [`imagegeneration` model API reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api).

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

## What's next

Read articles about Imagen and other Generative AI on Vertex AI products:

-   [A developer's guide to getting started with Imagen 3 on Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/a-developers-guide-to-imagen-3-on-vertex-ai?e=0?utm_source%3Dlinkedin)
-   [New generative media models and tools, built with and for creators](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/#veo)
-   [New in Gemini: Custom Gems and improved image generation with Imagen 3](https://blog.google/products/gemini/google-gemini-update-august-2024/)
-   [Google DeepMind: Imagen 3 - Our highest quality text-to-image model](https://deepmind.google/technologies/imagen-3/)