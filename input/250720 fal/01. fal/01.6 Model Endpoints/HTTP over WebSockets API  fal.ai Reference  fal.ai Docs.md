For applications that require real-time interaction or handle streaming, fal offers a WebSocket-based integration. This allows you to establish a persistent connection and stream data back and forth between your client and the fal API using the same format as the HTTP endpoints.

### WebSocket Endpoint

To utilize the WebSocket functionality, use the `wss` protocol with the the `ws.fal.run` domain:

```
<div><p><span>wss://ws.fal.run/{model_id}</span></p></div>
```

### Communication Protocol

Once connected, the communication follows a specific protocol with JSON messages for control flow and raw data for the actual response stream:

1.  **Payload Message:** Send a JSON message containing the payload for your application. This is equivalent to the request body you would send to the HTTP endpoint.
    
2.  **Start Metadata:** Receive a JSON message containing the HTTP response headers from your application. This allows you to understand the type and structure of the incoming response stream.
    
3.  **Response Stream:** Receive the actual response data as a sequence of messages. These can be binary chunks for media content or a JSON object for structured data, depending on the `Content-Type` header.
    
4.  **End Metadata:** Receive a final JSON message indicating the end of the response stream. This signals that the request has been fully processed and the next payload will be processed.
    

### Example Interaction

Here’s an example of a typical interaction with the WebSocket API:

**Client Sends (Payload Message):**

```
<div><p><span>{</span><span>"prompt"</span><span>: </span><span>"</span><span>generate a 10-second audio clip of a cat purring</span><span>"</span><span>}</span></p></div>
```

