Real-time models using WebSockets present challenges in ensuring the security of API secrets.

The WebSocket connection is established directly from the browser or native mobile application, making it unsafe to embed API keys and secrets directly into the client. To address this, we have developed additional tools to enable secure authentication with our servers without introducing unnecessary intermediaries between the client and our GPU servers. Instead of using traditional API keys, we recommend utilizing short-lived [JWT](https://jwt.io/) tokens for authentication.

Easiest way to communicate with fal using websockets is through our [javascript](https://github.com/fal-ai/fal-js) and [swift](https://github.com/fal-ai/fal-swift) clients and a [server proxy](https://docs.fal.ai/model-endpoints/server-side).

When `fal.realtime.connect` is invoked the fal client gets a short lived [JWT](https://jwt.io/) token through a server proxy to authenticate with fal services. This token is refreshed automatically by the client when it is needed.

-   [Javascript](https://docs.fal.ai/real-time/secrets#tab-panel-39)
-   [SWIFT](https://docs.fal.ai/real-time/secrets#tab-panel-40)

```
import { fal } from "@fal-ai/client";fal.config({ proxyUrl: "/api/fal/proxy",})
;const { send } = fal.realtime.connect("fal-ai/fast-lcm-diffusion", { connectionKey: "realtime-demo", throttleInterval: 128, onResult(result) 
{ // display },
})
;
```

Checkout the [FalRealtimeSampleApp (swift)](https://github.com/fal-ai/fal-swift/tree/main/Sources/Samples/FalRealtimeSampleApp) and [realtime demo (js)](https://github.com/fal-ai/fal-js/blob/main/apps/demo-nextjs-app-router/app/realtime/page.tsx) for more details.