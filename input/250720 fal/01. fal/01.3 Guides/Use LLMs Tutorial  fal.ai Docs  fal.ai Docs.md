fal provides an easy-to-use API for generating text using Language Models (LLMs). You can use the `fal-ai/any-llm` endpoint to generate text based on a given prompt and model.

Here’s an example of how to use the `fal-ai/any-llm` endpoint to generate text using the `anthropic/claude-3.5-sonnet` model:

```
<div><p><span>import</span><span> { fal } </span><span>from</span><span> </span><span>"</span><span>@fal-ai/client</span><span>"</span><span>;</span></p></div><div><p><span>const </span><span>result</span><span> = await </span><span>fal</span><span>.</span><span>subscribe</span><span>(</span><span>"</span><span>fal-ai/any-llm</span><span>"</span><span>, {</span></p></div><div><p><span><span>  </span></span><span>input: {</span></p></div><div><p><span><span>    </span></span><span>model: </span><span>"</span><span>anthropic/claude-3.5-sonnet</span><span>"</span><span>,</span></p></div><div><p><span><span>    </span></span><span>prompt: </span><span>"</span><span>What is the meaning of life?</span><span>"</span></p></div><div><p><span><span>  </span></span><span>},</span></p></div><div><p><span>}</span><span>);</span></p></div>
```

## How to select LLM model to use

fal offers a variety of LLM models. You can select the model that best fits your needs based on the style and quality of the text you want to generate. Here are some of the available models:

-   `anthropic/claude-3.5-sonnet`: Claude 3.5 Sonnet
-   `google/gemini-pro-1.5`: Gemini Pro 1.5
-   `meta-llama/llama-3.2-3b-instruct`: Llama 3.2 3B Instruct
-   `openai/gpt-4o`: GPT-4o

To select a model, simply specify the model ID in the `model` field as shown in the example above. You can find more LLMs in the [Any LLM](https://fal.ai/models/fal-ai/any-llm) page.