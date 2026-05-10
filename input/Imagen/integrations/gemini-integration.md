Gemini 2.0 Flash supports response generation in multiple modalities, including text and images.

## Image generation

Gemini 2.0 Flash's public preview for image generation (`gemini-2.0-flash-preview-image-generation`) supports the ability to generate images in addition to text. This expands Gemini's capabilities to include the following:

-   Iteratively generate images through conversation with natural language, adjusting images while maintaining consistency and context.
-   Generate images with high-quality long text rendering.
-   Generate interleaved text-image output. For example, a blog post with text and images in a single turn. Previously, this required stringing together multiple models.
-   Generate images using Gemini's world knowledge and reasoning capabilities.

With this public experimental release, Gemini 2.0 Flash can generate images in 1024px, supports generating and editing images of people, and contains updated safety filters that provide a more flexible and less restrictive user experience.

It supports the following modalities and capabilities:

-   Text to image
    
    -   **Example prompt:** "Generate an image of the Eiffel tower with fireworks in the background."
-   Text to image (text rendering)
    
    -   **Example prompt:** "generate a cinematic photo of a large building with this giant text projection mapped on the front of the building: "Gemini 2.0 can now generate long form text""
-   Text to image(s) and text (interleaved)
    
    -   **Example prompt:** "Generate an illustrated recipe for a paella. Create images alongside the text as you generate the recipe."
    -   **Example prompt:** "Generate a story about a dog in a 3D cartoon animation style. For each scene, generate an image"
-   Image(s) and text to image(s) and text (interleaved)
    
    -   **Example prompt:** (With an image of a furnished room) "What other color sofas would work in my space? Can you update the image?"
-   Image editing (text and image to image)
    
    -   **Example prompt:** "Edit this image to make it look like a cartoon"
    -   **Example prompt:** \[image of a cat\] + \[image of a pillow\] + "Create a cross stitch of my cat on this pillow."
-   Multi-turn image editing (chat)
    
    -   **Example prompts:** \[upload an image of a blue car.\] "Turn this car into a convertible." "Now change the color to yellow."

**Limitations:**

-   For best performance, use the following languages: EN, es-MX, ja-JP, zh-CN, hi-IN.
-   Image generation does not support audio or video inputs.
-   Image generation may not always trigger:
    -   The model may output text only. Try asking for image outputs explicitly. For example, "provide images as you go along."
    -   The model may generate text as an image. Try asking for text outputs explicitly. For example, "generate narrative text along with illustrations."
    -   The model may stop generating partway through. Try again or try a different prompt.

The following sections cover how to generate images using either Vertex AI Studio or using the API.

For guidance and best practices for prompting, see [Design multimodal prompts](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/design-multimodal-prompts#fundamentals).

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python-gen-ai-sdk)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Run the following command in the terminal to create or overwrite this file in the current directory:

```
curl<span> </span>-X<span> </span>POST<span> </span><span>\</span>
<span>  </span>-H<span> </span><span>"Authorization: Bearer </span><span>$(</span>gcloud<span> </span>auth<span> </span>print-access-token<span>)</span><span>"</span><span> </span><span>\</span>
<span>  </span>-H<span> </span><span>"Content-Type: application/json"</span><span> </span><span>\</span>
<span>  </span>https://<span>${</span><span>API_ENDPOINT</span><span>}</span>:generateContent<span> </span><span>\</span>
<span>  </span>-d<span> </span><span>'{</span>
<span>    "contents": {</span>
<span>      "role": "USER",</span>
<span>      "parts": { "text": "Create a tutorial explaining how to make a peanut butter and jelly sandwich in three easy steps."},</span>
<span>    },</span>
<span>    "generation_config": {</span>
<span>      "response_modalities": ["TEXT", "IMAGE"],</span>
<span>     },</span>
<span>     "safetySettings": {</span>
<span>      "method": "PROBABILITY",</span>
<span>      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",</span>
<span>      "threshold": "BLOCK_MEDIUM_AND_ABOVE"</span>
<span>    },</span>
<span>  }'</span><span> </span><span>2</span>&gt;/dev/null<span> </span>&gt;response.json
```

