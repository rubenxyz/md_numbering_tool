### You will learn how to:

-   Connect a Next.js app deployed on Vercel to fal.ai

### Prerequisites

1.  A [fal.ai](https://fal.ai/) account
2.  A [Vercel account](https://vercel.com/)
3.  A Next.js app. Check the [Next.js guide](https://docs.fal.ai/integrations/nextjs) if you don’t have one yet.
4.  App deployed on Vercel. Run `npx vercel` in your app directory to deploy it in case you haven’t done it yet.

### Vercel official integration

The recommended way to add fal.ai to your app deployed on Vercel is to use the official integration. You can find it in the [Vercel marketplace](https://vercel.com/integrations/fal).

Click on **Add integration** and follow the steps. After you’re done, re-deploy your app and you’re good to go!

![Vercel integration](https://integrations-og-image.vercel.sh/api/og/fal?42673700034a7509d66487f3ed68a2bd)

### Manual setup

You can also manually add fal credentials to your Vercel environment manually.

1.  Go to your [fal.ai dashboard](https://fal.ai/dashboard/keys), create an **API-scoped** key and copy it. Make sure you create an alias do identify which app is using it.
2.  Go to your app settings in Vercel and add a new environment variable called `FAL_KEY` with the value of the key you just copied. You can choose other names, but keep in mind that the default convention of fal-provided libraries is `FAL_KEY`.
3.  Re-deploy your app and you’re good to go!