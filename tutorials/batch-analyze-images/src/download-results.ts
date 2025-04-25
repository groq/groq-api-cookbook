/*
 * download-results.ts
 *
 * Logic to download the results of a completed batch job.
 * Usage: npm run download-results -- <batch_job_id>
 * 
 * Example:
 * npm run download-results -- batch_01jsf80ntwec1bg7dzx073ahf0
 */
import Groq from "groq-sdk";
import fs from "fs";
const groq = new Groq();

const main = async () => {
    const batch_job_id = process.argv[2];
    if (!batch_job_id || !batch_job_id.startsWith("batch_")) {
        console.error("Please provide a valid batch job ID as an argument.");
        return process.exit(1);
    }

    const batch_job = await groq.batches.retrieve(batch_job_id);
    console.log(batch_job);

    if (batch_job.status !== "completed") {
        console.error("Batch job is not completed yet.");
        return process.exit(1);
    }

    const output_file_id = batch_job.output_file_id;
    if (!output_file_id) {
        console.error("Batch job has no output file ID.");
        return process.exit(1);
    }

    // Download error file if it exists
    if (batch_job.error_file_id) {
        const error_file = "batch-errors.jsonl";
        const content = await groq.files.content(batch_job.error_file_id);
        fs.writeFileSync(error_file, await content.text());
        console.log(`File downloaded successfully to ${error_file}`);
    }

    // Download output file with the results
    const output_file = "batch-results.jsonl";
    const content = await groq.files.content(output_file_id);
    fs.writeFileSync(output_file, await content.text());
    console.log(`File downloaded successfully to ${output_file}`);
}

main();