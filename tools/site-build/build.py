import re
import os
HERE=os.path.dirname(os.path.abspath(__file__))+'/'
R=os.path.abspath(HERE+'../..')+'/'
YE_JS=r'''/* ---------- year-end countdown (homepage) ---------- */
var END=new Date(2026,11,31,23,59,59),START=new Date(2026,0,1);
function left(){var t=Math.max(0,(END-new Date())/1000);return{d:Math.floor(t/86400),h:Math.floor(t%86400/3600),m:Math.floor(t%3600/60)}}
var yeEl=$("ye");
if(new Date()>END){yeEl.hidden=true}else{
 var L=left(),groups=yeEl.querySelectorAll(".digits");
 groups.forEach(function(g){var w=g.getAttribute("data-u")==="d"&&L.d>99?3:2,html="";for(var i=0;i<w;i++){var r="";for(var k=0;k<10;k++)r+="<span>"+k+"</span>";html+='<div class="dg"><div class="rail">'+r+"</div></div>"}g.innerHTML=html});
 var setClock=function(first){var v=left();groups.forEach(function(g,gi){var t=String(v[g.getAttribute("data-u")]).padStart(g.children.length,"0");[].forEach.call(g.children,function(dg,i){var r=dg.firstChild;r.style.transitionDelay=first&&!reduce?(gi*.15+i*.08)+"s":"0s";r.style.transform="translateY(-"+(+t[i]*10)+"%)"})});
  var p=Math.min(1,Math.max(0,(new Date()-START)/(END-START)));yeEl.style.setProperty("--p",p.toFixed(4));$("yeNowLbl").textContent="Today · "+v.d+(v.d===1?" day":" days")+" left"};
 if(reduce)setClock(false);else requestAnimationFrame(function(){requestAnimationFrame(function(){setClock(true)})});
 setInterval(function(){if(!document.hidden)setClock(false)},15000);
}

'''
src=open(HERE+'year_end_src.html').read()
# line-of-credit card: plain words for customers who are not native English speakers
for a,b in [('>Draw</text>','>Use it</text>'),('>Repay</text>','>Pay it back</text>'),('>Draw again</text>','>Use it again</text>'),('Draw, repay, draw again.','Use it, pay it back, use it again.'),('so we can match the right lenders.','so we can find the right lender.')]:
    assert src.count(a)==1,a; src=src.replace(a,b)
