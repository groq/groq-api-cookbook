// set JIGSAWSTACK_API_KEY in the secrets

import { JigsawStack } from "jigsawstack";

const jigsaw = JigsawStack({
  apiKey: process.env.JIGSAWSTACK_API_KEY,
});

const params = {
  prompt: "How to cook {dish}", // The prompt for your use case
  inputs: [{ key: "dish" }], // dynamic vars that are in the brackets {}
  return_prompt: [
    {
      step: "name of the step",
      details: "details of this step",
    },
  ], //The structure of the JSON, in this case, an array of objects
  input_values: { dish: "pizza" }, // The values for the dynamic variables
  prompt_guard: ["sexual_content", "defamation"],
};

const result = await jigsaw.prompt_engine.run_prompt_direct(params);

console.log(result);
