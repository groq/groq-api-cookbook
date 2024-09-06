import { Serve } from "bun";
import { routes, notFoundHandler, Route } from "./routes";

const server: Serve = {
  port: process.env.PORT || 3000,
  fetch(req: Request) {
    const url = new URL(req.url);
    const route = routes.find(
      (r: Route) => r.path === url.pathname && r.method === req.method
    );

    if (route) {
      return route.handler(req);
    }

    return notFoundHandler();
  },
};

console.log(`Listening on http://localhost:${server.port}`);

export default server;
