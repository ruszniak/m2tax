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
  var sel='.section-head, .step, .letter, .pillar, .spec, .plan, .free, .person, .faq details, .bk-card, .cinfo, .urgent, .map-col, .sol, .duo-card, .town, .variant, .flow li, .cta-band';
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
    document.querySelectorAll('.pillar, .plan, .letter, .spec, .person, .free, .step, .cinfo, .urgent, .faq details, .bk-free, .callcard, .sol, .duo-card, .variant, .town').forEach(function(el){
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
    lenis=new window.Lenis({duration:1.15,smoothWheel:true});
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
      var W=dial.clientWidth, H=dial.clientHeight, R=470, cx=W*0.42-440, cy=H/2, step=0.13;
      lis.forEach(function(li,i){ var k=i-cur; if(k>data.length/2) k-=data.length; if(k<-data.length/2) k+=data.length;
        var a=k*step, x=cx+R*Math.cos(a), y=cy+R*Math.sin(a)-li.offsetHeight/2, vis=Math.abs(a)<0.56;
        li.style.transform='translate('+x.toFixed(1)+'px,'+(y-cy).toFixed(1)+'px)'; li.style.opacity=vis?(1-Math.abs(a)/0.75).toFixed(2):0; li.style.pointerEvents=vis?'':'none'; });
    }
    function go(i,user){ cur=(i+data.length)%data.length; var d=data[cur];
      lis.forEach(function(li,k){ li.classList.toggle('on',k===cur); });
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

  /* ---- złoty pył układający się w napis M2 TAX ---- */
  var cv=document.querySelector('canvas.dust'), host=cv&&cv.parentElement;
  if(cv && !reduce && fine && innerWidth>900){
    var c=cv.getContext('2d'), P=[], W, H, dpr=Math.min(devicePixelRatio||1,2), mouse={x:-9e3,y:-9e3}, running=true, born=performance.now();
    function targets(){ var spans=host.querySelectorAll('.giant span'), off=document.createElement('canvas'); off.width=W; off.height=H; var o=off.getContext('2d'), hr=host.getBoundingClientRect(), pts=[];
      spans.forEach(function(sp){ var r=sp.getBoundingClientRect(), cs=getComputedStyle(sp); o.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily; o.textBaseline='alphabetic'; o.fillStyle='#fff';
        var m=o.measureText(sp.textContent); o.fillText(sp.textContent, r.left-hr.left+(r.width-m.width)/2, r.top-hr.top+r.height*0.86); });
      var img=o.getImageData(0,0,W,H).data, gap=9; for(var y=0;y<H;y+=gap) for(var x=0;x<W;x+=gap){ if(img[(y*W+x)*4+3]>128) pts.push([x,y]); }
      return pts; }
    function init(){ var r=host.getBoundingClientRect(); W=Math.round(r.width); H=Math.round(r.height); cv.width=W*dpr; cv.height=H*dpr; c.setTransform(dpr,0,0,dpr,0,0);
      var t=targets(); if(t.length>2400) t=t.filter(function(_,i){ return i%Math.ceil(t.length/2400)===0; });
      P=t.map(function(q){ return {x:Math.random()*W,y:Math.random()*H,tx:q[0],ty:q[1],vx:0,vy:0,s:Math.random()*1.2+0.6,ph:Math.random()*6.28}; }); }
    function frame(now){ if(!running) return; c.clearRect(0,0,W,H); var t=(now-born)/1000;
      for(var i=0;i<P.length;i++){ var p=P[i], dx=p.tx+Math.sin(t*0.8+p.ph)*2-p.x, dy=p.ty+Math.cos(t*0.7+p.ph)*2-p.y;
        p.vx+=dx*0.012; p.vy+=dy*0.012;
        var mx2=p.x-mouse.x, my2=p.y-mouse.y, d2=mx2*mx2+my2*my2; if(d2<14000){ var f=(14000-d2)/14000*1.6; p.vx+=mx2/Math.sqrt(d2+1)*f; p.vy+=my2/Math.sqrt(d2+1)*f; }
        p.vx*=0.86; p.vy*=0.86; p.x+=p.vx; p.y+=p.vy;
        c.fillStyle='rgba(217,185,142,'+(0.22+0.25*Math.sin(t*1.5+p.ph)*0.5+0.12).toFixed(3)+')'; c.fillRect(p.x,p.y,p.s,p.s); }
      requestAnimationFrame(frame); }
    var go=function(){ init(); requestAnimationFrame(frame); };
    (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){ setTimeout(go,150); });
    host.addEventListener('pointermove',function(e){ var r=cv.getBoundingClientRect(); mouse.x=e.clientX-r.left; mouse.y=e.clientY-r.top; });
    host.addEventListener('pointerleave',function(){ mouse.x=mouse.y=-9e3; });
    var rt; addEventListener('resize',function(){ clearTimeout(rt); rt=setTimeout(init,200); });
    if('IntersectionObserver' in window) new IntersectionObserver(function(es){ var v=es[0].isIntersecting; if(v&&!running){ running=true; requestAnimationFrame(frame); } running=v; }).observe(host);
  }
})();
