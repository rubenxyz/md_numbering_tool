We believe fal has the fastest FLUX endpoint in the planet. If you can find a faster one, we guarantee to beat it within one week. 🤝

Here is a quick guide on how to use this model from an API in less than 1 minute.

Before we proceed, you need to create an [API key](https://fal.ai/dashboard/keys).

This key secret will be used to authenticate your requests to the fal API.

```
<div><p><span>fal</span><span>.</span><span>config</span><span>({</span></p></div><div><p><span><span>  </span></span><span>credentials: </span><span>"</span><span>PASTE_YOUR_FAL_KEY_HERE</span><span>"</span><span>,</span></p></div><div><p><span>});</span></p></div>
```

Now you can call our Model API endpoint using the [fal js client](https://docs.fal.ai/model-endpoints#the-fal-client):

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>const </span><span>result</span><span> = await </span><span>fal</span><span>.</span><span>subscribe</span><span>(</span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>, {</span></p></div><div><p><span><span>  </span></span><span>input: {</span></p></div><div><p><span><span>    </span></span><span>prompt:</span></p></div><div><p><span>      </span><span>"</span><span>photo of a rhino dressed suit and tie sitting at a table in a bar with a bar stools, award winning photography, Elke vogelsang</span><span>"</span><span>,</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>}</span><span>);</span></p></div>
```