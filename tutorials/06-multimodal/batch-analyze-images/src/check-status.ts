/*
 * check-status.ts
 *
 * Logic to check the status of a batch job.
 * Usage: npm run check-status -- <batch_job_id>
 * 
 * Example:
 * npm run check-status -- batch_01jsf80ntwec1bg7dzx073ahf0
 */
import Groq from "groq-sdk";
const groq = new Groq();

const main = async () => {
    const batch_job_id = process.argv[2];
    if (!batch_job_id || !batch_job_id.startsWith("batch_")) {
        console.error("Please provide a valid batch job ID as an argument.");
        return process.exit(1);
    }

    const batch_job = await groq.batches.retrieve(batch_job_id);
    console.log(batch_job);
}

main();