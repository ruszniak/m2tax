(function(){
  var btn=document.getElementById('menu-btn'),nav=document.getElementById('nav');
  btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
  nav.addEventListener('click',function(e){if(e.target.closest('a')){nav.classList.remove('open');btn.setAttribute('aria-expanded','false')}});
  var toast=document.getElementById('toast'),t;
  function show(msg){toast.textContent=msg;toast.hidden=false;clearTimeout(t);t=setTimeout(function(){toast.hidden=true},1800)}
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var v=b.getAttribute('data-copy');
      try{navigator.clipboard.writeText(v).then(function(){show('Skopiowano: '+v)},function(){show(v)})}catch(e){show(v)}
    });
  });
})();

/* Efekty 3D (bez bibliotek): tła w ciemnych sekcjach, wejście elementów, przechylanie kart.
   Animacje działają tylko dla widocznych sekcji; przy „ogranicz ruch” w systemie są wyłączone. */
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ACC='217,185,142', BG='22,23,26';
  document.documentElement.classList.add('fx');

  /* ---------- tła 3D ---------- */
  function rnd(seed){ return function(){ seed=(seed*16807)%2147483647; return (seed-1)/2147483646; }; }
  var modes = {
    wave: { init:function(){}, draw:function(c,W,H,t,m){
      var COLS=W<700?34:64, ROWS=W<700?26:34, SP=34, fov=W<700?420:620, camY=230+m.y*40, hz=H*0.36, cx=W*0.5+m.x*60;
      for(var j=ROWS-1;j>=0;j--){ var z=140+j*SP;
        for(var i=0;i<COLS;i++){ var x=(i-(COLS-1)/2)*SP;
          var y=Math.sin(i*0.22+t*0.9)*26+Math.cos(j*0.28+t*0.7)*22+Math.sin((i+j)*0.12+t*0.5)*14;
          var sc=fov/z, px=cx+x*sc, py=hz+(camY-y)*sc; if(px<-10||px>W+10||py<-10||py>H+10) continue;
          var a=(0.10+0.55*(1-j/ROWS))*(0.45+0.55*(y+62)/124);
          c.fillStyle='rgba('+ACC+','+a.toFixed(3)+')'; c.beginPath(); c.arc(px,py,Math.min(3.4,Math.max(0.6,2.2*sc)),0,6.283); c.fill(); } }
      fade(c,W,H,0.55, W>960?0.45:0); } },
    network: { init:function(st,W,H){ var r=rnd(7), n=W<700?60:110; st.p=[];
        for(var k=0;k<n;k++){ var th=r()*6.283, ph=Math.acos(2*r()-1), rad=0.55+0.45*Math.cbrt(r());
          st.p.push([Math.sin(ph)*Math.cos(th)*rad, Math.cos(ph)*rad*0.8, Math.sin(ph)*Math.sin(th)*rad]); } },
      draw:function(c,W,H,t,m,st){
        var R=Math.min(W,H)*(W<700?0.62:0.5), cx=W<900?W*0.6:W*0.6, cy=H*0.42, fov=2.4;
        var ay=t*0.12+m.x*0.6, ax=0.35+m.y*0.3, ca=Math.cos(ay), sa=Math.sin(ay), cb=Math.cos(ax), sb=Math.sin(ax), pr=[];
        for(var k=0;k<st.p.length;k++){ var q=st.p[k], x=q[0]*ca-q[2]*sa, z=q[0]*sa+q[2]*ca, y=q[1]*cb-z*sb; z=q[1]*sb+z*cb;
          var s=fov/(fov+z); pr.push([cx+x*R*s, cy+y*R*s, z, s, x, y]); }
        c.lineWidth=1;
        for(var i=0;i<pr.length;i++) for(var j=i+1;j<pr.length;j++){ var dx=pr[i][4]-pr[j][4], dy=pr[i][5]-pr[j][5], dz=pr[i][2]-pr[j][2], d=dx*dx+dy*dy+dz*dz;
          if(d<0.09){ var a=(1-d/0.09)*0.32*(1.2-(pr[i][2]+pr[j][2])/2.4); c.strokeStyle='rgba('+ACC+','+Math.max(0,a).toFixed(3)+')'; c.beginPath(); c.moveTo(pr[i][0],pr[i][1]); c.lineTo(pr[j][0],pr[j][1]); c.stroke(); } }
        for(var k2=0;k2<pr.length;k2++){ var P=pr[k2], al=0.25+0.6*(1-(P[2]+1)/2); c.fillStyle='rgba('+ACC+','+al.toFixed(3)+')'; c.beginPath(); c.arc(P[0],P[1],1.2+1.8*P[3],0,6.283); c.fill(); }
        var g=c.createLinearGradient(0,0,W<900?0:W*0.6,W<900?H*0.7:0); g.addColorStop(0,'rgba('+BG+',.88)'); g.addColorStop(0.7,'rgba('+BG+',.55)'); g.addColorStop(1,'rgba('+BG+',.15)'); c.fillStyle=g; c.fillRect(0,0,W,H); } },
    grid: { init:function(){}, draw:function(c,W,H,t,m){
        var hz=H*0.42, cx=W*0.5+m.x*80, fov=W<700?300:420, camY=160, step=60, far=2400, off=(t*40)%step;
        c.lineWidth=1;
        for(var z=far; z>40; z-=step){ var zz=z-off, sc=fov/zz, y=hz+camY*sc; if(y>H) continue; var a=0.04+0.38*(1-zz/far);
          c.strokeStyle='rgba('+ACC+','+a.toFixed(3)+')'; c.beginPath(); c.moveTo(0,y); c.lineTo(W,y); c.stroke(); }
        for(var x=-40;x<=40;x++){ var X=x*step+m.x*0, x1=cx+X*fov/far, x2=cx+X*fov/60, y2=hz+camY*fov/60;
          c.strokeStyle='rgba('+ACC+',0.16)'; c.beginPath(); c.moveTo(x1,hz+camY*fov/far); c.lineTo(x2,y2); c.stroke(); }
        var g=c.createLinearGradient(0,0,0,H); g.addColorStop(0,'rgba('+BG+',1)'); g.addColorStop(0.45,'rgba('+BG+',.9)'); g.addColorStop(0.75,'rgba('+BG+',.35)'); g.addColorStop(1,'rgba('+BG+',.15)'); c.fillStyle=g; c.fillRect(0,0,W,H); } },
    rings: { init:function(){}, draw:function(c,W,H,t,m){
        var cx=W*0.82+m.x*30, cy=H*0.22+m.y*20, base=Math.min(W,H)*0.55;
        for(var k=0;k<5;k++){ var rx=base*(0.45+k*0.16), tilt=0.35+0.1*Math.sin(t*0.4+k), rot=t*0.15*(k%2?1:-1)+k;
          c.save(); c.translate(cx,cy); c.rotate(rot); c.scale(1,tilt); c.strokeStyle='rgba('+ACC+','+(0.22-k*0.035).toFixed(3)+')'; c.lineWidth=1.2; c.beginPath(); c.arc(0,0,rx,0,6.283); c.stroke();
          var ang=t*0.6*(k%2?1:-1)+k*1.3; c.fillStyle='rgba('+ACC+',0.7)'; c.beginPath(); c.arc(Math.cos(ang)*rx,Math.sin(ang)*rx,2.6,0,6.283); c.fill(); c.restore(); } } }
  };
  function fade(c,W,H,top,left){ var g=c.createLinearGradient(0,0,0,H*top); g.addColorStop(0,'rgba('+BG+',1)'); g.addColorStop(1,'rgba('+BG+',0)'); c.fillStyle=g; c.fillRect(0,0,W,H*top);
    if(left){ var g2=c.createLinearGradient(0,0,W*left,0); g2.addColorStop(0,'rgba('+BG+',.85)'); g2.addColorStop(1,'rgba('+BG+',0)'); c.fillStyle=g2; c.fillRect(0,0,W*left,H); } }

  document.querySelectorAll('canvas.fx3d').forEach(function(cv){
    var mode=modes[cv.getAttribute('data-fx')]||modes.wave, c=cv.getContext('2d'); if(!c) return;
    var W=0,H=0,t=0,run=false,raf=0,m={x:0,y:0},tg={x:0,y:0},st={};
    function size(){ var r=cv.getBoundingClientRect(), d=Math.min(window.devicePixelRatio||1,2); W=r.width; H=r.height; cv.width=Math.round(W*d); cv.height=Math.round(H*d); c.setTransform(d,0,0,d,0,0); mode.init(st,W,H); }
    function frame(){ c.clearRect(0,0,W,H); m.x+=(tg.x-m.x)*0.04; m.y+=(tg.y-m.y)*0.04; mode.draw(c,W,H,t,m,st); if(!reduce){ t+=0.016; if(run) raf=requestAnimationFrame(frame); } }
    function start(){ if(run) return; run=true; raf=requestAnimationFrame(frame); }
    function stop(){ run=false; cancelAnimationFrame(raf); }
    size(); frame();
    var rt; window.addEventListener('resize',function(){ clearTimeout(rt); rt=setTimeout(function(){ size(); if(!run) frame(); },120); });
    if(!reduce){
      cv.parentElement.addEventListener('pointermove',function(e){ var r=cv.getBoundingClientRect(); tg.x=(e.clientX-r.left)/r.width-.5; tg.y=(e.clientY-r.top)/r.height-.5; });
      if('IntersectionObserver' in window) new IntersectionObserver(function(es){ es.forEach(function(en){ en.isIntersecting?start():stop(); }); }).observe(cv); else start();
    }
  });

  /* ---------- wejście elementów w perspektywie ---------- */
  var sel='.section-head, .step, .letter, .pillar, .spec, .plan, .free, .person, .bk-card, .cinfo, .urgent, .map-col, .sol, .duo-card, .town, .variant, .flow li, .cta-band';
  var items=[].slice.call(document.querySelectorAll(sel));
  if(!reduce && 'IntersectionObserver' in window){
    items.forEach(function(el){ var sib=el.parentElement?[].indexOf.call(el.parentElement.children,el):0; el.style.setProperty('--d',(Math.min(sib,5)*0.08)+'s'); el.classList.add('rv'); });
    var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } }); },{rootMargin:'0px 0px -8% 0px',threshold:0.08});
    items.forEach(function(el){ io.observe(el); });
    setTimeout(function(){ items.forEach(function(el){ var r=el.getBoundingClientRect(); if(r.top<innerHeight) el.classList.add('in'); }); },60);
  }

  /* ---------- przechylanie kart 3D (tylko mysz) ---------- */
  if(!reduce && window.matchMedia('(hover:hover) and (pointer:fine)').matches){
    /* podświetlenie za kursorem: przekazujemy pozycję myszy do CSS */
    document.querySelectorAll('.pillar, .plan, .letter, .spec, .person, .free, .step, .cinfo, .urgent, .bk-free, .callcard, .sol, .duo-card, .variant, .town').forEach(function(el){
      el.classList.add('glow');
      el.addEventListener('pointermove',function(e){ var r=el.getBoundingClientRect(); el.style.setProperty('--mx',(e.clientX-r.left)+'px'); el.style.setProperty('--my',(e.clientY-r.top)+'px'); });
    });
    document.querySelectorAll('.letter, .step, .cinfo, .town').forEach(function(el){ el.classList.add('lift'); });
    document.querySelectorAll('.pillar, .plan, .letter, .spec, .person, .free, .sol, .variant, .duo-card').forEach(function(el){
      el.classList.add('tilt');
      el.addEventListener('pointermove',function(e){ var r=el.getBoundingClientRect(), x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
        el.classList.add('tilting'); el.style.transform='perspective(1100px) rotateY('+(x*5).toFixed(2)+'deg) rotateX('+(-y*5).toFixed(2)+'deg) translateZ(4px)'; });
      el.addEventListener('pointerleave',function(){ el.classList.remove('tilting'); el.style.transform=''; });
    });
  }
})();

