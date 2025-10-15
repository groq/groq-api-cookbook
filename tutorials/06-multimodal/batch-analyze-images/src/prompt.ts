/*
 * prompt.ts
 *
 * Contains the prompt template for image analysis used in the batch workflow.
 *
 */

/**
 * Prompt for the AI to analyze an image and return structured JSON output.
 */
export const IMAGE_ANALYSIS_PROMPT = `
You are a helpful assistant that can answer questions and help with tasks.

You will be given a photo. Analyze this photo and output in JSON format with keys:
- description: A description of the photo
- tags: A list of 10 unique tags that describe the photo
- dominant_color: The dominant color of the photo in hex format (e.g. #000000). Do not use pure black or white.
- image_url: The URL of the input image
- author_name: The name of the author of the photo
- author_username: The username of the author of the photo
`