old=open(HERE+'original_index.html').read()
style=src[src.index('<style>')+7:src.index('</style>')]
# countdown CSS is left in place: unused rules are harmless and cutting lines broke the phone media query
extra='''
/* year-end panel in the hero */
.ye{margin-top:28px;padding:20px 22px 18px;border-radius:16px;background:rgba(11,21,48,.55);box-shadow:inset 0 0 0 1px rgba(157,184,245,.18);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);max-width:560px}
.ye-k{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--sky)}
.ye-k i{width:8px;height:8px;border-radius:50%;background:#F59E0B;box-shadow:0 0 0 4px rgba(245,158,11,.18)}
.ye .clock{margin-top:12px}
.ye .digits{min-height:56px;min-width:83px}
.track{margin-top:40px}
.bar{position:relative;height:8px;border-radius:8px;background:rgba(255,255,255,.1)}
.bar .fill{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:8px;background:linear-gradient(90deg,#1D4ED8,#F59E0B);transform-origin:0 50%;transform:scaleX(var(--p,0));transition:transform 1.4s cubic-bezier(.2,.8,.2,1) .3s}
.bar .now{position:absolute;top:50%;left:calc(var(--p,0)*100%);width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:#fff;box-shadow:0 0 0 4px rgba(245,158,11,.35);transition:left 1.4s cubic-bezier(.2,.8,.2,1) .3s}
.bar .now em{position:absolute;bottom:22px;left:50%;transform:translateX(-50%);white-space:nowrap;font-style:normal;font-size:11px;font-weight:700;color:#fff;background:#1D4ED8;padding:2px 8px;border-radius:10px}
.ends{display:flex;justify-content:space-between;margin-top:8px;font-size:11px;font-weight:600;color:#93A3C4}
.path{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:16px;counter-reset:p}
.path li{position:relative;padding-top:12px;border-top:2px solid rgba(157,184,245,.3);font-size:12px;line-height:1.3;color:#C7D2E8}
.path li.last{border-color:#F59E0B}
.path b{display:block;color:#fff;font-size:13px}
.ye-note{margin-top:14px;font-size:12.5px;line-height:1.5;color:#AEBBD6}
.ye-note a{color:#fff;font-weight:700}
@media (max-width:600px){.ye .digits{min-height:48px;min-width:71px}.hgrid .ye{order:3;margin-top:4px;padding:16px}.path{grid-template-columns:1fr 1fr;row-gap:12px}}

/* homepage sections */
.top a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.nav .links{display:flex;align-items:center;gap:26px}
.nav .links a:not(.btn){color:#D3DCEE;text-decoration:none;font-size:14px;font-weight:600}
.nav .links a:not(.btn):hover{color:#fff}
.feat{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:36px}
.feat article{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:24px;transition:transform .2s ease,box-shadow .2s ease,border-color .2s}
.feat article:hover{transform:translateY(-4px);box-shadow:0 18px 40px -18px rgba(15,23,42,.35);border-color:rgba(29,78,216,.3)}
.feat .ic{width:46px;height:46px;border-radius:12px;background:#EEF3FE;display:grid;place-items:center}
.feat h3{font-size:18px;margin-top:16px}
.feat p{font-size:15px;color:var(--gray2);margin-top:8px}
.serve{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:start}
.serve ul{list-style:none;display:grid;gap:12px;margin-top:26px}
.serve li{display:flex;gap:12px;font-size:16px}
.serve li::before{content:"";flex:0 0 22px;height:22px;margin-top:2px;border-radius:50%;background:var(--blue) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8l3 3 5-6' stroke='white' stroke-width='2' fill='none'/%3E%3C/svg%3E") center/13px no-repeat}
.fit{background:var(--navy);color:#fff;border-radius:18px;padding:30px}
.fit .eyebrow{color:var(--sky)}
.fit p{color:#A9B4C8;font-size:15px;margin-top:10px}
.fit b{display:block;font-size:20px;line-height:1.3;margin-top:22px;padding-top:22px;border-top:1px solid rgba(255,255,255,.12)}
.fit .btn{margin-top:22px;background:#fff;color:var(--navy)}
.fit .btn:hover{background:var(--sky)}
.quotes.q3{grid-template-columns:repeat(3,1fr)}
.stars{color:#F5B301;letter-spacing:2px;font-size:14px}
.rv{transform:translateY(14px);transition:transform .8s cubic-bezier(.2,.7,.3,1)}
.rv.on{transform:none}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:40;padding:10px max(16px,env(safe-area-inset-left)) calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.94);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:0 -8px 24px -12px rgba(15,23,42,.3);transform:translateY(110%);transition:transform .3s ease;display:none}
.sticky .btn{width:100%}
.sticky.show{transform:none}
@media (max-width:960px){.nav .links a:not(.btn){display:none}.feat{grid-template-columns:1fr 1fr}.serve{grid-template-columns:1fr}.quotes.q3{grid-template-columns:1fr}}
@media (max-width:760px){.sticky{display:block}}
/* desktop: tall enough that the excavator sits clear of the form card */
@media (min-width:961px){.hero{min-height:max(760px,min(calc(100vh - 38px),900px))}}
@media (max-width:600px){.feat{grid-template-columns:1fr}}
'''
style=style.replace('@media (max-width:960px){.hgrid','%s\n@media (max-width:960px){.hgrid'%extra,1)
hero_bg=src[src.index('<div class="bg" id="scene"'):src.index('<div class="wrap">',src.index('<div class="bg" id="scene"'))]
card=src[src.index('<div class="card" id="apply"'):src.index('</div>\n</div>\n</header>')]
card=card.replace('<p class="fine" style="font-size:15px">A Nexum advisor is reviewing your request now. Expect to hear from us within 24 hours, often sooner.</p>',
 '<p class="fine" style="font-size:15px">A Nexum financing advisor is reviewing your request for <b id="doneNeed">commercial financing</b> now. Expect to hear from us within 24 hours, often much sooner.</p>\n<p class="fine">Next, an advisor reaches out by phone or email to understand your goals and map the best path to funding.</p>')