/* Godło 3D: przechylanie za myszką */
(function(){
  var em=document.getElementById('emblem'); if(!em) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var host=em.closest('.hero')||document.body, st=em.querySelector('.em-stage');
  host.addEventListener('pointermove',function(e){ var r=em.getBoundingClientRect(), x=(e.clientX-(r.left+r.width/2))/r.width, y=(e.clientY-(r.top+r.height/2))/r.height;
    st.style.setProperty('--ry',(-10+x*16).toFixed(2)+'deg'); st.style.setProperty('--rx',(6-y*12).toFixed(2)+'deg'); });
  host.addEventListener('pointerleave',function(){ st.style.removeProperty('--ry'); st.style.removeProperty('--rx'); });
})();

/* =====================================================================
   NOWA WERSJA: motyw, płynne przewijanie, animacje słów, liczniki,
   paralaksa, magnetyczne przyciski, koło usług, złoty pył w hero
   ===================================================================== */
(function(){
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var root=document.documentElement;

  /* ---- jasny / ciemny motyw ---- */
  var tg=document.getElementById('theme-tg');
  if(tg){ tg.setAttribute('aria-pressed',root.getAttribute('data-theme')==='dark');
    tg.addEventListener('click',function(){ var d=root.getAttribute('data-theme')==='dark';
      if(d) root.removeAttribute('data-theme'); else root.setAttribute('data-theme','dark');
      tg.setAttribute('aria-pressed',!d); try{localStorage.setItem('m2-theme',d?'light':'dark')}catch(e){} }); }

  /* ---- płynne przewijanie (Lenis) ---- */
  var lenis=null;
  if(!reduce && fine && window.Lenis){
    lenis=new window.Lenis({duration:1.15,smoothWheel:true}); window.__lenis=lenis;
    (function raf(t){ lenis.raf(t); requestAnimationFrame(raf); })(0);
    document.querySelectorAll('a[href^="#"]').forEach(function(a){ a.addEventListener('click',function(e){ var id=a.getAttribute('href'); if(id.length>1&&document.querySelector(id)){ e.preventDefault(); lenis.scrollTo(id,{offset:-80}); } }); });
  }

  /* ---- nagłówki: słowa wjeżdżają po kolei ---- */
  var heads=[].slice.call(document.querySelectorAll('.split, .section-head h2, .page-hero h1'));
  heads.forEach(function(h){
    h.classList.add('split'); var n=0;
    (function walk(el){ [].slice.call(el.childNodes).forEach(function(c){
      if(c.nodeType===3){ var parts=c.textContent.split(/(\s+)/), f=document.createDocumentFragment();
        parts.forEach(function(w){ if(!w) return; if(/^\s+$/.test(w)){ f.appendChild(document.createTextNode(w)); return; }
          var o=document.createElement('span'); o.className='w'; var i=document.createElement('span'); i.textContent=w; i.style.setProperty('--i',n++); o.appendChild(i); f.appendChild(o); });
        el.replaceChild(f,c);
      } else if(c.nodeType===1 && !c.classList.contains('w')) walk(c); }); })(h);
  });
  if(reduce || !('IntersectionObserver' in window)){ heads.forEach(function(h){ h.classList.add('in'); }); }
  else { var hio=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); hio.unobserve(e.target); } }); },{threshold:0.2});
    heads.forEach(function(h){ hio.observe(h); }); }

  /* ---- cztery sposoby: wejście kart ---- */
  document.querySelectorAll('.sol-anim').forEach(function(g){
    if(reduce || !('IntersectionObserver' in window)){ g.classList.add('go'); return; }
    var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ g.classList.add('go'); o.disconnect(); } },{threshold:0.25}); o.observe(g);
  });

  /* ---- branże: rozwijane panele ---- */
  document.querySelectorAll('.acc-wrap').forEach(function(w){
    var ps=[].slice.call(w.querySelectorAll('.acc'));
    function act(el){ ps.forEach(function(x){ x.classList.toggle('on',x===el); }); }
    ps.forEach(function(el){
      if(fine) el.addEventListener('pointerenter',function(){ act(el); });
      el.addEventListener('focus',function(){ act(el); });
      el.addEventListener('click',function(e){ if(!el.classList.contains('on')){ e.preventDefault(); act(el); } });
    });
  });

  /* ---- kontakt: szklane kafelki ---- */
  document.querySelectorAll('.gl-grid').forEach(function(g){
    if(reduce || !('IntersectionObserver' in window)) g.classList.add('in');
    else { var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ g.classList.add('in'); o.disconnect(); } },{threshold:0.2}); o.observe(g); }
    if(fine && !reduce) g.querySelectorAll('.gl-t').forEach(function(t){
      t.addEventListener('pointermove',function(e){ var r=t.getBoundingClientRect(), x=e.clientX-r.left, y=e.clientY-r.top; t.classList.add('tl'); t.style.setProperty('--x',x+'px'); t.style.setProperty('--y',y+'px');
        t.style.transform='rotateY('+((x/r.width-.5)*10).toFixed(2)+'deg) rotateX('+(-(y/r.height-.5)*10).toFixed(2)+'deg)'; });
      t.addEventListener('pointerleave',function(){ t.style.transform=''; });
    });
  });

  /* ---- zakres działania: orbita miast ---- */
  document.querySelectorAll('.to-orb').forEach(function(orb){
    var cv=orb.querySelector('.to-cv'), c=cv.getContext('2d'), nds=[].slice.call(orb.querySelectorAll('.to-nd')), sec=orb.closest('.to-sec'),
        lis=[].slice.call(sec.querySelectorAll('.to-list li')), hl=null, run=false, t0=0, P=[];
    for(var i=0;i<90;i++) P.push([Math.random()*6.283,.5+Math.random()*.5,.0008+Math.random()*.002]);
    function setHl(t){ hl=t; nds.forEach(function(n){ n.classList.toggle('hl',n.dataset.t===t); }); lis.forEach(function(l){ l.classList.toggle('hl',l.dataset.t===t); }); }
    lis.concat(nds).forEach(function(el){ el.addEventListener('pointerenter',function(){ setHl(el.dataset.t); }); el.addEventListener('pointerleave',function(){ setHl(null); }); });
    function frame(now){ if(!t0) t0=now; var el=(now-t0)/1000, W=orb.clientWidth, H=orb.clientHeight, d=Math.min(devicePixelRatio||1,2);
      if(cv.width!==Math.round(W*d)||cv.height!==Math.round(H*d)){ cv.width=Math.round(W*d); cv.height=Math.round(H*d); c.setTransform(d,0,0,d,0,0); }
      c.clearRect(0,0,W,H); var cx=W/2, cy=H/2;
      [.44,.32].forEach(function(rr,k){ c.save(); c.translate(cx,cy); c.strokeStyle='rgba(217,185,142,'+(k?.12:.22)+')'; c.setLineDash(k?[]:[3,7]); c.lineDashOffset=-el*(k?4:8); c.beginPath(); c.ellipse(0,0,W*rr,H*rr,0,0,6.283); c.stroke(); c.restore(); });
      c.setLineDash([]);
      P.forEach(function(p){ p[0]+=reduce?0:p[2]; c.fillStyle='rgba(226,192,140,.45)'; c.fillRect(cx+Math.cos(p[0])*W*.5*p[1],cy+Math.sin(p[0])*H*.5*p[1],1.5,1.5); });
      nds.forEach(function(n,i){ var x=parseFloat(n.style.left)/100*W, y=parseFloat(n.style.top)/100*H, on=hl===n.dataset.t||hl==='Wrocław';
        var grow=reduce?1:Math.min(1,Math.max(0,(el-.2-i*.15)/1.2)), ex=cx+(x-cx)*grow, ey=cy+(y-cy)*grow;
        var g=c.createLinearGradient(cx,cy,x,y); g.addColorStop(0,'rgba(226,192,140,.05)'); g.addColorStop(1,'rgba(226,192,140,'+(on?.95:.55)+')');
        c.strokeStyle=g; c.lineWidth=on?2:1; c.beginPath(); c.moveTo(cx,cy); c.lineTo(ex,ey); c.stroke();
        if(grow>=1 && !reduce){ for(var j=0;j<2;j++){ var k=((now/1600)+i*.2+j*.5)%1; c.fillStyle='rgba(255,240,210,'+(1-k).toFixed(2)+')'; c.beginPath(); c.arc(cx+(x-cx)*k,cy+(y-cy)*k,on?3:2.2,0,6.283); c.fill(); } } });
      if(run && !reduce) requestAnimationFrame(frame); }
    if('IntersectionObserver' in window) new IntersectionObserver(function(es){ var v=es[0].isIntersecting; if(v&&!run){ run=true; requestAnimationFrame(frame); } run=v; }).observe(orb);
    else { run=true; requestAnimationFrame(frame); }
    if(reduce) requestAnimationFrame(frame);
  });

  /* ---- liczniki ---- */
  var cnt=[].slice.call(document.querySelectorAll('[data-count]'));
  function run(el){ var to=+el.getAttribute('data-count'), suf=el.getAttribute('data-suffix')||'', t0=null, dur=1400;
    function step(t){ if(!t0) t0=t; var k=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-k,3); el.textContent=Math.round(to*e).toLocaleString('pl-PL')+suf; if(k<1) requestAnimationFrame(step); }
    requestAnimationFrame(step); }
  if(!reduce && 'IntersectionObserver' in window){ var cio=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ run(e.target); cio.unobserve(e.target); } }); },{threshold:0.6}); cnt.forEach(function(el){ cio.observe(el); }); }

  /* ---- paralaksa przy przewijaniu + duże litery za myszką ---- */
  var par=[].slice.call(document.querySelectorAll('[data-parallax]')), giant=(document.querySelector('canvas.dust')&&fine&&innerWidth>900)?[]:[].slice.call(document.querySelectorAll('.giant span')), mx=0, my=0;
  if(!reduce){
    var tick=function(){ var y=window.scrollY||0;
      par.forEach(function(el){ el.style.transform='translate3d(0,'+(y*parseFloat(el.getAttribute('data-parallax'))).toFixed(1)+'px,0)'; });
      giant.forEach(function(el){ var d=parseFloat(el.getAttribute('data-depth')||1); el.style.transform='translate3d('+(mx*-30*d).toFixed(1)+'px,'+(y*0.18*d+my*-14*d).toFixed(1)+'px,0)'; });
      requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
    if(fine) window.addEventListener('pointermove',function(e){ mx=e.clientX/innerWidth-.5; my=e.clientY/innerHeight-.5; },{passive:true});
  }

  /* ---- magnetyczne przyciski ---- */
  if(!reduce && fine) document.querySelectorAll('.magnet').forEach(function(b){
    b.addEventListener('pointermove',function(e){ var r=b.getBoundingClientRect(); b.style.transform='translate('+((e.clientX-r.left-r.width/2)*0.18).toFixed(1)+'px,'+((e.clientY-r.top-r.height/2)*0.3).toFixed(1)+'px)'; });
    b.addEventListener('pointerleave',function(){ b.style.transform=''; });
  });

  /* ---- koło usług ---- */
  document.querySelectorAll('.wheel').forEach(function(w){
    var data=JSON.parse(w.getAttribute('data-items')), dial=w.querySelector('.wheel-dial'), lis=[].slice.call(w.querySelectorAll('.wheel-list li')),
        num=w.querySelector('.wheel-num span'), card=w.querySelector('.wheel-card'), cur=0, timer=null, hover=false;
    var $=function(s){ return card.querySelector(s); };
    function layout(){
      var mobile=innerWidth<=900; if(mobile){ lis.forEach(function(li){ li.style.transform=''; li.style.opacity=''; }); return; }
      var W=dial.clientWidth, H=dial.clientHeight, R=470, cx=W*0.40-440, cy=H/2, gap=18, n=lis.length, pos=new Array(n);
      lis.forEach(function(li){ li.firstElementChild.style.maxWidth=Math.max(160,W-(cx+R)-12)+'px'; });
      function rel(i){ var k=i-cur; if(k>n/2) k-=n; if(k<-n/2) k+=n; return k; }
      var order=lis.map(function(_,i){ return i; }).sort(function(a,b){ return Math.abs(rel(a))-Math.abs(rel(b)); });
      var down=lis[cur].offsetHeight/2, up=-lis[cur].offsetHeight/2; pos[cur]=0;
      for(var k=1;k<=Math.floor(n/2);k++){
        var iN=(cur+k)%n, iP=(cur-k+n)%n;
        if(rel(iN)===k){ var h=lis[iN].offsetHeight; pos[iN]=down+gap+h/2; down+=gap+h; }
        if(rel(iP)===-k && iP!==iN){ var h2=lis[iP].offsetHeight; pos[iP]=up-gap-h2/2; up-=gap+h2; }
      }
      lis.forEach(function(li,i){ var y=pos[i]||0, vis=Math.abs(y)<H/2-20, yy=Math.max(-R+1,Math.min(R-1,y));
        var x=cx+Math.sqrt(R*R-yy*yy);
        li.style.transform='translate('+x.toFixed(1)+'px,'+(y-li.offsetHeight/2).toFixed(1)+'px)';
        li.style.opacity=vis?Math.max(0.15,1-Math.abs(y)/(H/2)).toFixed(2):0; li.style.pointerEvents=vis?'':'none'; });
    }
    function go(i,user){ cur=(i+data.length)%data.length; var d=data[cur];
      lis.forEach(function(li,k){ li.classList.toggle('on',k===cur); }); requestAnimationFrame(layout);
      if(num){ num.parentElement.classList.add('flip'); setTimeout(function(){ num.textContent=(cur+1<10?'0':'')+(cur+1); num.parentElement.classList.remove('flip'); },220); }
      card.classList.add('swap');
      setTimeout(function(){ $('.wheel-ref').textContent=d.r; $('.wheel-title').textContent=d.t; $('.wheel-desc').textContent=d.d;
        $('.wheel-li').innerHTML=d.li.map(function(x){ return '<li>'+x+'</li>'; }).join(''); card.classList.remove('swap'); },260);
      layout();
      if(innerWidth<=900 && user){ var b=lis[cur].firstElementChild; dial.scrollTo({left:b.offsetLeft-20,behavior:reduce?'auto':'smooth'}); }
    }
    lis.forEach(function(li,i){ li.firstElementChild.addEventListener('click',function(){ go(i,true); restart(); }); });
    w.querySelector('.wheel-prev').addEventListener('click',function(){ go(cur-1,true); restart(); });
    w.querySelector('.wheel-next').addEventListener('click',function(){ go(cur+1,true); restart(); });
    w.addEventListener('keydown',function(e){ if(e.key==='ArrowDown'||e.key==='ArrowRight'){ e.preventDefault(); go(cur+1,true); } if(e.key==='ArrowUp'||e.key==='ArrowLeft'){ e.preventDefault(); go(cur-1,true); } });
    w.addEventListener('pointerenter',function(){ hover=true; }); w.addEventListener('pointerleave',function(){ hover=false; });
    function restart(){ clearInterval(timer); if(reduce) return; timer=setInterval(function(){ if(!hover && document.visibilityState==='visible') go(cur+1); },6500); }
    window.addEventListener('resize',layout);
    go(0); restart();
  });

  /* ---- złoty pył: zlatuje się w napis M2 TAX i rozpuszcza w złocie ---- */
  var cv=document.querySelector('canvas.dust'), host=cv&&cv.parentElement, ba=host&&host.querySelector('.brand-anim');
  if(cv && ba && !reduce && fine && innerWidth>900){
    var c=cv.getContext('2d'), P=[], W, H, dpr=Math.min(devicePixelRatio||1,2), t0=0, DUR=3400;
    var spr=document.createElement('canvas'); spr.width=spr.height=32; (function(){ var g=spr.getContext('2d'), r=g.createRadialGradient(16,16,0,16,16,16);
      r.addColorStop(0,'rgba(255,246,226,1)'); r.addColorStop(.25,'rgba(233,206,160,.9)'); r.addColorStop(.6,'rgba(217,185,142,.25)'); r.addColorStop(1,'rgba(217,185,142,0)'); g.fillStyle=r; g.fillRect(0,0,32,32); })();
    function targets(){ var hr=host.getBoundingClientRect(), logo=ba.querySelector('.ba-logo');
      if(logo){ var lr=logo.getBoundingClientRect(), off2=document.createElement('canvas'); off2.width=W; off2.height=H; var o2=off2.getContext('2d');
        o2.drawImage(logo, lr.left-hr.left, lr.top-hr.top, lr.width, lr.height); var d2=o2.getImageData(0,0,W,H).data, pts2=[], g2=4;
        for(var y2=0;y2<H;y2+=g2) for(var x2=0;x2<W;x2+=g2) if(d2[(y2*W+x2)*4+3]>140) pts2.push([x2+(Math.random()-.5)*2,y2+(Math.random()-.5)*2]);
        if(pts2.length>1700) pts2=pts2.filter(function(_,i){ return i%Math.ceil(pts2.length/1700)===0; }); return pts2; }
      var fill=ba.querySelector('.ba-fill'), r=fill.getBoundingClientRect(), fam=getComputedStyle(fill).fontFamily;
      var off=document.createElement('canvas'); off.width=W; off.height=H; var o=off.getContext('2d'); o.font='900 200px '+fam;
      var m=o.measureText('M2 TAX'), asc=m.actualBoundingBoxAscent, des=m.actualBoundingBoxDescent, l=m.actualBoundingBoxLeft, w=m.actualBoundingBoxRight+l;
      o.save(); o.translate(r.left-hr.left, r.top-hr.top); o.scale(r.width/w, r.height/(asc+des)); o.fillStyle='#fff'; o.fillText('M2 TAX', l, asc); o.restore();
      var img=o.getImageData(0,0,W,H).data, pts=[], gap=5; for(var y=0;y<H;y+=gap) for(var x=0;x<W;x+=gap) if(img[(y*W+x)*4+3]>140) pts.push([x+(Math.random()-.5)*2,y+(Math.random()-.5)*2]);
      if(pts.length>1600) pts=pts.filter(function(_,i){ return i%Math.ceil(pts.length/1600)===0; }); return pts; }
    function init(){ var r=host.getBoundingClientRect(); W=Math.round(r.width); H=Math.round(r.height); cv.width=W*dpr; cv.height=H*dpr; c.setTransform(dpr,0,0,dpr,0,0);
      P=targets().map(function(q){ var ang=Math.random()*6.283, d=300+Math.random()*700; return {sx:q[0]+Math.cos(ang)*d, sy:q[1]+Math.sin(ang)*d*0.6, tx:q[0], ty:q[1], s:4+Math.random()*7, dl:Math.random()*0.35}; }); }
    function ease(k){ return 1-Math.pow(1-k,4); }
    function frame(now){ if(!t0) t0=now; var el=now-t0; c.clearRect(0,0,W,H); c.globalCompositeOperation='lighter';
      var fade=el<1700?1:Math.max(0,1-(el-1700)/1300);
      for(var i=0;i<P.length;i++){ var p=P[i], k=Math.min(1,Math.max(0,(el/1600-p.dl)/(1-p.dl))), e=ease(k), x=p.sx+(p.tx-p.sx)*e, y=p.sy+(p.ty-p.sy)*e;
        var tw=0.55+0.45*Math.sin(now/180+i); c.globalAlpha=Math.min(1,k*3)*fade*tw; var sz=p.s*(1.6-0.8*e); c.drawImage(spr,x-sz/2,y-sz/2,sz,sz); }
      c.globalAlpha=1; c.globalCompositeOperation='source-over';
      if(el<DUR) requestAnimationFrame(frame); else { c.clearRect(0,0,W,H); ba.classList.add('glint-on'); } }
    var lg=ba.querySelector('.ba-logo'); Promise.all([document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve(), lg&&lg.decode?lg.decode().catch(function(){}):Promise.resolve()]).then(function(){ setTimeout(function(){ init(); requestAnimationFrame(frame); },80); });
  } else if(ba){ ba.classList.add('glint-on'); }
})();

