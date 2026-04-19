export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);

    let path = pathname === '/' ? '/index.html' : pathname;

    try {
      return await env.ASSETS.fetch(request.clone());
    } catch (error) {
      // Fallback to index.html for SPA routing
      return env.ASSETS.fetch(new Request(new URL('/index.html', request.url).toString(), request));
    }
  },
};