assert 'doneNeed' in card
script=src[src.index('<script>\n(function(){'):src.index('</script>',src.index('<script>\n(function(){'))+9]
a=script.index('/* ---------- countdown ---------- */'); b=script.index('/* ---------- attribution')
script=script[:a]+script[b:]
script=script.replace('var END=new Date(2026,11,31,23,59,59), reduce=','var reduce=')
script=script.replace('/* ---------- attribution',YE_JS+'/* ---------- attribution',1)
assert script.count('lead_page:"section-179"')==1
script=script.replace('lead_page:"section-179"','lead_page:"main",language:"en"')
script=script.replace('$("doneH").textContent="Request received, "+first+".";','$("doneH").textContent="Request received, "+first+".";$("doneNeed").textContent=pickVal("need")==="Business line of credit"?"a business line of credit":"commercial equipment financing";')
script=script.replace('})();\n</script>','''
/* ---------- section reveals (content is visible from the start; this only adds a short rise) ---------- */
if(!reduce&&"IntersectionObserver"in window){var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("on");ro.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});
 document.querySelectorAll(".rv").forEach(function(el){var r=el.getBoundingClientRect();if(r.top<innerHeight)el.classList.add("on");else ro.observe(el)})}
else document.querySelectorAll(".rv").forEach(function(el){el.classList.add("on")});

/* ---------- "Q4 2026" in the top strip goes away after December 31 ---------- */
if(new Date()>new Date(2026,11,31,23,59,59))$("q4").hidden=true;

/* ---------- phone: sticky apply button once the form is off screen ---------- */
var sticky=$("sticky");
if("IntersectionObserver"in window){var seen={apply:true,final:false};
 var so=new IntersectionObserver(function(es){es.forEach(function(e){seen[e.target.id]=e.isIntersecting});sticky.classList.toggle("show",!seen.apply&&!seen.final)});
 so.observe(card);so.observe($("final"))}
})();
</script>''')
assert 'sticky' in script
head_old=old[old.index('<helmet>')+8:old.index('<link rel="preconnect"')]
head_old=head_old.replace('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n','')
icons=['<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>','<path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/>','<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>','<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/>']
feats=[("Fast-track approvals","A streamlined digital process delivers decisions in hours or days — not weeks. Get your capital and get to work."),("Industry specialists","We only do commercial equipment financing and business lines of credit. We know your assets and what it takes to get complex deals funded."),("Transparent terms","No hidden fees, no last-minute surprises. Clear, straightforward financing you can understand and trust."),("Dedicated support","From application to funding, one dedicated advisor guides you through every step for a smooth experience.")]
feat_html=''.join(f'<article class="rv"><div class="ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1D4ED8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{i}</svg></div><h3>{t}</h3><p>{b}</p></article>' for i,(t,b) in zip(icons,feats))
faq=re.findall(r'\["(.*?)", "(.*?)"\]',old[old.index('const FAQ'):old.index('const PROOF')])
assert len(faq)==6
faq_html='\n'.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
cmp=src[src.index('<div class="cmp"'):src.index('<div class="quotes">')]
for a,b in [('<span role="rowheader" class="q">Lenders who see your deal</span><span role="cell" class="bk"><b class="big">1</b></span><span role="cell" class="nx"><b class="big">40+</b></span>',
             '<span role="rowheader" class="q">Where your information goes</span><span role="cell" class="bk">One bank, one set of rules</span><span role="cell" class="nx">Only to lenders that fit your deal</span>'),
            ('<span role="rowheader" class="q">If the answer is no</span><span role="cell" class="bk">You start over</span><span role="cell" class="nx">We go to the next lender that fits</span>',
             '<span role="rowheader" class="q">How the lender is chosen</span><span role="cell" class="bk">There is no choice</span><span role="cell" class="nx">We match your deal first, then send it</span>'),
            ('<span role="rowheader" class="q">Offers you compare</span><span role="cell" class="bk">One</span><span role="cell" class="nx">Several, side by side</span>',
             '<span role="rowheader" class="q">Who helps you</span><span role="cell" class="bk">Whoever is free</span><span role="cell" class="nx">One advisor, start to finish</span>')]:
    assert cmp.count(a)==1,a; cmp=cmp.replace(a,b)
