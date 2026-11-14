// deno-lint-ignore-file no-explicit-any
// Reminder emails. pg_cron calls this every hour (supabase/nudge.sql); it sends at most one email a week to each player
// who switched reminders on in their profile. Who gets what is decided in pick.js.
// A link in every email (GET or one-click POST with ?unsub=…&sig=…) turns reminders off.
//
// Deploy:  supabase functions deploy nudge --no-verify-jwt     (the cron call and the links carry their own secret)
// Secrets: supabase secrets set RESEND_API_KEY=… NUDGE_FROM="Pip <pip@your-domain>" NUDGE_SECRET=… SITE_URL=https://…/
// Try it:  POST {"dry": true} with the x-nudge-secret header lists who would get which email, and sends nothing.
import { createClient } from 'npm:@supabase/supabase-js@2';
import { pickNudge, writeNudge } from './pick.js';
import titles from './titles.json' with { type: 'json' };

const env = (k: string) => Deno.env.get(k) ?? '';
const sb = createClient(env('SUPABASE_URL'), env('SUPABASE_SERVICE_ROLE_KEY'), { auth: { persistSession: false } });
const enc = new TextEncoder();

async function sign(uid: string): Promise<string> {
  const key = await crypto.subtle.importKey('raw', enc.encode(env('NUDGE_SECRET')), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const mac = new Uint8Array(await crypto.subtle.sign('HMAC', key, enc.encode('unsub:' + uid)));
  return btoa(String.fromCharCode(...mac)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
const page = (t: string) => new Response(`<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Reminders</title>
<body style="font:17px/1.5 -apple-system,Segoe UI,sans-serif;max-width:480px;margin:60px auto;padding:0 20px;color:#12201A"><p>${t}</p></body>`, { headers: { 'content-type': 'text/html; charset=utf-8' } });

async function unsubscribe(url: URL): Promise<Response> {
  const uid = url.searchParams.get('unsub') ?? '', sig = url.searchParams.get('sig') ?? '';
  if (!uid || !env('NUDGE_SECRET') || sig !== await sign(uid)) return page('That link does not work any more. You can turn reminders off in your profile in the app.');
  const { data: row } = await sb.from('progress').select('data').eq('user_id', uid).maybeSingle();
  if (row && row.data) {
    const d = row.data as any; d.mail = { on: false, t: Date.now() };
    await sb.from('progress').update({ data: d }).eq('user_id', uid);
  }
  return page('Done: no more reminder emails. You can turn them back on in your profile in the app.');
}

async function send(to: string, mail: { subject: string; text: string; html: string }, unsub: string): Promise<boolean> {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env('RESEND_API_KEY')}`, 'content-type': 'application/json' },
    body: JSON.stringify({ from: env('NUDGE_FROM'), to: [to], subject: mail.subject, text: mail.text, html: mail.html,
      headers: { 'List-Unsubscribe': `<${unsub}>`, 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click' } }),
  });
  return r.ok;
}

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);
  if (url.searchParams.has('unsub')) return unsubscribe(url);
  if (req.method !== 'POST' || !env('NUDGE_SECRET') || req.headers.get('x-nudge-secret') !== env('NUDGE_SECRET')) return new Response('no', { status: 401 });
  const body = await req.json().catch(() => ({}));
  const dry = !!body.dry, now = Date.now(), self = `${env('SUPABASE_URL')}/functions/v1/nudge`;
  const report: any[] = [];
  for (let from = 0; ; from += 500) {
    const { data: rows, error } = await sb.from('progress').select('user_id, data').eq('data->mail->>on', 'true').range(from, from + 499);
    if (error) return Response.json({ error: error.message }, { status: 500 });
    if (!rows || !rows.length) break;
    const ids = rows.map((r: any) => r.user_id);
    const { data: past } = await sb.from('nudges').select('user_id, sent_at').in('user_id', ids).order('sent_at', { ascending: false });
    const last: Record<string, number> = {};
    for (const p of past ?? []) if (!last[p.user_id]) last[p.user_id] = Date.parse(p.sent_at);
    for (const r of rows as any[]) {
      const pick = pickNudge(r.data, now, last[r.user_id], titles as Record<string, string>);
      if (!pick) continue;
      const unsub = `${self}?unsub=${encodeURIComponent(r.user_id)}&sig=${await sign(r.user_id)}`;
      const mail = writeNudge(pick, env('SITE_URL'), unsub);
      if (dry) { report.push({ user: r.user_id, kind: pick.kind, subject: mail.subject }); continue; }
      const { data: u } = await sb.auth.admin.getUserById(r.user_id);
      const to = u && u.user && u.user.email;
      if (!to) continue;
      if (await send(to, mail, unsub)) {
        await sb.from('nudges').insert({ user_id: r.user_id, kind: pick.kind });
        report.push({ user: r.user_id, kind: pick.kind });
      }
    }
    if (rows.length < 500) break;
  }
  return Response.json({ dry, sent: report.length, report });
});