/* ---------- dla biur: most + FAQ ---------- */
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bb=document.querySelector('.bb-card');
  if(bb){
    if(reduce || !('IntersectionObserver' in window)) bb.classList.add('go');
    else { var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ bb.classList.add('go'); o.disconnect(); } },{threshold:0.3}); o.observe(bb); }
    var Qs=['pytanie o VAT','kontrola u klienta','JPK CIT','ulga B+R','sprzedaż działki','podatek u źródła'], qi=0, q=bb.querySelector('.bb-q');
    if(q) q.addEventListener('animationiteration',function(){ qi=(qi+1)%Qs.length; q.textContent=Qs[qi]; });
  }
  var fqs=[].slice.call(document.querySelectorAll('details.fq'));
  fqs.forEach(function(d){
    var s=d.querySelector('summary'), a=d.querySelector('.fq-a');
    s.addEventListener('click',function(e){
      e.preventDefault();
      if(d._busy) return;
      var opening=!d.open;
      if(opening) fqs.forEach(function(x){ if(x!==d && x.open) x.querySelector('summary').click(); });
      if(reduce || !a.animate){ d.open=opening; return; }
      d._busy=true;
      if(opening){ d.open=true; var h=a.scrollHeight; a.animate([{height:'0px',opacity:0},{height:h+'px',opacity:1}],{duration:380,easing:'cubic-bezier(.2,.8,.2,1)'}).onfinish=function(){ d._busy=false; }; }
      else { var h2=a.scrollHeight; var an=a.animate([{height:h2+'px',opacity:1},{height:'0px',opacity:0}],{duration:300,easing:'cubic-bezier(.4,0,.2,1)',fill:'forwards'}); an.onfinish=function(){ d.open=false; an.cancel(); d._busy=false; }; }
    });
  });
})();

