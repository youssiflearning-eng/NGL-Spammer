HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NGL Sender — Anonymous Messages via Web</title>
<meta name="description" content="Send anonymous messages to any NGL.link username directly from your browser. Python-powered, fast and simple.">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Geist:wght@500;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      fontFamily: { sans: ['Inter','sans-serif'] },
    }
  }
}
</script>
<style>
  * { -webkit-font-smoothing: antialiased; }
  @keyframes fadeUp { from { opacity:0; transform: translateY(12px)} to {opacity:1; transform:translateY(0)} }
  @keyframes fadeIn { from {opacity:0} to {opacity:1} }
  @keyframes scaleIn { from {opacity:0; transform: scale(0.96)} to {opacity:1; transform:scale(1)} }
  @keyframes shimmer { 0% { background-position: -200% 0 } 100% { background-position: 200% 0 } }
  @keyframes pulseDot { 0%,100% { opacity:1 } 50% { opacity:0.4 } }
  @keyframes checkDraw { from { stroke-dashoffset: 24 } to { stroke-dashoffset: 0 } }
  .fade-up { animation: fadeUp 0.6s cubic-bezier(0.16,1,0.3,1) forwards; }
  .fade-up-delay-1 { animation: fadeUp 0.6s 0.08s cubic-bezier(0.16,1,0.3,1) both; }
  .fade-up-delay-2 { animation: fadeUp 0.6s 0.16s cubic-bezier(0.16,1,0.3,1) both; }
  .card-shadow { box-shadow: 0 1px 2px rgba(16,24,40,0.06), 0 8px 24px rgba(16,24,40,0.06), 0 24px 48px rgba(16,24,40,0.04); }
  .input-focus:focus { box-shadow: 0 0 0 4px rgba(17,24,39,0.06); border-color: #111827; }
  .input-error { border-color: #ef4444 !important; box-shadow: 0 0 0 4px rgba(239,68,68,0.08) !important; }
  .btn-hover { transition: all 0.2s cubic-bezier(0.16,1,0.3,1); }
  .btn-hover:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(17,24,39,0.18); }
  .btn-hover:active { transform: translateY(0); }
  .number-btn { transition: all 0.15s ease; }
  .number-btn:hover { background: #f1f5f9; }
  .number-btn:active { transform: scale(0.96); }
  .shimmer { background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 37%, #f1f5f9 63%); background-size: 400% 100%; animation: shimmer 1.2s ease infinite; }
  .custom-scrollbar::-webkit-scrollbar { width:4px; height:4px; }
  .custom-scrollbar::-webkit-scrollbar-thumb { background:#e2e8f0; border-radius:10px; }
</style>
</head>
<body class="bg-[#f8fafc] text-[#0f172a] font-sans min-h-screen flex flex-col">
  <!-- Subtle background pattern -->
  <div class="fixed inset-0 -z-10 pointer-events-none">
    <div class="absolute inset-0 bg-[#f8fafc]"></div>
    <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(#0f172a 1px, transparent 1px); background-size: 24px 24px;"></div>
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-b from-[#e2e8f0]/40 to-transparent rounded-full blur-3xl"></div>
  </div>

  <!-- Header -->
  <header class="w-full max-w-[720px] mx-auto px-4 sm:px-6 pt-8 pb-4">
    <div class="flex items-center justify-between fade-up">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-[#0f172a] flex items-center justify-center">
          <span class="text-white font-extrabold text-[13px] tracking-tight">ngl</span>
        </div>
        <div>
          <div class="text-[14px] font-bold tracking-tight leading-none">NGL Sender</div>
          <div class="text-[11px] font-medium tracking-widest text-[#64748b] uppercase">Python • Vercel</div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span id="apiDot" class="w-2 h-2 rounded-full bg-[#e2e8f0]"></span>
        <span id="apiStatus" class="text-[11px] font-semibold tracking-wide text-[#64748b] uppercase">Checking</span>
        <a href="https://github.com/youssiflearning-eng/NGL-Spammer" target="_blank" class="hidden sm:inline-flex ml-2 px-3 py-1.5 rounded-full bg-white border border-[#e2e8f0] text-[11px] font-semibold hover:bg-[#f8fafc] transition">GitHub ↗</a>
      </div>
    </div>
  </header>

  <!-- Main Single Page Card -->
  <main class="flex-1 w-full max-w-[720px] mx-auto px-4 sm:px-6 pb-12">
    <div class="bg-white rounded-[24px] border border-[#e2e8f0] card-shadow overflow-hidden fade-up-delay-1">
      <!-- Card header -->
      <div class="px-6 sm:px-8 pt-8 pb-6">
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-[#f1f5f9] border border-[#e2e8f0]">
          <span class="w-1.5 h-1.5 rounded-full bg-[#10b981] animate-[pulseDot_2s_ease_infinite]"></span>
          <span class="text-[10px] font-bold tracking-widest text-[#475569] uppercase">Live • Python Backend</span>
        </div>
        <h1 class="mt-4 text-[26px] sm:text-[28px] font-[800] tracking-[-0.03em] leading-[1.1]">Send anonymous<br>message</h1>
        <p class="mt-2 text-[13px] leading-relaxed text-[#64748b] max-w-[420px]">Enter the NGL username, your message, and how many times to send. Powered by Python on Vercel — works on any device.</p>
      </div>

      <!-- Form -->
      <form id="mainForm" class="px-6 sm:px-8 pb-8 space-y-5">
        <!-- Username -->
        <div class="space-y-2">
          <label class="text-[11px] font-bold tracking-widest text-[#334155] uppercase">NGL Username <span class="text-[#ef4444]">*</span></label>
          <div class="relative group">
            <div class="absolute left-3.5 top-1/2 -translate-y-1/2 flex items-center gap-2 pointer-events-none">
              <span class="text-[12px] font-medium text-[#94a3b8]">ngl.link/</span>
            </div>
            <input id="username" required autocomplete="off" placeholder="johndoe" class="w-full pl-[82px] pr-10 py-3.5 rounded-xl bg-white border border-[#e2e8f0] text-[14px] font-medium placeholder:text-[#cbd5e1] focus:outline-none input-focus transition">
            <div id="userCheck" class="absolute right-3 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-[#f0fdf4] border border-[#bbf7d0] hidden items-center justify-center">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2.5 6L4.8 8.5L9.5 3.5" stroke="#10b981" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
          </div>
          <p class="text-[11px] text-[#94a3b8]">Example: <span class="font-mono text-[#475569] bg-[#f8fafc] border border-[#e2e8f0] px-1 py-0.5 rounded">ngl.link/johndoe</span> → type <span class="font-medium text-[#0f172a]">johndoe</span> only</p>
        </div>

        <!-- Message -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-[11px] font-bold tracking-widest text-[#334155] uppercase">Message <span class="text-[#ef4444]">*</span></label>
            <span id="charCount" class="text-[11px] font-medium font-mono text-[#94a3b8]">0 / 300</span>
          </div>
          <div class="relative">
            <textarea id="message" required maxlength="300" rows="4" placeholder="Write your anonymous message here..." class="w-full px-3.5 py-3 rounded-xl bg-white border border-[#e2e8f0] text-[14px] font-[450] leading-relaxed placeholder:text-[#cbd5e1] focus:outline-none input-focus transition resize-none"></textarea>
          </div>
          <div class="flex gap-1.5 flex-wrap">
            <button type="button" data-quick="Hey! How are you? 😊" class="quick-btn px-3 py-1 rounded-full bg-[#f8fafc] hover:bg-[#f1f5f9] border border-[#e2e8f0] text-[11px] font-medium transition">Hey! How are you? 😊</button>
            <button type="button" data-quick="You inspire me! Keep going 💙" class="quick-btn px-3 py-1 rounded-full bg-[#f8fafc] hover:bg-[#f1f5f9] border border-[#e2e8f0] text-[11px] font-medium transition">You inspire me 💙</button>
            <button type="button" data-quick="Confession: I like you 👀" class="quick-btn px-3 py-1 rounded-full bg-[#f8fafc] hover:bg-[#f1f5f9] border border-[#e2e8f0] text-[11px] font-medium transition">Confession 👀</button>
          </div>
        </div>

        <!-- Amount -->
        <div class="space-y-2">
          <label class="text-[11px] font-bold tracking-widest text-[#334155] uppercase">Amount <span class="text-[#ef4444]">*</span></label>
          <div class="flex items-center gap-3">
            <div class="flex-1 relative flex items-center bg-white border border-[#e2e8f0] rounded-xl overflow-hidden focus-within:border-[#0f172a] focus-within:shadow-[0_0_0_4px_rgba(15,23,42,0.06)] transition">
              <button type="button" id="minusBtn" class="number-btn w-11 h-[46px] flex items-center justify-center border-r border-[#e2e8f0] text-[#475569]">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7H11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              </button>
              <input id="amount" type="number" min="1" max="100" value="5" class="flex-1 h-[46px] text-center text-[15px] font-bold bg-transparent border-0 focus:outline-none focus:ring-0">
              <button type="button" id="plusBtn" class="number-btn w-11 h-[46px] flex items-center justify-center border-l border-[#e2e8f0] text-[#475569]">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 3V11M3 7H11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="hidden sm:flex items-center gap-1.5 text-[11px] font-medium text-[#94a3b8]">
              <span class="px-2 py-1 rounded-full bg-[#f1f5f9] border border-[#e2e8f0]">1</span>
              <span>—</span>
              <span class="px-2 py-1 rounded-full bg-[#f1f5f9] border border-[#e2e8f0]">100</span>
            </div>
          </div>
          <p class="text-[11px] text-[#94a3b8]">We’ll batch automatically to stay within Vercel limits.</p>
        </div>

        <!-- Consent -->
        <label class="flex items-start gap-3 p-3 rounded-xl bg-[#f8fafc] border border-[#e2e8f0] cursor-pointer hover:bg-[#f1f5f9] transition group">
          <input type="checkbox" id="consent" class="mt-0.5 w-4 h-4 rounded border-[#cbd5e1] text-[#0f172a] focus:ring-0 focus:ring-offset-0">
          <span class="text-[11px] leading-relaxed text-[#475569] group-hover:text-[#334155]">I have permission to message this user and will use this responsibly. I understand NGL may limit after many messages.</span>
        </label>

        <!-- Action -->
        <button id="sendBtn" type="submit" class="btn-hover w-full h-[48px] rounded-xl bg-[#0f172a] text-white text-[13px] font-bold tracking-wide flex items-center justify-center gap-2 hover:bg-black disabled:opacity-40 disabled:cursor-not-allowed">
          <span id="sendLabel">Send messages</span>
          <svg id="sendArrow" width="14" height="14" viewBox="0 0 14 14" fill="none" class="opacity-70"><path d="M5 3L9 7L5 11" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span id="sendSpinner" class="hidden w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
        </button>

        <!-- Result - only success count -->
        <div id="resultCard" class="hidden rounded-2xl border overflow-hidden">
          <div id="resultContent" class="px-5 py-5 flex items-center gap-4">
            <!-- injected via JS -->
          </div>
          <div id="resultMeta" class="px-5 py-3 bg-[#f8fafc] border-t border-[#e2e8f0] flex items-center justify-between text-[11px] font-medium text-[#64748b]">
            <span id="resultSub"></span>
            <button type="button" id="resetBtn" class="px-3 py-1 rounded-full bg-white border border-[#e2e8f0] text-[#0f172a] font-semibold hover:bg-[#f8fafc] transition">Send again</button>
          </div>
        </div>

        <!-- Minimal progress (thin bar) -->
        <div id="progressWrap" class="hidden space-y-2">
          <div class="flex items-center justify-between text-[11px] font-medium">
            <span class="text-[#475569]"><span id="progressText">Sending…</span> <span id="progressCount" class="font-mono text-[#0f172a]">0 / 0</span></span>
            <span id="progressPct" class="font-mono text-[#94a3b8]">0%</span>
          </div>
          <div class="h-1.5 bg-[#f1f5f9] rounded-full overflow-hidden border border-[#e2e8f0]/60">
            <div id="progressBar" class="h-full bg-[#0f172a] rounded-full transition-all duration-300" style="width:0%"></div>
          </div>
        </div>
      </form>

      <!-- Card footer -->
      <div class="px-6 sm:px-8 py-4 bg-[#f8fafc] border-t border-[#e2e8f0] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
        <div class="flex items-center gap-2 text-[11px] text-[#94a3b8]">
          <span class="w-2 h-2 rounded-full bg-[#10b981]"></span>
          <span class="font-medium">Python backend on Vercel</span>
          <span class="hidden sm:inline">•</span>
          <span>For educational use</span>
        </div>
        <div class="flex items-center gap-2">
          <a href="https://ngl.link" target="_blank" class="text-[11px] font-semibold text-[#334155] hover:text-[#0f172a]">ngl.link ↗</a>
          <span class="text-[#e2e8f0]">|</span>
          <button type="button" onclick="copyLink()" class="text-[11px] font-semibold text-[#334155] hover:text-[#0f172a]">Copy link</button>
        </div>
      </div>
    </div>

    <!-- Tiny trust row (still single page, but adds pro feel) -->
    <div class="mt-4 flex items-center justify-center gap-4 sm:gap-6 fade-up-delay-2">
      <span class="inline-flex items-center gap-1.5 text-[11px] font-medium text-[#94a3b8]"><span class="w-3.5 h-3.5 rounded-full bg-white border border-[#e2e8f0] flex items-center justify-center text-[10px]">✓</span> No login</span>
      <span class="inline-flex items-center gap-1.5 text-[11px] font-medium text-[#94a3b8]"><span class="w-3.5 h-3.5 rounded-full bg-white border border-[#e2e8f0] flex items-center justify-center text-[10px]">✓</span> Mobile ready</span>
      <span class="inline-flex items-center gap-1.5 text-[11px] font-medium text-[#94a3b8]"><span class="w-3.5 h-3.5 rounded-full bg-white border border-[#e2e8f0] flex items-center justify-center text-[10px]">✓</span> Google indexed</span>
    </div>
  </main>

  <footer class="mt-auto py-6 text-center">
    <p class="text-[11px] font-medium text-[#94a3b8]">© 2026 NGL Sender • Built with Python • <a href="https://github.com/youssiflearning-eng/NGL-Spammer" class="underline hover:text-[#475569]">GitHub</a> • Deployed on Vercel ▲</p>
  </footer>

<script>
  const usernameEl = document.getElementById('username');
  const messageEl = document.getElementById('message');
  const amountEl = document.getElementById('amount');
  const charCount = document.getElementById('charCount');
  const minusBtn = document.getElementById('minusBtn');
  const plusBtn = document.getElementById('plusBtn');
  const form = document.getElementById('mainForm');
  const sendBtn = document.getElementById('sendBtn');
  const sendLabel = document.getElementById('sendLabel');
  const sendArrow = document.getElementById('sendArrow');
  const sendSpinner = document.getElementById('sendSpinner');
  const resultCard = document.getElementById('resultCard');
  const resultContent = document.getElementById('resultContent');
  const resultSub = document.getElementById('resultSub');
  const resetBtn = document.getElementById('resetBtn');
  const progressWrap = document.getElementById('progressWrap');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const progressCount = document.getElementById('progressCount');
  const progressPct = document.getElementById('progressPct');
  const apiDot = document.getElementById('apiDot');
  const apiStatus = document.getElementById('apiStatus');
  const userCheck = document.getElementById('userCheck');

  // Char count
  messageEl.addEventListener('input', () => {
    charCount.textContent = messageEl.value.length + ' / 300';
    charCount.className = messageEl.value.length > 280 ? 'text-[11px] font-medium font-mono text-[#ef4444]' : 'text-[11px] font-medium font-mono text-[#94a3b8]';
  });
  // Quick messages
  document.querySelectorAll('.quick-btn').forEach(b => b.addEventListener('click', () => {
    messageEl.value = b.dataset.quick;
    messageEl.dispatchEvent(new Event('input'));
    messageEl.focus();
  }));
  // Amount stepper
  minusBtn.addEventListener('click', () => {
    let v = parseInt(amountEl.value||'1',10);
    if (v > 1) amountEl.value = v - 1;
  });
  plusBtn.addEventListener('click', () => {
    let v = parseInt(amountEl.value||'1',10);
    if (v < 100) amountEl.value = v + 1;
  });
  amountEl.addEventListener('change', () => {
    let v = parseInt(amountEl.value,10);
    if (isNaN(v) || v < 1) v = 1;
    if (v > 100) v = 100;
    amountEl.value = v;
  });
  // Username validation UI
  usernameEl.addEventListener('input', () => {
    const v = usernameEl.value.trim().replace(/^@/,'').replace(/.*ngl\\.link\\//,'').replace('/','');
    if (v.length >= 2) { userCheck.classList.remove('hidden'); userCheck.classList.add('flex'); } else { userCheck.classList.add('hidden'); userCheck.classList.remove('flex'); }
  });
  function copyLink(){ navigator.clipboard.writeText(location.href); apiStatus.textContent='Link copied'; setTimeout(()=>checkHealth(),1200); }
  window.copyLink = copyLink;

  // Health check
  async function checkHealth(){
    try{
      const r = await fetch('/api/health', {cache:'no-store'});
      const j = await r.json();
      if(j.status==='ok'){ apiDot.className='w-2 h-2 rounded-full bg-[#10b981]'; apiStatus.textContent='API online'; apiStatus.className='text-[11px] font-semibold tracking-wide text-[#059669] uppercase'; }
      else throw new Error();
    }catch{ apiDot.className='w-2 h-2 rounded-full bg-[#f59e0b]'; apiStatus.textContent='API offline'; }
  }
  checkHealth(); setInterval(checkHealth,30000);

  function setProgress(done,total){
    const pct = total ? Math.round(done/total*100) : 0;
    progressBar.style.width = pct+'%';
    progressPct.textContent = pct+'%';
    progressCount.textContent = done+' / '+total;
  }

  function showResult(successCount, total){
    resultCard.className = 'rounded-2xl border overflow-hidden fade-up';
    if(successCount>0){
      resultCard.style.borderColor = '#bbf7d0';
      resultContent.innerHTML = `
        <div class="w-10 h-10 rounded-full bg-[#f0fdf4] border border-[#bbf7d0] flex items-center justify-center shrink-0">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M4 9L7.5 12.5L14 5.5" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <div class="flex-1">
          <div class="text-[13px] font-bold tracking-tight text-[#065f46]"><span class="text-[22px] font-extrabold tracking-tight text-[#065f46]">${successCount}</span> <span class="ml-1 font-bold">messages delivered</span></div>
          <div class="text-[11px] font-medium text-[#047857] mt-0.5">Real successful sends via Python — NGL confirmed</div>
        </div>
        <div class="hidden sm:flex w-10 h-10 rounded-full bg-[#10b981] items-center justify-center text-white font-bold text-[14px]">✓</div>
      `;
      resultContent.parentElement?.classList?.remove('hidden');
      resultCard.querySelector('#resultContent').parentElement; // no-op
      resultSub.textContent = successCount === total ? 'All requested messages were delivered.' : successCount + ' of ' + total + ' requested — some were rate-limited. Try again with same message.';
      resultCard.classList.remove('hidden');
      // subtle celebration: button pulse
      sendBtn.classList.add('ring-4','ring-[#10b981]/10');
      setTimeout(()=>sendBtn.classList.remove('ring-4','ring-[#10b981]/10'),600);
    } else {
      resultCard.style.borderColor = '#fecaca';
      resultContent.innerHTML = `
        <div class="w-10 h-10 rounded-full bg-[#fef2f2] border border-[#fecaca] flex items-center justify-center shrink-0">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 5V9M9 11.5V11.5" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/><circle cx="9" cy="9" r="6.5" stroke="#ef4444" stroke-width="1.4"/></svg>
        </div>
        <div class="flex-1">
          <div class="text-[13px] font-bold text-[#991b1b]">No messages delivered</div>
          <div class="text-[11px] font-medium text-[#b91c1c] mt-0.5">Check username or NGL rate-limit. Try delay via smaller batches.</div>
        </div>
      `;
      resultSub.textContent = '0 of '+total+' delivered — verify the NGL username exists.';
      resultCard.classList.remove('hidden');
    }
    resultCard.scrollIntoView({behavior:'smooth', block:'nearest'});
  }

  resetBtn.addEventListener('click', ()=>{ resultCard.classList.add('hidden'); progressWrap.classList.add('hidden'); });

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const username = usernameEl.value.trim().replace(/^@/,'').replace(/.*ngl\\.link\\//,'').split('/')[0].split('?')[0];
    const message = messageEl.value.trim();
    const amount = parseInt(amountEl.value,10);
    const consent = document.getElementById('consent').checked;

    // Validation with light error styles
    [usernameEl, messageEl].forEach(el=>el.classList.remove('input-error'));
    if(!username){ usernameEl.classList.add('input-error'); usernameEl.focus(); return; }
    if(username.length<2||username.length>30){ usernameEl.classList.add('input-error'); alert('Invalid username (2-30 chars)'); return; }
    if(!message){ messageEl.classList.add('input-error'); messageEl.focus(); return; }
    if(!consent){ alert('Please confirm you have permission.'); return; }
    if(amount<1||amount>100){ alert('Amount must be 1-100'); return; }

    // UI lock
    sendBtn.disabled = true;
    sendLabel.textContent = 'Sending…';
    sendArrow.classList.add('hidden');
    sendSpinner.classList.remove('hidden');
    resultCard.classList.add('hidden');
    progressWrap.classList.remove('hidden');
    progressText.textContent = 'Sending…';
    setProgress(0, amount);

    let totalSent = 0;
    const CHUNK = 10; // Vercel limit 20, we use 10 for safety
    const delay = 0.4; // hidden default to avoid rate-limit

    for(let offset=0; offset<amount; ){
      const chunkSize = Math.min(CHUNK, amount - offset);
      try{
        const res = await fetch('/api/send', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ username, message, count: chunkSize, delay })
        });
        const data = await res.json();
        if(!res.ok || !data.success){
          // count as failed but continue
          offset += chunkSize;
          setProgress(offset, amount);
          continue;
        }
        // Count real successes only
        const successes = (data.results||[]).filter(r=>r.success).length;
        totalSent += successes;
        offset += chunkSize;
        setProgress(offset, amount);
        progressText.textContent = 'Sent '+totalSent+' delivered…';
        // small breather between chunks to be kind to NGL
        if(offset < amount) await new Promise(r=>setTimeout(r, 400));
      }catch(err){
        offset += chunkSize;
        setProgress(offset, amount);
      }
    }

    // Done
    sendBtn.disabled = false;
    sendLabel.textContent = 'Send messages';
    sendArrow.classList.remove('hidden');
    sendSpinner.classList.add('hidden');
    progressWrap.classList.add('hidden');
    showResult(totalSent, amount);
  });
</script>
</body>
</html>

"""
