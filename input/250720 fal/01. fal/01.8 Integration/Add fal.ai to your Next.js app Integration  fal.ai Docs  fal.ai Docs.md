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
npm install @fal-ai/client @fal-ai/server-proxy
```

### 2\. Setup the proxy

The proxy will protect your API Key and prevent it from being exposed to the client. Usually app implementation have to handle that integration themselves, but in order to make the integration as smooth as possible, we provide a drop-in proxy implementation that can be integrated with either the **Page Router** or the **App Router**.

#### 2.1. Page Router

If you are using the **Page Router** (i.e. `src/pages/_app.js`), create an API handler in `src/pages/api/fal/proxy.js` (or `.ts` in case of TypeScript), and re-export the built-in proxy handler:

```
export { handler as default } from "@fal-ai/server-proxy/nextjs";
```

#### 2.2. App Router

If you are using the **App Router** (i.e. `src/app/page.jsx`) create a route handler in `src/app/api/fal/proxy/route.js` (or `.ts` in case of TypeScript), and re-export the route handler:

```
import { route } from "@fal-ai/server-proxy/nextjs";export const { GET,
POST } = route;
```

#### 2.3. Setup the API Key

Make sure you have your API Key available as an environment variable. You can setup in your `.env.local` file for development and also in your hosting provider for production, such as [Vercel](https://vercel.com/docs/projects/environment-variables).

```
FAL_KEY="key_id:key_secret"
```

#### 2.4. Custom proxy logic

It’s common for applications to execute custom logic before or after the proxy handler. For example, you may want to add a custom header to the request, or log the request and response, or apply some rate limit. The good news is that the proxy implementation is simply a standard Next.js API/route handler function, which means you can compose it with other handlers.

For example, let’s assume you want to add some analytics and apply some rate limit to the proxy handler:

```
import { route } from "@fal-ai/server-proxy/nextjs";// Let's add some custom logic to POST requests - i.e. when the request is// submitted for processingexport const POST = (req) 
=&gt; { // Add some analytics analytics.track("fal.ai request", { targetUrl: req.headers["x-fal-target-url"], userId: req.user.id, })
; // Apply some rate limit if (rateLimiter.shouldLimit(req)
) 
{ res.status(429)
.json({ error: "Too many requests" })
; } // If everything passed your custom logic,
now execute the proxy handler return route.POST(req)
;};// For GET requests we will just use the built-in proxy handler// But you could also add some custom logic here if you needexport const GET = route.GET;
```

Note that the URL that will be forwarded to server is available as a header named `x-fal-target-url`. Also, keep in mind the example above is just an example, `rateLimiter` and `analytics` are just placeholders.

The example above used the app router, but the same logic can be applied to the page router and its `handler` function.

### 3\. Configure the client

On your main file (i.e. `src/pages/_app.jsx` or `src/app/page.jsx`), configure the client to use the proxy:

```
import { fal } from "@fal-ai/client";fal.config({ proxyUrl: "/api/fal/proxy",});
```

### 4\. Generate an image

Now that the client is configured, you can generate an image using `fal.subscribe` and pass the model id and the input parameters:

```
const result = await fal.subscribe("fal-ai/flux/dev", { input: { prompt, image_size: "square_hd", }, pollInterval: 5000, logs: true, onQueueUpdate(update) 
{ console.log("queue update", update)
; },
})
;const imageUrl = result.images[0].url;
```

See more about Flux Dev used in this example on [fal.ai/models/fal-ai/flux/dev](https://fal.ai/models/fal-ai/flux/dev).

### What’s next?

Image generation is just one of the many cool things you can do with fal. Make sure you:

-   Check our demo application at [github.com/fal-ai/serverless-js/apps/demo-nextjs-app-router](https://github.com/fal-ai/fal-js/tree/main/apps/demo-nextjs-app-router)
-   Check all the available [Model APIs](https://fal.ai/models)
-   Learn how to write your own model APIs on [Introduction to serverless functions](https://docs.fal.ai/private-serverless-apps)
-   Read more about function endpoints on [private serverless models](https://docs.fal.ai/private-serverless-apps)
-   Check the next page to learn how to [deploy your app to Vercel](https://docs.fal.ai/integrations/vercel)