/* ---------- pismo z urzędu: oś czasu + koperta ---------- */
(function(){
  var sec=document.querySelector('.pf-sec'); if(!sec) return;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var line=sec.querySelector('.pf-line'), steps=[].slice.call(sec.querySelectorAll('.pf-step')), stamp=sec.querySelector('.pf-stamp'),
      cnt=sec.querySelector('.pf-cnt'), ring=sec.querySelector('.pf-ring'), docs=sec.querySelector('.pf-docs'), cur=-1;
  function setStep(i){ if(i===cur) return; cur=i;
    steps.forEach(function(s,k){ s.classList.toggle('on',k===i); s.classList.toggle('done',k<i); });
    if(cnt) cnt.textContent=i+1; if(ring) ring.style.setProperty('--r',(i+1)/steps.length);
    if(stamp){ stamp.textContent=steps[i].getAttribute('data-stamp'); stamp.classList.remove('hit'); void stamp.offsetWidth; if(sec.classList.contains('open')) stamp.classList.add('hit'); } }
  function upd(){ var vh=innerHeight, r=line.getBoundingClientRect(), mid=vh*.55;
    var p=Math.max(0,Math.min(1,(mid-r.top)/r.height)); line.style.setProperty('--p',p.toFixed(3));
    var idx=0; steps.forEach(function(s,k){ if(s.getBoundingClientRect().top<mid) idx=k; }); setStep(idx);
    if(!sec.classList.contains('open') && sec.getBoundingClientRect().top<vh*.6){ sec.classList.add('open'); setTimeout(function(){ stamp&&stamp.classList.add('hit'); },1200); } }
  if(reduce){ sec.classList.add('open'); setStep(0); if(stamp) stamp.style.opacity=1; docs.classList.add('in'); return; }
  addEventListener('scroll',function(){ requestAnimationFrame(upd); },{passive:true}); addEventListener('resize',upd); upd();
  if('IntersectionObserver' in window){ var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ docs.classList.add('in'); o.disconnect(); } },{threshold:.2}); o.observe(docs); } else docs.classList.add('in');
  sec.querySelectorAll('.pf-doc').forEach(function(d){ d.addEventListener('pointermove',function(e){ var r=d.getBoundingClientRect(); d.style.setProperty('--mx',(e.clientX-r.left)+'px'); d.style.setProperty('--my',(e.clientY-r.top)+'px'); }); });
})();

