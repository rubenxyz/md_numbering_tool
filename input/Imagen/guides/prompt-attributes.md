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
        -   Configure Imagen parameters
            
        
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

## Prompt and image attribute guide

bookmark\_border Stay organized with collections Save and categorize content based on your preferences.

To use Imagen on Vertex AI you must provide a text description of what you want to generate or edit. These descriptions are called _prompts_, and these prompts are the primary way you communicate with Generative AI on Vertex AI.

This guide shows you how modifying parts of a text-to-image prompt can produce different results and gives you examples of images you can create. This guide also provides guidance on how you can edit images using text prompts and iteration.

## Product usage

To view usage standards and content restrictions associated with Imagen on Vertex AI, see the [usage guidelines](https://cloud.google.com/vertex-ai/generative-ai/docs/image/responsible-ai-imagen#imagen-guidelines).

## Content filtering - input text, uploaded images, and generated images

Generated images are filtered for undesirable or harmful content. Similarly, any input Imagen on Vertex AI receives is checked for offensive content. This includes the input text prompt and uploaded photos in the case of image editing. For more information, see [Responsible AI and usage guidelines for Imagen](https://cloud.google.com/vertex-ai/generative-ai/docs/image/responsible-ai-imagen).

You can also report suspected abuse of Imagen on Vertex AI or any generated output that contains inappropriate material or inaccurate information using the [Report suspected abuse on Google Cloud](https://support.google.com/code/contact/cloud_platform_report) form.

## Prompt writing basics (subject, context, and style)

While there's no one way to write good prompts, adding some keywords and modifiers will help you get closer to your end goal. Prompts don't need to be long or complex, but most good prompts are descriptive and clear.

A good starting point can be to think of **subject**, **context**, and **style**.

![Prompt with subject, context, and style emphasized](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/style-subject-context.png)

Image text: A _sketch_ (**style**) of a _modern apartment building_ (**subject**) surrounded by _skyscrapers_ (**context and background**).

1.  **Subject**: The first thing to think about with any prompt is the _subject_: the object, person, animal, or scenery you want an image of.
    
2.  **Context and background:** Just as important is the _background or context_ in which the subject will be placed. Try placing your subject in a variety of backgrounds. For example, a studio with a white background, outdoors, or indoor environments.
    
3.  **Style:** Finally, add the style of image you want. _Styles_ can be general (painting, photograph, sketches) or very specific (pastel painting, charcoal drawing, isometric 3D).
    

After you write a first version of your prompt, refine your prompt by adding more details until you get to the image that you want. Iteration is important. Start by establishing your core idea, and then refine and expand upon that core idea until the generated image is close to your vision.

### Imagen 3 prompt writing

[View Imagen for Generation model card](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/imagen-4.0-generate-preview-06-06)

Imagen 3 can transform your ideas into detailed images, whether your prompts are short or long and detailed. Refine your vision through iterative prompting, adding details until you achieve the perfect result.

<table><tbody><tr><td><div><p>Short prompts let you generate an image quickly.</p><figure><img src="https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/imagen3_short-prompt.png" alt="Imagen 3 short prompt example"><figcaption>Prompt: close-up photo of a woman in her 20s, street photography, movie still, muted orange warm tones</figcaption></figure></div></td><td><div><p>Longer prompts let you add specific details and build your image.</p><figure><img src="https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/imagen3_long-prompt.png" alt="Imagen 3 long prompt example"><figcaption>Prompt: captivating photo of a woman in her 20s utilizing a street photography style. The image should look like a movie still with muted orange warm tones.</figcaption></figure></div></td></tr></tbody></table>

Additional advice for Imagen 3 prompt writing:

-   **Use descriptive language**: Employ detailed adjectives and adverbs to paint a clear picture for Imagen 3.
-   **Provide context**: If necessary, include background information to aid the AI's understanding.
-   **Reference specific artists or styles**: If you have a particular aesthetic in mind, referencing specific artists or art movements can be helpful.
-   **Use prompt engineering tools**: Consider exploring prompt engineering tools or resources to help you refine your prompts and achieve optimal results.
-   **Enhancing the facial details in your personal and group images**:
    -   Specify facial details as a focus of the photo (for example, use the word "portrait" in the prompt).
    -   Consider using a larger model like Imagen 3 instead of Imagen 3 Fast to improve detail.

### Generate text in images

Imagen 3's ability to add text into your images opens up creative image generation possibilities. Use the following guidance to get the most out of this feature:

-   **Iterate with confidence**: You might have to regenerate images until you achieve the look you want. Imagen's text integration is still evolving, and sometimes multiple attempts yield the best results.
-   **Keep it short**: Limit text to 25 characters or less for optimal generation.
-   **Multiple phrases**: Experiment with two or three distinct phrases to provide additional information. Avoid exceeding three phrases for cleaner compositions.
    
    ![Imagen 3 generate text example](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/imagen3_generate-text.png)
    
    Prompt: A poster with the text "Summerland" in bold font as a title, underneath this text is the slogan "Summer never felt so good"
    
-   **Guide Placement**: While Imagen can attempt to position text as directed, you should expect occasional variations. This feature is continually improving.
    
-   **Inspire font style**: Specify a general font style to subtly influence Imagen's choices. Don't rely on precise font replication, but expect creative interpretations.
    
-   **Font size**: Specify a font size or a general indication of size (for example, _small_, _medium_, _large_) to influence the font size generation.
    

### Prompt parameterization

To better control output results, you might find it helpful to parameterize the inputs into Imagen when working with the Imagen API or Vertex AI SDK for Python. For example, suppose you want your customers to be able to generate logos for their business, and you want to make sure logos are always generated on a solid color background. You also want to limit the options that the client can select from a menu.

In this example, you can create a parameterized prompt similar to the following:

```
A <devsite-var rendered="" translate="no" is-upgraded="" scope="{logo_style}"><span><var spellcheck="false" is-upgraded="">{logo_style}</var></span></devsite-var> logo for a <devsite-var rendered="" translate="no" is-upgraded="" scope="{company_area}"><span><var spellcheck="false" is-upgraded="">{company_area}</var></span></devsite-var> company on a solid color background. Include the text <devsite-var rendered="" translate="no" is-upgraded="" scope="{company_name}"><span><var spellcheck="false" is-upgraded="">{company_name}</var></span></devsite-var>.
```

In your custom user interface, the customer can input the parameters using a menu, and their chosen value populates the prompt Imagen receives.

For example:

1.  Prompt: `A minimalist logo for a health care company on a solid color background. Include the text Journey.`
    
    ![Imagen 3 prompt parameterization example 1](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/imagen3_prompt-param_healthcare.png)
    
2.  Prompt: `A modern logo for a software company on a solid color background. Include the text Silo.`
    
    ![Imagen 3 prompt parameterization example 2](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/imagen3_prompt-param_software.png)
    
3.  Prompt: `A traditional logo for a baking company on a solid color background. Include the text Seed.`
    
    ![Imagen 3 prompt parameterization example 3](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/imagen3_prompt-param_baking.png)
    

### Style: photography

-   Prompt includes: _"A photo of..."_

To use this style, start with using keywords that clearly tell Imagen on Vertex AI that you're looking for a photograph. Start your prompts with _"A photo of. . ."_. For example:

<sup>Image source: Each image was generated using its corresponding text prompt with the Imagen&nbsp;3 model.</sup>

### Style: illustration and art

-   Prompt includes: _"A painting of..."_, _"A sketch of..."_

Art styles vary from monochrome styles like pencil sketches, to hyper-realistic digital art. For example, the following images use the same prompt with different styles:

_"An \[art style or creation technique\] of an angular sporty electric sedan with skyscrapers in the background"_

<sup>Image source: Each image was generated using its corresponding text prompt with the Imagen&nbsp;2 model.</sup>

## Advanced prompt writing techniques

Use the following examples to create more specific prompts based on the attributes: photography descriptors, shapes and materials, historical art movements, and image quality modifiers.

### Photography modifiers

In the following examples, you can see several photography-specific modifiers and parameters.

1.  **Camera Proximity** - _Close up, taken from far away_
    
2.  **Camera Position** - _aerial, from below_
    
3.  **Lighting** - _natural, dramatic, warm, cold_
    
4.  **Camera Settings** _\- motion blur, soft focus, bokeh, portrait_
    
5.  **Lens types** - _35mm, 50mm, fisheye, wide angle, macro_
    
6.  **Film types** - _black and white, polaroid_
    

<sup>Image source: Each image was generated using its corresponding text prompt with the Imagen&nbsp;3 model.</sup>

### Shapes and materials

-   Prompt includes: _"...made of..."_, _"...in the shape of..."_

One of the strengths of this technology is that you can create imagery that is otherwise difficult or impossible. For example, you can recreate your company logo in different materials and textures.

<sup>Image source: Each image was generated using its corresponding text prompt with the Imagen&nbsp;3 model.</sup>

### Historical art references

-   Prompt includes: _"...in the style of..."_

Certain styles have become iconic over the years. The following are some ideas of historical painting or art styles that you can try.

_"generate an image in the style of \[art period or movement\]: a wind farm"_

<sup>Image source: Each image was generated using its corresponding text prompt with the Imagen&nbsp;3 model.</sup>

### Image quality modifiers

Certain keywords can let the model know that you're looking for a high-quality asset. Examples of quality modifiers include the following:

-   **General Modifiers** - _high-quality, beautiful, stylized_
-   **Photos** - _4K, HDR, Studio Photo_
-   **Art, Illustration** - _by a professional, detailed_

The following are a few examples of prompts without quality modifiers and the same prompt with quality modifiers.

<sup>Image source: Each image was generated using its corresponding text prompt with the Imagen&nbsp;3 model.</sup>

### Aspect ratios

Imagen 3 image generation lets you set five distinct image aspect ratios.

1.  **Square** (1:1, default) - A standard square photo. Common uses for this aspect ratio include social media posts.
2.  **Fullscreen** (4:3) - This aspect ratio is commonly used in media or film. It is also the dimensions of most old (non-widescreen) TVs and medium format cameras. It captures more of the scene horizontally (compared to 1:1), making it a preferred aspect ratio for photography.
    
3.  **Portrait full screen** (3:4) - This is the fullscreen aspect ratio rotated 90 degrees. This lets to capture more of the scene vertically compared to the 1:1 aspect ratio.
    
4.  **Widescreen** (16:9) - This ratio has replaced 4:3 and is now the most common aspect ratio for TVs, monitors, and mobile phone screens (landscape). Use this aspect ratio when you want to capture more of the background (for example, scenic landscapes).
    
    ![aspect ratio example](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratios_16-9_man.png)
    
    Prompt: a man wearing all white clothing sitting on the beach, close up, golden hour lighting (16:9 aspect ratio)
    
5.  **Portrait** (9:16) - This ratio is widescreen but rotated. This a relatively new aspect ratio that has been popularized by short form video apps (for example, YouTube shorts). Use this for tall objects with strong vertical orientations such as buildings, trees, waterfalls, or other similar objects.
    
    ![aspect ratio example](https://cloud.google.com/static/vertex-ai/generative-ai/docs/image/images/aspect-ratios_9-16_skyscraper.png)
    
    Prompt: a digital render of a massive skyscraper, modern, grand, epic with a beautiful sunset in the background (9:16 aspect ratio)
    

### Negative prompts

The previous examples focus on writing prompts for what you want Imagen to create, but you can also provide a _negative_ prompt along with the original prompt to help the product generate or edit images. These negative prompts can be a powerful tool that helps specify what elements to omit from the image. Simply describe what you _don't want_.

Recommended — Plainly describe what you don't want to see. For example "_wall, frame_".

Not recommended — Avoid instructive language or words like "no" or "don't". For example, avoid phrases like "_**no** walls_" or "_**don't show** walls_".

### Photorealistic images

Different [versions](https://cloud.google.com/vertex-ai/generative-ai/docs/image/model-versioning) of the image generation model might offer a mix of artistic and photorealistic output. Use the following wording in prompts to generate more photorealistic output, based on the subject you want to generate.

| Use case | Lens type | Focal lengths | Additional details |
| --- | --- | --- | --- |
| People (portraits) | Prime, zoom | 24-35mm | black and white film, Film noir, Depth of field, duotone (mention two colors) |
| Food, insects, plants (objects, still life) | Macro | 60-105mm | High detail, precise focusing, controlled lighting |
| Sports, wildlife (motion) | Telephoto zoom | 100-400mm | Fast shutter speed, Action or movement tracking |
| Astronomical, landscape (wide-angle) | Wide-angle | 10-24mm | Long exposure times, sharp focus, long exposure, smooth water or clouds |

#### Portraits

| Use case | Lens type | Focal lengths | Additional details |
| --- | --- | --- | --- |
| People (portraits) | Prime, zoom | 24-35mm | black and white film, Film noir, Depth of field, duotone (mention two colors) |

Using several keywords from the table, Imagen can generate the following portraits.

Prompt: _A woman, 35mm portrait, blue and grey duotones_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

Prompt: _A woman, 35mm portrait, film noir_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

#### Objects

| Use case | Lens type | Focal lengths | Additional details |
| --- | --- | --- | --- |
| Food, insects, plants (objects, still life) | Macro | 60-105mm | High detail, precise focusing, controlled lighting |

Using several keywords from the table, Imagen can generate the following object images.

Prompt: _leaf of a prayer plant, macro lens, 60mm_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

Prompt: _a plate of pasta, 100mm Macro lens_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

#### Motion

| Use case | Lens type | Focal lengths | Additional details |
| --- | --- | --- | --- |
| Sports, wildlife (motion) | Telephoto zoom | 100-400mm | Fast shutter speed, Action or movement tracking |

Using several keywords from the table, Imagen can generate the following motion images.

Prompt: _a winning touchdown, fast shutter speed, movement tracking_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

Prompt: _A deer running in the forest, fast shutter speed, movement tracking_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

#### Wide-angle

| Use case | Lens type | Focal lengths | Additional details |
| --- | --- | --- | --- |
| Astronomical, landscape (wide-angle) | Wide-angle | 10-24mm | Long exposure times, sharp focus, long exposure, smooth water or clouds |

Using several keywords from the table, Imagen can generate the following wide-angle images.

Prompt: _an expansive mountain range, landscape wide angle 10mm_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

Prompt: _a photo of the moon, astro photography, wide angle 10mm_  
Model: Imagen 3 (`imagen-3.0-generate-002`)

## What's next

Read articles about Imagen and other Generative AI on Vertex AI products:

-   [A developer's guide to getting started with Imagen 3 on Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/a-developers-guide-to-imagen-3-on-vertex-ai?e=0?utm_source%3Dlinkedin)
-   [New generative media models and tools, built with and for creators](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/#veo)
-   [New in Gemini: Custom Gems and improved image generation with Imagen 3](https://blog.google/products/gemini/google-gemini-update-august-2024/)
-   [Google DeepMind: Imagen 3 - Our highest quality text-to-image model](https://deepmind.google/technologies/imagen-3/)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-18 UTC.

The new page has loaded..