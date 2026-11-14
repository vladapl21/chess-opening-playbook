// Who gets a reminder email, and which one. Pure: no network, no clock of its own, so tests/nudge_check.mjs can run it
// under Node and the edge function (index.ts) under Deno.
//
// The rules keep the emails scarce:
//   - only players who switched reminders on (data.mail.on), and never more than one email in seven days;
//   - only in the early evening where the player is (data.tz), and only when today's five lines are not done yet;
//   - "streak": a streak of three days or more that ends at midnight unless five lines are played today;
//   - "slips": three or more lines the player slipped on and has not played for three days, after two quiet days.
// Anything else: no email.

export const DAILY = 5;
const DAY = 864e5, WEEK = 7 * DAY;
export const COACHES = {knight: 'Pip', rook: 'Rocco', pawn: 'Dot'};

// the date (YYYY-MM-DD) and hour in a time zone
export function localParts(now, tz){
  let f;
  try { f = new Intl.DateTimeFormat('en-CA', {timeZone: tz || 'UTC', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23'}); }
  catch(e){ f = new Intl.DateTimeFormat('en-CA', {timeZone: 'UTC', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23'}); }
  const p = Object.fromEntries(f.formatToParts(new Date(now)).map(x => [x.type, x.value]));
  return {key: `${p.year}-${p.month}-${p.day}`, hour: Number(p.hour) % 24};
}
export function shiftKey(key, d){ const [y, m, dd] = key.split('-').map(Number); return new Date(Date.UTC(y, m - 1, dd + d)).toISOString().slice(0, 10); }

const count = v => Array.isArray(v) ? v.length : (v || 0);

export function pickNudge(data, now, lastSent, titles = {}){
  if (!data || !data.mail || !data.mail.on) return null;
  if (lastSent && now - lastSent < WEEK) return null;
  const L = localParts(now, data.tz);
  if (L.hour < 17 || L.hour > 20) return null;
  const days = data.days || {}, n = k => count(days[k]);
  if (n(L.key) >= DAILY) return null;
  const recs = Object.entries(data.lines || {});
  if (!recs.length) return null;
  const coach = COACHES[(data.set || {}).who] || 'Pip';
  let streak = 0; for (let k = shiftKey(L.key, -1); n(k) >= DAILY; k = shiftKey(k, -1)) streak++;
  if (streak >= 3) return {kind: 'streak', coach, streak, count: 0, lessons: []};
  const lastActive = Math.max(0, ...recs.map(([, r]) => (r && r.last) || 0));
  const slips = recs.filter(([, r]) => r && r.seen && !r.box && (r.last || 0) < now - 3 * DAY).sort((a, b) => (a[1].last || 0) - (b[1].last || 0));
  if (slips.length >= 3 && now - lastActive > 2 * DAY){
    const lessons = [...new Set(slips.map(([id]) => titles[id]).filter(Boolean))].slice(0, 2);
    return {kind: 'slips', coach, streak: 0, count: slips.length, lessons};
  }
  return null;
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const words = n => ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'][n] || String(n);
const listOf = xs => xs.length < 2 ? xs.join('') : xs.slice(0, -1).join(', ') + ' and ' + xs[xs.length - 1];

// the email itself: a subject, a plain-text body and a small HTML body, in the coach's voice and without notation
export function writeNudge(pick, site, unsub){
  const go = (site || '').replace(/#.*$/, '') + '#drill';
  let subject, lines;
  if (pick.kind === 'streak'){
    subject = `Your ${pick.streak}-day streak ends at midnight`;
    lines = [`${pick.coach} here.`, `You've played five lines a day for ${words(pick.streak)} days running. Five more tonight keeps the streak going, about ten minutes.`];
  } else {
    subject = `${pick.count} lines you slipped on are waiting`;
    lines = [`${pick.coach} here.`, `${pick.count > 10 ? 'More than ten' : words(pick.count)[0].toUpperCase() + words(pick.count).slice(1)} of your lines had a slip last time${pick.lessons.length ? `, ${pick.lessons.length > 1 ? 'among them' : 'including'} ${listOf(pick.lessons)}` : ''}. The second try is where a line sticks: today's five start with them.`];
  }
  const foot = `You get this at most once a week, and only because reminders are on in your profile. Turn them off: ${unsub}`;
  const text = lines.join('\n\n') + `\n\nPlay today's five: ${go}\n\n${foot}\n`;
  const html = `<div style="font:16px/1.55 -apple-system,Segoe UI,sans-serif;color:#12201A;max-width:520px;margin:0 auto;padding:24px">
${lines.map(l => `<p style="margin:0 0 14px">${esc(l)}</p>`).join('\n')}
<p style="margin:22px 0"><a href="${esc(go)}" style="display:inline-block;background:#0D6A4E;color:#fff;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:5px">Play today's five</a></p>
<p style="margin:28px 0 0;font-size:12.5px;color:#566960">You get this at most once a week, and only because reminders are on in your profile. <a href="${esc(unsub)}" style="color:#566960">Turn them off</a>.</p></div>`;
  return {subject, text, html};
}