/* ---------- przezroczysty nagłówek (dopasowuje się do tła pod spodem) ---------- */
(function(){
  var tb=document.querySelector('.topbar'), main=document.querySelector('main'); if(!tb||!main) return;
  var first=main.firstElementChild;
  tb.classList.add('ov');
  if(first && /(^|\s)(hero|page-hero|bk-section)(\s|$)/.test(first.className)) first.classList.add('ov-first'); else tb.classList.add('ov-flow');
  if(first && first.classList.contains('hero2') && document.querySelector('.brand-anim')) tb.classList.add('home');
  function lum(c){ var m=c.match(/[\d.]+/g); if(!m) return null; if(m.length>3 && +m[3]<.5) return null; return (.299*m[0]+.587*m[1]+.114*m[2])/255; }
  function bgAt(y){ var x=innerWidth/2, el=document.elementsFromPoint(x,y).filter(function(e){ return !tb.contains(e) && !e.closest('.fab-stack'); })[0];
    while(el && el!==document.documentElement){ var L=lum(getComputedStyle(el).backgroundColor); if(L!==null) return L; el=el.parentElement; }
    return lum(getComputedStyle(document.body).backgroundColor); }
  var tk=false;
  function upd(){ tk=false; var h=tb.offsetHeight, L=bgAt(h+2);
    tb.classList.toggle('sc', scrollY>12);
    tb.classList.toggle('lt', L!==null && L>.55); }
  function req(){ if(!tk){ tk=true; requestAnimationFrame(upd); } }
  addEventListener('scroll',req,{passive:true}); addEventListener('resize',req); upd(); setTimeout(upd,400);
  var mb=document.getElementById('menu-btn');
  if(mb) mb.addEventListener('click',function(){ setTimeout(function(){ tb.classList.toggle('open', mb.getAttribute('aria-expanded')==='true'); },0); });
})();

