Workflows are a way to chain multiple models together to create a more complex pipeline. This allows you to create a single endpoint that can take an input and pass it through multiple models in sequence. This is useful for creating more complex models that require multiple steps, or for creating a single endpoint that can handle multiple tasks.

### Workflow as an API

Workflow APIs work the same way as other model endpoints, you can simply send a request and get a response back. However, it is common for workflows to contain multiple steps and produce intermediate results, as each step contains their own response that could be relevant in your use-case.

Therefore, workflows benefit from the **streaming** feature, which allows you to get partial results as they are being generated.

### Workflow events

The workflow API will trigger a few events during its execution, these events can be used to monitor the progress of the workflow and get intermediate results. Below are the events that you can expect from a workflow stream:

#### The `submit` event

This events is triggered every time a new step has been submitted to execution. It contains the `app_id`, `request_id` and the `node_id`.

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"type"</span><span>: </span><span>"</span><span>submit</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"node_id"</span><span>: </span><span>"</span><span>stable_diffusion_xl</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"app_id"</span><span>: </span><span>"</span><span>fal-ai/fast-sdxl</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"request_id"</span><span>: </span><span>"</span><span>d778bdf4-0275-47c2-9f23-16c27041cbeb</span><span>"</span></p></div><div><p><span>}</span></p></div>
```

#### The `completion` event

This event is triggered upon the completion of a specific step.

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"type"</span><span>: </span><span>"</span><span>completion</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"node_id"</span><span>: </span><span>"</span><span>stable_diffusion_xl</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"output"</span><span>: {</span></p></div><div><p><span>    </span><span>"images"</span><span>: [</span></p></div><div><p><span><span>      </span></span><span>{</span></p></div><div><p><span>        </span><span>"url"</span><span>: </span><span>"</span><span>https://fal.media/result.jpeg</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"width"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>        </span><span>"height"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>        </span><span>"content_type"</span><span>: </span><span>"</span><span>image/jpeg</span><span>"</span></p></div><div><p><span><span>      </span></span><span>}</span></p></div><div><p><span><span>    </span></span><span>],</span></p></div><div><p><span>    </span><span>"timings"</span><span>: { </span><span>"inference"</span><span>: </span><span>2.1733</span><span> },</span></p></div><div><p><span>    </span><span>"seed"</span><span>: </span><span>6252023</span><span>,</span></p></div><div><p><span>    </span><span>"has_nsfw_concepts"</span><span>: [</span><span>false</span><span>],</span></p></div><div><p><span>    </span><span>"prompt"</span><span>: </span><span>"</span><span>a cute puppy</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>}</span></p></div>
```

#### The `output` event

The `output` event means that the workflow has completed and the final result is ready.

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"type"</span><span>: </span><span>"</span><span>output</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"output"</span><span>: {</span></p></div><div><p><span>    </span><span>"images"</span><span>: [</span></p></div><div><p><span><span>      </span></span><span>{</span></p></div><div><p><span>        </span><span>"url"</span><span>: </span><span>"</span><span>https://fal.media/result.jpeg</span><span>"</span><span>,</span></p></div><div><p><span>        </span><span>"width"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>        </span><span>"height"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>        </span><span>"content_type"</span><span>: </span><span>"</span><span>image/jpeg</span><span>"</span></p></div><div><p><span><span>      </span></span><span>}</span></p></div><div><p><span><span>    </span></span><span>]</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>}</span></p></div>
```

#### The `error` event

The `error` event is triggered when an error occurs during the execution of a step. The `error` object contains the `error.status` with the HTTP status code, an error `message` as well as `error.body` with the underlying error serialized.

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"type"</span><span>: </span><span>"</span><span>error</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"node_id"</span><span>: </span><span>"</span><span>stable_diffusion_xl</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"message"</span><span>: </span><span>"</span><span>Error while fetching the result of the request d778bdf4-0275-47c2-9f23-16c27041cbeb</span><span>"</span><span>,</span></p></div><div><p><span>  </span><span>"error"</span><span>: {</span></p></div><div><p><span>    </span><span>"status"</span><span>: </span><span>422</span><span>,</span></p></div><div><p><span>    </span><span>"body"</span><span>: {</span></p></div><div><p><span>      </span><span>"detail"</span><span>: [</span></p></div><div><p><span><span>        </span></span><span>{</span></p></div><div><p><span>          </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>num_images</span><span>"</span><span>],</span></p></div><div><p><span>          </span><span>"msg"</span><span>: </span><span>"</span><span>ensure this value is less than or equal to 8</span><span>"</span><span>,</span></p></div><div><p><span>          </span><span>"type"</span><span>: </span><span>"</span><span>value_error.number.not_le</span><span>"</span><span>,</span></p></div><div><p><span>          </span><span>"ctx"</span><span>: { </span><span>"limit_value"</span><span>: </span><span>8</span><span> }</span></p></div><div><p><span><span>        </span></span><span>}</span></p></div><div><p><span><span>      </span></span><span>]</span></p></div><div><p><span><span>    </span></span><span>}</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>}</span></p></div>
```

### Example