**Server Responds (Start Metadata):**

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"type"</span><span>: </span><span>"</span><span>start</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"request_id"</span><span>: </span><span>"</span><span>5d76da89-5d75-4887-a715-4302bf435614</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"status"</span><span>: </span><span>200</span><span>,</span></p></div><div><p><span>  </span><span>"headers"</span><span>: {</span></p></div><div><p><span>    </span><span>"Content-Type"</span><span>: </span><span>"</span><span>text/event-stream; charset=utf-8</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"Transfer-Encoding"</span><span>: </span><span>"</span><span>chunked</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>// ...</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>}</span></p></div>
```

**Server Sends (Response Stream):**

```
<div><p><span>&lt;binary audio data chunk 1&gt;</span></p></div><div><p><span>&lt;binary audio data chunk 2&gt;</span></p></div><div><p><span>...</span></p></div><div><p><span>&lt;binary audio data chunk N&gt;</span></p></div>
```

**Server Sends (Completion Message):**

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"type"</span><span>: </span><span>"</span><span>end</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"request_id"</span><span>: </span><span>"</span><span>5d76da89-5d75-4887-a715-4302bf435614</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"status"</span><span>: </span><span>200</span><span>,</span></p></div><div><p><span>  </span><span>"time_to_first_byte_seconds"</span><span>: </span><span>0.577083</span></p></div><div><p><span>}</span></p></div>
```

This WebSocket integration provides a powerful mechanism for building dynamic and responsive AI applications on the fal platform. By leveraging the streaming capabilities, you can unlock new possibilities for creative and interactive user experiences.

### Example Program

For instance, should you want to make fast prompts to any LLM, you can use `fal-ai/any-llm`.

```
<div><p><span>import</span><span> fal.apps</span></p></div><div><p><span>with</span><span> fal.apps.</span><span>ws</span><span>(</span><span>"</span><span>fal-ai/any-llm</span><span>"</span><span>) </span><span>as</span><span> connection:</span></p></div><div><p><span>    </span><span>for</span><span> i </span><span>in</span><span> </span><span>range</span><span>(</span><span>3</span><span>):</span></p></div><div><p><span><span>        </span></span><span>connection.</span><span>send</span><span>(</span></p></div><div><p><span><span>            </span></span><span>{</span></p></div><div><p><span>                </span><span>"</span><span>model</span><span>"</span><span>: </span><span>"</span><span>google/gemini-flash-1.5</span><span>"</span><span>,</span></p></div><div><p><span>                </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>f</span><span>"What is the meaning of life? Respond in </span><span>{i}</span><span> words."</span><span>,</span></p></div><div><p><span><span>            </span></span><span>}</span></p></div><div><p><span>        </span><span>)</span></p></div><div><p><span>    </span><span># they should be in order</span></p></div><div><p><span>    </span><span>for</span><span> i </span><span>in</span><span> </span><span>range</span><span>(</span><span>3</span><span>):</span></p></div><div><p><span>        </span><span>import</span><span> json</span></p></div><div><p><span><span>        </span></span><span>response </span><span>=</span><span> json.</span><span>loads</span><span>(</span><span>connection.</span><span>recv</span><span>())</span></p></div><div><p><span>        </span><span>print</span><span>(</span><span>response</span><span>)</span></p></div>
```

And running this program would output:

```
<div><p><span>{</span><span>'output'</span><span>:</span><span> </span><span>'</span><span>(Silence)\n</span><span>'</span><span>,</span><span> </span><span>'</span><span>partial</span><span>'</span><span>:</span><span> </span><span>False,</span><span> </span><span>'</span><span>error</span><span>'</span><span>:</span><span> </span><span>None}</span></p></div><div><p><span>{</span><span>'output'</span><span>:</span><span> </span><span>'</span><span>Growth\n</span><span>'</span><span>,</span><span> </span><span>'</span><span>partial</span><span>'</span><span>:</span><span> </span><span>False,</span><span> </span><span>'</span><span>error</span><span>'</span><span>:</span><span> </span><span>None}</span></p></div><div><p><span>{</span><span>'output'</span><span>:</span><span> </span><span>'</span><span>Personal fulfillment.\n</span><span>'</span><span>,</span><span> </span><span>'</span><span>partial</span><span>'</span><span>:</span><span> </span><span>False,</span><span> </span><span>'</span><span>error</span><span>'</span><span>:</span><span> </span><span>None}</span></p></div>
```

### Example Program with Stream

The `fal-ai/any-llm/stream` model is a streaming model that can generate text in real-time. Here’s an example of how you can use it:

```
<div><p><span>with</span><span> fal.apps.</span><span>ws</span><span>(</span><span>"</span><span>fal-ai/any-llm/stream</span><span>"</span><span>) </span><span>as</span><span> connection:</span></p></div><div><p><span>    </span><span># </span><span>NOTE</span><span>: this app responds in 'text/event-stream' format</span></p></div><div><p><span>    </span><span># For example:</span></p></div><div><p><span>    </span><span>#</span></p></div><div><p><span>    </span><span>#    event: event</span></p></div><div><p><span>    </span><span>#    data: {"output": "Growth", "partial": true, "error": null}</span></p></div><div><p><span>    </span><span>for</span><span> i </span><span>in</span><span> </span><span>range</span><span>(</span><span>3</span><span>):</span></p></div><div><p><span><span>        </span></span><span>connection.</span><span>send</span><span>(</span></p></div><div><p><span><span>            </span></span><span>{</span></p></div><div><p><span>                </span><span>"</span><span>model</span><span>"</span><span>: </span><span>"</span><span>google/gemini-flash-1.5</span><span>"</span><span>,</span></p></div><div><p><span>                </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>f</span><span>"What is the meaning of life? Respond in </span><span>{i</span><span>+</span><span>1</span><span>}</span><span> words."</span><span>,</span></p></div><div><p><span><span>            </span></span><span>}</span></p></div><div><p><span>        </span><span>)</span></p></div><div><p><span>    </span><span>for</span><span> i </span><span>in</span><span> </span><span>range</span><span>(</span><span>3</span><span>):</span></p></div><div><p><span>        </span><span>for</span><span> bs </span><span>in</span><span> connection.</span><span>stream</span><span>():</span></p></div><div><p><span><span>            </span></span><span>lines </span><span>=</span><span> bs.</span><span>decode</span><span>().</span><span>replace</span><span>(</span><span>"</span><span>\r\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>\n</span><span>"</span><span>).</span><span>split</span><span>(</span><span>"</span><span>\n</span><span>"</span><span>)</span></p></div><div><p><span><span>            </span></span><span>event </span><span>=</span><span> {}</span></p></div><div><p><span>            </span><span>for</span><span> line </span><span>in</span><span> lines:</span></p></div><div><p><span>                </span><span>if</span><span> </span><span>not</span><span> line:</span></p></div><div><p><span>                    </span><span>continue</span></p></div><div><p><span><span>                </span></span><span>key, value </span><span>=</span><span> line.</span><span>split</span><span>(</span><span>"</span><span>:</span><span>"</span><span>,</span><span> </span><span>1</span><span>)</span></p></div><div><p><span><span>                </span></span><span>event[key] </span><span>=</span><span> value.</span><span>strip</span><span>()</span></p></div><div><p><span>            </span><span>print</span><span>(</span><span>event</span><span>[</span><span>"</span><span>data</span><span>"</span><span>])</span></p></div><div><p><span>        </span><span>print</span><span>(</span><span>"</span><span>----</span><span>"</span><span>)</span></p></div>
```

And running this program would output:

```
<div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Perspective</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Perspective.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Perspective.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Perspective.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>false</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>----</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Find</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Find meaning.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Find meaning.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Find meaning.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>false</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>----</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Be</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Be, love, grow.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Be, love, grow.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>true</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>{</span><span>"output"</span><span>:</span><span> </span><span>"</span><span>Be, love, grow.\n</span><span>"</span><span>,</span><span> </span><span>"</span><span>partial</span><span>"</span><span>:</span><span> </span><span><span>false</span><span>,</span></span><span> </span><span>"</span><span>error</span><span>"</span><span>:</span><span> </span><span>null}</span></p></div><div><p><span>----</span></p></div>
```