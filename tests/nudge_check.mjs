// The reminder-email rules (supabase/functions/nudge/pick.js) on made-up progress records: node tests/nudge_check.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { pickNudge, writeNudge, localParts, shiftKey } from '../supabase/functions/nudge/pick.js';

const titles = JSON.parse(readFileSync(new URL('../supabase/functions/nudge/titles.json', import.meta.url)));
const DAY = 864e5;
// 18:30 in New York on a Friday
const now = Date.parse('2026-11-13T23:30:00Z');
const tz = 'America/New_York';
const today = localParts(now, tz).key;
assert.equal(today, '2026-11-13'); assert.equal(localParts(now, tz).hour, 18);
assert.equal(shiftKey('2026-03-01', -1), '2026-02-28'); assert.equal(shiftKey('2026-12-31', 1), '2027-01-01');

const five = k => ({[k]: ['a', 'b', 'c', 'd', 'e']});
const days = n => Object.assign({}, ...Array.from({length: n}, (_, i) => five(shiftKey(today, -1 - i))));
const ids = Object.keys(titles);
const slipped = (n, age) => Object.fromEntries(ids.slice(0, n).map(id => [id, {box: 0, seen: 2, clean: 1, last: now - age, due: now - age}]));
const base = {mail: {on: true, t: 1}, tz, set: {who: 'rook'}};

// a four-day streak, today not done: the streak email, from Rocco
let p = pickNudge({...base, days: days(4), lines: slipped(1, DAY)}, now, 0, titles);
assert.equal(p.kind, 'streak'); assert.equal(p.streak, 4); assert.equal(p.coach, 'Rocco');
let m = writeNudge(p, 'https://example.org/app/#course', 'https://x/unsub');
assert.equal(m.subject, 'Your 4-day streak ends at midnight');
assert.ok(m.text.includes('Rocco here.') && m.text.includes('https://example.org/app/#drill') && m.text.includes('https://x/unsub'));
assert.ok(!/\b[KQRBN]?x?[a-h][1-8]\b/.test(m.text.replace(/https?:\S+/g, '')), 'no notation in the email');

// reminders off, or an email in the last week, or the wrong hour, or today's five already done: nothing
assert.equal(pickNudge({...base, mail: {on: false}, days: days(4), lines: slipped(1, DAY)}, now, 0, titles), null);
assert.equal(pickNudge({...base, days: days(4), lines: slipped(1, DAY)}, now, now - 3 * DAY, titles), null);
assert.equal(pickNudge({...base, tz: 'Europe/London', days: days(4), lines: slipped(1, DAY)}, now, 0, titles), null);   // 23:30 there
assert.equal(pickNudge({...base, days: Object.assign(days(4), five(today)), lines: slipped(1, DAY)}, now, 0, titles), null);
// eight days after the last email, it may go again
assert.equal(pickNudge({...base, days: days(4), lines: slipped(1, DAY)}, now, now - 8 * DAY, titles).kind, 'streak');

// a two-day streak is not worth an email; old slips after a quiet spell are
assert.equal(pickNudge({...base, days: days(2), lines: slipped(1, 4 * DAY)}, now, 0, titles), null);
p = pickNudge({...base, days: days(2), lines: slipped(4, 4 * DAY)}, now, 0, titles);
assert.equal(p.kind, 'slips'); assert.equal(p.count, 4); assert.ok(p.lessons.length >= 1 && p.lessons.length <= 2, p.lessons);
m = writeNudge(p, 'https://example.org/app/', 'https://x/unsub');
assert.equal(m.subject, '4 lines you slipped on are waiting'); assert.ok(m.text.startsWith('Rocco here.') && m.text.includes('Four of your lines'), m.text);
console.log('slips email:', m.text.split('\n\n')[1]);
// slips from yesterday, or a player who played yesterday: wait
assert.equal(pickNudge({...base, lines: slipped(4, DAY)}, now, 0, titles), null);
assert.equal(pickNudge({...base, lines: Object.assign(slipped(4, 4 * DAY), {other: {box: 2, seen: 1, last: now - DAY}})}, now, 0, titles), null);
// nothing ever drilled: nothing to remind about
assert.equal(pickNudge({...base, days: days(5)}, now, 0, titles), null);
console.log('nudge rules: ok');
