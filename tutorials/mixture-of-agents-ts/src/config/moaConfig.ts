import { MOAConfig } from "../types/moaTypes";

export const moaConfig: MOAConfig = {
  mainModel: "mixtral-8x7b-32768",
  cycles: 2,
  mainModelTemperature: 0.7,
  layerAgentConfig: {
    layer_agent_1: {
      systemPrompt:
        "Think through your response step by step. {helper_response}",
      modelName: "llama3-8b-8192",
      temperature: 0.5,
    },
    layer_agent_2: {
      systemPrompt:
        "Respond with a thought and then your response to the question. {helper_response}",
      modelName: "gemma-7b-it",
      temperature: 0.6,
    },
    layer_agent_3: {
      systemPrompt:
        "You are an expert at logic and reasoning. Always take a logical approach to the answer. {helper_response}",
      modelName: "llama3-8b-8192",
      temperature: 0.4,
    },
  },
};
