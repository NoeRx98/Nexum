"""Builds the Nexum ad concepts as HTML, one file per concept and size.
Render them with render.mjs (Playwright) into ../out/*.jpg.
Brand: navy #0F172A / ink #0B1530, blue #1D4ED8, sky #9DB8F5, Montserrat, Nexum logo."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "html")
os.makedirs(OUT, exist_ok=True)

SIZES = {"1x1": (1080, 1080), "4x5": (1080, 1350), "9x16": (1080, 1920)}

RATE_NOTE = ("*For qualified buyers. Rate depends on credit profile, time in business, equipment and term. "
             "Not all applicants qualify. Nexum Commercial Finance is a broker, not a lender.")
BROKER_NOTE = "Nexum Commercial Finance is a broker, not a lender. Financing subject to lender approval."
TAX_NOTE = "Section 179 eligibility depends on your business. Ask your CPA. Nexum does not give tax advice."

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:var(--W);height:var(--H);background:#0B1530}
.ad{position:relative;width:var(--W);height:var(--H);overflow:hidden;font-family:Montserrat,sans-serif;color:#fff;display:flex;flex-direction:column;padding:var(--pad)}
.ad>*{position:relative;z-index:2}
.bg{position:absolute!important;inset:0;z-index:0!important}
.bg img{width:100%;height:100%;object-fit:cover}
.shade{position:absolute!important;inset:0;z-index:1!important}
.logo{height:var(--logo);width:auto;display:block;align-self:flex-start}
.eyebrow{font-size:calc(var(--u)*24);font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#9DB8F5}
h1{font-weight:900;letter-spacing:-.03em;line-height:1.02;font-size:calc(var(--u)*var(--h1))}
h1 em{font-style:normal;color:#9DB8F5}
.sub{font-size:calc(var(--u)*30);font-weight:500;line-height:1.35;color:#D3DCEE}
.cta{display:flex;align-items:center;gap:calc(var(--u)*22)}
.btn{background:#1D4ED8;color:#fff;font-weight:800;font-size:calc(var(--u)*32);padding:calc(var(--u)*24) calc(var(--u)*38);border-radius:calc(var(--u)*16);box-shadow:0 18px 40px -16px rgba(29,78,216,.9);white-space:nowrap}
.cta small{font-size:calc(var(--u)*22);font-weight:600;color:#C7D2E8;line-height:1.35}
.note{font-size:calc(var(--u)*16);line-height:1.4;color:rgba(214,222,238,.72);font-weight:500}
.spacer{flex:1}
.chip{justify-self:start;display:inline-flex;align-items:center;gap:10px;background:#F59E0B;color:#0B1530;font-weight:900;font-size:calc(var(--u)*22);letter-spacing:.12em;text-transform:uppercase;padding:calc(var(--u)*10) calc(var(--u)*18);border-radius:999px}
"""

def page(name, size, body, extra_css="", h1=92):
    W, H = SIZES[size]
    tall = {"1x1": 0, "4x5": 1, "9x16": 2}[size]
    # Stories keep text out of the top 250px and bottom 340px that the app's UI covers.
    pad = ["64px 64px 56px", "72px 72px 64px", "250px 72px 340px"][tall]
    html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap"><style>
:root{{--W:{W}px;--H:{H}px;--u:1px;--pad:{pad};--logo:{[84,92,100][tall]}px;--h1:{h1 + [0, 8, 14][tall]}}}
{CSS}{extra_css}</style></head><body class="s{size.replace('x','_')}"><div class="ad">{body}</div></body></html>"""
    with open(os.path.join(OUT, f"{name}_{size}.html"), "w") as f:
        f.write(html)

LOGO = '<img class="logo" src="../logo.png" alt="Nexum Commercial Finance">'

# ---------------- General campaign ----------------

def g1(size):  # Rate pill over the studio excavator
    css = """