/* ---------- dwóch doradców ---------- */
(function(){
  document.querySelectorAll('.dv-sec').forEach(function(sec){
    var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches, cs=[].slice.call(sec.querySelectorAll('.dv-c')), i=-1, tm=null, hold=false;
    function set(k){ i=k; sec.setAttribute('data-on',k); cs.forEach(function(c,n){ c.classList.toggle('on',n===k); }); }
    function cyc(){ if(!hold) set((i+1)%cs.length); }
    cs.forEach(function(c,n){ c.addEventListener('pointerenter',function(){ hold=true; set(n); }); c.addEventListener('pointerleave',function(){ hold=false; }); });
    function go(){ sec.classList.add('go'); if(!reduce){ setTimeout(function(){ cyc(); tm=setInterval(cyc,3200); },2400); } else set(0); }
    if(!('IntersectionObserver' in window)) go();
    else { var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ go(); o.disconnect(); } },{threshold:.25}); o.observe(sec); }
  });
})();

/* ---------- cennik ---------- */
(function(){
  document.querySelectorAll('.pr-grid').forEach(function(g){
    if(!('IntersectionObserver' in window)) g.classList.add('in');
    else { var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ g.classList.add('in'); o.disconnect(); } },{threshold:.2}); o.observe(g); }
    g.querySelectorAll('.pr').forEach(function(c){ c.addEventListener('pointermove',function(e){ var r=c.getBoundingClientRect(); c.style.setProperty('--mx',(e.clientX-r.left)+'px'); c.style.setProperty('--my',(e.clientY-r.top)+'px'); }); });
  });
})();
(function(){ var g=document.querySelector('.hb-grid'); if(!g) return;
  if(!('IntersectionObserver' in window)) return g.classList.add('in');
  var o=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ g.classList.add('in'); o.disconnect(); } },{threshold:.15}); o.observe(g); })();

