Real-time models using WebSockets present challenges in ensuring the security of API secrets.

The WebSocket connection is established directly from the browser or native mobile application, making it unsafe to embed API keys and secrets directly into the client. To address this, we have developed additional tools to enable secure authentication with our servers without introducing unnecessary intermediaries between the client and our GPU servers. Instead of using traditional API keys, we recommend utilizing short-lived [JWT](https://jwt.io/) tokens for authentication.

Easiest way to communicate with fal using websockets is through our [javascript](https://github.com/fal-ai/fal-js) and [swift](https://github.com/fal-ai/fal-swift) clients and a [server proxy](https://docs.fal.ai/model-endpoints/server-side).

When `fal.realtime.connect` is invoked the fal client gets a short lived [JWT](https://jwt.io/) token through a server proxy to authenticate with fal services. This token is refreshed automatically by the client when it is needed.

-   [Javascript](https://docs.fal.ai/real-time/secrets#tab-panel-39)
-   [SWIFT](https://docs.fal.ai/real-time/secrets#tab-panel-40)

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>fal</span><span>.</span><span>config</span><span>({</span></p></div><div><p><span><span>  </span></span><span>proxyUrl: </span><span>"</span><span>/api/fal/proxy</span><span>"</span><span>,</span></p></div><div><p><span>});</span></p></div><div><p><span>const { </span><span>send</span><span> } = </span><span>fal</span><span>.</span><span>realtime</span><span>.</span><span>connect</span><span>(</span><span>"</span><span>fal-ai/fast-lcm-diffusion</span><span>"</span><span>, {</span></p></div><div><p><span><span>  </span></span><span>connectionKey: </span><span>"</span><span>realtime-demo</span><span>"</span><span>,</span></p></div><div><p><span><span>  </span></span><span>throttleInterval: </span><span>128</span><span>,</span></p></div><div><p><span>  </span><span>onResult</span><span>(</span><span>result</span><span>)</span><span> {</span></p></div><div><p><span>    </span><span>// display</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>}</span><span>);</span></p></div>
```

Checkout the [FalRealtimeSampleApp (swift)](https://github.com/fal-ai/fal-swift/tree/main/Sources/Samples/FalRealtimeSampleApp) and [realtime demo (js)](https://github.com/fal-ai/fal-js/blob/main/apps/demo-nextjs-app-router/app/realtime/page.tsx) for more details.