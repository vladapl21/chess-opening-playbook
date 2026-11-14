/* A stand-in for supabase-js in the browser tests. It exposes the same calls the app uses
   (auth.signUp, signInWithPassword, signOut, resetPasswordForEmail, updateUser, onAuthStateChange,
   from(table).select().eq().maybeSingle(), from(table).upsert()) and sends each one to a fake server
   that the Playwright test runs, so two browser contexts behave like two devices on one account. */
(function(){
  function createClient(url, key){
    const SKEY = 'fake-sb-session', listeners = [];
    let session = null;
    try { session = JSON.parse(localStorage.getItem(SKEY) || 'null'); } catch(e){}
    const emit = ev => listeners.slice().forEach(cb => { try { cb(ev, session); } catch(e){ console.error(e); } });
    const keep = s => { session = s; try { s ? localStorage.setItem(SKEY, JSON.stringify(s)) : localStorage.removeItem(SKEY); } catch(e){} };
    async function call(path, body){
      const r = await fetch(url + '/__fake/' + path, {method: 'POST', headers: {'content-type': 'application/json', apikey: key},
        body: JSON.stringify(Object.assign({token: session && session.access_token}, body || {}))});
      return r.json();
    }
    // like the real client: a ?code=… link from an email is exchanged for a session first, and every new
    // subscriber then gets INITIAL_SESSION once initialisation is done
    const ready = (async () => {
      const q = new URLSearchParams(location.search);
      if (q.has('code')){ const r = await call('exchange', {code: q.get('code')}); if (r.session) keep(r.session); }
    })();
    const auth = {
      onAuthStateChange(cb){
        listeners.push(cb); ready.then(() => { try { cb('INITIAL_SESSION', session); } catch(e){ console.error(e); } });
        return {data: {subscription: {unsubscribe(){ const i = listeners.indexOf(cb); if (i >= 0) listeners.splice(i, 1); }}}};
      },
      async getSession(){ await ready; return {data: {session}, error: null}; },
      async signUp({email, password, options}){
        const r = await call('signup', {email, password, redirect: options && options.emailRedirectTo, data: (options && options.data) || {}});
        if (r.error) return {data: {user: null, session: null}, error: r.error};
        if (r.session){ keep(r.session); emit('SIGNED_IN'); }
        return {data: {user: r.user, session: r.session || null}, error: null};
      },
      async signInWithPassword({email, password}){
        const r = await call('signin', {email, password});
        if (r.error) return {data: {user: null, session: null}, error: r.error};
        keep(r.session); emit('SIGNED_IN');
        return {data: {user: r.session.user, session: r.session}, error: null};
      },
      async signOut(){ keep(null); emit('SIGNED_OUT'); return {error: null}; },
      async resetPasswordForEmail(email, o){ const r = await call('reset', {email, redirect: o && o.redirectTo}); return {data: {}, error: r.error || null}; },
      async updateUser({password}){ const r = await call('update', {password}); if (r.error) return {data: {user: null}, error: r.error}; emit('USER_UPDATED'); return {data: {user: session && session.user}, error: null}; }
    };
    function from(table){
      return {
        select(cols){
          const q = {table, cols, filters: {}};
          const b = {eq(c, v){ q.filters[c] = v; return b; }, async maybeSingle(){ const r = await call('select', q); return {data: r.row || null, error: r.error || null}; }};
          return b;
        },
        async upsert(row){ const r = await call('upsert', {table, row}); return {data: null, error: r.error || null}; }
      };
    }
    return {auth, from};
  }
  window.supabase = {createClient};
})();
