[Try image generation (Vertex AI Studio)](https://console.cloud.google.com/vertex-ai/studio/media/generate;tab=image)

[Try Imagen in a Colab](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen4_image_generation.ipynb)

This page describes how you can set an optional Imagen on Vertex AI parameter to specify the prompt language that you use. If you don't specify a language, then Imagen automatically detects the language.

<table><tbody><tr><td><figure><p><img src="https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/gen-img_param_prompt-lang_hindi.png" alt="a book image generated from a prompt in hindi"></p><figcaption>Image generated from prompt: ऊपर से देखा गया किताबों का ढेर। सबसे ऊपरी पुस्तक में एक पक्षी का जलरंग चित्रण है। किताब पर VERTEX AI मोटे अक्षरों में लिखा हुआ है <sup>1</sup><p><sup>1</sup> <i>A pile of books seen from above. The topmost book contains a watercolor illustration of a bird. <b>VERTEX AI</b> is written in bold letters on the book.</i></p></figcaption></figure></td><td><figure><p><img src="https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/gen-img_param_prompt-lang_korean.png" alt="an image of a woman from a prompt in korean"></p><figcaption>Image generated from prompt: 어두운 노란색과 청록색으로 이루어진 밝은 색의 옷을입고 귀걸이를 끼고있는 여자 포스트 모던 패션 사진 <sup>2</sup><p><sup>2</sup> <i>Woman wearing bright colors, in the style of dark yellow and dark cyan, wearing earrings, postmodern fashion photography.</i></p></figcaption></figure></td></tr></tbody></table>

The following input values are supported for the text-prompt lanague:

-   Chinese (simplified) (`zh`/`zh-CN`)
-   Chinese (traditional) (`zh-TW`)
-   English (`en`, default value)
-   French (`fr`)
-   German (`de`)
-   Hindi (`hi`)
-   Japanese (`ja`)
-   Korean (`ko`)
-   Portuguese (`pt`)
-   Spanish (`es`)
    

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console) [REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Before using any of the request data, make the following replacements:

-   PROJECT\_ID: Your Google Cloud [project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifiers).
-   TEXT\_PROMPT: The text prompt that guides what images the model generates. This field is required for both generation and editing.
-   PROMPT\_LANGUAGE: string. Optional. The language code that corresponds to your text prompt language. In this example it would be `hi`. Available values:
    -   `auto` - Automatic detection. If Imagen detects a supported language, the prompt (and optionally, a negative prompt), are translated to English. If the language detected is not supported, Imagen uses the input text verbatim, which might result in unexpected output. No error code is returned.
    -   `en` - English (default value if omitted)
    -   `es` - Spanish
    -   `hi` - Hindi
    -   `ja` - Japanese
    -   `ko` - Korean
    -   `pt` - Portuguese
    -   `zh-TW` - Chinese (traditional)
    -   `zh` or `zh-CN` - Chinese (simplified)

HTTP method and URL:

```
POST https://us-central1-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/us-central1/publishers/google/models/imagegeneration<devsite-var rendered="" translate="no" is-upgraded="" scope="@005" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit @005" aria-label="Edit @005">@005</var></span></devsite-var>:predict
```

Request JSON body:

```
{
  "instances": [
    {
      "prompt": "<devsite-var rendered="" translate="no" is-upgraded="" scope="सूर्यास्त के समय एक समुद्र तट। उड़ते पक्षी, हवा में लहराते नारियल के पेड़। लोग समुद्र तट पर सैर का आनंद ले रहे हैं।" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit सूर्यास्त के समय एक समुद्र तट। उड़ते पक्षी, हवा में लहराते नारियल के पेड़। लोग समुद्र तट पर सैर का आनंद ले रहे हैं।" aria-label="Edit सूर्यास्त के समय एक समुद्र तट। उड़ते पक्षी, हवा में लहराते नारियल के पेड़। लोग समुद्र तट पर सैर का आनंद ले रहे हैं।">सूर्यास्त के समय एक समुद्र तट। उड़ते पक्षी, हवा में लहराते नारियल के पेड़। लोग समुद्र तट पर सैर का आनंद ले रहे हैं।</var></span></devsite-var>"
    }
  ],
  "parameters": {<strong>
    "language": "<devsite-var rendered="" translate="no" is-upgraded="" scope="PROMPT_LANGUAGE" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROMPT_LANGUAGE" aria-label="Edit PROMPT_LANGUAGE">PROMPT_LANGUAGE</var></span></devsite-var>"</strong>
  }
}
```

To send your request, choose one of these options:

[curl](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#curl)[PowerShell](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#powershell)

Save the request body in a file named `request.json`, and execute the following command:

```
curl -X POST \<br>     -H "Authorization: Bearer $(gcloud auth print-access-token)" \<br>     -H "Content-Type: application/json; charset=utf-8" \<br>     -d @request.json \<br>     "https://us-central1-aiplatform.googleapis.com/v1/projects/<devsite-var rendered="" translate="no" is-upgraded="" scope="PROJECT_ID" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit PROJECT_ID" aria-label="Edit PROJECT_ID">PROJECT_ID</var></span></devsite-var>/locations/us-central1/publishers/google/models/imagegeneration<devsite-var rendered="" translate="no" is-upgraded="" scope="@005" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit @005" aria-label="Edit @005">@005</var></span></devsite-var>:predict"
```

The following sample response is for a request with `"sampleCount": 2`. The response returns two prediction objects, with the generated image bytes base64-encoded.

```
{
  "predictions": [
    {
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES</var></span></devsite-var>",
      "mimeType": "image/png"
    },
    {
      "mimeType": "image/png",
      "bytesBase64Encoded": "<devsite-var rendered="" translate="no" is-upgraded="" scope="BASE64_IMG_BYTES"><span><var spellcheck="false" is-upgraded="">BASE64_IMG_BYTES</var></span></devsite-var>"
    }
  ]
}
```

## What's next

-   [Use prompt rewriter](https://cloud.google.com/vertex-ai/generative-ai/docs/image/use-prompt-rewriter)
-   [Configure aspect ratio](https://cloud.google.com/vertex-ai/generative-ai/docs/image/configure-aspect-ratio)
-   [Omit content using a negative prompt](https://cloud.google.com/vertex-ai/generative-ai/docs/image/omit-content-using-a-negative-prompt)
-   [Generate deterministic images](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-deterministic-images)