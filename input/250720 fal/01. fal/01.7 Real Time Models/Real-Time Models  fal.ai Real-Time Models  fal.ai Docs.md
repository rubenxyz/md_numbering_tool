Real-time AI is here! With the recent introduction of Latent Consistency Models (LCM) and distilled models like Stability’s SDXL Turbo and SD Turbo, it is now possible to generate images in under 100ms.

This fast inference capability opens up new possibilities for application types that were previously not feasible, such as real-time creativity tools and using the camera as a real-time model input.

You can find the fastest real time models in fal’s [Model Registry](https://fal.ai/models).

**How does fal provide the fastest real-time inference?**

We did all the optimizations in the book.

-   fal has built custom infrastructure and optimized the model inference to make sure these models are served to the end user as fast as possible.
-   fal has a globally distributed network of GPUs to make sure the inference happens as close to the user as possible.
-   We do very few hops between the user and the GPU. Our authentication service is written in Rust and deployed on the edge as close to the user and the GPUs as possible.
-   Our websocket and streaming clients provide the most efficient client/server communication possible.
-   We only authenticate through a jwt token, from the client directly to our services, we have built integrations to popular backend frameworks to facilitate token refreshes.

**Is fal’s real time AI inference ready for prime time?**

Several amazing demos and products were built using fal’s real time inference infrastructure. These demos went viral on social media and are still used by thousands of people every day.

You can see an example at [https://fal.ai/camera](https://fal.ai/camera).