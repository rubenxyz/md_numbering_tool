In this example, we’ll be using our most popular [optimized ultra fast latent consistency model](https://fal.ai/models/fast-lcm-diffusion-turbo/api).

All our Model Endpoint’s support HTTP/REST. Additionally our real-time models support WebSockets. You can use the HTTP/REST endpoint for any real time model but if you are sending back to back requests using websockets gives the best results.

Before we proceed, you need to create your [API key](https://fal.ai/dashboard/keys).

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>fal</span><span>.</span><span>config</span><span>({</span></p></div><div><p><span><span>  </span></span><span>credentials: </span><span>"</span><span>PASTE_YOUR_FAL_KEY_HERE</span><span>"</span><span>,</span></p></div><div><p><span>});</span></p></div><div><p><span>const </span><span>connection</span><span> = </span><span>fal</span><span>.</span><span>realtime</span><span>.</span><span>connect</span><span>(</span><span>"</span><span>fal-ai/fast-lcm-diffusion</span><span>"</span><span>, {</span></p></div><div><p><span>  </span><span>onResult</span><span>: </span><span>(</span><span>result</span><span>)</span><span> =&gt; {</span></p></div><div><p><span>    </span><span>console</span><span>.</span><span>log</span><span><span>(</span><span>result</span><span>)</span></span><span>;</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>  </span><span>onError</span><span>: </span><span>(</span><span>error</span><span>)</span><span> =&gt; {</span></p></div><div><p><span>    </span><span>console</span><span>.</span><span>error</span><span><span>(</span><span>error</span><span>)</span></span><span>;</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>}</span><span>);</span></p></div><div><p><span>connection</span><span>.</span><span>send</span><span>({</span></p></div><div><p><span><span>  </span></span><span>prompt:</span></p></div><div><p><span>    </span><span>"</span><span>an island near sea, with seagulls, moon shining over the sea, light house, boats int he background, fish flying over the sea</span><span>"</span><span>,</span></p></div><div><p><span><span>  </span></span><span>sync_mode: </span><span>true</span><span>,</span></p></div><div><p><span><span>  </span></span><span>image_url:</span></p></div><div><p><span>    </span><span>"</span><span>data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==</span><span>"</span><span>,</span></p></div><div><p><span>});</span></p></div>
```

You can read more about the real time clients in our [real time client docs](https://docs.fal.ai/model-endpoints#the-fal-client) section.

**To get the best performance from this model:**

-   Make sure the image is provided as a base64 encoded data url.
-   Make sure the image\_url is exactly **512x512**.
-   Make sure sync\_mode is true, this will make sure you also get a base64 encoded data url back from our API.

You can also use **768x768** or **1024x1024** as your image dimensions, the inference will be faster for this configuration compared to random dimensions but wont be as fast as **512x512**.

**Video Tutorial:** _Latent Consistency - Build a Real-Time AI Image App with WebSockets, Next.js, and fal.ai by [Nader Dabit](https://twitter.com/dabit3)_

<iframe width="560" height="315" src="https://www.youtube.com/embed/freyCo3pcz4?si=OFfGsi0xwJVe__Yt" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen=""></iframe>