html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head_old.strip()}
<link rel="preload" as="image" type="image/webp" media="(min-width:961px)" imagesrcset="/uploads/nightshift-yard-1280.webp 1280w, /uploads/nightshift-yard-2000.webp 2000w" imagesizes="120vw" fetchpriority="high">
<link rel="preload" as="image" type="image/webp" media="(max-width:960px)" imagesrcset="/uploads/nightshift-hero-800.webp 800w, /uploads/nightshift-hero.webp 1344w" imagesizes="100vw" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{style}</style>
</head>
<body>
<a class="skip" href="#apply">Skip to the application</a>
<div class="strip top"><div class="wrap"><span>Now funding · Equipment financing &amp; business lines of credit<span id="q4"> for Q4 2026</span></span><span><a href="#apply">Apply in about 5 minutes →</a></span></div></div>

<header class="hero">
{hero_bg.strip()}
<div class="wrap">
<div class="nav"><a href="/"><img src="/uploads/nexum-logo-sm.png" width="560" height="144" alt="Nexum Commercial Finance"></a><div class="links"><a href="#advantage">Advantage</a><a href="#process">Process</a><a href="#faq">FAQ</a><a class="lang" href="/es/" hreflang="es" lang="es">Español</a><a class="btn" href="#apply"><span class="lg">See my options</span><span class="sm">Apply now</span></a></div></div>
<div class="hgrid">
<div>
<p class="eyebrow" style="color:var(--sky)">Nexum Commercial Finance · DFW &amp; nationwide</p>
<h1 id="h1">One application. <span>More ways to fund your business.</span></h1>
<p class="sub">Get matched with commercial equipment financing and business lines of credit. We match your deal first, then send it only to lenders that fit. Fast decisions, straightforward terms, one relationship with Nexum.</p>
<script>(function(){{var A={{
"stop-renting":["Stop renting. <span>Start owning your equipment.</span>","Your monthly rental could be a payment on a machine you own. We match your deal first, then send it only to lenders that fit."],
"zero-down":["Keep your cash. <span>$0 down for qualified buyers.</span>","Finance new or used equipment with little or nothing down, on approval. We match your deal first, then send it only to lenders that fit."],
"won-the-bid":["Won the bid? <span>Get the machine.</span>","Decisions often in 24–48 hours, so you can start the job on time. We match your deal first, then send it only to lenders that fit."],
"private-sale":["Found it at auction? <span>We can finance it.</span>","Private sales, auctions and dealers. New or used equipment. We match your deal first, then send it only to lenders that fit."]}};
var a=A[(new URLSearchParams(location.search).get("ad")||"").toLowerCase()];if(a){{document.getElementById("h1").innerHTML=a[0];document.querySelector(".hero .sub").textContent=a[1]}}}})()</script>
<ul class="checks"><li>Simple application</li><li>Competitive financing options</li><li>Dedicated support from application to funding</li></ul>
<div class="ye" id="ye" aria-label="Time left in 2026">
<p class="ye-k"><i></i>2026 ends in</p>
<div class="clock"><div class="unit"><div class="digits" data-u="d"></div><small>Days</small></div><div class="sep">:</div><div class="unit"><div class="digits" data-u="h"></div><small>Hours</small></div><div class="sep">:</div><div class="unit"><div class="digits" data-u="m"></div><small>Min</small></div></div>
<div class="track" aria-hidden="true"><div class="bar"><span class="fill" id="yeFill"></span><span class="now" id="yeNow"><em id="yeNowLbl">Today</em></span></div><div class="ends"><span>Jan 1</span><span>Dec 31</span></div></div>
<ol class="path"><li><b>Apply today</b><span>5 minutes</span></li><li><b>Decision</b><span>often 24–48 hrs</span></li><li><b>Funded</b><span>days after docs</span></li><li class="last"><b>On the job</b><span>before Dec 31</span></li></ol>
<p class="ye-note">Get your equipment working before the year ends, and start 2027 ready for bigger jobs. <a href="#apply">Start today →</a></p>
</div>
</div>

{card.strip()}
</div>
</div>
</header>

