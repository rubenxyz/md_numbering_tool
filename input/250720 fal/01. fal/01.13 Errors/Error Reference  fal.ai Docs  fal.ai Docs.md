> **Warning:** We are currently in a migration process and some APIs might not strictly follow the error structure documented below. We’re working to ensure all errors conform to this specification as soon as possible.

## Error Response

When an API request fails due to client-side input issues (like validation errors) or server-side problems, the API returns a structured error response. This response includes a standard HTTP status code, specific headers, and a JSON body detailing the errors.

### Error Response Structure

The error response consists of:

1.  **HTTP Status Code:** Indicates the general category of the error (e.g., `500` for internal errors, `504` for timeouts).
2.  **Headers:** Includes required headers like `X-Fal-Retryable`.
3.  **JSON Body:** Contains a `detail` field which is an array of `Error` objects.

| Header | Description |
| --- | --- |
| `X-Fal-Retryable` | **\[OPTIONAL\]** A boolean (`"true"` or `"false"`) indicating if retrying the _exact same_ request might succeed (e.g., transient issues). |

### Error Object Structure

The `detail` field is an array where each object represents a specific error.

| Property | Description |
| --- | --- |
| `loc` | **\[REQUIRED\]** An array indicating the location of the error (e.g., `["body", "field_name"]` for input validation, `["body"]` for general errors). The first item in the loc list will be the field where the error occurred, and if the field is a sub-model, subsequent items will be present to indicate the nested location of the error. |
| `msg` | **\[REQUIRED\]** A human-readable description of the error. **Client code should not parse and rely on the msg field.** |
| `type` | **\[REQUIRED\]** A unique, **machine-readable** string identifying the error category (e.g., `image_too_large`). Use this for conditional logic. |
| `url` | **\[REQUIRED\]** A link to documentation about this specific error `type` (e.g., [https://docs.fal.ai/errors/#image\_too\_large\`](https://docs.fal.ai/errors/#image_too_large%60)). Primarily for developers. |
| `ctx` | **\[OPTIONAL\]** An object with additional structured, **machine-readable** context for the error `type` (e.g., `{"max_height": 1024, "max_width": 1024}` for `image_too_large`). |
| `input` | **\[OPTIONAL\]** The input that caused the error. |

### Guidance

-   **For Machine Processing:** Rely on the `type` field for conditional logic. Use `ctx` for specific error details if available. Check the `X-Fal-Retryable` header for retry decisions.
-   **For Human Display:** Use the `msg` field to show error messages to end-users. **Client code should not parse and rely on the msg field.**
-   **For Documentation:** Use the `url` field to link to further documentation about the specific error. This is primarily intended for developers to get more detailed information about error handling and resolution.

___

## Error Types

This document details the specific error types returned by the API, following the structure defined in the error specification. Each error type has a unique `type` string, a human-readable `msg`, and potentially a `ctx` object with more context.

##### `internal_server_error`

This error indicates an unexpected issue occurred on the server that prevented the request from being fulfilled.

-   **Status Code:** 500
-   **Retryable:** Can be `true` or `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Internal server error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>internal_server_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#internal_server_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: { </span><span>"prompt"</span><span>: </span><span>"</span><span>a cat</span><span>"</span><span> }</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `generation_timeout`

This error occurs when the requested operation took longer than the allowed time limit to complete.

-   **Status Code:** 504
-   **Retryable:** Can be `true` or `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Generation timeout</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>generation_timeout</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#generation_timeout</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: { </span><span>"prompt"</span><span>: </span><span>"</span><span>a very complex scene taking too long</span><span>"</span><span> }</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `downstream_service_error`

This error signifies a problem when communicating with an external service required to fulfill the request.

-   **Status Code:** 400
-   **Retryable:** Can be `true` or `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Downstream service error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>downstream_service_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#downstream_service_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: { </span><span>"some_input"</span><span>: </span><span>"</span><span>value</span><span>"</span><span> }</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `downstream_service_unavailable`

This error indicates that a required third-party service (**including partner APIs**) is currently unavailable, preventing the request from being fulfilled.

-   **Status Code:** 500
-   **Retryable:** Can be `true` or `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Downstream service unavailable</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>downstream_service_unavailable</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#downstream_service_unavailable</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: { </span><span>"prompt"</span><span>: </span><span>"</span><span>a cat</span><span>"</span><span> }</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `content_policy_violation`

This error indicates that the provided input content (e.g., text prompt, uploaded image) could not be processed because it was flagged by automated safety systems as potentially violating usage policies or responsible AI guidelines.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):** None

These filters are in place to ensure safe, ethical, and legal use of the platform. **The content may have been flagged by either fal’s filter or one of our partners’. Sensitivity levels can vary between partner APIs.**

Violations may include, but are not limited to:

-   Content depicting NSFW content, promoting illegal acts or hate speech.
-   Severely harmful content, such as depictions of extreme violence, gore, or content promoting self-harm.
-   Content intended to promote misinformation, deception, harassment, or discrimination.
-   Generation of content that infringes on third-party intellectual property rights.
-   Content that perpetuates harmful stereotypes.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>prompt</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>The content could not be processed because it contained material flagged by a content checker.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>content_policy_violation</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#content_policy_violation</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>a prompt containing forbidden content</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `image_too_small`

This error indicates that the provided image dimensions are smaller than the required minimum.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `min_height`: The minimum required height in pixels.
    -   `min_width`: The minimum required width in pixels.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>image_url</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Image too small</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>image_too_small</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#image_too_small</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"min_height"</span><span>: </span><span>512</span><span>,</span></p></div><div><p><span>      </span><span>"min_width"</span><span>: </span><span>512</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/image_100x100.jpg</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `image_too_large`

This error indicates that the provided image dimensions exceed the maximum allowed limits.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `max_height`: The maximum allowed height in pixels.
    -   `max_width`: The maximum allowed width in pixels.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>input_image</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Image too large</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>image_too_large</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#image_too_large</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"max_height"</span><span>: </span><span>1024</span><span>,</span></p></div><div><p><span>      </span><span>"max_width"</span><span>: </span><span>1024</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/image_2000x2000.jpg</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `image_load_error`

This error occurs when the server failed to load or process the provided image, possibly due to corruption or an unsupported format.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>control_image</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Image load error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>image_load_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#image_load_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/corrupted_image.webp</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `file_download_error`

This error indicates that the server failed to download a file specified by a URL in the input. Make sure the URL is publicly accessible and that the file is not behind a login or authentication wall.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>video_url</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>File download error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>file_download_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#file_download_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://private-server.com/file.mp4</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `face_detection_error`

This error is raised when the system could not detect a face in the provided image, and face detection was required for the operation.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>face_image</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Could not detect face in the image</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>face_detection_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#face_detection_error</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/landscape_no_face.jpg</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `file_too_large`

This error indicates that the provided file exceeds the maximum allowed size.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `max_size`: The maximum allowed file size in bytes.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>upload_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>File too large</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>file_too_large</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#file_too_large</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"max_size"</span><span>: </span><span>10485760</span><span> </span><span>// 10MB</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/large_video.mp4</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `greater_than`

This error occurs when a numeric input value is not strictly greater than the specified threshold.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `gt`: The value the input must be greater than.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>num_inference_steps</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Input should be greater than 0</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>greater_than</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#greater_than</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"gt"</span><span>: </span><span>0</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>0</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `greater_than_equal`

This error occurs when a numeric input value is less than the specified threshold.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `ge`: The value the input must be greater than or equal to.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>strength</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Input should be greater than or equal to 0</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>greater_than_equal</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#greater_than_equal</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"ge"</span><span>: </span><span>0</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>-0.5</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `less_than`

This error occurs when a numeric input value is not strictly less than the specified threshold.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `lt`: The value the input must be less than.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>negative_prompt_weight</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Input should be less than 1</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>less_than</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#less_than</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"lt"</span><span>: </span><span>1.0</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>1.0</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `less_than_equal`

This error occurs when a numeric input value is greater than the specified threshold.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `le`: The value the input must be less than or equal to.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>guidance_scale</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Input should be less than or equal to 20</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>less_than_equal</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#less_than_equal</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"le"</span><span>: </span><span>20</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>21</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `multiple_of`

This error indicates that a numeric input value is not a multiple of the required factor.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `multiple_of`: The factor the input must be a multiple of.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>width</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Input should be a multiple of 8</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>multiple_of</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#multiple_of</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"multiple_of"</span><span>: </span><span>8</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>513</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `sequence_too_short`

This error occurs when a sequence (like a list or string) has fewer items/characters than the required minimum length.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `min_length`: The minimum required length of the sequence.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>prompts</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Sequence should have at least 1 items</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>sequence_too_short</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#sequence_too_short</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"min_length"</span><span>: </span><span>1</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: []</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `sequence_too_long`

This error occurs when a sequence (like a list or string) has more items/characters than the allowed maximum length.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `max_length`: The maximum allowed length of the sequence.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>controlnet_images</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Sequence should have at most 4 items</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>sequence_too_long</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#sequence_too_long</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"max_length"</span><span>: </span><span>4</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: [</span><span>"</span><span>img1.jpg</span><span>"</span><span>, </span><span>"</span><span>img2.jpg</span><span>"</span><span>, </span><span>"</span><span>img3.jpg</span><span>"</span><span>, </span><span>"</span><span>img4.jpg</span><span>"</span><span>, </span><span>"</span><span>img5.jpg</span><span>"</span><span>]</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `one_of`

This error indicates that the input value provided for a field is not among the set of allowed values.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `expected`: A list containing the allowed values.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>scheduler</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Input should be 'EulerA' or 'DPM++'</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>one_of</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#one_of</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"expected"</span><span>: [</span><span>"</span><span>EulerA</span><span>"</span><span>, </span><span>"</span><span>DPM++</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>InvalidScheduler</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `feature_not_supported`

This error is raised when the combination of input parameters requests a feature or mode that is not supported by the endpoint.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):** None

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>advanced_feature</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Feature not supported</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>feature_not_supported</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#feature_not_supported</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>true</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `invalid_archive`

