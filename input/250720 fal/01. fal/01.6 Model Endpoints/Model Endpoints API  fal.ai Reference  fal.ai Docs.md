Model endpoints are the entry point to interact with the fal API. They are exposed through simple HTTP APIs that can be called from any programming language.

In the next sections you will learn how to call these endpoints in 3 ways:

-   `https://queue.fal.run` exposes our [Queue](https://docs.fal.ai/model-endpoints/queue), the recommended way to interact with the fal API
-   `https://fal.run` allows [synchronous execution](https://docs.fal.ai/model-endpoints/synchronous-requests) of models
-   `wss://ws.fal.run` allows submitting requests via a [WebSocket connection](https://docs.fal.ai/model-endpoints/websockets)

We also offer [clients](https://docs.fal.ai/clients) for some of the popular programming languages used by our community.