Gemini will generate an image based on your description. This process should take a few seconds, but may be comparatively slower depending on capacity.

## Edit an image

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python-gen-ai-sdk)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Run the following command in the terminal to create or overwrite this file in the current directory:

```
curl<span> </span>-X<span> </span>POST<span> </span><span>\</span>
<span>  </span>-H<span> </span><span>"Authorization: Bearer </span><span>$(</span>gcloud<span> </span>auth<span> </span>print-access-token<span>)</span><span>"</span><span> </span><span>\</span>
<span>  </span>-H<span> </span><span>"Content-Type: application/json"</span><span> </span><span>\</span>
<span>  </span>https://<span>${</span><span>API_ENDPOINT</span><span>}</span>:generateContent<span> </span><span>\</span>
<span>  </span>-d<span> </span><span>'{</span>
<span>    "contents": {</span>
<span>      "role": "USER",</span>
<span>      "parts": [</span>
<span>        {"file_data": {</span>
<span>          "mime_type": "image/jpg",</span>
<span>          "file_uri": "&lt;var&gt;FILE_NAME&lt;/var&gt;"</span>
<span>          }</span>
<span>        },</span>
<span>        {"text": "Convert this photo to black and white, in a cartoonish style."},</span>
<span>      ]</span>

<span>    },</span>
<span>    "generation_config": {</span>
<span>      "response_modalities": ["TEXT", "IMAGE"],</span>
<span>    },</span>
<span>    "safetySettings": {</span>
<span>      "method": "PROBABILITY",</span>
<span>      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",</span>
<span>      "threshold": "BLOCK_MEDIUM_AND_ABOVE"</span>
<span>    },</span>
<span>  }'</span><span> </span><span>2</span>&gt;/dev/null<span> </span>&gt;response.json
```

Gemini will generate an image based on your description. This process should take a few seconds, but may be comparatively slower depending on capacity.

## Generate interleaved images and text

Gemini 2.0 Flash can generate interleaved images with its text responses. For example, you can generate images of what each step of a generated recipe might look like to go along with the text of that step, without having to make separate requests to the model to do so.

[Console](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#console)[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python-gen-ai-sdk)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)

Run the following command in the terminal to create or overwrite this file in the current directory:

```
curl<span> </span>-X<span> </span>POST<span> </span><span>\</span>
<span>  </span>-H<span> </span><span>"Authorization: Bearer </span><span>$(</span>gcloud<span> </span>auth<span> </span>print-access-token<span>)</span><span>"</span><span> </span><span>\</span>
<span>  </span>-H<span> </span><span>"Content-Type: application/json"</span><span> </span><span>\</span>
<span>  </span>https://<span>${</span><span>API_ENDPOINT</span><span>}</span>:generateContent<span> </span><span>\</span>
<span>  </span>-d<span> </span><span>'{</span>
<span>    "contents": {</span>
<span>      "role": "USER",</span>
<span>      "parts": { "text": "Create a tutorial explaining how to make a peanut butter and jelly sandwich in three easy steps. For each step, provide a title with the number of the step, an explanation, and also generate an image, generate each image in a 1:1 aspect ratio."},</span>
<span>    },</span>
<span>    "generation_config": {</span>
<span>      "response_modalities": ["TEXT", "IMAGE"],</span>
<span>     },</span>
<span>     "safetySettings": {</span>
<span>      "method": "PROBABILITY",</span>
<span>      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",</span>
<span>      "threshold": "BLOCK_MEDIUM_AND_ABOVE"</span>
<span>    },</span>
<span>  }'</span><span> </span><span>2</span>&gt;/dev/null<span> </span>&gt;response.json
```

Gemini will generate an image based on your description. This process should take a few seconds, but may be comparatively slower depending on capacity.