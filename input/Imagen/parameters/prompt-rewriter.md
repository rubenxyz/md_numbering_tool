Imagen on Vertex AI offers an LLM-based prompt rewriting tool, also known as a prompt rewriter. The prompt rewriter helps you obtain higher quality output images by adding more detail to your prompt.

If you disable the prompt rewriter, the quality of the images and how well the output resembles the prompt that you supplied may be impacted. This feature is enabled by default for the following model versions:

The rewritten prompt is delivered by API response only if the original prompt is fewer than 30 words long.

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Before using any of the request data, make the following replacements:

-   PROJECT\_ID: Your Google Cloud [project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifiers).
-   MODEL\_VERSION: The image generation model version to use.
    
    For more information about model versions and features, see [model versions](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#model-versions).
    
-   LOCATION: Your project's region. For example, `us-central1`, `europe-west2`, or `asia-northeast3`. For a list of available regions, see [Generative AI on Vertex AI locations](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations-genai).
-   TEXT\_PROMPT: The text prompt that guides what images the model generates. Before images are generated, this base prompt is enhanced with more detail and descripitive language using the LLM-based prompt rewriting tool.
-   IMAGE\_COUNT: The number of generated images. Accepted integer values: 1-4. Default value: 4.
-   `enhancePrompt` - A boolean to enable LLM-based prompt enhancement. By default, this value is set to `true`.

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
    "sampleCount": <devsite-var rendered="" translate="no" is-upgraded="" scope="IMAGE_COUNT" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit IMAGE_COUNT" aria-label="Edit IMAGE_COUNT">IMAGE_COUNT</var></span></devsite-var>,<strong>
    "enhancePrompt": <devsite-var rendered="" translate="no" is-upgraded="" scope="true" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit true" aria-label="Edit true">true</var></span></devsite-var></strong>
  }
}
```

To send your request, choose one of these options:

[curl](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#curl)[PowerShell](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#powershell)

Save the request body in a file named `request.json`, and execute the following command:

```
curl -X POST \<br>     -H "Authorization: Bearer $(gcloud auth print-access-token)" \<br>     -H "Content-Type: application/json; charset=utf-8" \<br>     -d @request.json \<br>     "https://<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/<devsite-var rendered="" translate="no" is-upgraded="" scope="LOCATION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit LOCATION" aria-label="Edit LOCATION">LOCATION</var></span></devsite-var>/publishers/google/models/<devsite-var rendered="" translate="no" is-upgraded="" scope="MODEL_VERSION" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit MODEL_VERSION" aria-label="Edit MODEL_VERSION">MODEL_VERSION</var></span></devsite-var>:predict"
```

With prompt enhancement enabled, the response includes an additional `prompt` field that shows the enhanced prompt and its associated generated image:  ```
<span>  </span><span>{</span>
<span>    </span><span>"predictions"</span><span>:</span><span> </span><span>[</span>
<span>      </span><span>{</span>
<span>        </span><span>"mimeType"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="MIME_TYPE"><span><var spellcheck="false" is-upgraded="">MIME_TYPE</var></span></devsite-var>"</span><span>,</span><strong>
<span>        </span><span>"prompt"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="ENHANCED_PROMPT_1"><span><var spellcheck="false" is-upgraded="">ENHANCED_PROMPT_1</var></span></devsite-var>"</span><span>,</span></strong>
<span>        </span><span>"bytesBase64Encoded"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES_1"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES_1</var></span></devsite-var>"</span>
<span>      </span><span>},</span>
<span>      </span><span>{</span>
<span>        </span><span>"mimeType"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="MIME_TYPE"><span><var spellcheck="false" is-upgraded="">MIME_TYPE</var></span></devsite-var>"</span><span>,</span><strong>
<span>        </span><span>"prompt"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="ENHANCED_PROMPT_2"><span><var spellcheck="false" is-upgraded="">ENHANCED_PROMPT_2</var></span></devsite-var>"</span><span>,</span></strong>
<span>        </span><span>"bytesBase64Encoded"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES_2"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES_2</var></span></devsite-var>"</span>
<span>      </span><span>}</span>
<span>    </span><span>]</span>
<span>  </span><span>}</span>
```

For example, the following sample response is for a request with `"sampleCount": 2` and `"prompt": "A raccoon wearing formal clothes, wearing a top hat. Oil painting in the style of Vincent Van Gogh."`. The response returns two prediction objects, each with their enhanced prompt and the generated image bytes base64-encoded.

```
{
  "predictions": [
    {
      "mimeType": "image/png",<strong>
      "prompt": "<devsite-var rendered="" translate="no" is-upgraded="" scope="An oil painting in the style of Vincent van Gogh, depicting a raccoon adorned
        in a finely tailored tuxedo, complete with a crisp white shirt and a bow tie. The raccoon
        also sports a classic top hat, perched jauntily on its head. The painting uses thick,
        swirling brushstrokes characteristic of van Gogh, with vibrant hues of blue, yellow, and
        green in the background, contrasting with the dark tones of the raccoon's attire. The light
        source is subtly placed, casting a dramatic shadow of the raccoon's attire onto the surface
        it sits upon, further enhancing the depth and dimensionality of the composition. The
        overall impression is one of a whimsical and sophisticated character, a raccoon elevated to
        a higher class through its formal attire, rendered in van Gogh's iconic style."><span><var spellcheck="false" is-upgraded="">An oil painting in the style of Vincent van Gogh, depicting a raccoon adorned in a finely tailored tuxedo, complete with a crisp white shirt and a bow tie. The raccoon also sports a classic top hat, perched jauntily on its head. The painting uses thick, swirling brushstrokes characteristic of van Gogh, with vibrant hues of blue, yellow, and green in the background, contrasting with the dark tones of the raccoon's attire. The light source is subtly placed, casting a dramatic shadow of the raccoon's attire onto the surface it sits upon, further enhancing the depth and dimensionality of the composition. The overall impression is one of a whimsical and sophisticated character, a raccoon elevated to a higher class through its formal attire, rendered in van Gogh's iconic style.</var></span></devsite-var>",</strong>
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES</var></span></devsite-var>"
    },
    {
      "mimeType": "image/png",<strong>
      "prompt": "<devsite-var rendered="" translate="no" is-upgraded="" scope="An oil painting in the style of Vincent van Gogh featuring a raccoon in a
        dapper suit, complete with a black jacket, crisp white shirt, and a black bow tie. The
        raccoon is wearing a black top hat, adding a touch of elegance to its ensemble. The
        painting is rendered with characteristic van Gogh brushwork, utilizing thick, impasto
        strokes of color. The background is a swirl of blues, greens, and yellows, creating a
        vibrant yet slightly chaotic atmosphere that contrasts with the raccoon's formal attire.
        The lighting is dramatic, casting sharp shadows and highlighting the textures of the fabric
        and the raccoon's fur, enhancing the sense of realism within the fantastical scene. The
        composition focuses on the raccoon's proud posture, highlighting the whimsical contrast of
        a wild animal dressed in formal attire, captured in the unique artistic language of van
        Gogh. "><span><var spellcheck="false" is-upgraded="">An oil painting in the style of Vincent van Gogh featuring a raccoon in a dapper suit, complete with a black jacket, crisp white shirt, and a black bow tie. The raccoon is wearing a black top hat, adding a touch of elegance to its ensemble. The painting is rendered with characteristic van Gogh brushwork, utilizing thick, impasto strokes of color. The background is a swirl of blues, greens, and yellows, creating a vibrant yet slightly chaotic atmosphere that contrasts with the raccoon's formal attire. The lighting is dramatic, casting sharp shadows and highlighting the textures of the fabric and the raccoon's fur, enhancing the sense of realism within the fantastical scene. The composition focuses on the raccoon's proud posture, highlighting the whimsical contrast of a wild animal dressed in formal attire, captured in the unique artistic language of van Gogh. </var></span></devsite-var>",</strong>
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES</var></span></devsite-var>"
    }
  ]
}
```