This error occurs when the provided archive file (e.g., .zip, .tar) cannot be read or processed, likely due to corruption or an unsupported format.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `supported_extensions`: A list of supported archive file extensions.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>training_data</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Could not read or process the provided archive. Ensure it's a valid, non-corrupted archive.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>invalid_archive</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#invalid_archive</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"supported_extensions"</span><span>: [</span><span>"</span><span>.zip</span><span>"</span><span>, </span><span>"</span><span>.tar.gz</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/corrupted_archive.rar</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `archive_file_count_below_minimum`

This error indicates that the provided archive contains fewer files matching the required criteria (e.g., specific extensions) than the minimum required count.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `min_count`: The minimum number of required files.
    -   `provided_count`: The number of matching files found in the archive.
    -   `supported_extensions`: The file extensions that were counted. (e.g., extensions like `.jpg`, `.png` when used for image archives or `.mp4` when used for video archives).

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>image_archive</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Too few files in the archive. Expected at least 10 files with extensions .jpg, .png, found 8. Add more matching files to the archive.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>archive_file_count_below_minimum</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#archive_file_count_below_minimum</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"min_count"</span><span>: </span><span>10</span><span>,</span></p></div><div><p><span>      </span><span>"provided_count"</span><span>: </span><span>8</span><span>,</span></p></div><div><p><span>      </span><span>"supported_extensions"</span><span>: [</span><span>"</span><span>.jpg</span><span>"</span><span>, </span><span>"</span><span>.png</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/images_few.zip</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `archive_file_count_exceeds_maximum`

