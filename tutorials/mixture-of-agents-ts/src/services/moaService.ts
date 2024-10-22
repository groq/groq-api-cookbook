import Groq from "groq-sdk";
import { LayerAgentConfig, MOAConfig } from "../types/moaTypes";

const groq = new Groq();

const createMessage = (
  role: "user" | "assistant" | "system",
  content: string
) => ({
  role,
  content,
});

const createSystemMessage = (content: string) =>
  createMessage("system", content);

const createUserMessage = (content: string) => createMessage("user", content);

const runLayerAgent = async (
  input: string,
  helperResponse: string,
  agentConfig: LayerAgentConfig
): Promise<string> => {
  const messages = [
    createSystemMessage(agentConfig.systemPrompt),
    createUserMessage(input),
    createSystemMessage(helperResponse),
  ];

  const response = await groq.chat.completions.create({
    messages,
    model: agentConfig.modelName,
    temperature: agentConfig.temperature ?? 0.7,
  });

  return response.choices[0]?.message?.content || "";
};

const runLayerAgents = async (
  input: string,
  helperResponse: string,
  layerAgentConfig: Record<string, LayerAgentConfig>
): Promise<string> => {
  const responses = await Promise.all(
    Object.entries(layerAgentConfig).map(async ([agentName, config]) => {
      const response = await runLayerAgent(input, helperResponse, config);
      console.log(`${agentName}: ${response}`);
      return response;
    })
  );
  return responses.join("\n");
};

export const runMOA = async (
  input: string,
  config: MOAConfig,
  onUpdate: (update: string) => void
): Promise<string> => {
  const runCycle = async (
    cycleCount: number,
    helperResponse: string
  ): Promise<string> => {
    if (cycleCount === 0) {
      const finalMessages = [
        createSystemMessage("You are a helpful assistant."),
        createUserMessage(input),
        createSystemMessage(helperResponse),
      ];

      const finalResponse = await groq.chat.completions.create({
        messages: finalMessages,
        model: config.mainModel,
        temperature: config.mainModelTemperature ?? 0.7,
      });

      const result = finalResponse.choices[0]?.message?.content || "";
      onUpdate(`Final Response: ${result}`);
      return result;
    }

    onUpdate(`Cycle ${config.cycles - cycleCount + 1}:`);
    const newHelperResponse = await runLayerAgents(
      input,
      helperResponse,
      config.layerAgentConfig
    );
    onUpdate(newHelperResponse);
    return runCycle(cycleCount - 1, newHelperResponse);
  };

  return runCycle(config.cycles, "");
};
