[Skip to main content](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#main-content)

-   Build
    
    -   Agents
        
    -   [Overview](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-builder/overview)
    
    -   Agent2Agent (A2A) Protocol
        
    
    -   Prompt design
        
    -   [Introduction to prompting](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design)
    
    -   Task-specific prompt guidance
        
    -   Capabilities
        
    
    -   Image generation
        
        -   Gemini
            
        -   [Generate images with Gemini](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation)
        -   Imagen
            
        -   [Imagen overview](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)
        -   [Generate images using text prompts](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images)
        -   [Verify an image watermark](https://cloud.google.com/vertex-ai/generative-ai/docs/image/verify-watermark)
        
        -   [Upscale an image](https://cloud.google.com/vertex-ai/generative-ai/docs/image/upscale-image)
        -   [Prompt and image attribute guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide)
        -   [Base64 encode and decode files](https://cloud.google.com/vertex-ai/generative-ai/docs/image/base64-encode)
        -   [Responsible AI and usage guidelines for Imagen](https://cloud.google.com/vertex-ai/generative-ai/docs/image/responsible-ai-imagen)
        
    
    -   [URL context](https://cloud.google.com/vertex-ai/generative-ai/docs/url-context)
    -   [Thinking](https://cloud.google.com/vertex-ai/generative-ai/docs/thinking)
    
    -   [Translation](https://cloud.google.com/vertex-ai/generative-ai/docs/translate/translate-text)
    -   [Generate speech from text](https://cloud.google.com/vertex-ai/generative-ai/docs/speech/text-to-speech)
    -   [Transcribe speech](https://cloud.google.com/vertex-ai/generative-ai/docs/speech/speech-to-text)
    -   Development tools
        
    -   Use AI-powered prompt writing tools
        
    
    -   [Multimodal datasets](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/datasets)
    -   [Use Vertex AI Search](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/vertex-ai-search)
    -   Model tuning
        
    -   [Introduction to tuning](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models)
    
    -   [Tuning recommendations with LoRA and QLoRA](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/lora-qlora)
    -   Migrate
        
    -   Call Vertex AI models using OpenAI libraries
        
    -   [Migrate from Google AI to Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai)
    

-   Go to Vertex AI documentation
    
-   [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)

## Configure aspect ratio

bookmark\_border Stay organized with collections Save and categorize content based on your preferences.

[Try image generation (Vertex AI Studio)](https://console.cloud.google.com/vertex-ai/studio/media/generate;tab=image)

[Try Imagen in a Colab](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen4_image_generation.ipynb)

This page describes how to configure the aspect ratio that Imagen on Vertex AI generates images for.

Depending on how you plan to use your generated images, some aspect ratios may work better than others. Choose the aspect ratio that best suits your use case.

There are multiple image generation models that you can use, and certain aspect ratios are available to specific Imagen models. For more information, see [Imagen models](https://cloud.google.com/vertex-ai/generative-ai/docs/models#imagen-models).

| Aspect ratio | Intended use | Sample image |
| --- | --- | --- |
| `1:1` | default, square, general use | 
![Sample generated image in the console](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratio-1-1.png)

<sup>Prompt: <i>overhead shot of a pasta dinner, studio photo in the style of food magazine cover</i>.</sup>



 |
| `3:4` | TV, media, film | 

![Sample generated image in the console](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratio-3-4.png)

<sup>Prompt: <i>commercial photoshoot, fragrance ad, lavender vanilla scented bottle on a light colored background</i>.</sup>



 |
| `4:3` | TV, media, film | 

![Sample generated image in the console](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratio-4-3.png)

<sup>Prompt: <i>commercial photoshoot, green and gray high top sneakers, 4k, dramatic angles</i>.</sup>



 |
| `9:16` | portrait, tall objects, mobile devices | 

![Sample generated image in the console](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratio-16-9.png)

<sup>Prompt: <i>nature photography, a beach in hawaii with the ocean in the background, lens flare, sunset</i>.</sup>



 |
| `16:9` | landscape | 

![Sample generated image in the console](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratio-9-16.png)

<sup>Prompt: <i>skyscrapers in new york city, futuristic rendering, concept, digital art</i>.</sup>



 |

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Aspect ratio is an optional field in the `parameters` object of a JSON request body.

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

-   [Use prompt rewriter](https://cloud.google.com/vertex-ai/generative-ai/docs/image/use-prompt-rewriter)
-   [Set text prompt language](https://cloud.google.com/vertex-ai/generative-ai/docs/image/set-text-prompt-language)
-   [Omit content using a negative prompt](https://cloud.google.com/vertex-ai/generative-ai/docs/image/omit-content-using-a-negative-prompt)
-   [Generate deterministic images](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-deterministic-images)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-18 UTC.

The new page has loaded.