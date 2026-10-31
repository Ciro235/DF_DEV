const reply = (status, error) => new Response(JSON.stringify({ ok: status === 200, error }), {
  status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
});

export async function onRequestPost({ request, env }) {
  const origin = new URL(request.url).origin;
  if (request.headers.get('Origin') !== origin) return reply(403, 'origin');
  if (!request.headers.get('Content-Type')?.startsWith('application/json')) return reply(415, 'content_type');
  // Never collect real inquiries while the published controller details are mockups.
  if (env.LEGAL_REVIEWED !== 'true' || !env.RESEND_API_KEY || !env.CONTACT_FROM || !env.TURNSTILE_SECRET) {
    return reply(503, 'not_configured');
  }
  const key = request.headers.get('Idempotency-Key') || '';
  if (!/^[a-zA-Z0-9-]{16,80}$/.test(key)) return reply(400, 'request_id');
  let data;
  try {
    const reader = request.body?.getReader();
    if (!reader) return reply(400, 'body');
    let size = 0; const chunks = [];
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.length;
      if (size > 8192) { await reader.cancel(); return reply(413, 'body_too_large'); }
      chunks.push(value);
    }
    const bytes = new Uint8Array(size); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
    data = JSON.parse(new TextDecoder().decode(bytes));
  } catch { return reply(400, 'invalid_json'); }
  if (!data || typeof data !== 'object' || Array.isArray(data)) return reply(400, 'invalid_data');
  if (typeof data.website !== 'string' || data.website !== '') return reply(422, 'invalid_data');
  if (!['automation', 'web', 'integrations'].includes(data.service)) return reply(422, 'service');
  if (typeof data.email !== 'string' || data.email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return reply(422, 'email');
  if (typeof data.message !== 'string' || data.message.trim().length < 15 || data.message.length > 4000) return reply(422, 'message');
  if (typeof data.name !== 'string' || data.name.length > 120) return reply(422, 'name');
  if (typeof data.turnstileToken !== 'string' || data.turnstileToken.length > 2048) return reply(422, 'verification');
  try {
    const verification = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: data.turnstileToken }),
      signal: AbortSignal.timeout(10000)
    });
    if (!verification.ok) return reply(502, 'verification_unavailable');
    const challenge = await verification.json();
    if (!challenge.success || challenge.hostname !== new URL(request.url).hostname) return reply(422, 'verification');
    const sent = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + env.RESEND_API_KEY, 'Content-Type': 'application/json', 'Idempotency-Key': key },
      body: JSON.stringify({
        from: env.CONTACT_FROM,
        to: ['dariosc235@gmail.com', 'fsegui16@gmail.com'],
        reply_to: data.email,
        subject: 'readytoprod · ' + data.service,
        text: 'Name: ' + data.name + '\nEmail: ' + data.email + '\nService: ' + data.service + '\n\n' + data.message.trim()
      }),
      signal: AbortSignal.timeout(15000)
    });
    if (!sent.ok) return reply(502, 'delivery_not_accepted');
    return reply(200);
  } catch { return reply(502, 'temporarily_unavailable'); }
}

export function onRequestGet() { return reply(405, 'method'); }
