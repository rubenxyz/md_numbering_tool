### You will learn how to:

1.  Install the fal.ai libraries
2.  Add a server proxy to protect your credentials
3.  Generate an image using SDXL

### Prerequisites

1.  Have an existing Next.js app or create a new one using `npx create-next-app`
2.  Have a [fal.ai](https://fal.ai/) account
3.  Have an API Key. You can [create one here](https://fal.ai/dashboard/keys)

### 1\. Install the fal.ai libraries

Using your favorite package manager, install both the `@fal-ai/client` and `@fal-ai/server-proxy` libraries.

-   [npm](https://docs.fal.ai/integrations/nextjs#tab-panel-24)
-   [yarn](https://docs.fal.ai/integrations/nextjs#tab-panel-25)
-   [pnpm](https://docs.fal.ai/integrations/nextjs#tab-panel-26)

```
<div><p><span>npm</span><span> </span><span>install</span><span> </span><span>@fal-ai/client</span><span> </span><span>@fal-ai/server-proxy</span></p></div>
```

### 2\. Setup the proxy

The proxy will protect your API Key and prevent it from being exposed to the client. Usually app implementation have to handle that integration themselves, but in order to make the integration as smooth as possible, we provide a drop-in proxy implementation that can be integrated with either the **Page Router** or the **App Router**.

#### 2.1. Page Router

If you are using the **Page Router** (i.e. `src/pages/_app.js`), create an API handler in `src/pages/api/fal/proxy.js` (or `.ts` in case of TypeScript), and re-export the built-in proxy handler:

```
<div><p><span>export</span><span> { handler </span><span>as</span><span> </span><span>default</span><span> } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/server-proxy/nextjs</span><span>"</span><span>;</span></p></div>
```

#### 2.2. App Router

If you are using the **App Router** (i.e. `src/app/page.jsx`) create a route handler in `src/app/api/fal/proxy/route.js` (or `.ts` in case of TypeScript), and re-export the route handler:

```
<div><p><span>import</span><span> { route } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/server-proxy/nextjs</span><span>"</span><span>;</span></p></div><div><p><span>export const { </span><span>GET</span><span>, </span><span>POST</span><span> } = </span><span>route;</span></p></div>
```

#### 2.3. Setup the API Key

Make sure you have your API Key available as an environment variable. You can setup in your `.env.local` file for development and also in your hosting provider for production, such as [Vercel](https://vercel.com/docs/projects/environment-variables).

```
<div><p><span>FAL_KEY</span><span>=</span><span>"</span><span>key_id:key_secret</span><span>"</span></p></div>
```

#### 2.4. Custom proxy logic

It’s common for applications to execute custom logic before or after the proxy handler. For example, you may want to add a custom header to the request, or log the request and response, or apply some rate limit. The good news is that the proxy implementation is simply a standard Next.js API/route handler function, which means you can compose it with other handlers.

For example, let’s assume you want to add some analytics and apply some rate limit to the proxy handler:

```
<div><p><span>import</span><span> { route } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/server-proxy/nextjs</span><span>"</span><span>;</span></p></div><div><p><span>// Let's add some custom logic to POST requests - i.e. when the request is</span></p></div><div><p><span>// submitted for processing</span></p></div><div><p><span>export const </span><span>POST</span><span> = </span><span>(</span><span>req</span><span>)</span><span> =&gt; {</span></p></div><div><p><span>  </span><span>// Add some analytics</span></p></div><div><p><span>  </span><span>analytics</span><span>.</span><span>track</span><span>(</span><span>"</span><span>fal.ai request</span><span>"</span><span>, {</span></p></div><div><p><span><span>    </span></span><span>targetUrl: </span><span>req</span><span>.</span><span>headers</span><span>[</span><span>"</span><span>x-fal-target-url</span><span>"</span><span>]</span><span>,</span></p></div><div><p><span><span>    </span></span><span>userId: </span><span>req</span><span>.</span><span>user</span><span>.</span><span>id</span><span>,</span></p></div><div><p><span><span>  </span></span><span>}</span><span>)</span><span>;</span></p></div><div><p><span>  </span><span>// Apply some rate limit</span></p></div><div><p><span><span>  </span></span><span>if </span><span>(rateLimiter</span><span>.</span><span>shouldLimit</span><span>(req))</span><span> {</span></p></div><div><p><span>    </span><span>res</span><span>.</span><span>status</span><span>(</span><span>429</span><span>)</span><span>.</span><span>json</span><span>(</span><span>{ error: </span><span>"</span><span>Too many requests</span><span>"</span><span> }</span><span>)</span><span>;</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>  </span><span>// If everything passed your custom logic, now execute the proxy handler</span></p></div><div><p><span><span>  </span></span><span>return </span><span>route</span><span>.</span><span>POST</span><span>(req)</span><span>;</span></p></div><div><p><span>}</span><span>;</span></p></div><div><p><span>// For GET requests we will just use the built-in proxy handler</span></p></div><div><p><span>// But you could also add some custom logic here if you need</span></p></div><div><p><span>export const </span><span>GET</span><span> = </span><span>route</span><span>.</span><span>GET</span><span>;</span></p></div>
```

Note that the URL that will be forwarded to server is available as a header named `x-fal-target-url`. Also, keep in mind the example above is just an example, `rateLimiter` and `analytics` are just placeholders.

The example above used the app router, but the same logic can be applied to the page router and its `handler` function.

### 3\. Configure the client

On your main file (i.e. `src/pages/_app.jsx` or `src/app/page.jsx`), configure the client to use the proxy:

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>fal</span><span>.</span><span>config</span><span>({</span></p></div><div><p><span><span>  </span></span><span>proxyUrl: </span><span>"</span><span>/api/fal/proxy</span><span>"</span><span>,</span></p></div><div><p><span>});</span></p></div>
```

### 4\. Generate an image

Now that the client is configured, you can generate an image using `fal.subscribe` and pass the model id and the input parameters:

```
<div><p><span>const </span><span>result</span><span> = await </span><span>fal</span><span>.</span><span>subscribe</span><span>(</span><span>"</span><span>fal-ai/flux/dev</span><span>"</span><span>, {</span></p></div><div><p><span><span>  </span></span><span>input: {</span></p></div><div><p><span>    </span><span>prompt</span><span>,</span></p></div><div><p><span><span>    </span></span><span>image_size: </span><span>"</span><span>square_hd</span><span>"</span><span>,</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span><span>  </span></span><span>pollInterval: </span><span>5000</span><span>,</span></p></div><div><p><span><span>  </span></span><span>logs: </span><span>true</span><span>,</span></p></div><div><p><span>  </span><span>onQueueUpdate</span><span>(</span><span>update</span><span>)</span><span> {</span></p></div><div><p><span>    </span><span>console</span><span>.</span><span>log</span><span>(</span><span>"</span><span>queue update</span><span>"</span><span>, </span><span>update)</span><span>;</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>}</span><span>);</span></p></div><div><p><span>const </span><span>imageUrl</span><span> = </span><span>result</span><span>.</span><span>images</span><span>[</span><span>0</span><span>]</span><span>.</span><span>url</span><span>;</span></p></div>
```

See more about Flux Dev used in this example on [fal.ai/models/fal-ai/flux/dev](https://fal.ai/models/fal-ai/flux/dev).

### What’s next?

Image generation is just one of the many cool things you can do with fal. Make sure you:

-   Check our demo application at [github.com/fal-ai/serverless-js/apps/demo-nextjs-app-router](https://github.com/fal-ai/fal-js/tree/main/apps/demo-nextjs-app-router)
-   Check all the available [Model APIs](https://fal.ai/models)
-   Learn how to write your own model APIs on [Introduction to serverless functions](https://docs.fal.ai/private-serverless-apps)
-   Read more about function endpoints on [private serverless models](https://docs.fal.ai/private-serverless-apps)
-   Check the next page to learn how to [deploy your app to Vercel](https://docs.fal.ai/integrations/vercel)