This error indicates that the provided archive contains more files matching the required criteria (e.g., specific extensions) than the maximum allowed count.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `max_count`: The maximum number of allowed files.
    -   `provided_count`: The number of matching files found in the archive.
    -   `supported_extensions`: The file extensions that were counted. (e.g., extensions like `.jpg`, `.png` when used for image archives or `.mp4` when used for video archives).

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>image_archive</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Too many files in the archive. Maximum is 100 files with extensions .jpg, .png, found 150. Remove 50 matching files from the archive.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>archive_file_count_exceeds_maximum</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#archive_file_count_exceeds_maximum</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"max_count"</span><span>: </span><span>100</span><span>,</span></p></div><div><p><span>      </span><span>"provided_count"</span><span>: </span><span>150</span><span>,</span></p></div><div><p><span>      </span><span>"supported_extensions"</span><span>: [</span><span>"</span><span>.jpg</span><span>"</span><span>, </span><span>"</span><span>.png</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/images_many.zip</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `audio_duration_too_long`

This error indicates that the provided audio file exceeds the maximum allowed duration.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `max_duration`: The maximum allowed duration in seconds.
    -   `provided_duration`: The duration of the provided audio file in seconds.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>audio_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Audio duration exceeds the maximum allowed. Maximum is 60 seconds, provided is 90 seconds.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>audio_duration_too_long</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#audio_duration_too_long</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"max_duration"</span><span>: </span><span>60</span><span>,</span></p></div><div><p><span>      </span><span>"provided_duration"</span><span>: </span><span>90</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/long_audio.mp3</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `audio_duration_too_short`

