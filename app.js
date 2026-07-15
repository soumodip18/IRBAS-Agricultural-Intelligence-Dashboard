/* ── TAB SWITCHING ── */
  const R = {
    kartik:{
      file:'india_crop_water_resource_dashboard.pbix',
      url:'https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/raw/main/dashboard/india_crop_water_resource_dashboard-kartik.pbix',
      thumb:'https://raw.githubusercontent.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/main/thumbnails/kartik_thumb.png',
      title:'Crop Water \u0026 Resource Dashboard',
      desc:'28 states \u00b7 Irrigation risk \u00b7 Water footprint \u00b7 Crop season calendar'
    },
    malvika:{
      file:'executive_commodity_analysis.pbix',
      url:'https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/raw/main/dashboard/executive_commodity_analysis-malvika.pbix',
      thumb:'https://raw.githubusercontent.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/main/thumbnails/malvika_thumb.png',
      title:'Executive Commodity Analysis',
      desc:'State-level market intelligence \u00b7 Commodity price trends \u00b7 Region comparison'
    },
    lavanya:{
      file:'commodity_price_intelligence_dashboard.pbix',
      url:'https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/raw/main/dashboard/commodity_price_intelligence_dashboard-lavanya.pbix',
      thumb:'https://raw.githubusercontent.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/main/thumbnails/lavanya_thumb.png',
      title:'Commodity Price Intelligence',
      desc:'Mandi price analytics \u00b7 District-level breakdown \u00b7 Arrival volume trends'
    }
  };
  function pick(btn,key){
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
    btn.classList.add('on');
    const d = R[key];
    document.getElementById('scr-file').textContent  = d.file;
    document.getElementById('scr-open').dataset.url  = d.url;
    document.getElementById('scr-bg').style.backgroundImage = 'url(\''+d.thumb+'\')';
    document.getElementById('scr-title').textContent = d.title;
    document.getElementById('scr-desc').textContent  = d.desc;
  }

  /* ── DISCLAIMER POPUP ── */
  var SHEETS_URL  = 'https://script.google.com/macros/s/AKfycbymvpoiQ7NR59bx6Ft7pd5pRymfn5waEPuyNaDcGiIV73F7m4gsn6NP5QE4GRml0VVx/exec';
  var SUBMIT_TOKEN = 'irbas-2026-mulbiotech';

  /* ── ANTI-FLOOD: rate limit submissions to 1 per 30s per session ── */
  var _lastSubmit = 0;
  var _submitCount = 0;
  var RATE_LIMIT_MS = 30000;
  var MAX_SUBMITS   = 5;

  function isRateLimited(){
    var now = Date.now();
    if(_submitCount >= MAX_SUBMITS) return true;
    if(now - _lastSubmit < RATE_LIMIT_MS) return true;
    return false;
  }

  function showDisclaimer(url){
    document.getElementById('disc-url').dataset.href = url;
    // clear previous inputs and errors
    ['disc-name','disc-email','disc-org','disc-phone'].forEach(function(id){ document.getElementById(id).value=''; });
    document.getElementById('disc-err').style.display='none';
    document.getElementById('disc-overlay').classList.add('open');
  }
  function closeDisclaimer(){ document.getElementById('disc-overlay').classList.remove('open'); }

  /* #6 — URL allowlist */
  var ALLOWED_ORIGINS = [
    'https://github.com/soumodip18/',
    'https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard/raw/'
  ];
  function isSafeUrl(url){
    try {
      var u = new URL(url);
      if(u.protocol !== 'https:') return false;
      return ALLOWED_ORIGINS.some(function(o){ return url.startsWith(o); });
    } catch(e){ return false; }
  }

  function proceedDownload(){
    var name  = document.getElementById('disc-name').value.trim();
    var email = document.getElementById('disc-email').value.trim();
    var org   = document.getElementById('disc-org').value.trim();
    var phone = document.getElementById('disc-phone').value.trim();
    var url   = document.getElementById('disc-url').dataset.href;
    var errEl = document.getElementById('disc-err');

    /* #8 — email regex validation */
    var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
    if(!name || !email || !emailOk){
      errEl.textContent = (!name || !email)
        ? 'Please enter your name and email to continue.'
        : 'Please enter a valid email address.';
      errEl.style.display='block';
      return;
    }
    errEl.style.display='none';

    /* #6 — allowlist check */
    if(!isSafeUrl(url)){
      errEl.textContent = 'Blocked: destination URL is not permitted.';
      errEl.style.display='block';
      return;
    }

    /* honeypot check — bots fill the hidden field, humans don't */
    if(document.getElementById('disc-trap').value !== ''){
      closeDisclaimer();
      return;
    }

    /* rate limit check */
    if(isRateLimited()){
      errEl.textContent = 'Too many requests. Please wait a moment before continuing.';
      errEl.style.display='block';
      return;
    }
    _lastSubmit = Date.now();
    _submitCount++;

    var btn = document.getElementById('disc-url');
    btn.textContent = 'Logging access…';
    btn.disabled = true;

    var payload = new FormData();
    payload.append('name',  name);
    payload.append('email', email);
    payload.append('org',   org);
    payload.append('phone', phone);
    payload.append('file',  url);
    payload.append('time',  new Date().toISOString());
    payload.append('token', SUBMIT_TOKEN);

    fetch(SHEETS_URL, { method:'POST', body:payload, mode:'no-cors' })
      .catch(function(){})
      .finally(function(){
        btn.textContent = 'I agree · Continue ↗';
        btn.disabled = false;
        closeDisclaimer();
        window.open(url,'_blank','noopener');
      });
  }

  function showRepoDisclaimer(e){
    e.preventDefault();
    showDisclaimer('https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard');
  }

  /* ── HAMBURGER ── */
  function toggleMenu(){
    document.getElementById('hbg').classList.toggle('open');
    document.getElementById('mob-menu').classList.toggle('open');
  }
  function closeMenu(){
    document.getElementById('hbg').classList.remove('open');
    document.getElementById('mob-menu').classList.remove('open');
  }
  document.addEventListener('click', e=>{
    const hbg=document.getElementById('hbg'), menu=document.getElementById('mob-menu');
    if(hbg&&menu&&!hbg.contains(e.target)&&!menu.contains(e.target)) closeMenu();
  });

  /* ── PARTICLES ── */
  (function spawnParticles(){
    const field = document.getElementById('particles');
    if(!field) return;
    for(let i=0;i<22;i++){
      const p = document.createElement('div');
      p.className = 'particle';
      p.style.cssText = `
        left:${Math.random()*100}%;
        bottom:${Math.random()*30}%;
        width:${1+Math.random()*2.5}px;
        height:${1+Math.random()*2.5}px;
        animation-delay:${Math.random()*8}s;
        animation-duration:${6+Math.random()*6}s;
        opacity:${.2+Math.random()*.5}
      `;
      field.appendChild(p);
    }
  })();

  /* ── NUMBER COUNTER ── */
  function animateCounter(el){
    const target = parseInt(el.dataset.target,10);
    const suffix = el.dataset.suffix||'';
    const isLarge = target >= 1000;
    const duration = 1200;
    const start = performance.now();
    function step(now){
      const p = Math.min((now-start)/duration,1);
      // ease-out
      const ease = 1-Math.pow(1-p,3);
      const val = Math.round(ease*target);
      el.textContent = isLarge
        ? (val/1000).toFixed(0)+'K+'
        : val.toLocaleString()+suffix;
      if(p<1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ── INTERSECTION OBSERVER — fires at 20% depth, 60px bottom margin ── */
  const obs = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      if(!entry.isIntersecting) return;
      const el = entry.target;

      // standard reveal classes
      if(el.classList.contains('reveal')||
         el.classList.contains('reveal-left')||
         el.classList.contains('reveal-right')||
         el.classList.contains('stagger')){
        el.classList.add('visible');
      }

      // clip lines inside this element
      el.querySelectorAll('.clip-line').forEach(c=>c.classList.add('visible'));

      // line-draw inside this element
      el.querySelectorAll('.line-draw').forEach(l=>l.classList.add('visible'));

      // fade-blur inside this element
      el.querySelectorAll('.fade-blur').forEach(f=>f.classList.add('visible'));

      // counters
      el.querySelectorAll('.count-num').forEach(c=>animateCounter(c));

      obs.unobserve(el);
    });
  },{
    threshold: 0.2,           // element must be 20% visible — fires LATER
    rootMargin: '0px 0px -80px 0px'  // extra 80px buffer from bottom edge
  });

  // observe everything
  document.querySelectorAll(
    '.reveal,.reveal-left,.reveal-right,.stagger,.stamp'
  ).forEach(el=>obs.observe(el));

  // also observe sec-head elements for their child animations
  document.querySelectorAll('.sec-head').forEach(el=>obs.observe(el));

  /* ── EVENT DELEGATION (replaces inline onclick) ── */
  document.addEventListener('DOMContentLoaded', function(){

    // Hamburger
    var hbg = document.getElementById('hbg');
    if(hbg) hbg.addEventListener('click', toggleMenu);

    // Mobile nav close
    document.querySelectorAll('#mob-menu a').forEach(function(a){
      a.addEventListener('click', closeMenu);
    });

    // Dashboard tabs
    document.querySelectorAll('.tab[data-key]').forEach(function(btn){
      btn.addEventListener('click', function(){ pick(this, this.dataset.key); });
    });

    // Screen body click → download button
    var scrBody = document.getElementById('scr-body');
    if(scrBody) scrBody.addEventListener('click', function(){
      var btn = document.getElementById('scr-open');
      if(btn) btn.click();
    });

    // scr-open download button
    var scrOpen = document.getElementById('scr-open');
    if(scrOpen) scrOpen.addEventListener('click', function(e){
      e.preventDefault(); e.stopPropagation();
      showDisclaimer(this.dataset.url);
    });

    // Asset download links
    document.querySelectorAll('a[data-disc-url]').forEach(function(a){
      a.addEventListener('click', function(e){
        e.preventDefault();
        showDisclaimer(this.dataset.discUrl);
      });
    });

    // Footer GitHub link
    var ghLink = document.getElementById('gh-repo-link');
    if(ghLink) ghLink.addEventListener('click', function(e){
      e.preventDefault();
      showDisclaimer('https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard');
    });

    // Disclaimer buttons
    var cancelBtn = document.getElementById('disc-cancel');
    if(cancelBtn) cancelBtn.addEventListener('click', closeDisclaimer);
    var proceedBtn = document.getElementById('disc-url');
    if(proceedBtn) proceedBtn.addEventListener('click', proceedDownload);

    // temp slider
    var slider = document.getElementById('temp-slider');
    if(slider) slider.addEventListener('input', function(){ setTemp(this.value); });
  });
