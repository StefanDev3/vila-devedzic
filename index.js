export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let pathname = url.pathname;

    // Default to index.html for root
    if (pathname === '/' || pathname === '') {
      pathname = '/index.html';
    }

    try {
      // Try to fetch the requested file
      const response = await env.ASSETS.fetch(request);

      // If 404, serve index.html (for SPA routing)
      if (response.status === 404 && !pathname.includes('.')) {
        return await env.ASSETS.fetch(new Request(new URL('/index.html', url).toString(), request));
      }

      return response;
    } catch (error) {
      // Fallback to index.html on error
      return await env.ASSETS.fetch(new Request(new URL('/index.html', url).toString(), request));
    }
  },
};