This error indicates that the provided audio file is shorter than the minimum required duration.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `min_duration`: The minimum required duration in seconds.
    -   `provided_duration`: The duration of the provided audio file in seconds.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>audio_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Audio duration is too short. Minimum is 5 seconds, provided is 2 seconds.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>audio_duration_too_short</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#audio_duration_too_short</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"min_duration"</span><span>: </span><span>5</span><span>,</span></p></div><div><p><span>      </span><span>"provided_duration"</span><span>: </span><span>2</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/short_audio.mp3</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `unsupported_audio_format`

This error indicates that the audio file format is not supported by the endpoint.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `supported_formats`: A list of supported audio file extensions.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>audio_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Unsupported audio format. Supported formats are .mp3, .wav, .ogg.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>unsupported_audio_format</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#unsupported_audio_format</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"supported_formats"</span><span>: [</span><span>"</span><span>.mp3</span><span>"</span><span>, </span><span>"</span><span>.wav</span><span>"</span><span>, </span><span>"</span><span>.ogg</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/audio.midi</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `unsupported_image_format`

This error indicates that the image file format is not supported by the endpoint.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `supported_formats`: A list of supported image file extensions.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>image</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Unsupported image format. Supported formats are .jpg, .jpeg, .png, .webp.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>unsupported_image_format</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#unsupported_image_format</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"supported_formats"</span><span>: [</span><span>"</span><span>.jpg</span><span>"</span><span>, </span><span>"</span><span>.jpeg</span><span>"</span><span>, </span><span>"</span><span>.png</span><span>"</span><span>, </span><span>"</span><span>.webp</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/image.tiff</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `unsupported_video_format`

This error indicates that the video file format is not supported by the endpoint.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `supported_formats`: A list of supported video file extensions.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>video_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Unsupported video format. Supported formats are .mp4, .mov, .webm.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>unsupported_video_format</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#unsupported_video_format</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"supported_formats"</span><span>: [</span><span>"</span><span>.mp4</span><span>"</span><span>, </span><span>"</span><span>.mov</span><span>"</span><span>, </span><span>"</span><span>.webm</span><span>"</span><span>]</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/video.avi</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `video_duration_too_long`

This error indicates that the provided video file exceeds the maximum allowed duration.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `max_duration`: The maximum allowed duration in seconds.
    -   `provided_duration`: The duration of the provided video file in seconds.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>video_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Video duration exceeds the maximum allowed. Maximum is 60 seconds, provided is 120 seconds.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>video_duration_too_long</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#video_duration_too_long</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"max_duration"</span><span>: </span><span>60</span><span>,</span></p></div><div><p><span>      </span><span>"provided_duration"</span><span>: </span><span>120</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/long_video.mp4</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```

##### `video_duration_too_short`

This error indicates that the provided video file is shorter than the minimum required duration.

-   **Status Code:** 422
-   **Retryable:** `false`.
-   **Context (`ctx`):**
    -   `min_duration`: The minimum required duration in seconds.
    -   `provided_duration`: The duration of the provided video file in seconds.

```
<div><p><span>[</span></p></div><div><p><span><span>  </span></span><span>{</span></p></div><div><p><span>    </span><span>"loc"</span><span>: [</span><span>"</span><span>body</span><span>"</span><span>, </span><span>"</span><span>video_file</span><span>"</span><span>],</span></p></div><div><p><span>    </span><span>"msg"</span><span>: </span><span>"</span><span>Video duration is too short. Minimum is 3 seconds, provided is 1 seconds.</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"type"</span><span>: </span><span>"</span><span>video_duration_too_short</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"url"</span><span>: </span><span>"</span><span>https://docs.fal.ai/errors/#video_duration_too_short</span><span>"</span><span>,</span></p></div><div><p><span>    </span><span>"ctx"</span><span>: {</span></p></div><div><p><span>      </span><span>"min_duration"</span><span>: </span><span>3</span><span>,</span></p></div><div><p><span>      </span><span>"provided_duration"</span><span>: </span><span>1</span></p></div><div><p><span><span>    </span></span><span>},</span></p></div><div><p><span>    </span><span>"input"</span><span>: </span><span>"</span><span>https://example.com/short_video.mp4</span><span>"</span></p></div><div><p><span><span>  </span></span><span>}</span></p></div><div><p><span>]</span></p></div>
```