<iframe frameborder="0" allowfullscreen="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" width="640" height="360" src="https://www.youtube.com/embed/nEuNwULfGXk?origin=https%3A%2F%2Fcloud.google.com&amp;autoplay&amp;controls&amp;embed_domain&amp;enablejsapi=1&amp;end&amp;hl&amp;showinfo&amp;start&amp;video-id=nEuNwULfGXk&amp;widgetid=5&amp;forigin=https%3A%2F%2Fcloud.google.com%2Fvertex-ai%2Fgenerative-ai%2Fdocs%2Fimage%2Foverview&amp;aoriginsup=1&amp;vf=1" id="widget6" data-title="Photorealistic images from Imagen 3"></iframe>

Imagen on Vertex AI brings Google's state of the art image generative AI capabilities to application developers. With Imagen on Vertex AI, application developers can build next-generation AI products that transform their user's imagination into high quality visual assets using AI generation, in seconds.

[Try image generation (Vertex AI Studio)](https://console.cloud.google.com/vertex-ai/studio/media/generate;tab=image)

[Try Imagen in a Colab](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/imagen4_image_generation.ipynb)

With Imagen, you can do the following:

-   Generate novel images using only a text prompt (text-to-image AI generation).
-   Edit or expand an uploaded or generated image using a mask area you define.
-   Upscale existing, generated, or edited images.

#### Prompts for preceding images

## Quickstart: Generate images from text prompts

You can generate novel images using only descriptive text as an input. The following samples show a simplified case for generating images, but you can use [additional parameters](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images#use-params) to tailor the generated images to your needs.

2.  Set up authentication for your environment.
    
    Select the tab for how you plan to use the samples on this page:
    
    [Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)
    
    To use the REST API samples on this page in a local development environment, you use the credentials you provide to the gcloud CLI.
    
    After [installing](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI, [initialize](https://cloud.google.com/sdk/docs/initializing) it by running the following command:
    
    ```
    gcloud<span> </span>init
    ```
    
    If you're using an external identity provider (IdP), you must first [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
    
    For more information, see [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest) in the Google Cloud authentication documentation.
    
3.  Use the following samples to generate an image:
    
    [Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python)[REST](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#rest)
    
    1.  Set environment variables:
        
        ```
        <span>export</span><span> </span><span>GOOGLE_CLOUD_PROJECT</span><span>=</span><devsite-var rendered="" translate="no" is-upgraded="" scope="GOOGLE_CLOUD_PROJECT" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit GOOGLE_CLOUD_PROJECT" aria-label="Edit GOOGLE_CLOUD_PROJECT">GOOGLE_CLOUD_PROJECT</var></span></devsite-var><span> </span><span># Replace with your Google Cloud project</span>
        <span>export</span><span> </span><span>GOOGLE_CLOUD_LOCATION</span><span>=</span>us-central1<span> </span><span># Replace with the appropriate location for your project</span>
        <span>            </span>
        ```
                    
    2.  Run the following:
        
        ```
        curl<span> </span>-X<span> </span>POST<span> </span><span>\</span>
        -H<span> </span><span>"Authorization: Bearer </span><span>$(</span>gcloud<span> </span>auth<span> </span>print-access-token<span>)</span><span>"</span><span> </span><span>\</span>
        -H<span> </span><span>"Content-Type: application/json; charset=utf-8"</span><span> </span><span>\</span>
        <span>"https://</span><span>${</span><span>GOOGLE_CLOUD_LOCATION</span><span>}</span><span>-aiplatform.googleapis.com/v1/projects/</span><span>${</span><span>GOOGLE_CLOUD_PROJECT</span><span>}</span><span>/locations/</span><span>${</span><span>GOOGLE_CLOUD_LOCATION</span><span>}</span><span>/publishers/google/models/imagen-4.0-generate-preview-05-20:predict"</span><span> </span>-d<span> </span><span>\</span>
        <span>$'{</span>
        <span>  "instances": [</span>
        <span>    {</span>
        <span>      "prompt": "a cat reading a book"</span>
        <span>    }</span>
        <span>  ],</span>
        <span>  "parameters": {</span>
        <span>    "sampleCount": 1</span>
        <span>  }</span>
        <span>}'</span>
        <span>            </span>
        ```
                    
        
        The model returns a base64 image bytes object.
        
    
    For more information, see the Imagen [Generate images API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api).
    

## Product usage

To view usage standards and content restrictions associated with Imagen on Vertex AI, see the [usage guidelines](https://cloud.google.com/vertex-ai/generative-ai/docs/image/responsible-ai-imagen#imagen-guidelines).

## Model versions

There are multiple image generation models that you can use. For more information, see [Imagen models](https://cloud.google.com/vertex-ai/generative-ai/docs/models#imagen-models).

## Try more examples

For a full list of Jupyter notebook tutorials using Imagen, see the [Generative AI on Vertex AI cookbook](https://cloud.google.com/vertex-ai/generative-ai/docs/cookbook).

## What's next

Use the following links to view the feature documentation.

Image credit: All images generated using Imagen on Vertex AI.