// Exact tables for the three smallest endings, worked out backwards from the end (node pipeline/endtables.mjs):
//   kqk, krk  king and queen, king and rook against a lone king: plies to mate with best play on both sides
//   kpk       king and pawn against king: plies to a promotion that wins (a queen or a rook that the other king
//             can neither take nor be stalemated by), with best play on both sides
// The stronger side is White in every table. Squares are 0..63 (a1 = 0, h1 = 7, a8 = 56). One byte per position:
// index ((wk * 64 + piece) * 64 + bk) * 2 + side to move (0 White, 1 Black); 0 is a draw (or no legal position),
// anything else is the distance in plies plus one. The bytes go into data/endings/tables.json, zlib-packed and in
// base64, for the page (app/endings.js reads them with DecompressionStream). pipeline/check_tables.py checks every
// value against python-chess's own move rules.
import fs from 'fs';
import zlib from 'zlib';
import path from 'path';
import {fileURLToPath} from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const F = s => s & 7, R = s => s >> 3;
const dist = (a, b) => Math.max(Math.abs(F(a) - F(b)), Math.abs(R(a) - R(b)));
const KM = Array.from({length: 64}, (_, s) => {
  const o = [];
  for (let df = -1; df <= 1; df++) for (let dr = -1; dr <= 1; dr++){
    if (!df && !dr) continue;
    const f = F(s) + df, r = R(s) + dr; if (f >= 0 && f < 8 && r >= 0 && r < 8) o.push(r * 8 + f);
  }
  return o;
});
const ROOK = [[1, 0], [-1, 0], [0, 1], [0, -1]], BISHOP = [[1, 1], [1, -1], [-1, 1], [-1, -1]], QUEEN = ROOK.concat(BISHOP);
// the squares a slider on s reaches, up to and including the first square in occ
function rays(s, dirs, occ){
  const o = [];
  for (const [df, dr] of dirs){
    let f = F(s) + df, r = R(s) + dr;
    while (f >= 0 && f < 8 && r >= 0 && r < 8){ const t = r * 8 + f; o.push(t); if (occ.includes(t)) break; f += df; r += dr; }
  }
  return o;
}
const I = (a, b, c) => (a * 64 + b) * 64 + c;
const SZ = 64 * 64 * 64;
const DRAW = -1;            // a successor that is a draw at once (the piece taken)

// Alternate sweeps: White to move wins in n plies when a move reaches a Black-to-move position lost in n - 1; Black to
// move is lost in n when every move reaches a White win and the longest of them is n - 1. W and B hold plies, -1 unknown.
function solve(W, B, wSucc, bSucc, wNow){
  for (let ply = 1, idle = 0; idle < 2; ply++){
    let ch = 0;
    if (ply % 2){
      for (let i = 0; i < SZ; i++){
        if (W[i] !== -1 || !wSucc[i]) continue;
        if (wNow && wNow[i]){ if (ply === 1){ W[i] = 1; ch++; } continue; }
        for (const s of wSucc[i]) if (s !== DRAW && B[s] === ply - 1){ W[i] = ply; ch++; break; }
      }
    } else {
      for (let i = 0; i < SZ; i++){
        if (B[i] !== -1 || !bSucc[i] || !bSucc[i].length) continue;
        let mx = -1, ok = true;
        for (const s of bSucc[i]){ if (s === DRAW || W[s] < 0){ ok = false; break; } if (W[s] > mx) mx = W[s]; }
        if (ok && mx === ply - 1){ B[i] = ply; ch++; }
      }
    }
    idle = ch ? 0 : idle + 1;
  }
}

