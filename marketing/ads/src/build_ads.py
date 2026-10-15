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
<div class="head"><h1>Finance your <em>next machine.</em></h1><p class="sub">One application. 40+ lenders. Decisions often in 24–48 hours.</p></div>
<div class="pill"><small>Rates from</small><b>6.99%<sup>*</sup></b><span>for qualified buyers</span></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">Check my rate</span><small>No credit impact<br>to check your options</small></div><p class="note">{RATE_NOTE}</p></div>"""
    page("G1-rate", size, body, css, h1=96)

def g2(size):  # 1 vs 40+
    css = """
.bg img{object-position:78% 70%;filter:saturate(1.05)}
.shade{background:linear-gradient(180deg,rgba(11,21,48,.95) 0%,rgba(11,21,48,.82) 45%,rgba(11,21,48,.35) 75%,rgba(11,21,48,.85) 100%)}
.head{margin-top:44px;display:grid;gap:18px}
.vs{display:grid;grid-template-columns:auto auto;gap:36px;align-items:end;margin-top:var(--vt)}
.vs div{display:grid;gap:6px}
.vs small{font-size:24px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.vs .bank b{font-size:150px;font-weight:900;line-height:.9;color:rgba(255,255,255,.35)}
.vs .bank small{color:#93A3C4}
.vs .nx b{font-size:230px;font-weight:900;line-height:.85;letter-spacing:-.05em;color:#fff;text-shadow:0 0 60px rgba(59,130,246,.55)}
.vs .nx small{color:#9DB8F5}
.bottom{display:grid;gap:20px}
body.s1_1{--vt:40px} body.s4_5{--vt:70px} body.s9_16{--vt:120px}
body.s1_1 .vs .nx b{font-size:200px} body.s1_1 .vs .bank b{font-size:130px}
"""
    body = f"""<div class="bg"><img src="../yard.jpg"></div><div class="shade"></div>
{LOGO}
<div class="head"><h1>Your bank is one lender.<br><em>We bring you 40+.</em></h1></div>
<div class="vs"><div class="bank"><b>1</b><small>Your bank</small></div><div class="nx"><b>40+</b><small>Nexum lenders</small></div></div>
<div class="spacer"></div>
<div class="bottom"><div class="cta"><span class="btn">See my options</span><small>One 5-minute application<br>Offers side by side</small></div><p class="note">{BROKER_NOTE}</p></div>"""
    page("G2-40-lenders", size, body, css, h1=84)

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
<div class="bottom"><div class="cta"><span class="btn">Get matched</span><small>40+ lenders · decisions<br>often in 24–48 hrs</small></div><p class="note">{BROKER_NOTE}</p></div>"""
    page("G3-lineup", size, body, css, h1=80)

# ---------------- Year-end campaign ----------------

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

for fn in (g1, g2, g3, y1, y2, y3):
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
             "Finance new or used equipment through 40+ lenders. Decisions often in 24–48 hours.",
             "See my options", "No credit impact<br>to check", BROKER_NOTE)

def g5(size):
    photo_ad("G5-semi", size, "u-semi.jpg", "60% 60%",
             "Your next truck, <em>financed.</em>",
             "Trucks and trailers for established businesses. One application, 40+ lenders.",
             "Get matched", "5-minute<br>application", BROKER_NOTE)

def g6(size):
    photo_ad("G6-dozer", size, "u-dozer.jpg", "55% 55%",
             "Keep your cash. <em>Finance the dozer.</em>",
             "No-money-down options for qualified borrowers. Compare offers side by side.",
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

for fn in (g4, g5, g6, y4, y5):
    for s in SIZES:
        fn(s)
print("built", len(os.listdir(OUT)), "pages")
