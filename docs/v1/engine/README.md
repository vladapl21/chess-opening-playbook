# The engine in the app

`stockfish-19-lite-single.js` and `stockfish-19-lite-single.wasm` are the lite, single-threaded build of
[Stockfish.js](https://github.com/nmrugg/stockfish.js) 19.0.1 (release `v19.0.1`), a WebAssembly port of
[Stockfish](https://github.com/official-stockfish/Stockfish). They are unchanged copies of the release files.

The app starts them in a web worker the first time the engine is needed (`new Worker('engine/stockfish-19-lite-single.js')`);
the script loads the `.wasm` from the same folder. The single-threaded build needs no cross-origin isolation, so it
runs on GitHub Pages and other plain static hosts. It does not run from a `file://` page.

Stockfish and Stockfish.js are free software under the GNU General Public License version 3; the full text is in
[`COPYING.txt`](COPYING.txt). Source code: <https://github.com/nmrugg/stockfish.js/tree/v19.0.1> and
<https://github.com/official-stockfish/Stockfish>.

The rest of the app does not link against the engine: it talks to the worker over the UCI text protocol.
