## Base64 encode images

To make image generation requests you must send image data as [Base64 encoded](https://en.wikipedia.org/wiki/Base64) text.

## Using the command line

Within a gRPC request, you can simply write binary data out directly; however, JSON is used when making a REST request. JSON is a text format that does not directly support binary data, so you will need to convert such binary data into text using [Base64](https://en.wikipedia.org/wiki/Base64) encoding.

Most development environments contain a native `base64` utility to encode a binary into ASCII text data. To encode a file:

[Linux](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#linux)[macOS](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#macos)[Windows](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#windows)[PowerShell](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#powershell)

Encode the file using the `base64` command line tool, making sure to prevent line-wrapping by using the `-w 0` flag:

```
base64 <devsite-var rendered="" translate="no" is-upgraded="" scope="INPUT_FILE" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit INPUT_FILE" aria-label="Edit INPUT_FILE">INPUT_FILE</var></span></devsite-var> -w 0 &gt; <devsite-var rendered="" translate="no" is-upgraded="" scope="OUTPUT_FILE" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit OUTPUT_FILE" aria-label="Edit OUTPUT_FILE">OUTPUT_FILE</var></span></devsite-var>
```

Create a JSON request file, inlining the base64-encoded data:

[JSON](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#json)

```
<span>{</span>
<span>  </span><span>"instances"</span><span>:</span><span> </span><span>[</span>
<span>    </span><span>{</span>
<span>      </span><span>"prompt"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="TEXT_PROMPT" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit TEXT_PROMPT" aria-label="Edit TEXT_PROMPT">TEXT_PROMPT</var></span></devsite-var>"</span><span>,</span>
<span>      </span><span>"image"</span><span>:</span><span> </span><span>{</span>
<span>        </span><span>"bytes_base64_encoded"</span><span>:</span><span> </span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="B64_BASE_IMAGE" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit B64_BASE_IMAGE" aria-label="Edit B64_BASE_IMAGE">B64_BASE_IMAGE</var></span></devsite-var>"</span>
<span>      </span><span>}</span>
<span>    </span><span>}</span>
<span>  </span><span>]</span>
<span>}</span>
```

## Using client libraries

Embedding binary data into requests through text editors is neither desirable or practical. In practice, you will be embedding base64 encoded files within client code. All supported programming languages have built-in mechanisms for base64 encoding content.

[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python)[Node.js](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#node.js)[Java](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#java)[Go](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#go)

```
<span># Import the base64 encoding library.</span>
<span>import</span><span> </span><span>base64</span>

<span># Pass the image data to an encoding function.</span>
<span>def</span><span> </span><span>encode_image</span><span>(</span><span>image</span><span>):</span>
    <span>with</span> <span>open</span><span>(</span><span>image</span><span>,</span> <span>"rb"</span><span>)</span> <span>as</span> <span>image_file</span><span>:</span>
        <span>encoded_string</span> <span>=</span> <span>base64</span><span>.</span><span>b64encode</span><span>(</span><span>image_file</span><span>.</span><span>read</span><span>())</span>
    <span>return</span> <span>encoded_string</span>
```

## Base64 decode images

API requests return generated or edited images as base64-encoded strings. You can use the following client library samples to decode this data and save it locally as an image file.

[Python](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#python)[Node.js](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#node.js)[Java](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#java)[Go](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#go)

```
<span># Import the base64 encoding library.</span>
<span>import</span><span> </span><span>base64</span>

<span># Pass the base64 encoded image data to a decoding function and save image file.</span>
<span>def</span><span> </span><span>decode_image</span><span>(</span><span>b64_encoded_string</span><span>):</span>
   <span>with</span> <span>open</span><span>(</span><span>"b64DecodedImage.png"</span><span>,</span> <span>"wb"</span><span>)</span> <span>as</span> <span>fh</span><span>:</span>
     <span>fh</span><span>.</span><span>write</span><span>(</span><span>base64</span><span>.</span><span>decodebytes</span><span>(</span><span>b64_encoded_string</span><span>))</span>
```