function kxk(dirs){
  const W = new Int16Array(SZ).fill(-1), B = new Int16Array(SZ).fill(-1), wSucc = new Array(SZ), bSucc = new Array(SZ);
  for (let wk = 0; wk < 64; wk++) for (let x = 0; x < 64; x++) for (let bk = 0; bk < 64; bk++){
    if (wk === x || wk === bk || x === bk || dist(wk, bk) < 2) continue;
    const i = I(wk, x, bk), att = rays(x, dirs, [wk, bk]), check = att.includes(bk);
    // Black to move: the king may not step next to White's king or onto a square the piece reaches (seen through the
    // king's own square), and takes the piece when White's king doesn't guard it
    const seen = rays(x, dirs, [wk]), bs = [];
    for (const t of KM[bk]){
      if (dist(t, wk) < 2) continue;
      if (t === x){ if (dist(x, wk) > 1) bs.push(DRAW); continue; }
      if (!seen.includes(t)) bs.push(I(wk, x, t));
    }
    bSucc[i] = bs;
    if (!bs.length) B[i] = check ? 0 : -2;     // mate, or stalemate (settled as a draw)
    if (check) continue;                          // White to move with Black in check can't happen
    const ws = [];
    for (const t of KM[wk]) if (t !== x && dist(t, bk) > 1) ws.push(I(t, x, bk));
    for (const t of att) if (t !== wk && t !== bk) ws.push(I(wk, t, bk));
    wSucc[i] = ws;
  }
  solve(W, B, wSucc, bSucc, null);
  return {W, B};
}

function kpk(Q, Rk){
  const W = new Int16Array(SZ).fill(-1), B = new Int16Array(SZ).fill(-1), wSucc = new Array(SZ), bSucc = new Array(SZ), now = new Uint8Array(SZ);
  const pAtt = p => [F(p) > 0 ? p + 7 : -1, F(p) < 7 ? p + 9 : -1].filter(t => t >= 0 && t < 64);
  for (let wk = 0; wk < 64; wk++) for (let p = 8; p < 56; p++) for (let bk = 0; bk < 64; bk++){
    if (wk === p || wk === bk || p === bk || dist(wk, bk) < 2) continue;
    const i = I(wk, p, bk), att = pAtt(p), check = att.includes(bk), bs = [];
    for (const t of KM[bk]){
      if (dist(t, wk) < 2 || att.includes(t)) continue;
      if (t === p){ if (dist(p, wk) > 1) bs.push(DRAW); continue; }
      bs.push(I(wk, p, t));
    }
    bSucc[i] = bs;
    if (!bs.length) B[i] = check ? 0 : -2;
    if (check) continue;
    const ws = [];
    for (const t of KM[wk]) if (t !== p && dist(t, bk) > 1) ws.push(I(t, p, bk));
    const p1 = p + 8;
    if (p1 !== wk && p1 !== bk){
      if (R(p1) === 7){
        // a promotion: a win when the queen (or a rook, where a queen would stalemate) wins from there
        if (Q.B[I(wk, p1, bk)] >= 0 || Rk.B[I(wk, p1, bk)] >= 0) now[i] = 1;
        else ws.push(DRAW);
      } else {
        ws.push(I(wk, p1, bk));
        const p2 = p + 16;
        if (R(p) === 1 && p2 !== wk && p2 !== bk) ws.push(I(wk, p2, bk));
      }
    }
    wSucc[i] = ws;
  }
  solve(W, B, wSucc, bSucc, now);
  return {W, B};
}

function pack({W, B}){
  const out = new Uint8Array(SZ * 2);
  let mx = 0;
  for (let i = 0; i < SZ; i++){
    if (W[i] >= 0){ out[2 * i] = W[i] + 1; mx = Math.max(mx, W[i]); }
    if (B[i] >= 0){ out[2 * i + 1] = B[i] + 1; mx = Math.max(mx, B[i]); }
  }
  if (mx > 254) throw new Error('distance too long for a byte');
  return {bytes: out, max: mx};
}

const t0 = Date.now();
const q = kxk(QUEEN), r = kxk(ROOK), p = kpk(q, r);
const out = {}, meta = {};
for (const [name, t] of [['kqk', q], ['krk', r], ['kpk', p]]){
  const {bytes, max} = pack(t);
  const z = zlib.deflateSync(bytes, {level: 9});
  out[name] = z.toString('base64');
  let wins = 0, lost = 0; for (let i = 0; i < SZ; i++){ if (t.W[i] >= 0) wins++; if (t.B[i] >= 0) lost++; }
  meta[name] = {max, wins, lost, packed: z.length};
  if (process.argv.includes('--raw')) fs.writeFileSync(path.join(ROOT, 'data', 'endings', name + '.bin'), bytes);
}
fs.mkdirSync(path.join(ROOT, 'data', 'endings'), {recursive: true});
fs.writeFileSync(path.join(ROOT, 'data', 'endings', 'tables.json'), JSON.stringify(Object.assign({meta}, out)) + '\n');
console.log(JSON.stringify(meta), ((Date.now() - t0) / 1000).toFixed(1) + 's');
