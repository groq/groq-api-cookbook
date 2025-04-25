# Analyze and Tag Images with Llama 4 on Groq Batch

This tutorial will guide you through the process of analyzing a bulk set of images to tag and categorize them. We'll be using the [Groq Batch API](https://console.groq.com/docs/batch), which is great for asynchronously processing large datasets and workloads at a reduced price.


## Setup This Tutorial

To clone just this tutorial (instead of the entire cookbook), run these commands:

For Linux/Mac:
```bash
mkdir groq-batch-analyze-images
cd groq-batch-analyze-images
git init
git remote add origin https://github.com/groq/groq-api-cookbook.git
git config core.sparseCheckout true
echo "tutorials/batch-analyze-images/*" >> .git/info/sparse-checkout
git pull origin main
cd tutorials/batch-analyze-images
```

For Windows (Command Prompt):
```cmd
mkdir groq-batch-analyze-images
cd groq-batch-analyze-images
git init
git remote add origin https://github.com/groq/groq-api-cookbook.git
git config core.sparseCheckout true
echo tutorials/batch-analyze-images/* > .git\info\sparse-checkout
git pull origin main
cd tutorials/batch-analyze-images
```

## Download Dataset

First, we need to download our images dataset. For this, we'll be using [Unsplash](https://unsplash.com) to grab 100 random images to analyze.

Run the setup script to download the lite dataset:
```sh
./setup.sh
```

If you get an access denied error, make sure you have permissions to execute the setup file:
```
sh
chmod +x ./setup.sh
```