<div class="proof"><div class="wrap">
<div class="s"><b>$50M+</b><span>Funded by our team</span></div>
<div class="s"><b>24–48 hrs</b><span>Typical decision</span></div>
<div class="s"><b>5 minutes</b><span>To apply</span></div>
<div class="s"><b>No credit impact</b><span>To check your options</span></div>
<div class="s"><b>1 advisor</b><span>Start to finish</span></div>
<div class="s"><b>New &amp; used</b><span>Equipment financed</span></div>
</div></div>

<section class="sec"><div class="wrap">
<p class="eyebrow rv" style="color:var(--blue)">The problem</p>
<h2 class="rv" style="margin-top:12px">Business moves fast. Your financing should too.</h2>
<p class="lede rv">Traditional financing can involve multiple applications, long timelines and limited options. Nexum keeps it simple. We study your business first, then send your file only to lenders that fit your deal. Your information is not passed around.</p>
{cmp.strip()}
</div></section>

<section class="sec" id="advantage" style="background:var(--off)"><div class="wrap">
<p class="eyebrow rv" style="color:var(--blue)">The Nexum advantage</p>
<h2 class="rv" style="margin-top:12px">Financing that moves like you do.</h2>
<p class="lede rv">Deep industry expertise plus modern technology, so you get funded faster on terms you can actually read.</p>
<div class="feat">{feat_html}</div>
</div></section>

<section class="sec"><div class="wrap serve">
<div class="rv">
<p class="eyebrow" style="color:var(--blue)">Who we serve</p>
<h2 style="margin-top:12px">Built for builders.</h2>
<p class="lede">Purpose-built for established businesses in construction, agriculture, transportation and manufacturing that are ready to scale. Based in Dallas-Fort Worth and serving businesses nationwide.</p>
<ul><li>You need new or used heavy equipment quickly to take on bigger projects.</li><li>You're tired of rejections and runaround from traditional banks.</li><li>You want a straightforward process with an expert partner who gets your industry.</li><li>You've been in business a year or more and are ready for the next stage of growth.</li></ul>
</div>
<aside class="fit rv">
<p class="eyebrow">Not the right fit?</p>
<p>This program isn't designed for brand-new startups with no revenue history, or for businesses seeking personal loans.</p>
<b>Built for established businesses ready to make their next move.</b>
<p>Nexum primarily works with operating businesses seeking capital for equipment, expansion and other commercial needs. Qualification requirements vary by lender, financing program, credit profile and business history.</p>
<a class="btn" href="#apply">Check if you qualify</a>
</aside>
</div></section>

<section class="sec" id="process" style="background:var(--off)"><div class="wrap">
<p class="eyebrow rv" style="color:var(--blue)">Our process</p>
<h2 class="rv" style="margin-top:12px">From application to asset in four steps.</h2>
<p class="lede rv">No mountain of paperwork. Just a clear path to capital.</p>
<ol class="tl">
<li class="rv"><p class="when">Step 01</p><h3>Apply online</h3><p>Three short steps, about 5 minutes. No mountain of paperwork to get started.</p></li>
<li class="rv"><p class="when">Step 02</p><h3>Quick review</h3><p>Our specialists review your application and reach out with initial options, often within hours.</p></li>
<li class="rv"><p class="when">Step 03</p><h3>Select your offer</h3><p>We present clear, competitive terms. Choose the option that best fits your business goals.</p></li>
<li class="rv"><p class="when">Step 04</p><h3>Get funded</h3><p>Receive your capital, purchase the equipment and drive your business forward.</p></li>
</ol>
</div></section>

<section class="sec"><div class="wrap">
<p class="eyebrow rv" style="color:var(--blue)">Trusted by operators</p>
<h2 class="rv" style="margin-top:12px">Real businesses. Real approvals.</h2>
<div class="quotes q3">
<blockquote class="rv"><span class="stars" aria-hidden="true">★★★★★</span><p>"We needed a dozer to land a municipal contract and our bank wanted three weeks just to look at it. Nexum had an approval to me the next afternoon. Straight terms, no games."</p><footer>Marcus D. <span>· Texas</span></footer></blockquote>
<blockquote class="rv"><span class="stars" aria-hidden="true">★★★★★</span><p>"I'd been turned down twice because of a rough year. They actually understood my numbers and found a lender who did too. Financed a used excavator with a down payment I could live with."</p><footer>Ray T. <span>· Ohio</span></footer></blockquote>
<blockquote class="rv"><span class="stars" aria-hidden="true">★★★★★</span><p>"Two trucks and a trailer financed in under a week. My advisor picked up every call and explained the financing so I could plan around Section 179 with my CPA. This is how it should work."</p><footer>Alicia M. <span>· Georgia</span></footer></blockquote>
</div>
<p class="fine" style="margin-top:12px">Testimonials reflect individual experiences. Individual results vary.</p>
</div></section>