.bg img{object-position:50% 100%}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.96) 0%,rgba(11,21,48,.86) 34%,rgba(11,21,48,0) 58%,rgba(11,21,48,0) 72%,rgba(11,21,48,.92) 100%)}
.head{margin-top:44px;display:grid;gap:18px;max-width:900px}
.pill{position:absolute!important;right:var(--pr);top:var(--pt);background:#fff;color:#0F172A;border-radius:28px;padding:26px 34px 24px;box-shadow:0 30px 60px -20px rgba(0,0,0,.6);text-align:left}
.pill small{display:block;font-size:22px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#5B6576}
.pill b{display:block;font-size:112px;font-weight:900;letter-spacing:-.04em;line-height:1;color:#1D4ED8}
.pill b sup{font-size:48px;vertical-align:top;position:relative;top:10px}
.pill span{display:block;font-size:22px;font-weight:700;color:#0F172A;margin-top:4px}
.bottom{display:grid;gap:20px}
body.s1_1{--pr:64px;--pt:480px}
body.s4_5{--pr:72px;--pt:520px}
body.s9_16{--pr:72px;--pt:860px}
body.s1_1 .bg img{object-position:30% 120%}
"""
    body = f"""<div class="bg"><img src="../excavator.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><h1>Finance your <em>next machine.</em></h1><p class="sub">One application, sent only to lenders that fit. Decisions often in 24–48 hours.</p></div>
<div class="pill"><small>Rates from</small><b>6.99%<sup>*</sup></b><span>for qualified buyers</span></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Check my rate</span><small>No credit impact<br>to check your options</small></div><p class="note">{RATE_NOTE}</p></div>"""
    page("G1-rate", size, body, css, h1=96)

def g2(size):  # matched first, then sent: the precision message
    css = """
.bg img{object-position:78% 70%;filter:saturate(1.05)}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.95) 0%,rgba(11,21,48,.82) 45%,rgba(11,21,48,.35) 75%,rgba(11,21,48,.85) 100%)}
.head{margin-top:44px;display:grid;gap:18px}
.vs{display:grid;grid-template-columns:auto 1fr;gap:40px;align-items:center;margin-top:var(--vt)}
.vs svg{width:var(--tg);height:var(--tg);filter:drop-shadow(0 0 40px rgba(59,130,246,.5))}
.vs b{display:block;font-size:64px;font-weight:900;line-height:1.02;letter-spacing:-.02em}
.vs b+b{color:#F59E0B}
.vs small{display:block;margin-top:14px;font-size:26px;font-weight:600;color:#C7D2E8;line-height:1.3}
.bottom{display:grid;gap:20px}
body.s1_1{--vt:36px;--tg:230px} body.s4_5{--vt:70px;--tg:280px} body.s9_16{--vt:120px;--tg:300px}
body.s1_1 .vs b{font-size:56px}
"""
    body = f"""<div class="bg"><img src="../yard.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><h1>We don't send your deal everywhere.<br><em>We send it where it fits.</em></h1></div>
<div class="vs"><svg viewBox="0 0 200 200" fill="none" aria-hidden="true"><circle cx="100" cy="100" r="92" stroke="#9DB8F5" stroke-opacity=".45" stroke-width="4"/><circle cx="100" cy="100" r="62" stroke="#9DB8F5" stroke-opacity=".7" stroke-width="4"/><circle cx="100" cy="100" r="32" stroke="#fff" stroke-width="5"/><path d="M100 0v52M100 148v52M0 100h52M148 100h52" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="100" cy="100" r="12" fill="#F59E0B"/></svg><div><b>Matched first.</b><b>Then sent.</b><small>Your file goes only to lenders<br>that fit your deal.</small></div></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">See my options</span><small>One 5-minute application<br>No credit impact to check</small></div><p class="note">{BROKER_NOTE}</p></div>"""
    page("G2-right-lender", size, body, css, h1=80)

def g3(size):  # machine lineup
    css = """
.ad{background:radial-gradient(120% 80% at 80% 0%,#1E3A8A 0%,#0F1E45 45%,#0B1530 100%)}
.head{margin-top:40px;display:grid;gap:16px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:var(--gt)}
.grid figure{position:relative;border-radius:18px;overflow:hidden;background:#0F172A;box-shadow:0 0 0 1px rgba(157,184,245,.18)}
.grid img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.grid figcaption{position:absolute;left:12px;bottom:12px;background:rgba(11,18,34,.8);padding:6px 14px;border-radius:999px;font-size:20px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#C9D6F2}
.bottom{display:grid;gap:20px}
body.s1_1{--gt:30px} body.s1_1 .grid{grid-template-columns:repeat(4,1fr)} body.s1_1 .grid img{aspect-ratio:3/4} body.s1_1 .grid figcaption{font-size:16px;left:8px;bottom:8px;padding:5px 10px}
body.s4_5{--gt:36px} body.s4_5 .grid img{aspect-ratio:16/10} body.s9_16{--gt:60px}
body.s9_16 .grid{gap:18px}
"""
    tiles = "".join(f'<figure><img src="../{f}.jpg"><figcaption>{c}</figcaption></figure>' for f, c in
                    [("excavator", "Excavators"), ("dozer", "Dozers"), ("wheel-loader", "Loaders"), ("dump-truck", "Trucks")])
    body = f"""{LOGO}
<div class="head"><h1>New or used.<br><em>We finance the iron.</em></h1><p class="sub">Excavators, dozers, loaders, trucks and trailers for established businesses.</p></div>
<div class="grid">{tiles}</div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Get matched</span><small>Only to lenders that fit<br>Decisions often in 24–48 hrs</small></div><p class="note">{BROKER_NOTE}</p></div>"""
    page("G3-lineup", size, body, css, h1=80)

# ---------------- Year-end campaign ----------------
# OFF for 2026: the owner is running only the general campaign this year. The y* functions are kept
# for next year but are not built. Their copy still says "40+ lenders"; rewrite it before reuse.

def y1(size):  # December calendar, 31 circled
    css = """
.ad{background:radial-gradient(110% 70% at 85% 10%,#1E3A8A 0%,#0F1E45 50%,#0B1530 100%)}
.head{margin-top:40px;display:grid;gap:16px}
.cal{margin-top:var(--ct);background:rgba(255,255,255,.04);border-radius:24px;box-shadow:inset 0 0 0 1px rgba(157,184,245,.2);padding:26px 28px 22px}
.cal header{display:flex;justify-content:space-between;align-items:baseline;font-weight:900;font-size:34px;letter-spacing:.02em}
.cal header span{font-size:20px;font-weight:700;color:#93A3C4;letter-spacing:.14em}
.cal .g{display:grid;grid-template-columns:repeat(7,1fr);gap:var(--cg);margin-top:16px;text-align:center}
.cal .g i{font-style:normal;font-size:18px;font-weight:800;color:#5E6F94;letter-spacing:.1em}
.cal .g b{font-size:var(--cf);font-weight:700;color:rgba(214,222,238,.55);line-height:var(--cl)}
.cal .g b.x{color:rgba(214,222,238,.25);text-decoration:line-through;text-decoration-color:rgba(245,158,11,.5)}
.cal .g b.d31{position:relative;color:#0B1530;z-index:0}
.cal .g b.d31::before{content:"";position:absolute;inset:-4px 8px;border-radius:999px;background:#F59E0B;z-index:-1;box-shadow:0 0 0 8px rgba(245,158,11,.25),0 0 40px rgba(245,158,11,.6)}
.bottom{display:grid;gap:20px}
body.s1_1{--ct:26px;--cg:4px;--cf:28px;--cl:44px} body.s1_1 .cal{padding:18px 24px 14px}
body.s4_5{--ct:48px;--cg:8px;--cf:34px;--cl:66px}
body.s9_16{--ct:60px;--cg:10px;--cf:36px;--cl:72px}
"""
    # December 2026 starts on a Tuesday.
    days = "".join(f"<i>{d}</i>" for d in "SMTWTFS")
    days += "<b></b><b></b>"
    for d in range(1, 32):
        cls = "d31" if d == 31 else ("x" if d < 15 else "")
        days += f'<b class="{cls}">{d}</b>'
    body = f"""{LOGO}
<div class="head"><span class="chip">Year-end financing</span><h1>The tax year ends <em>December&nbsp;31.</em></h1><p class="sub">Finance the machine now and put it to work this year.</p></div>
<div class="cal"><header>December <span>2026</span></header><div class="g">{days}</div></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Start before Dec 31</span><small>5-minute application<br>40+ lenders</small></div><p class="note">{TAX_NOTE} {BROKER_NOTE}</p></div>"""
    page("Y1-calendar", size, body, css, h1=86)

def y2(size):  # Night yard + path to Dec 31
    css = """
.bg img{object-position:82% 80%}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.96) 0%,rgba(11,21,48,.8) 40%,rgba(11,21,48,.1) 66%,rgba(11,21,48,.9) 100%)}
.head{margin-top:40px;display:grid;gap:16px}
.path{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:var(--pt)}
.path li{border-top:4px solid rgba(157,184,245,.45);padding-top:14px;font-size:20px;font-weight:600;color:#C7D2E8;line-height:1.3}
.path li b{display:block;font-size:25px;color:#fff;font-weight:800}
.path li.last{border-color:#F59E0B}
.bottom{display:grid;gap:20px}
body.s1_1{--pt:28px} body.s4_5{--pt:40px} body.s9_16{--pt:60px}
body.s9_16 .path{grid-template-columns:1fr 1fr;row-gap:26px}
"""
    body = f"""<div class="bg"><img src="../yard.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><span class="chip">Before Dec 31</span><h1>Put it in service <em>this year.</em></h1></div>
<ol class="path"><li><b>Apply</b>5 minutes</li><li><b>Decision</b>often 24–48 hrs</li><li><b>Funded</b>days after docs</li><li class="last"><b>In service</b>by Dec 31</li></ol>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Start my application</span><small>40+ lenders<br>No credit impact to check</small></div><p class="note">{TAX_NOTE}</p></div>"""
    page("Y2-path", size, body, css, h1=92)

def y3(size):  # Section 179 hook over the studio dozer
    css = """
.bg img{object-position:50% 100%}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.97) 0%,rgba(11,21,48,.86) 38%,rgba(11,21,48,0) 62%,rgba(11,21,48,0) 74%,rgba(11,21,48,.94) 100%)}
.head{margin-top:40px;display:grid;gap:18px;max-width:920px}
.bottom{display:grid;gap:20px}
body.s1_1 .bg img{object-position:50% 140%}
"""
    body = f"""<div class="bg"><img src="../dozer.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><span class="chip">Section 179</span><h1>Planning a year-end <em>equipment purchase?</em></h1><p class="sub">Don't let the financing be what makes you miss the year.</p></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Get matched before Dec 31</span></div><p class="note">{TAX_NOTE} {BROKER_NOTE}</p></div>"""
    page("Y3-section-179", size, body, css, h1=80)

for fn in (g1, g2, g3):
    for s in SIZES:
        fn(s)
print("built", len(os.listdir(OUT)), "pages")

# ---------------- Unsplash photo concepts ----------------
# Photos are the owner's Unsplash picks (free licence), brand badges / plates / windshields blurred in build.

def photo_ad(name, size, img, pos, h1, sub, btn, small, note, chip="", mode="band", h1size=88):
    if mode == "band":
        css = f"""
.bg{{bottom:auto!important;height:var(--bh)}}
.bg img{{object-position:{pos}}}
.shade{{background:linear-gradient(180deg,rgba(11,21,48,.55) 0%,rgba(11,21,48,0) 22%,rgba(11,21,48,0) calc(var(--bh)*.55),#0B1530 var(--bh))}}
.ad{{background:#0B1530}}
body.s1_1{{--bh:640px}} body.s4_5{{--bh:820px}} body.s9_16{{--bh:1180px}}
"""
    else:
        css = f"""
.bg img{{object-position:{pos}}}
.shade{{background:linear-gradient(180deg,rgba(11,21,48,.75) 0%,rgba(11,21,48,.15) 30%,rgba(11,21,48,.25) 52%,rgba(11,21,48,.92) 80%,#0B1530 100%)}}
"""
    css += ".head{display:grid;gap:16px}.bottom{display:grid;gap:20px;margin-top:28px}"
    chip_html = f'<span class="chip">{chip}</span>' if chip else ""
    small_html = f"<small>{small}</small>" if small else ""
    body = f"""<div class="bg"><img src="../{img}"></div><div class="shade"></div>
{LOGO}
<div class="spacer"></div>
<div class="head">{chip_html}<h1>{h1}</h1><p class="sub">{sub}</p></div>
<div class="bottom"><div class="cta"><span class="btn">{btn}</span>{small_html}</div><p class="note">{note}</p></div>"""
    page(name, size, body, css, h1=h1size)

def g4(size):
    photo_ad("G4-haul-truck", size, "u-haul-truck.jpg", "50% 55%",
             "Bigger jobs need <em>bigger iron.</em>",
             "Finance new or used equipment. We send it only to lenders that fit. Decisions often in 24–48 hours.",
             "See my options", "No credit impact<br>to check", BROKER_NOTE)

def g5(size):
    photo_ad("G5-semi", size, "u-semi.jpg", "60% 60%",
             "Your next truck, <em>financed.</em>",
             "Trucks and trailers for established businesses. One application, sent only to lenders that fit.",
             "Get matched", "5-minute<br>application", BROKER_NOTE)

def g6(size):
    photo_ad("G6-dozer", size, "u-dozer.jpg", "55% 55%",
             "Keep your cash. <em>Finance the dozer.</em>",
             "No-money-down options for qualified borrowers. Keep your cash for the job.",
             "Check my options", "No credit impact<br>to check", BROKER_NOTE)

def y4(size):
    photo_ad("Y4-cranes-dusk", size, "u-cranes.jpg", "45% 40%",
             "Tax year 2026 <em>ends December&nbsp;31.</em>",
             "Finance the equipment and put it in service before the year runs out.",
             "Start before Dec 31", "40+ lenders<br>5-minute application", TAX_NOTE + " " + BROKER_NOTE,
             chip="Year-end financing", mode="full", h1size=84)

def y5(size):
    photo_ad("Y5-fleet", size, "u-box-trucks.jpg", "45% 50%",
             "Adding trucks <em>before year-end?</em>",
             "Trucks financed and put in service by December 31 may qualify for Section 179. Ask your CPA.",
             "Get matched before Dec 31", "", TAX_NOTE + " " + BROKER_NOTE, chip="Fleet upgrade")

for fn in (g4, g5, g6):
    for s in SIZES:
        fn(s)
print("built", len(os.listdir(OUT)), "pages")

# ---------------- Round 3: variations to reach 10 per campaign ----------------

def g7(size):
    photo_ad("G7-excavator", size, "excavator.jpg", "50% 70%",
             "Built for contractors, <em>not paperwork.</em>",
             "One 5-minute application, sent only to lenders that fit. No credit impact to check your options.",
             "See my options", "", BROKER_NOTE)

def g8(size):
    photo_ad("G8-bank-said-no", size, "wheel-loader.jpg", "50% 70%",
             "Turned down <em>by your bank?</em>",
             "Your bank is one opinion. We send your deal only to lenders that fit it.",
             "Get a second look", "No credit impact<br>to check", BROKER_NOTE)

def g9(size):
    photo_ad("G9-truck-trailer", size, "truck-trailer.jpg", "45% 70%",
             "Trucks. Trailers. <em>Lowboys.</em>",
             "Financing for established hauling businesses. Decisions often in 24–48 hours.",
             "Get matched", "Only to lenders<br>that fit", BROKER_NOTE)

def list_ad(name, size, img, pos, chip, h1, items, btn, small, note, h1size=84):
    """Numbered steps or a checklist over a darkened photo. No testimonials."""
    css = f"""
.bg img{{object-position:{pos}}}
.shade{{background:linear-gradient(180deg,rgba(11,21,48,.94) 0%,rgba(11,21,48,.7) 45%,rgba(11,21,48,.78) 70%,#0B1530 100%)}}
.head{{margin-top:36px;display:grid;gap:16px}}
.list{{list-style:none;display:grid;gap:var(--lg);margin-top:var(--lt)}}
.list li{{display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;background:rgba(11,21,48,.6);box-shadow:inset 0 0 0 1px rgba(157,184,245,.22);border-radius:18px;padding:18px 22px}}
.list i{{font-style:normal;width:56px;height:56px;border-radius:50%;background:#1D4ED8;display:grid;place-items:center;font-size:26px;font-weight:900}}
.list li.last i{{background:#F59E0B;color:#0B1530}}
.list b{{display:block;font-size:30px;font-weight:800;line-height:1.15}}
.list span{{display:block;font-size:21px;color:#C7D2E8;margin-top:3px}}
.bottom{{display:grid;gap:20px}}
body.s1_1{{--lt:26px;--lg:10px}} body.s1_1 .list li{{padding:12px 18px}} body.s1_1 .list i{{width:46px;height:46px;font-size:22px}} body.s1_1 .list b{{font-size:26px}} body.s1_1 .list span{{font-size:18px}}
body.s4_5{{--lt:40px;--lg:14px}} body.s9_16{{--lt:60px;--lg:18px}}
"""
    rows = "".join(f'<li class="{"last" if i == len(items) - 1 else ""}"><i>{m}</i><div><b>{t}</b><span>{d}</span></div></li>'
                   for i, (m, t, d) in enumerate(items))
    chip_html = f'<span class="chip">{chip}</span>' if chip else ""
    small_html = f"<small>{small}</small>" if small else ""
    body = f"""<div class="bg"><img src="../{img}"></div><div class="shade"></div>
{LOGO}
<div class="head">{chip_html}<h1>{h1}</h1></div>
<ol class="list">{rows}</ol>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">{btn}</span>{small_html}</div><p class="note">{note}</p></div>"""
    page(name, size, body, css, h1=h1size)

def g10(size):
    list_ad("G10-three-steps", size, "yard.jpg", "80% 75%", "How it works",
            "Financing in <em>three steps.</em>",
            [("1", "Apply in 5 minutes", "One short application, no credit impact to check"),
             ("2", "We pick lenders that fit", "Your file goes only where it fits"),
             ("3", "Get your offer", "Clear terms, then you decide")],
            "Start my application", "", BROKER_NOTE)

def y6(size):
    photo_ad("Y6-buy-it-this-year", size, "excavator.jpg", "50% 70%",
             "Buy it in 2026. <em>Put it to work in 2026.</em>",
             "Year-end equipment financing through 40+ lenders. Decisions often in 24–48 hours.",
             "Start before Dec 31", "", TAX_NOTE + " " + BROKER_NOTE, chip="Before Dec 31")

def y7(size):
    photo_ad("Y7-hauling-next-year", size, "u-semi.jpg", "60% 60%",
             "Hauling more next year? <em>Finance the truck this year.</em>",
             "Trucks financed and put in service by December 31 may qualify for Section 179. Ask your CPA.",
             "Get matched before Dec 31", "", TAX_NOTE + " " + BROKER_NOTE, chip="Year-end financing", h1size=80)

def y8(size):
    photo_ad("Y8-179-deadline", size, "u-dozer.jpg", "55% 55%",
             "Section 179 has a deadline. <em>December&nbsp;31.</em>",
             "Finance the equipment now. Ask your CPA what it could mean for this year's taxes.",
             "Start my application", "No credit impact<br>to check", TAX_NOTE + " " + BROKER_NOTE, chip="Section 179")

def y9(size):
    list_ad("Y9-checklist", size, "u-cranes.jpg", "45% 40%", "Year-end checklist",
            "Before <em>December&nbsp;31.</em>",
            [("✓", "Pick the machine", "New or used, the one your jobs need"),
             ("✓", "Apply with Nexum", "5 minutes, 40+ lenders"),
             ("✓", "Get funded", "Often days after documents are in"),
             ("✓", "Put it in service", "On the job before the year closes")],
            "Start before Dec 31", "Ask your CPA about<br>Section 179", TAX_NOTE + " " + BROKER_NOTE)

def y10(size):  # machine lineup, year-end version
    css = """
.ad{background:radial-gradient(120% 80% at 80% 0%,#1E3A8A 0%,#0F1E45 45%,#0B1530 100%)}
.head{margin-top:36px;display:grid;gap:16px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:var(--gt)}
.grid figure{position:relative;border-radius:18px;overflow:hidden;background:#0F172A;box-shadow:0 0 0 1px rgba(157,184,245,.18)}
.grid img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.grid figcaption{position:absolute;left:12px;bottom:12px;background:rgba(11,18,34,.8);padding:6px 14px;border-radius:999px;font-size:20px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#C9D6F2}
.grid figure.hot{box-shadow:0 0 0 3px #F59E0B}
.bottom{display:grid;gap:20px}
body.s1_1{--gt:26px} body.s1_1 .grid{grid-template-columns:repeat(4,1fr)} body.s1_1 .grid img{aspect-ratio:3/4} body.s1_1 .grid figcaption{font-size:16px;left:8px;bottom:8px;padding:5px 10px}
body.s4_5{--gt:32px} body.s4_5 .grid img{aspect-ratio:16/10} body.s9_16{--gt:56px}
"""
    tiles = "".join(f'<figure><img src="../{f}.jpg"><figcaption>{c}</figcaption></figure>' for f, c in
                    [("excavator", "Excavators"), ("dozer", "Dozers"), ("wheel-loader", "Loaders"), ("dump-truck", "Trucks")])
    body = f"""{LOGO}
<div class="head"><span class="chip">Year-end financing</span><h1>Whatever you're buying, <em>fund it before Dec&nbsp;31.</em></h1></div>
<div class="grid">{tiles}</div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Get matched</span><small>40+ lenders · decisions<br>often in 24–48 hrs</small></div><p class="note">{TAX_NOTE} {BROKER_NOTE}</p></div>"""
    page("Y10-lineup", size, body, css, h1=76)

for fn in (g7, g8, g9, g10):
    for s in SIZES:
        fn(s)
print("built", len(os.listdir(OUT)), "pages")

# ---------------- Round 4: situation ads (each links to /?ad=<key> so the homepage headline matches) ----------------
ZERO_NOTE = ("$0 down is available for qualified buyers, on lender approval. Not all applicants qualify. "
             "Nexum Commercial Finance is a broker, not a lender.")

def g11(size):  # stop renting: rent vs finance table   -> /?ad=stop-renting
    css = """
.bg img{object-position:50% 70%}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.96) 0%,rgba(11,21,48,.8) 40%,rgba(11,21,48,.55) 62%,rgba(11,21,48,.95) 100%)}
.head{margin-top:36px;display:grid;gap:16px}
.cmp{margin-top:var(--ct);border-radius:20px;overflow:hidden;background:rgba(11,21,48,.72);box-shadow:inset 0 0 0 1px rgba(157,184,245,.25)}
.cmp div{display:grid;grid-template-columns:1fr 150px 150px;align-items:center;padding:var(--rp) 26px;border-top:1px solid rgba(157,184,245,.15)}
.cmp div:first-child{border-top:0;padding-top:16px;padding-bottom:12px}
.cmp div:first-child span{font-size:22px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#93A3C4;text-align:center}
.cmp div:first-child span.nx{color:#fff;background:#1D4ED8;border-radius:10px;padding:6px 0}
.cmp b{font-size:28px;font-weight:700}
.cmp i{font-style:normal;text-align:center;font-size:40px;font-weight:900;line-height:1}
.cmp i.y{color:#22C55E} .cmp i.n{color:#64748B}
.bottom{display:grid;gap:20px}
body.s1_1{--ct:26px;--rp:14px} body.s1_1 .cmp b{font-size:24px} body.s1_1 .cmp i{font-size:34px}
body.s4_5{--ct:44px;--rp:22px} body.s9_16{--ct:70px;--rp:28px}
"""
    rows = [("Monthly payment", "y", "y"), ("It's yours at the end", "n", "y"), ("Adds value to your business", "n", "y")]
    mark = {"y": "✓", "n": "✕"}
    table = '<div><span></span><span>Rent</span><span class="nx">Finance</span></div>' + "".join(
        f'<div><b>{t}</b><i class="{a}">{mark[a]}</i><i class="{b}">{mark[b]}</i></div>' for t, a, b in rows)
    body = f"""<div class="bg"><img src="../wheel-loader.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><h1>Stop renting.<br><em>Start owning.</em></h1><p class="sub">Your monthly rental could be a payment on a machine you own.</p></div>
<div class="cmp">{table}</div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">See my options</span><small>No credit impact<br>to check</small></div><p class="note">{BROKER_NOTE}</p></div>"""
    page("G11-stop-renting", size, body, css, h1=92)

def g12(size):  # $0 down pill over the studio dozer   -> /?ad=zero-down
    css = """
.bg img{object-position:50% 100%}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.96) 0%,rgba(11,21,48,.86) 34%,rgba(11,21,48,0) 58%,rgba(11,21,48,0) 72%,rgba(11,21,48,.92) 100%)}
.head{margin-top:44px;display:grid;gap:18px;max-width:900px}
.pill{align-self:flex-start;margin-top:var(--pt);background:#fff;color:#0F172A;border-radius:28px;padding:24px 34px 22px;box-shadow:0 30px 60px -20px rgba(0,0,0,.6)}
.pill small{display:block;font-size:22px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#5B6576}
.pill b{display:block;font-size:128px;font-weight:900;letter-spacing:-.04em;line-height:1;color:#1D4ED8}
.pill span{display:block;font-size:22px;font-weight:700;margin-top:4px}
.bottom{display:grid;gap:20px}
body.s1_1{--pt:24px} body.s4_5{--pt:36px} body.s9_16{--pt:60px}
body.s1_1 .bg img{object-position:40% 120%}
body.s1_1 .pill b{font-size:96px} body.s1_1 .pill{padding:18px 28px 16px}
"""
    body = f"""<div class="bg"><img src="../dozer.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><h1>Keep your cash.<br><em>Get the machine.</em></h1><p class="sub">Finance new or used equipment with little or nothing down.</p></div>
<div class="pill"><small>Down payment</small><b>$0</b><span>for qualified buyers</span></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">See if I qualify</span><small>No credit impact<br>to check</small></div><p class="note">{ZERO_NOTE}</p></div>"""
    page("G12-zero-down", size, body, css, h1=86)

def g13(size):  # won the bid   -> /?ad=won-the-bid
    photo_ad("G13-won-the-bid", size, "u-cranes.jpg", "45% 40%",
             "Won the bid? <em>Get the machine.</em>",
             "Decisions often in 24–48 hours, so you can start the job on time.",
             "Get matched", "No credit impact<br>to check", BROKER_NOTE, chip="New contract?")

def g14(size):  # private sale / auction   -> /?ad=private-sale
    photo_ad("G14-private-sale", size, "dump-truck.jpg", "50% 70%",
             "Found it at auction? <em>We can finance it.</em>",
             "Private sales, auctions and dealers. New or used equipment.",
             "See my options", "No credit impact<br>to check", BROKER_NOTE, chip="Private sale · Auction · Dealer")

for fn in (g11, g12, g13, g14):
    for s in SIZES:
        fn(s)
print("built", len(os.listdir(OUT)), "pages")
