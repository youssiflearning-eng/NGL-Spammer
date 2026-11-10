HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NGL Sender — Anonymous Messages</title>
<meta name="description" content="Send anonymous messages to any NGL.link username instantly.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<style>
  *{-webkit-font-smoothing:antialiased}
  @keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
  @keyframes scaleIn{from{opacity:0;transform:scale(0.98)}to{opacity:1;transform:scale(1)}}
  .fade-up{animation:fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) both}
  .card-shadow{box-shadow:0 1px 2px rgba(15,23,42,0.04),0 8px 24px rgba(15,23,42,0.06),0 20px 40px rgba(15,23,42,0.04)}
  .input-focus:focus{box-shadow:0 0 0 4px rgba(15,23,42,0.06);border-color:#0f172a}
  .btn-hover{transition:all 0.18s cubic-bezier(0.16,1,0.3,1)}
  .btn-hover:hover{transform:translateY(-1px);box-shadow:0 10px 24px rgba(15,23,42,0.18)}
  .btn-hover:active{transform:translateY(0)}
  .num-btn{transition:all 0.12s ease}
  .num-btn:hover{background:#f1f5f9}
  .num-btn:active{transform:scale(0.97)}
</style>
</head>
<body class="bg-[#f8fafc] text-[#0f172a] font-[Inter] min-h-screen flex flex-col">
  <div class="fixed inset-0 -z-10">
    <div class="absolute inset-0 bg-[#f8fafc]"></div>
    <div class="absolute inset-0 opacity-[0.025]" style="background-image:radial-gradient(#0f172a 1px, transparent 1px);background-size:24px 24px"></div>
  </div>

  <header class="w-full max-w-[560px] mx-auto px-4 pt-10 pb-6">
    <div class="flex items-center justify-center gap-2.5 fade-up">
      <div class="w-9 h-9 rounded-xl bg-[#0f172a] flex items-center justify-center">
        <span class="text-white font-extrabold text-[13px] tracking-tight">ngl</span>
      </div>
      <div class="text-[15px] font-bold tracking-tight">NGL Sender</div>
    </div>
  </header>

  <main class="flex-1 w-full max-w-[560px] mx-auto px-4 pb-10">
    <div class="bg-white rounded-[24px] border border-[#e2e8f0] card-shadow overflow-hidden fade-up" style="animation-delay:.06s">
      <div class="px-6 sm:px-8 pt-8 pb-1">
        <h1 class="text-[23px] font-extrabold tracking-[-0.03em]">Send a message</h1>
        <p class="mt-1 text-[13px] text-[#64748b]">To any <b class="font-semibold text-[#334155]">ngl.link</b> profile — 1 to 1000 real messages.</p>
      </div>

      <form id="mainForm" class="px-6 sm:px-8 pt-6 pb-7 space-y-5">
        <div class="space-y-2">
          <label class="text-[11px] font-bold tracking-widest text-[#334155] uppercase">NGL Username</label>
          <div class="relative">
            <div class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[13px] font-medium text-[#94a3b8] pointer-events-none">ngl.link/</div>
            <input id="username" required placeholder="johndoe" class="w-full pl-[84px] pr-3 py-3.5 rounded-xl bg-white border border-[#e2e8f0] text-[14px] font-medium placeholder:text-[#cbd5e1] focus:outline-none input-focus transition">
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-[11px] font-bold tracking-widest text-[#334155] uppercase flex justify-between">Message <span id="charCount" class="font-medium text-[#94a3b8] normal-case tracking-normal">0 / 300</span></label>
          <textarea id="message" required maxlength="300" rows="4" placeholder="Type your message..." class="w-full px-3.5 py-3 rounded-xl bg-white border border-[#e2e8f0] text-[14px] leading-relaxed placeholder:text-[#cbd5e1] focus:outline-none input-focus transition resize-none"></textarea>
        </div>

        <div class="space-y-2">
          <label class="text-[11px] font-bold tracking-widest text-[#334155] uppercase">Amount</label>
          <div class="flex items-center bg-white border border-[#e2e8f0] rounded-xl overflow-hidden focus-within:border-[#0f172a] focus-within:shadow-[0_0_0_4px_rgba(15,23,42,0.06)] transition">
            <button type="button" id="minusBtn" class="num-btn w-12 h-[46px] flex items-center justify-center border-r border-[#e2e8f0] text-[#475569] shrink-0"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3.5 7H10.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
            <input id="amount" type="number" min="1" max="1000" value="25" class="flex-1 h-[46px] text-center text-[15px] font-bold bg-transparent border-0 focus:outline-none">
            <button type="button" id="plusBtn" class="num-btn w-12 h-[46px] flex items-center justify-center border-l border-[#e2e8f0] text-[#475569] shrink-0"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 3.5V10.5M3.5 7H10.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
          </div>
          <div class="flex justify-between text-[11px] font-medium text-[#94a3b8]"><span>1</span><span>100 = 100 real requests to NGL</span><span>1000</span></div>
        </div>

        <button id="sendBtn" type="submit" class="btn-hover w-full h-[48px] rounded-xl bg-[#0f172a] text-white text-[13px] font-bold flex items-center justify-center gap-2">
          <span id="sendLabel">Send messages</span>
          <span id="sendSpinner" class="hidden w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
        </button>

        <div id="progressWrap" class="hidden space-y-2 pt-1">
          <div class="flex justify-between text-[11px] font-medium text-[#64748b]"><span id="progressText">Sending real requests to NGL…</span><span id="progressCount" class="font-mono text-[#0f172a]">0 / 0</span></div>
          <div class="h-1.5 bg-[#f1f5f9] rounded-full overflow-hidden border border-[#e2e8f0]/60"><div id="progressBar" class="h-full bg-[#0f172a] rounded-full transition-all duration-300" style="width:0%"></div></div>
          <div id="liveStats" class="text-[11px] font-medium text-[#64748b]"></div>
        </div>

        <div id="resultCard" class="hidden rounded-2xl border overflow-hidden" style="animation:scaleIn .35s cubic-bezier(0.16,1,0.3,1)">
          <div id="resultContent" class="px-5 py-5 flex items-center gap-4 bg-white"></div>
        </div>
      </form>
    </div>
    <p class="mt-3 text-center text-[11px] text-[#94a3b8]">We count only <b class="text-[#475569]">HTTP 200 from ngl.link</b> — no fake numbers.</p>
  </main>

<script>
const $ = s => document.getElementById(s);
const usernameEl=$('username'), messageEl=$('message'), amountEl=$('amount'), charCount=$('charCount');
const minusBtn=$('minusBtn'), plusBtn=$('plusBtn'), form=$('mainForm'), sendBtn=$('sendBtn'), sendLabel=$('sendLabel'), sendSpinner=$('sendSpinner');
const progressWrap=$('progressWrap'), progressBar=$('progressBar'), progressText=$('progressText'), progressCount=$('progressCount'), liveStats=$('liveStats');
const resultCard=$('resultCard'), resultContent=$('resultContent');

messageEl.addEventListener('input',()=> charCount.textContent = messageEl.value.length + ' / 300');
minusBtn.onclick=()=>{let v=parseInt(amountEl.value||'1',10); if(v>1) amountEl.value=v-1};
plusBtn.onclick=()=>{let v=parseInt(amountEl.value||'1',10); if(v<1000) amountEl.value=v+1};
amountEl.onchange=()=>{let v=parseInt(amountEl.value,10); if(isNaN(v)||v<1) v=1; if(v>1000) v=1000; amountEl.value=v};
let hold=null;
minusBtn.onmousedown=()=> hold=setInterval(()=>{let v=parseInt(amountEl.value,10); if(v>1) amountEl.value=v-1},70);
plusBtn.onmousedown=()=> hold=setInterval(()=>{let v=parseInt(amountEl.value,10); if(v<1000) amountEl.value=v+1},70);
['mouseup','mouseleave','touchend','touchcancel'].forEach(e=>{ minusBtn.addEventListener(e,()=>clearInterval(hold)); plusBtn.addEventListener(e,()=>clearInterval(hold)); });

function setProgress(done,total){ progressBar.style.width=(total?Math.round(done/total*100):0)+'%'; progressCount.textContent=done+' / '+total; }

function showResult(delivered, total){
  resultCard.classList.remove('hidden');
  if(delivered>0){
    const all = delivered===total;
    resultCard.style.borderColor='#bbf7d0';
    resultContent.innerHTML=`
      <div class="w-10 h-10 rounded-full bg-[#f0fdf4] border border-[#bbf7d0] flex items-center justify-center shrink-0"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M4 9L7.5 12.5L14 5.5" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="flex-1">
        <div class="text-[13px] font-bold text-[#065f46]"><span class="text-[22px] font-extrabold">${delivered}</span> ${delivered===1?'message delivered':'messages delivered'}</div>
        <div class="text-[11px] font-medium text-[#047857] mt-0.5">${all? 'All '+total+' sent — every one was a real request to NGL.' : delivered+' of '+total+' delivered. '+(total-delivered)+' blocked by NGL rate-limit.'}</div>
        <div class="text-[10px] font-medium text-[#6ee7b7] mt-1">Real • verified by HTTP 200 from ngl.link/api/submit</div>
      </div>`;
  } else {
    resultCard.style.borderColor='#fecaca';
    resultContent.innerHTML=`
      <div class="w-10 h-10 rounded-full bg-[#fef2f2] border border-[#fecaca] flex items-center justify-center shrink-0"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="#ef4444" stroke-width="1.4"/><path d="M8 5V8" stroke="#ef4444" stroke-width="1.6" stroke-linecap="round"/></svg></div>
      <div class="flex-1"><div class="text-[13px] font-bold text-[#991b1b]">0 delivered</div><div class="text-[11px] font-medium text-[#b91c1c] mt-0.5">NGL blocked all requests — check username or try later.</div></div>`;
  }
}

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const username = usernameEl.value.trim().replace(/^@/,'').replace(/.*ngl\\.link\\//,'').split('/')[0].split('?')[0].trim();
  const message = messageEl.value.trim();
  let amount = parseInt(amountEl.value,10);
  if(!username){ usernameEl.focus(); usernameEl.classList.add('!border-[#ef4444]'); setTimeout(()=>usernameEl.classList.remove('!border-[#ef4444]'),800); return; }
  if(username.length<2||username.length>30){ alert('Username must be 2-30 chars'); return; }
  if(!message){ messageEl.focus(); return; }
  if(isNaN(amount)||amount<1) amount=1; if(amount>1000) amount=1000;

  sendBtn.disabled=true; sendLabel.textContent='Sending…'; sendSpinner.classList.remove('hidden');
  resultCard.classList.add('hidden'); progressWrap.classList.remove('hidden'); setProgress(0,amount); progressText.textContent='Sending real requests to NGL…'; liveStats.textContent='';

  let delivered=0, done=0;
  const CHUNK=20;          // Vercel limit per function call (10s timeout)
  const DELAY=0.15;        // tiny delay inside each chunk -> faster + avoids instant 429
  const CONCURRENCY=4;     // parallel chunks -> 100 messages = 5 chunks in 2 batches = fast

  async function sendChunk(sz){
    const r = await fetch('/api/send', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ username, message, count: sz, delay: DELAY })
    });
    const data = await r.json();
    if(!data || !data.success) return { ok:0, total:sz, results:data?.results||[] };
    const ok = (data.results||[]).filter(x=>x.success).length;
    return { ok, total: (data.results||[]).length || sz, results: data.results||[] };
  }

  const chunks=[];
  for(let o=0;o<amount;o+=CHUNK) chunks.push(Math.min(CHUNK, amount-o));

  for(let i=0;i<chunks.length;i+=CONCURRENCY){
    const batch = chunks.slice(i, i+CONCURRENCY);
    const results = await Promise.all(batch.map(s=>sendChunk(s)));
    for(const r of results){ delivered += r.ok; done += r.total; }
    setProgress(done, amount);
    progressText.textContent = delivered + ' delivered of ' + done + ' tried…';
    liveStats.textContent = done < amount ? (amount-done)+' remaining — all real NGL requests' : delivered===amount ? 'Done — 100% real' : delivered+' real • '+(done-delivered)+' rate-limited';
    // tiny pause between batches to let NGL breathe -> more real successes
    if(i+CONCURRENCY < chunks.length) await new Promise(x=>setTimeout(x, 350));
  }

  sendBtn.disabled=false; sendLabel.textContent='Send messages'; sendSpinner.classList.add('hidden'); progressWrap.classList.add('hidden');
  showResult(delivered, amount);
});
</script>
</body>
</html>

"""
