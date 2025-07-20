While our [Queue system](https://docs.fal.ai/model-endpoints/queue) is the more reliable and recommended way to submit requests, we also support synchronous requests via `https://fal.run`.

Synchronous endpoints are beneficial if when you know the request is quick and you are looking for minimal latency. The drawbacks are:

-   You need to keep the connection open until receiving the result
-   The request cannot be interrupted
-   If the connection is interrupted there is not way to obtain the result
-   You will be charged for the full request whether or not you were able to receive the result

The endpoint format and parameters are similar to the Queue ones:

| Endpoint | Method | Description |
| --- | --- | --- |
| **`https://fal.run/{model_id}`** | POST | Adds a request to the queue for a top-level path |
| **`https://fal.run/{model_id}/{subpath}`** | POST | Adds a request to the queue for an optional subpath |

Parameters:

-   `model_id`: the model ID consists of a namespace and model name separated by a slash, e.g. `fal-ai/fast-sdxl`. Many models expose only a single top-level endpoint, so you can directly call them by `model_id`.
-   `subpath`: some models expose different capabilities at different sub-paths, e.g. `fal-ai/flux/dev`. The subpath (`/dev` in this case) should be used

### Submit a request

Here is an example of using the curl command to submit a synchronous request:

```
<div><p><span>curl</span><span> </span><span>-X</span><span> </span><span>POST</span><span> </span><span>https://fal.run/fal-ai/fast-sdxl</span><span> </span><span>\</span></p></div><div><p><span>  </span><span>-H</span><span> </span><span>"</span><span>Authorization: Key </span><span>$FAL_KEY</span><span>"</span><span> </span><span>\</span></p></div><div><p><span>  </span><span>-d</span><span> </span><span>'</span><span>{"prompt": "a cat"}</span><span>'</span></p></div>
```

The response will come directly from the model:

```
<div><p><span>{</span></p></div><div><p><span>  </span><span>"images"</span><span>: [</span></p></div><div><p><span><span>    </span></span><span>{</span></p></div><div><p><span>      </span><span>"url"</span><span>: </span><span>"</span><span>https://v3.fal.media/files/rabbit/YYbm6L3DaXYHDL1_A4OaL.jpeg</span><span>"</span><span>,</span></p></div><div><p><span>      </span><span>"width"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>      </span><span>"height"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>      </span><span>"content_type"</span><span>: </span><span>"</span><span>image/jpeg</span><span>"</span></p></div><div><p><span><span>    </span></span><span>}</span></p></div><div><p><span><span>  </span></span><span>],</span></p></div><div><p><span>  </span><span>"timings"</span><span>: {</span></p></div><div><p><span>    </span><span>"inference"</span><span>: </span><span>2.507048434985336</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>  </span><span>"seed"</span><span>: </span><span>15860307465884635512</span><span>,</span></p></div><div><p><span>  </span><span>"has_nsfw_concepts"</span><span>: [</span></p></div><div><p><span>    </span><span>false</span></p></div><div><p><span><span>  </span></span><span>],</span></p></div><div><p><span>  </span><span>"prompt"</span><span>: </span><span>"</span><span>a cat</span><span>"</span></p></div><div><p><span>}</span></p></div>
```