Make sure to read and agree to the [Unsplash Lite Dataset Terms of Service](https://github.com/unsplash/datasets/blob/master/TERMS.md) before downloading it.


## Create the Batch Job

For this tutorial, we'll be using [NodeJS](https://nodejs.org) and Typescript to create and manage the batch image analysis job. 

To install dependencies, run:
```sh
npm install
```

Next, grab your [Groq API key from here](https://console.groq.com/keys). You'll need to be on the [developer tier](https://console.groq.com/settings/billing/plans) (paid) to use batch processing.

Rename the `.env.example` file to `.env.local` and add your API key to it:
```sh
GROQ_API_KEY="gsk_XXXXX"
```

Now let's dive into the code!

### Preparing the JSONL File

To create a batch job, we need to upload a `jsonl` file to Groq. This `jsonl` file is a list of requests that we want Groq to perform. For more information, please take a look at the [Groq batch processing documentation](https://console.groq.com/docs/batch).

In our case, we want to send a `jsonl` file with requests including URLs to the images we want to analyze and our prompts that tell the AI what to do. 

Let's take a look at `src/helpers.ts`.

Inside, we can see a function `createJsonlFile`, which creates an object filled with lines of JSON. Each JSON line corresponds to a [chat completion request](https://console.groq.com/docs/text-chat). We're using the [Llama 4 Maverick model](https://console.groq.com/docs/model/llama-4-maverick-17b-128e-instruct) because it has intelligent vision capabilities, which is necessary for analyzing images.

In the messages array, the user has a few pieces of content in their messages:
 - the image analysis prompt, telling the AI how and what to analyze
 - the image URL as text, which will be useful for showing the original image later
 - the author information, used for attribution
 - the image URL as an `image_url`, which is used to tell the AI that this is an image that it should fetch and take a look at

After the user's messages, we also set an assistant message to prefill the expected assistant's response. Because we want the AI to output JSON, we can help steer it in the right direction by showing it that it's already started outputting valid JSON - now it just needs to continue with it. Without prefilling, the assistant might add remarks in the beginning before outputting JSON, such as "Great, let me do that!" or "Okay, I will create the JSON."

Let's take a quick look at the prompt we're using to analyze our images. Open `src/prompt.ts` and you'll see this prompt:

```
You are a helpful assistant that can answer questions and help with tasks.

You will be given a photo. Analyze this photo and output in JSON format with keys:
- description: A description of the photo
- tags: A list of 10 unique tags that describe the photo
- dominant_color: The dominant color of the photo in hex format (e.g. #000000). Do not use pure black or white.
- image_url: The URL of the input image
- author_name: The name of the author of the photo
- author_username: The username of the author of the photo
```

This prompt is fairly simple, but it works well with Llama 4's capabilities. You can see how easy it is to extract more information from the images - just add more to the prompt.

In our prompt, we're asking the model to output JSON that looks something like this:

```json
{
    "description": "An aerial view of a beach with waves gently lapping at the shore.",
    "tags": [
        "beach",
        "ocean",
        "waves",
        "sand",
        "aerial view",
        "coastline",
        "seaside",
        "water's edge",
        "serene",
        "nature"
    ],
    "dominant_color": "#6495a5",
    "image_url": "https://images.unsplash.com/photo-1516610627349-1b52a4ff315e",
    "author_name": "Juan Jose",
    "author_username": "jjalonso"
}
```

If we open up [the image](https://images.unsplash.com/photo-1516610627349-1b52a4ff315e), we can see that this is very accurate! It's analyzed that this is a view from above of a serene beach coastline, and it's correctly given us the dominant color of the water. 

Before performing a batch operation on thousands of images, it's important to test and fine-tune your prompt to make sure it works on all types of images. Edge cases might arise, and it's important to make sure your prompt can handle them properly. 

For example: what might happen if the author's name or username are not available in the dataset? Should we instruct the AI to fill in empty data with "Unknown", or do we want to handle it ourselves when viewing the results later? How you handle these cases is dependent on your use case.

### Uploading the JSONL File to Groq

Now that we've created the input `batch.jsonl` file, we need to upload it to Groq. This is done in step 2 in `src/index.ts`:

```ts
const file_upload_response = await groq.files.create({
    file: fs.createReadStream("batch.jsonl"),
    purpose: "batch",
});
```

### Creating the Batch Job

Once our batch input file has been uploaded, we can use it to start the batch job. This is done in step 3 of `src/index.ts`:

```ts
const batch_job = await groq.batches.create({
    completion_window: "24h",
    input_file_id: file_upload_response.id,
    endpoint: "/v1/chat/completions"
});
```

Run the entire script to create the `jsonl` file, upload it, and create the batch job:
```
npm run start
```

After the batch job has been created, we can [track it in the dashboard](https://console.groq.com/dashboard/batch) or use the SDK. We've created a script in `src/check-status.ts` to check the status of our batch job:
```ts
const batch_job = await groq.batches.retrieve(batch_job_id);
console.log(batch_job);
```

To run the script:
```
npm run check-status -- batch_01jsf80ntwec1bg7dzx073ahf0
```

The output will look something like this:

```js
{
    id: 'batch_01jsht3h8eetvan84vnmdvar2h',
    object: 'batch',
    endpoint: '/v1/chat/completions',
    input_file_id: 'file_01jsht3h0jevh8y8be0fqqmjk4',
    completion_window: '24h',
    status: 'completed',
    output_file_id: 'file_01jsht4v0zfq2r40h5spje2nvp',
    error_file_id: null,
    created_at: 1745428268,
    in_progress_at: 1745428273,
    finalizing_at: 1745428310,
    completed_at: 1745428311,
    failed_at: null,
    cancelling_at: null,
    cancelled_at: null,
    expires_at: 1745514668,
    expired_at: null,
    request_counts: { completed: 100, failed: 0, total: 100 },
    metadata: null,
    errors: null
}
```

## Analyze the Results

Once the batch job is complete, we can download the results and view them:

```ts
const output_file = "batch-results.jsonl";
const content = await groq.files.content(output_file_id);
fs.writeFileSync(output_file, await content.text());
```

To run the script:
```
npm run download-results -- batch_01jsf80ntwec1bg7dzx073ahf0
```

This script will download the file content as text from Groq and store it in `batch-results.jsonl`. These results have one line for each line of the input `jsonl` file. With so many lines, it's a bit difficult to sift through to see what's really inside them, so we can use a static webpage to visualize our analysis.

Open `gallery.html` in a web browser - you can drag it into your web browser to load it. Once you have it loaded, you should see a button to select your JSONL file - go ahead and select the `batch-results.jsonl` file we just downloaded.

![image gallery](https://github.com/user-attachments/assets/f5c1fd4a-8e88-441d-af5f-a303e7611cf9)

The web page will display all the results of the batch job as an image galllery. Each image is accompanied by the author's name (which links to their profile), the generated description, tags, and even the dominant color.

All of these fields were parsed out of the JSON that we told the AI to generate for all of these images. Now we can easily sort and search through these images that were previously uncategorized! Try clicking on tags to filter by tag, or type text into the search box at the top.

## Next Steps

Pat yourself on the back for completing this tutorial! Nice job! 

But now that you've finished this - what's next?

A few follow-up challenges for you to consider:
 - Extract more information out of each of the photos by adjusting the prompt, and then display that information on the gallery page
 - Use your own images! Grab some images from your camera roll and analyze those. You could even turn this into an entire pipeline for categorizing and analyzing your own images.
 - Try analyzing a video! _Hint: you'll need to extract the frames from the video, then analyze those._ 