<section class="sec" id="faq" style="background:var(--off)"><div class="wrap">
<p class="eyebrow rv" style="color:var(--blue)">Questions?</p>
<h2 class="rv" style="margin-top:12px">We have answers.</h2>
<div class="faq">
{faq_html}
</div>
</div></section>

<section class="sec final" id="final"><div class="wrap">
<h2>Ready to upgrade your fleet?</h2>
<p>Don't let financing be the bottleneck. Win more bids, run more efficiently and grow your bottom line. Get your no-obligation options today.</p>
<a class="btn" href="#apply">See my financing options</a>
<p class="fine" style="color:#8B95A8;margin-top:18px">One application. We send your file only to lenders that fit your deal. Approval and terms are subject to lender underwriting.</p>
</div></section>

<footer class="ft"><div class="wrap">
<p>Nexum Commercial Finance is a financing broker, not a lender or bank. We arrange financing through third-party lenders; we do not make credit decisions or guarantee approval. All financing is subject to lender review, credit approval, and final terms, which vary by applicant and lender. Rates, amounts, and timelines described on this page are estimates and examples, not offers or guarantees. Nothing on this site is legal, tax, or financial advice — consult your own accountant or advisor regarding any tax matter.</p>
<p>© 2026 Nexum Commercial Finance. Based in Dallas-Fort Worth, serving businesses nationwide. <a href="#">Privacy Policy</a> · <a href="#">Terms of Service</a></p>
</div></footer>

<div class="sticky" id="sticky"><a class="btn" href="#apply">See my financing options</a></div>

{script}
</body>
</html>
'''
html=html.replace('@media (max-width:760px){.sticky{display:block}}','@media (max-width:760px){.sticky{display:block}}\n@media (max-width:600px){.strip.top .wrap>span:first-child{display:none}.strip.top .wrap>span:last-child{display:inline}.strip.top .wrap{flex-wrap:nowrap;white-space:nowrap}}',1)
html=html.replace('</style>','''
/* proof bar: six facts, 3 across on desktop, 2 across on phones */
.proof .wrap{grid-template-columns:repeat(3,1fr)}
.proof .s{border-left:1px solid rgba(255,255,255,.1);padding-left:18px}
.proof .s:nth-child(3n+1){border-left:0;padding-left:0}
.proof .s:nth-child(n+4){border-top:1px solid rgba(255,255,255,.1)}
@media (max-width:600px){.proof .wrap{grid-template-columns:1fr 1fr}.proof .s{border-left:1px solid rgba(255,255,255,.1);padding-left:14px;border-top:0}.proof .s:nth-child(odd){border-left:0;padding-left:0}.proof .s:nth-child(n+3){border-top:1px solid rgba(255,255,255,.1)}.proof b{font-size:20px}}
</style>''',1)
html=html.replace('<link rel="canonical" href="https://nexumcf.com/">','<link rel="canonical" href="https://nexumcf.com/">\n<link rel="alternate" hreflang="en" href="https://nexumcf.com/">\n<link rel="alternate" hreflang="es" href="https://nexumcf.com/es/">\n<link rel="alternate" hreflang="x-default" href="https://nexumcf.com/">',1)
html=html.replace('</style>','''
/* language switch: always visible, phones included */
.nav .links a.lang:not(.btn){display:inline-flex;align-items:center;padding:7px 12px;border-radius:999px;box-shadow:inset 0 0 0 1.5px rgba(157,184,245,.45);color:#fff;font-size:13px;font-weight:700}
.nav .links a.lang:not(.btn):hover{box-shadow:inset 0 0 0 1.5px #fff}
@media (max-width:960px){.nav .links{gap:10px}}
</style>''',1)
assert 'hreflang="es"' in html
open(R+'index.html','w').write(html)
print(len(html))
