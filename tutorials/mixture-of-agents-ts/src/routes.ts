import { processMOA } from "./controllers/moaController";

export type Route = {
  path: string;
  method: string;
  handler: (req: Request) => Promise<Response>;
};

export const routes: Route[] = [
  {
    path: "/moa/process",
    method: "POST",
    handler: processMOA,
  },
];

export const notFoundHandler = (): Response => {
  return new Response("Not Found", { status: 404 });
};
