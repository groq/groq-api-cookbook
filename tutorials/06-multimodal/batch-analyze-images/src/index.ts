import Groq from "groq-sdk";
import { createJsonlFile } from "./helpers";
import fs from "fs";

const groq = new Groq({
    apiKey: process.env.GROQ_API_KEY,
});

// Number of images to analyze
const NUM_IMAGES = 100;

/*
 * index.ts
 *
 * Main entry point for the batch image analysis workflow.
 * - Generates a JSONL file with prompts for image analysis.
 * - Uploads the JSONL file to Groq for batch processing.
 * - Initiates a batch job using the uploaded file.
 * 
 * To run: npm run start
 *
 */
const main = async () => {
    // Step 1: Generate the JSONL file with prompts for image analysis
    console.log("Creating JSONL file...");
    const jsonl_lines = await createJsonlFile(NUM_IMAGES);
    const jsonl_file_contents = jsonl_lines.map((line) => JSON.stringify(line)).join("\n");

    fs.writeFileSync("batch.jsonl", jsonl_file_contents);

    // Step 2: Upload the JSONL file to Groq
    console.log("Uploading file...");
    const file_upload_response = await groq.files.create({
        file: fs.createReadStream("batch.jsonl"),
        purpose: "batch",
    });

    if (!file_upload_response.id) {
        throw new Error("File upload failed");
    }

    // Step 3: Create a batch job using the uploaded file
    console.log("Creating batch job...");
    const batch_job = await groq.batches.create({
        completion_window: "24h",
        input_file_id: file_upload_response.id,
        endpoint: "/v1/chat/completions"
    });

    console.log("Batch job created:", batch_job.id);
}

main();