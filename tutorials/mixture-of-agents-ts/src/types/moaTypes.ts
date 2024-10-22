export type LayerAgentConfig = {
  systemPrompt: string;
  modelName: string;
  temperature?: number;
};

export type MOAConfig = {
  mainModel: string;
  cycles: number;
  layerAgentConfig: Record<string, LayerAgentConfig>;
  mainModelTemperature?: number;
};