A cool and simple example of the power of workflows is `workflows/fal-ai/sdxl-sticker`, which consists of three steps:

1.  Generates an image using `fal-ai/fast-sdxl`.
2.  Remove the background of the image using `fal-ai/imageutils/rembg`.
3.  Converts the image to a sticker using `fal-ai/face-to-sticker`.

What could be a tedious process of running and coordinating three different models is now a single endpoint that you can call with a single request.

-   [Javascript](https://docs.fal.ai/model-endpoints/workflows#tab-panel-29)
-   [python](https://docs.fal.ai/model-endpoints/workflows#tab-panel-30)
-   [python (async)](https://docs.fal.ai/model-endpoints/workflows#tab-panel-31)
-   [Swift](https://docs.fal.ai/model-endpoints/workflows#tab-panel-32)

```
<div><p><span>import</span><span> fal_client</span></p></div><div><p><span>stream </span><span>=</span><span> fal_client.</span><span>stream</span><span>(</span></p></div><div><p><span>    </span><span>"</span><span>workflows/fal-ai/sdxl-sticker</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>arguments</span><span>=</span><span>{</span></p></div><div><p><span>        </span><span>"</span><span>prompt</span><span>"</span><span>: </span><span>"</span><span>a face of a cute puppy, in the style of pixar animation</span><span>"</span><span>,</span></p></div><div><p><span><span>    </span></span><span>}</span><span>,</span></p></div><div><p><span>)</span></p></div><div><p><span>for</span><span> event </span><span>in</span><span> stream:</span></p></div><div><p><span>    </span><span>print</span><span>(</span><span>event</span><span>)</span></p></div>
```

### Type definitions

Below are the type definition in TypeScript of events that you can expect from a workflow stream:

```
<div><p><span>type</span><span> WorkflowBaseEvent </span><span>=</span><span> {</span></p></div><div><p><span><span>  </span></span><span>type</span><span>:</span><span> </span><span>"</span><span>submit</span><span>"</span><span> </span><span>|</span><span> </span><span>"</span><span>completion</span><span>"</span><span> </span><span>|</span><span> </span><span>"</span><span>error</span><span>"</span><span> </span><span>|</span><span> </span><span>"</span><span>output</span><span>"</span><span>;</span></p></div><div><p><span><span>  </span></span><span>node_id</span><span>:</span><span> </span><span>string</span><span>;</span></p></div><div><p><span>};</span></p></div><div><p><span>export</span><span> </span><span>type</span><span> WorkflowSubmitEvent </span><span>=</span><span> </span><span>WorkflowBaseEvent</span><span> </span><span>&amp;</span><span> {</span></p></div><div><p><span><span>  </span></span><span>type</span><span>:</span><span> </span><span>"</span><span>submit</span><span>"</span><span>;</span></p></div><div><p><span><span>  </span></span><span>app_id</span><span>:</span><span> </span><span>string</span><span>;</span></p></div><div><p><span><span>  </span></span><span>request_id</span><span>:</span><span> </span><span>string</span><span>;</span></p></div><div><p><span>};</span></p></div><div><p><span>export</span><span> </span><span>type</span><span> WorkflowCompletionEvent&lt;</span><span>Output</span><span> </span><span>=</span><span> </span><span>any</span><span>&gt; </span><span>=</span><span> </span><span>WorkflowBaseEvent</span><span> </span><span>&amp;</span><span> {</span></p></div><div><p><span><span>  </span></span><span>type</span><span>:</span><span> </span><span>"</span><span>completion</span><span>"</span><span>;</span></p></div><div><p><span><span>  </span></span><span>app_id</span><span>:</span><span> </span><span>string</span><span>;</span></p></div><div><p><span><span>  </span></span><span>output</span><span>:</span><span> </span><span>Output</span><span>;</span></p></div><div><p><span>};</span></p></div><div><p><span>export</span><span> </span><span>type</span><span> WorkflowDoneEvent&lt;</span><span>Output</span><span> </span><span>=</span><span> </span><span>any</span><span>&gt; </span><span>=</span><span> </span><span>WorkflowBaseEvent</span><span> </span><span>&amp;</span><span> {</span></p></div><div><p><span><span>  </span></span><span>type</span><span>:</span><span> </span><span>"</span><span>output</span><span>"</span><span>;</span></p></div><div><p><span><span>  </span></span><span>output</span><span>:</span><span> </span><span>Output</span><span>;</span></p></div><div><p><span>};</span></p></div><div><p><span>export</span><span> </span><span>type</span><span> WorkflowErrorEvent </span><span>=</span><span> </span><span>WorkflowBaseEvent</span><span> </span><span>&amp;</span><span> {</span></p></div><div><p><span><span>  </span></span><span>type</span><span>:</span><span> </span><span>"</span><span>error</span><span>"</span><span>;</span></p></div><div><p><span><span>  </span></span><span>message</span><span>:</span><span> </span><span>string</span><span>;</span></p></div><div><p><span><span>  </span></span><span>error</span><span>:</span><span> </span><span>any</span><span>;</span></p></div><div><p><span>};</span></p></div>
```