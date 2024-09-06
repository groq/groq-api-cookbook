import { runMOA } from "../services/moaService";
import { moaConfig } from "../config/moaConfig";

export const processMOA = async (req: Request): Promise<Response> => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }
  const body = await req.json();
  const question = (body as { question?: string }).question;

  if (!question) {
    return new Response(JSON.stringify({ error: "Question is required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const stream = new ReadableStream({
    async start(controller) {
      try {
        await runMOA(question, moaConfig, (update) => {
          controller.enqueue(`${update}\n`);
        });
        controller.close();
      } catch (error) {
        console.error("An error occurred:", error);
        controller.enqueue("An error occurred while processing the request.\n");
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: { "Content-Type": "text/plain" },
  });
};
