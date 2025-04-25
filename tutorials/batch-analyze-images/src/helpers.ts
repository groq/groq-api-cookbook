import { ChatCompletionCreateParamsNonStreaming } from "groq-sdk/resources/chat/completions.mjs";
import Groq from "groq-sdk";
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { IMAGE_ANALYSIS_PROMPT } from "./prompt";

/*
 * helpers.ts
 *
 * Utility functions for the batch image analysis workflow.
 * - Generates JSONL lines for batch processing.
 * - Selects random images from a dataset, ensuring they meet size and dimension requirements.
 *
 */

/**
 * Represents a single line in the JSONL file for batch processing.
 */
interface JsonlFileLine {
    custom_id: string;
    method: "POST";
    url: "/v1/chat/completions" | "/v1/audio/transcriptions" | "/v1/audio/translations";
    body: ChatCompletionCreateParamsNonStreaming | Groq.Audio.Transcriptions.TranscriptionCreateParams | Groq.Audio.Translations.TranslationCreateParams;
}

/**
 * Represents information about an image from the dataset.
 */
interface ImageInfo {
    url: string;
    authorName: string;
    authorUsername: string;
}

// Image limits: https://console.groq.com/docs/vision
const MAX_IMAGE_SIZE = 1024 * 1024 * 20; // 20MB
const MAX_IMAGE_DIMENSIONS = 30_000_000; // 30MP

/**
 * Generates JSONL lines for batch image analysis.
 * @param num_images Number of images to include in the batch.
 * @returns Array of JSONL lines for batch processing.
 */
export const createJsonlFile = async (num_images: number): Promise<JsonlFileLine[]> => {
    const jsonl_file_contents: JsonlFileLine[] = [];
    const images = await getRandomImages(num_images);

    for (let i = 0; i < num_images; i++) {
        jsonl_file_contents.push({
            custom_id: `image-${i}`,
            method: "POST",
            url: "/v1/chat/completions",
            body: {
                model: "meta-llama/llama-4-maverick-17b-128e-instruct",
                messages: [
                    {
                        role: "user",
                        content: [
                            // Prompt the AI to analyze the image
                            {
                                type: "text",
                                text: IMAGE_ANALYSIS_PROMPT
                            },
                            // Include the image URL in the prompt so we can display them in the gallery
                            {
                                type: "text",
                                text: `Image URL: ${images[i].url}`
                            },
                            // Include the author info in the prompt
                            {
                                type: "text",
                                text: `Author: ${images[i].authorName} - ${images[i].authorUsername}`
                            },
                            // Include the image for the AI to analyze
                            {
                                type: "image_url",
                                image_url: {
                                    url: images[i].url
                                }
                            },
                        ]
                    },
                    {
                        role: "assistant",
                        // Prefill assistant response
                        content: "```json"
                    }
                ],
                stop: "```"
            }
        });
    }

    return jsonl_file_contents;
}

/**
 * Selects random images from the dataset, ensuring they meet size and dimension requirements.
 * @param num_images Number of images to select.
 * @returns Array of image info objects.
 * @throws If not enough valid images are found or the dataset is missing.
 */
export const getRandomImages = async (num_images: number): Promise<ImageInfo[]> => {
    const datasetPath = path.join(__dirname, "../dataset/photos.tsv000");
    if (!fs.existsSync(datasetPath)) {
        throw new Error("dataset/photos.tsv000 not found. Please run setup.sh first.");
    }

    // Read the entire file into memory
    const fileContent = fs.readFileSync(datasetPath, { encoding: "utf8" });
    const lines = fileContent.split("\n").filter(Boolean);
    const totalLines = lines.length;
    if (num_images > totalLines) {
        throw new Error(`Requested ${num_images} images, but only ${totalLines} available.`);
    }

    const images: ImageInfo[] = [];

    // Get random images from the dataset that fit size requirements
    while (images.length < num_images) {
        const idx = crypto.randomInt(0, totalLines);
        const line = lines[idx];
        const cols = line.split("\t");
        if (cols.length < 13) continue; // Need enough columns for author info

        const width = parseInt(cols[5], 10);
        const height = parseInt(cols[6], 10);
        const estimatedSize = width * height * 2; // 2 bytes per pixel estimate
        if (
            isNaN(width) ||
            isNaN(height) ||
            width * height > MAX_IMAGE_DIMENSIONS ||
            estimatedSize > MAX_IMAGE_SIZE
        ) {
            // Skip if image is too large or has invalid dimensions
            continue;
        }
        const url = cols[2];
        const authorUsername = cols[9];
        const authorFirst = cols[10];
        const authorLast = cols[11];
        const authorName = `${authorFirst} ${authorLast}`.trim();
        images.push({ url, authorName, authorUsername });
    }

    if (images.length < num_images) {
        throw new Error(`Could not find enough valid images. Only found ${images.length}.`);
    }
    return images;
}