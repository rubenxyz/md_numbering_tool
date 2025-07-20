## How to Generate Videos using the fal API

fal offers a simple and easy-to-use API that allows you to generate videos from your images using pre-trained models. This endpoint is perfect for creating video clips from your images for various use cases such as social media, marketing, and more.

Here is an example of how to generate videos using the fal API:

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>const </span><span>result</span><span> = await </span><span>fal</span><span>.</span><span>subscribe</span><span>(</span><span>"</span><span>fal-ai/minimax-video/image-to-video</span><span>"</span><span>, {</span></p></div><div><p><span><span>  </span></span><span>input: {</span></p></div><div><p><span><span>    </span></span><span>prompt: </span><span>"</span><span>A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage.</span><span>"</span><span>,</span></p></div><div><p><span><span>    </span></span><span>image_url: </span><span>"</span><span>https://fal.media/files/elephant/8kkhB12hEZI2kkbU8pZPA_test.jpeg</span><span>"</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>}</span><span>);</span></p></div>
```

## How to select the model to use

fal offers a variety of video generation models. You can select the model that best fits your needs based on the style and quality of the images you want to generate. Here are some of the available models:

-   [fal-ai/minimax-video](https://fal.ai/models/fal-ai/minimax-video/image-to-video): Generate video clips from your images using MiniMax Video model.
-   [fal-ai/luma-dream-machine](https://fal.ai/models/fal-ai/luma-dream-machine/image-to-video): Generate video clips from your images using Luma Dream Machine v1.5
-   [fal-ai/kling-video/v1/standard](https://fal.ai/models/fal-ai/kling-video/v1/standard/image-to-video): Generate video clips from your images using Kling 1.0

To select a model, simply specify the model ID in the subscribe method as shown in the example above. You can find more models and their descriptions in the [Image to Video Models](https://fal.ai/models?categories=image-to-video) page.