/* ---------- W czym możemy pomóc? — tarcza ---------- */
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.sw').forEach(function(w){
    var data=JSON.parse(w.getAttribute('data-items')), dial=w.querySelector('.sw-dial'), all=[].slice.call(dial.querySelectorAll('.sw-list li')),
        items=all.filter(function(li){ return li.classList.contains('sw-i'); }), num=w.querySelector('.sw-num'), card=w.querySelector('.sw-card'),
        cnt=w.querySelector('.sw-count b'), bar=w.querySelector('.sw-bar'), cur=0, timer=null, hover=false, n=data.length;
    var $=function(s){ return card.querySelector(s); };
    function layout(){
      if(innerWidth<=900){ all.forEach(function(li){ li.style.transform=''; li.style.opacity=''; }); return; }
      var H=dial.clientHeight, W=dial.clientWidth, R=640, cx=-410, cy=H/2, gap=26, m=all.length, ai=all.indexOf(items[cur]), pos=[];
      function rel(i){ var k=i-ai; if(k>m/2) k-=m; if(k<-m/2) k+=m; return k; }
      var down=all[ai].offsetHeight/2, up=-down; pos[ai]=0;
      for(var k=1;k<=Math.floor(m/2);k++){ var iN=(ai+k)%m, iP=(ai-k+m)%m;
        if(rel(iN)===k){ var h=all[iN].offsetHeight; pos[iN]=down+gap+h/2; down+=gap+h; }
        if(rel(iP)===-k && iP!==iN){ var h2=all[iP].offsetHeight; pos[iP]=up-gap-h2/2; up-=gap+h2; } }
      all.forEach(function(li,i){ var y=pos[i]||0, vis=Math.abs(y)<H/2-10, yy=Math.max(-R+1,Math.min(R-1,y)), x=cx+Math.sqrt(R*R-yy*yy)+(li.classList.contains('sw-g')?-10:0);
        x=Math.min(x, W-li.offsetWidth-8);
        li.style.transform='translate('+x.toFixed(1)+'px,'+(cy+y-li.offsetHeight/2).toFixed(1)+'px)';
        li.style.opacity=vis?Math.max(0.12,1-Math.pow(Math.abs(y)/(H/2),1.2)).toFixed(2):0; li.style.pointerEvents=vis?'':'none'; });
    }
    function go(i,user){ cur=(i+n)%n; var d=data[cur];
      items.forEach(function(li,k){ li.classList.toggle('on',k===cur); });
      if(num){ num.classList.add('flip'); setTimeout(function(){ num.querySelector('span').textContent=(cur+1<10?'0':'')+(cur+1); num.classList.remove('flip'); },220); }
      if(cnt) cnt.textContent=(cur+1<10?'0':'')+(cur+1); if(bar) bar.style.setProperty('--w',((cur+1)/n*100).toFixed(1)+'%');
      card.classList.add('swap');
      setTimeout(function(){ $('.sw-cat').textContent=d.g; $('.sw-title').textContent=d.t; $('.sw-desc').textContent=d.d; $('.sw-ref').textContent=d.r; card.classList.remove('swap'); },260);
      var mh=w.querySelector('.sw-mhead'); if(mh){ mh.classList.add('swap'); setTimeout(function(){ mh.querySelector('.sw-mg').textContent=d.g; mh.querySelector('.sw-mname').textContent=d.s; mh.classList.remove('swap'); },220); }
      requestAnimationFrame(layout);
      if(innerWidth<=900 && user){ var b=items[cur].firstElementChild; dial.scrollTo({left:b.offsetLeft-20,behavior:reduce?'auto':'smooth'}); }
    }
    items.forEach(function(li,i){ li.firstElementChild.addEventListener('click',function(){ go(i,true); restart(); }); });
    w.querySelector('.sw-prev').addEventListener('click',function(){ go(cur-1,true); restart(); });
    w.querySelector('.sw-next').addEventListener('click',function(){ go(cur+1,true); restart(); });
    w.querySelector('.sw-mprev').addEventListener('click',function(){ go(cur-1); restart(); });
    w.querySelector('.sw-mnext').addEventListener('click',function(){ go(cur+1); restart(); });
    (function(){ var x0=null, cw=w.querySelector('.sw-cwrap'); cw.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; },{passive:true});
      cw.addEventListener('touchend',function(e){ if(x0===null) return; var dx=e.changedTouches[0].clientX-x0; if(Math.abs(dx)>45){ go(cur+(dx<0?1:-1)); restart(); } x0=null; },{passive:true}); })();
    w.addEventListener('keydown',function(e){ if(e.key==='ArrowDown'||e.key==='ArrowRight'){ e.preventDefault(); go(cur+1,true); } if(e.key==='ArrowUp'||e.key==='ArrowLeft'){ e.preventDefault(); go(cur-1,true); } });
    w.addEventListener('pointerenter',function(){ hover=true; }); w.addEventListener('pointerleave',function(){ hover=false; });
    function restart(){ clearInterval(timer); if(reduce || (w.closest('.sw-pinwrap') && innerWidth>900)) return; timer=setInterval(function(){ if(!hover && document.visibilityState==='visible') go(cur+1); },6500); }
    var pin=w.closest('.sw-pinwrap');
    function pinned(){ return pin && innerWidth>900 && pin.offsetHeight>innerHeight*1.5; }
    function range(){ var r=pin.getBoundingClientRect(); return {top:r.top+scrollY, len:pin.offsetHeight-innerHeight}; }
    function onScroll(){ if(!pinned()) return; var R=range(), p=Math.max(0,Math.min(0.9999,(scrollY-R.top)/R.len)), i=Math.floor(p*n);
      if(i!==cur) go(i); }
    function jump(i){ if(!pinned()){ go(i,true); restart(); return; } i=Math.max(0,Math.min(n-1,i)); var R=range(), y=R.top+(i+0.5)/n*R.len;
      if(window.__lenis) window.__lenis.scrollTo(y,{duration:.9}); else scrollTo({top:y,behavior:reduce?'auto':'smooth'}); }
    if(pin){
      items.forEach(function(li,i){ li.firstElementChild.addEventListener('click',function(e){ if(pinned()){ e.stopImmediatePropagation(); jump(i); } },true); });
      w.querySelector('.sw-prev').addEventListener('click',function(e){ if(pinned()){ e.stopImmediatePropagation(); jump(cur-1); } },true);
      w.querySelector('.sw-next').addEventListener('click',function(e){ if(pinned()){ e.stopImmediatePropagation(); jump(cur+1); } },true);
      addEventListener('scroll',onScroll,{passive:true});
    }
    addEventListener('resize',layout); (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(layout);
    go(0); if(pinned()) onScroll(); else restart();
    addEventListener('resize',function(){ if(pinned()) clearInterval(timer); });
  });
})();
/* kropki pod przesuwanymi rzędami (telefon) */
(function(){ document.querySelectorAll('.pf-docs,.dv-cards').forEach(function(row){
  var kids=[].slice.call(row.children), d=document.createElement('div'); d.className='sc-dots'; d.setAttribute('aria-hidden','true');
  kids.forEach(function(){ d.appendChild(document.createElement('i')); }); row.parentNode.insertBefore(d,row.nextSibling);
  function upd(){ var c=row.scrollLeft+row.clientWidth/2, best=0, bd=1e9; kids.forEach(function(k,i){ var m=k.offsetLeft+k.offsetWidth/2, dd=Math.abs(m-c); if(dd<bd){ bd=dd; best=i; } });
    [].forEach.call(d.children,function(x,i){ x.classList.toggle('on',i===best); }); }
  row.addEventListener('scroll',function(){ requestAnimationFrame(upd); },{passive:true}); upd(); }); })();
