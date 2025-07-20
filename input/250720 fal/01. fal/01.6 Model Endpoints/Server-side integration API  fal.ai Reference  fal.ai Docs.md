Although the endpoints are designed to be called directly from the client, it is not safe to keep API Keys in client side code. Most use cases require developers to create their own server-side APIs, that call a 3rd party service, fal, and then return the result to the client. It is a straightforward process, but always get in the way of developers and teams trying to focus on their own business, their own idea.

Therefore, we implemented the client libraries to support a proxy mode, which allows you to use the client libraries in the client, while keeping the API Keys in your own server-side code.

### Ready-to-use proxy implementations

We provide ready-to-use proxy implementations for the following languages/frameworks:

-   [Node.js with Next.js](https://docs.fal.ai/integrations/nextjs): a Next.js API route handler that can be used in any Next.js app. It supports both Page and App routers. We use it ourselves in all of our apps in production.
-   [Node.js with Express](https://github.com/fal-ai/serverless-js/tree/main/apps/demo-express-app): an Express route handler that can be used in any Express app. You can also implement custom logic and compose together with your own handlers.

That’s it for now, but we are looking out for our community needs and will add more implementations in the future. If you have any requests, join our community in our [Discord server](https://discord.gg/fal-ai).

### The proxy formula

In case fal doesn’t provide a plug-and-play proxy implementation for your language/framework, you can use the following formula to implement your own proxy:

1.  Provide a single endpoint that will ingest all requests from the client (e.g. `/api/fal/proxy` is commonly used as the default route path).
2.  The endpoint must support both `GET` and `POST` requests. When an unsupported HTTP method is used, the proxy must return status code `405`, Method Not Allowed.
3.  The URL the proxy needs to call is provided by the `x-fal-target-url` header. If the header is missing, the proxy must return status code `400`, Bad Request. In case it doesn’t point to a valid URL, or the URL’s domain is not `*.fal.ai` or `*.fal.run`, the proxy must return status code `412`, Precondition Failed.
4.  The request body, when present, is always in the JSON format - i.e. `content-type` header is `application/json`. Any other type of content must be rejected with status code `415`, Unsupported Media Type.
5.  The proxy must add the `authorization` header in the format of `Key <your-api-key>` to the request it sends to the target URL. Your API key should be resolved from the environment variable `FAL_KEY`.
6.  The response from the target URL will always be in the JSON format, the proxy must return the same response to the client.
7.  The proxy must return the same HTTP status code as the target URL.
8.  The proxy must return the same headers as the target URL, except for the `content-length` and `content-encoding` headers, which should be set by the your own server/framework automatically.

### Configure the client

To use the proxy, you need to configure the client to use the proxy endpoint. You can do that by setting the `proxyUrl` option in the client configuration:

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>fal</span><span>.</span><span>config</span><span>({</span></p></div><div><p><span><span>  </span></span><span>proxyUrl: </span><span>"</span><span>/api/fal/proxy</span><span>"</span><span>,</span></p></div><div><p><span>});</span></p></div>
```

### Example implementation

You can find a reference implementation of the proxy formula using TypeScript, which supports both Express and Next.js, in [serverless-js/libs/proxy/src/index.ts](https://github.com/fal-ai/serverless-js/blob/main/libs/proxy/src/index.ts).