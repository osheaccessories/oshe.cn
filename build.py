#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""欧奢内贸站页面生成器 — 按 sxl「锻造工业」模板风格"""
import pathlib, json, os

# CSS 版本号：样式文件一变，URL 立即变化，绕过浏览器/CDN 缓存
_css = pathlib.Path(__file__).parent / "assets" / "style.css"
CSSV = f"v={int(_css.stat().st_mtime)}-{_css.stat().st_size}"

ROOT = pathlib.Path("/workspace/site-cn")
KEY = "622fb2ca-f8a6-48c6-940f-2927be959635"   # Web3Forms Access Key（复用外贸站，提交发到 163 邮箱）
SITE = "https://oshee.cn"                   # 先占位：正式域名确定后全局替换

def _img(name):
    """images/ 下静态图的带版本号 URL（轮播/横幅换图后缓存自动失效）"""
    p = ROOT / "images" / name
    return f"/images/{name}{_ver(p)}"

SAMPLE_CATS = ["餐厨用具", "储物水具", "家居摆件", "五金配件"]

def _ver(p):
    """给图片 URL 附带内容版本号，换图后浏览器/边缘缓存自动失效"""
    try:
        return "?v=" + str(int(p.stat().st_mtime)) + "-" + str(p.stat().st_size)
    except OSError:
        return ""


NAV = [("首页","/"),("样品展示","/samples/"),("服务","/services/"),("关于","/about/"),("博客","/blog/"),("联系我们","/contact/")]

def nav_html(cur):
    out = []
    for name, href in NAV:
        cls = ' class="on"' if href == cur or (cur != "/" and href != "/" and cur.startswith(href)) else ""
        out.append(f'<a{cls} href="{href}">{name}</a>')
    return "\n".join(out)

def page(fname, title, desc, body, cur, h1=None, sub=None, crumb=None, breadcrumb=True):
    nav_cls = "nav"
    """生成一个完整页面。fname 为相对路径，cur 为导航高亮项。"""
    url = SITE + ("/" + fname.replace("index.html","").rstrip("/") if fname != "index.html" else "/")
    hero = ""
    if h1:
        inner = f"<h1>{h1}</h1>" + (f"<p>{sub}</p>" if sub else "")
        if crumb:
            inner = f'<div class="crumb" style="color:rgba(255,255,255,.6)">{crumb}</div>' + inner
        hero = f'<section class="page-hero"><div class="wrap">{inner}</div></section>'
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="web3forms-verify" content="{KEY}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="欧奢五金">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<link rel="stylesheet" href="/assets/style.css?{CSSV}">
</head>
<body>
<div class="topbar"><div class="wrap">
  <a class="brand" href="/"><span class="brand-mark">{BRAND_SVG_DARK}</span>欧奢五金·拉链</a>
  <div class="lang"><span class="cur">中文</span>&nbsp;/&nbsp;<a href="https://osheaccessories.com/" target="_blank" rel="noopener">English</a></div>
</div></div>
<header class="nav">
  <div class="nav-in">
    <nav class="nav-links">
{nav_html(cur)}
    </nav>
  </div>
</header>
{hero}
<main>
{body}
</main>
<footer class="footer">
  <div class="footer-in">
    <div>
      <div class="brand"><span class="brand-mark">{BRAND_SVG_LIGHT}</span>欧奢五金·拉链</div>
      <p>欧奢（东莞）五金有限公司<br>箱包五金 · 不锈钢拉链源头工厂</p>
      <p>广东省东莞市长安镇厦边社区<br>大板地一路10号8幢</p>
    </div>
    <div>
      <h4>快速导航</h4>
      <a href="/">首页</a>
      <a href="/samples/">样品展示</a>
      <a href="/services/">服务</a>
      <a href="/about/">关于我们</a>
    </div>
    <div>
      <h4>了解我们</h4>
      <a href="/samples/">样品展示</a>
      <a href="/services/">定制服务</a>
      <a href="/blog/">博客</a>
      <a href="/about/">关于我们</a>
    </div>
    <div>
      <h4>联系方式</h4>
      <a href="tel:18002758559">📱 180 0275 8559（微信同号）</a>
      <a href="mailto:sales@osheaccessories.com">✉ sales@osheaccessories.com</a>
      <p>周一至周六 08:30–18:30</p>
    </div>
  </div>
  <div class="footer-bottom"><div class="fb-in">
    <span>© {YEAR} 欧奢（东莞）五金有限公司 版权所有</span>
    <!-- ICP 备案通过后，在此加入备案号，例如：<span>粤ICP备XXXXXXXX号</span> -->
  </div></div>
</footer>

<div class="backtop"><button type="button" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="回到顶部">↑</button></div>
<div class="float">
  <div class="float-item">
    <button class="float-btn" type="button" data-panel="fTel" aria-label="电话微信">📱</button>
    <div class="float-panel" id="fTel">
      <b>电话 / 微信</b>
      <span class="fp-num">180 0275 8559（微信同号）</span>
    </div>
  </div>
  <div class="float-item">
    <button class="float-btn" type="button" data-panel="fMail" aria-label="邮箱">✉</button>
    <div class="float-panel" id="fMail">
      <b>电子邮箱</b>
      <span class="fp-num">sales@osheaccessories.com</span>
    </div>
  </div>
</div>
<script>
(function(){{
  var slides=document.querySelectorAll('.hero .slide'), dots=document.querySelectorAll('.hero-dots span');
  if(slides.length && dots.length){{
    var cur=0, timer=null;
    function show(i){{
      cur=i;
      slides.forEach(function(s,j){{ s.classList.toggle('on', j===i); }});
      dots.forEach(function(d,j){{ d.classList.toggle('on', j===i); }});
    }}
    function next(){{ show((cur+1) % slides.length); }}
    function arm(){{ clearInterval(timer); timer=setInterval(next, 6000); }}
    dots.forEach(function(d,i){{ d.addEventListener('click', function(){{ show(i); arm(); }}); }});
    arm();
  }}
  var bar=document.querySelector('.float'); if(!bar) return;
  bar.addEventListener('click',function(e){{
    var btn=e.target.closest('.float-btn');
    if(!btn) return;
    var item=btn.parentElement, was=item.classList.contains('open');
    bar.querySelectorAll('.float-item.open').forEach(function(x){{x.classList.remove('open');}});
    clearTimeout(bar._t);
    if(!was){{
      item.classList.add('open');
      bar._t=setTimeout(function(){{ bar.querySelectorAll('.float-item.open').forEach(function(x){{x.classList.remove('open');}}); }},7000);
    }}
  }});
  document.addEventListener('click',function(e){{ if(!bar.contains(e.target)) bar.querySelectorAll('.float-item.open').forEach(function(x){{x.classList.remove('open');}}); }});
  document.addEventListener('keydown',function(e){{ if(e.key==='Escape') bar.querySelectorAll('.float-item.open').forEach(function(x){{x.classList.remove('open');}}); }});
  var p = new URLSearchParams(location.search);
  var ok = document.getElementById('formOk'), er = document.getElementById('formErr');
  var f = document.querySelector('form[action*="web3forms"]');
  var box = (p.get('sent') === '1' && ok) ? ok : (p.get('sent') === '0' && er) ? er : null;
  if (box && f) {{
    box.hidden = false; f.insertBefore(box, f.firstChild);
    box.scrollIntoView({{block:'center',behavior:'smooth'}});
    setTimeout(function(){{ box.classList.add('fade'); setTimeout(function(){{ box.hidden = true; }}, 700); }}, 6000);
    history.replaceState(null, '', location.pathname);
  }}
}})();
</script>
</body>
</html>'''
    p = ROOT / fname
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    print("✓", fname)

YEAR = 2025

FORM = f'''<div class="form-ok" id="formOk" hidden><span><b>询价已提交，谢谢！</b>我们会在工作时间内 12 小时回复您。急事请直接拨打 180 0275 8559（微信同号）。</span></div>
<div class="form-err" id="formErr" hidden><span><b>提交失败。</b>请重试，或直接加微信 / 拨打 180 0275 8559。</span></div>
<form action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="{KEY}">
  <input type="hidden" name="subject" value="内贸站询价 — {{SUBJ}}">
  <input type="hidden" name="from_name" value="欧奢内贸站">
  <input type="hidden" name="redirect_to" value="{{REDIR}}?sent=1">
  <input type="checkbox" name="botcheck" class="hp" style="display:none" tabindex="-1" autocomplete="off">
  <label>您的称呼 <span class="req">*</span></label>
  <input type="text" name="name" required placeholder="如：张经理 / 东莞市××箱包厂">
  <label>手机 / 微信号 <span class="req">*</span></label>
  <input type="text" name="phone" required placeholder="方便我们直接联系您">
  <label>采购需求 <span class="req">*</span></label>
  <textarea name="message" rows="5" required placeholder="产品类型、规格尺寸、数量、有没有图纸或样品，都可以写在这里"></textarea>
  <button class="btn btn-accent" type="submit">提交询价</button>
  <p class="form-note">提交后 12 小时内回复；急单请直接打电话或加微信（180 0275 8559）。</p>
</form>'''


# 品牌 "Ō" 图形：圆环 + 人字帽（参照用户提供的图形，无背景方块）
BRAND_SVG_DARK = ('<svg viewBox="0 0 100 98" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
  '<path d="M0 31 L50 0 L100 31 L100 44 L50 13 L0 44 Z" fill="#1c1c1e"/>'
  '<circle cx="50" cy="65" r="23.5" fill="none" stroke="#1c1c1e" stroke-width="13"/></svg>')
BRAND_SVG_LIGHT = BRAND_SVG_DARK.replace('#1c1c1e', '#ffffff')

def form(subj, redir):
    return FORM.replace("{SUBJ}", subj).replace("{REDIR}", SITE + redir)

# ═══════════════════════ 首页 ═══════════════════════
index_body = f'''
<section class="hero">
  <div class="slides"><div class="slide on" style="background-image:url({_img('zip-hero-1.jpg')})"></div><div class="slide" style="background-image:url({_img('zip-pull.jpg')})"></div><div class="slide" style="background-image:url({_img('zip-hero-4.jpg')})"></div><div class="shade"></div></div>
  <div class="wrap hero-in">
    <div class="hero-tag"><span>OSHE HARDWARE</span></div>
    <h1>拉链与箱包五金<br><span class="em">一站式制造</span></h1>
    <p class="hero-sub">用心做好每一件五金 · 12 年源头工厂 · 支持按图来样定制</p>
    <div class="hero-cta">
      <a class="btn btn-accent" href="/samples/">样品展示</a>
      <a class="btn btn-ghost" href="/contact/">联系我们</a>
    </div>
  </div>
  <div class="hero-dots"><span class="on"></span><span></span><span></span></div>
</section>


<div class="keywords"><div class="wrap"><b>热门关键词：</b>铜箱包五金、不锈钢五金、不锈钢拉链、压铸锌合金、D 环 / 三角环 / 插扣、按图定制</div></div>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">三大产品线</span>
      <span class="en">PRODUCTS</span>
      <p>铜五金、不锈钢五金、不锈钢拉链，均支持按图纸或样品定制。实物与工艺细节请看样品展示。</p>
    </div>
    <div class="grid grid-3">
      <div class="pcard">
        <div class="pcard-media">产 品 图 片 占 位</div>
        <div class="pcard-body">
          <h3>铜箱包五金</h3>
          <p>铜质 D 环、三角环、八字扣、插扣、铆钉、脚钉等。材质 H62/H65 黄铜，表面滚光、电镀、仿古多种工艺。</p>
          <div class="pcard-meta"><span>100 件起订</span></div>
        </div>
      </div>
      <div class="pcard">
        <div class="pcard-media">产 品 图 片 占 位</div>
        <div class="pcard-body">
          <h3>不锈钢箱包五金</h3>
          <p>304/316 不锈钢环扣、勾扣、调节扣、拉片。强度高、不生锈，适合户外包、工具包、医卫行业箱包。</p>
          <div class="pcard-meta"><span>100 件起订</span></div>
        </div>
      </div>
      <div class="pcard">
        <div class="pcard-media">产 品 图 片 占 位</div>
        <div class="pcard-body">
          <h3>不锈钢拉链</h3>
          <p>316 不锈钢链牙拉链，耐盐雾、耐腐蚀，#3/#5/#8 等规格，支持开口、闭口、双头拉链定制。</p>
          <div class="pcard-meta"><span>100 条起订</span></div>
        </div>
      </div>
    </div>
    
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">核心工序 · 全部自有车间完成</span>
      <span class="en">CAPABILITY</span>
      <p>主要工序自有车间完成，不转包、不外包——这是交期和品质的底气。</p>
    </div>
    <div class="cap-grid">
      <div class="cap-card" style="background:linear-gradient(rgba(14,17,21,.45),rgba(14,17,21,.72)),url(/images/cap-polish.jpg) center/cover"><h3>打磨抛光</h3><p>机打与手抛结合，边角圆滑无毛刺，手感与光泽一致。</p></div>
      <div class="cap-card" style="background:linear-gradient(rgba(14,17,21,.45),rgba(14,17,21,.72)),url(/images/cap-tumble.jpg) center/cover"><h3>振动研磨</h3><p>批量去毛刺与镜面处理，大批量订单光泽均匀不花。</p></div>
      <div class="cap-card" style="background:linear-gradient(rgba(14,17,21,.45),rgba(14,17,21,.72)),url(/images/cap-wash.jpg) center/cover"><h3>超声波清洗</h3><p>出机前超声波除油除屑，洁净达标才转下一道工序。</p></div>
      <div class="cap-card" style="background:linear-gradient(rgba(14,17,21,.45),rgba(14,17,21,.72)),url(/images/cap-sanding.jpg) center/cover"><h3>平面砂光</h3><p>平面件精密砂光，保证平整度与扣合手感。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">六大合作保障</span>
      <span class="en">WHY US</span>
    </div>
    <div class="grid grid-3">
      <div class="card"><span class="num">01</span><h3>工厂直供，没有中间商</h3><p>自有厂房与生产线，价格直接对接产能。同等品质下，比贸易商低 10%–20%。</p></div>
      <div class="card"><span class="num">02</span><h3>打样快，起订低</h3><p>有库存样 2–3 天寄出，定制样 15 天内完成；100 件起订，混色混码下单，减少您的库存压力。</p></div>
      <div class="card"><span class="num">03</span><h3>品质看得见</h3><p>支持第三方验货（SGS / BV 等），可保留留样对照。出厂前全检外观与尺寸，24 小时内响应客诉。</p></div>
      <div class="card"><span class="num">04</span><h3>包装可定制</h3><p>包装可印您的 logo、按您的装箱规格执行，发货前拍照确认。</p></div>
      <div class="card"><span class="num">05</span><h3>交期稳定</h3><p>大货常规 30 天内交货，旺季提前排产锁定产能。</p></div>
      <div class="card"><span class="num">06</span><h3>付款简单</h3><p>30% 定金排产，发货前付清余款；对公转账，开具发票。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">从询价到收货，五步搞定</span>
      <span class="en">PROCESS</span>
    </div>
    <div class="steps">
      <div class="step"><b>询价 / 寄样</b><p>发图纸、样品或需求清单</p></div>
      <div class="step"><b>3D 打样确认</b><p>3–7 天出 1:1 白样，确认后锁价</p></div>
      <div class="step"><b>支付定金</b><p>30% 定金，排产锁定交期</p></div>
      <div class="step"><b>生产质检</b><p>30 天内完成，全检出货</p></div>
      <div class="step"><b>发货结算</b><p>付清余款，物流全国直达</p></div>
    </div>
  </div>
</section>

<section class="banner banner--photo">
  <div class="wrap">
    <h2>把您的图纸变成实物</h2>
    <p>发图纸或样品给我们，当天报价，48 小时内给出打样方案。</p>
    <a class="btn btn-accent" href="/contact/">联系我们</a>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">欧奢 · 新闻资讯</span>
      <span class="en">NEWS</span>
    </div>
    <div class="news-split">
      <a class="news-lead" href="/blog/">
        <img src="/images/cap-tumble.jpg" alt="振动研磨车间实拍">
        <div class="body"><span class="date">即将上线</span><h3>箱包五金怎么选：铜的、钢的、锌合金的到底差在哪</h3></div>
      </a>
      <div class="news-list">
        <a class="item" href="/blog/"><span class="idx">01</span><div><h3>304 和 316 不锈钢差在哪？一张表看懂</h3><span class="date">即将上线</span><p>户外包、医卫包、海边用的包，材质选错就是客诉的开始。</p></div></a>
        <a class="item" href="/blog/"><span class="idx">02</span><div><h3>为什么你的拉链用半年就拉不动了</h3><span class="date">即将上线</span><p>拉链卡齿、锈死的真正原因，以及验收拉链该看哪几项。</p></div></a>
        <a class="item" href="/blog/"><span class="idx">03</span><div><h3>五金件验货看哪几项？给你一份核对清单</h3><span class="date">即将上线</span><p>外观、尺寸、盐雾、扣合力——照着验，不吃亏。</p></div></a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">采购前您可能想问的</span>
      <span class="en">FAQ</span>
    </div>
    <details open><summary>起订量是多少？能混色混码吗？</summary><div class="ans">五金件和拉链均 100 件（条）起订，支持混颜色、混规格下单，按总量计算，不必每个颜色单独达到起订量。</div></details>
    <details><summary>打样要多久？收费吗？</summary><div class="ans">有库存样 2–3 天寄出；按图纸定制的样品约 15 天。样品费与运费视产品而定，确认大货订单后可在货款中抵扣。</div></details>
    <details><summary>大货交期多久？</summary><div class="ans">常规 30 天内交货，具体视数量与工艺，下单时书面确认交期。</div></details>
    <details><summary>怎么付款？</summary><div class="ans">30% 定金排产，发货前付清 70% 余款，对公转账，可开具增值税发票。</div></details>
    <details><summary>质量问题怎么办？</summary><div class="ans">出厂前全检；收货后发现质量问题，24 小时内响应处理，补货或退款按合同约定执行。</div></details>
    <details><summary>包装能印我的 logo 吗？</summary><div class="ans">可以。内包装、外箱均可按您的要求印刷 logo 与唛头，出货前拍照确认。</div></details>
  </div>
</section>'''
page("index.html", "欧奢五金 — 箱包五金与不锈钢拉链源头工厂 | 欧奢（东莞）五金有限公司",
     "欧奢（东莞）五金有限公司：12 年箱包五金、不锈钢拉链源头工厂。铜五金、不锈钢五金、316 不锈钢拉链按图定制，100 件起订，混色混码，30 天交货。",
     index_body, "/",
     h1=None)

# ═══════════════════════ 样品展示 ═══════════════════════
# 产品以用户命名为准；images/samples/<slug>/ 内：main.jpg 白底首图，main-N.jpg 其余白底图，detail-N.jpg 细节实拍
SAMPLE_PRODUCTS = [
    ("spoon",           "多功能勺子",   "餐厨用具"),
    ("ring-spoon",      "环形柄勺子",   "餐厨用具"),
    ("knife",           "餐刀",         "餐厨用具"),
    ("cutlery-set",     "餐具四件套",   "餐厨用具"),
    ("nutcracker",      "胡桃钳",       "餐厨用具"),
    ("corkscrew",       "红酒开瓶器",   "餐厨用具"),
    ("bowl",            "碗",           "餐厨用具"),
    ("fruit-bowl",      "高脚果盘",     "餐厨用具"),
    ("canister",        "储物罐",       "储物水具"),
    ("canister-blue",   "储物罐（蓝）", "储物水具"),
    ("kettle",          "水壶",         "储物水具"),
    ("ornament",        "摆件",         "家居摆件"),
    ("ornament-flower", "摆件花",       "家居摆件"),
    ("candleholder",    "烛台",         "家居摆件"),
    ("candleholder-sm", "小烛台",       "家居摆件"),
    ("vase",            "花瓶",         "家居摆件"),
    ("reindeer",        "麋鹿",         "家居摆件"),
    ("branch",          "配件",         "家居摆件"),
    ("leaf-ornament",   "配件底座",     "家居摆件"),
    ("round-tray",      "配件圆饼",     "家居摆件"),
    ("cup",             "杯子",         "储物水具"),
    ("tea-canister",    "茶罐",         "储物水具"),
    ("teapot",          "茶壶",         "储物水具"),
    ("lamp-base",       "底座",         "五金配件"),
    ("hinge",           "合页",         "五金配件"),
    ("hinge set",       "合页套装",     "五金配件"),
    ("fine-part",       "精细配件",     "五金配件"),
    ("corkscrew-bent",  "开瓶器（弯柄款）", "餐厨用具"),
]
def scan_products():
    out = []
    for slug, name, cat in SAMPLE_PRODUCTS:
        d = ROOT / "images/samples" / slug
        if not (d / "main.jpg").exists():
            continue
        mains = ["main.jpg"] + [f"main-{i}.jpg" for i in range(2, 9) if (d / f"main-{i}.jpg").exists()]
        details = [f"detail-{i}.jpg" for i in range(1, 9) if (d / f"detail-{i}.jpg").exists()]
        imgs = [("/images/samples/" + slug + "/" + m + _ver(d / m), "白底图") for m in mains] \
             + [("/images/samples/" + slug + "/" + dt + _ver(d / dt), "细节图") for dt in details]
        out.append(dict(slug=slug, name=name, cat=cat, main=imgs[0][0], imgs=imgs, n=len(imgs)))
    return out

PRODUCTS_DATA = scan_products()

_filt = ['<button type="button" class="on" data-f="all">全部<em>%d</em></button>' % len(PRODUCTS_DATA)]
for _cat in SAMPLE_CATS:
    _n = sum(1 for _p in PRODUCTS_DATA if _p["cat"] == _cat)
    _filt.append(f'<button type="button" data-f="{_cat}">{_cat}<em>{_n}</em></button>')

_cards = []
for _i, _p in enumerate(PRODUCTS_DATA):
    _cards.append(
        f'<button type="button" class="gal-item" data-i="{_i}" data-c="{_p["cat"]}">'
        f'<span class="gal-img"><img src="{_p["main"]}" alt="{_p["name"]} 白底样品图 — 欧奢五金" loading="lazy"></span>'
        f'<span class="gal-name">{_p["name"]}</span>'
        f'<span class="gal-n">{_p["n"]} 张实拍 · 点击查看</span>'
        f'</button>')

import json as _json
_DATA_JS = _json.dumps([dict(name=_p["name"], cat=_p["cat"], imgs=_p["imgs"]) for _p in PRODUCTS_DATA],
                       ensure_ascii=False).replace("</", "<\\/")

_gal_js = r"""(function(){
  var bar=document.querySelector('.gal-bar'), grid=document.querySelector('.gal-grid');
  if(bar&&grid){
    bar.addEventListener('click',function(e){
      var b=e.target.closest('button'); if(!b) return;
      bar.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on');
      var f=b.dataset.f;
      grid.querySelectorAll('.gal-item').forEach(function(it){
        it.style.display=(f==='all'||it.dataset.c===f)?'':'none';
      });
    });
  }
  var DATA=""" + _DATA_JS + r""";
  var pm=document.getElementById('pmodal'); if(!pm) return;
  var pmImg=document.getElementById('pmImg'), pmName=document.getElementById('pmName'),
      pmCat=document.getElementById('pmCat'), pmCount=document.getElementById('pmCount'),
      pmThumbs=document.getElementById('pmThumbs');
  var cur=0, idx=0;
  function render(){
    var p=DATA[cur];
    pmName.textContent=p.name; pmCat.textContent=p.cat;
    pmCount.textContent=(idx+1)+' / '+p.imgs.length+' · '+p.imgs[idx][1];
    pmImg.src=p.imgs[idx][0]; pmImg.alt=p.name+' '+p.imgs[idx][1];
    pmThumbs.innerHTML='';
    p.imgs.forEach(function(im,i){
      var b=document.createElement('button');
      if(i===idx) b.className='on';
      var t=document.createElement('img'); t.src=im[0]; t.alt='';
      b.appendChild(t);
      b.addEventListener('click',function(){ idx=i; render(); });
      pmThumbs.appendChild(b);
    });
    var on=pmThumbs.querySelector('.on'); if(on) on.scrollIntoView({block:'nearest',inline:'nearest'});
  }
  function open(i){ cur=i; idx=0; render(); pm.classList.add('on'); document.body.style.overflow='hidden'; }
  function close(){ pm.classList.remove('on'); document.body.style.overflow=''; pmImg.removeAttribute('src'); }
  document.querySelectorAll('.gal-item').forEach(function(c){
    c.addEventListener('click',function(){ open(+c.dataset.i); });
  });
  pm.querySelector('.pm-close').addEventListener('click',close);
  pm.addEventListener('click',function(e){ if(e.target===pm) close(); });
  document.addEventListener('keydown',function(e){
    if(!pm.classList.contains('on')) return;
    if(e.key==='Escape') close();
    if(e.key==='ArrowLeft'){ idx=(idx-1+DATA[cur].imgs.length)%DATA[cur].imgs.length; render(); }
    if(e.key==='ArrowRight'){ idx=(idx+1)%DATA[cur].imgs.length; render(); }
  });
  pm.querySelector('.pm-prev').addEventListener('click',function(){ idx=(idx-1+DATA[cur].imgs.length)%DATA[cur].imgs.length; render(); });
  pm.querySelector('.pm-next').addEventListener('click',function(){ idx=(idx+1)%DATA[cur].imgs.length; render(); });
})();"""

samples_body = f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">不锈钢器具定制样品</span>
      <span class="en">SAMPLE GALLERY</span>
      <p>勺子、碗、储物罐、水壶、摆件、烛台……都是本厂打样与量产的实物：首图为白底样品图，点开可看材质、钢印、工艺细节。</p>
    </div>
    <div class="gal-bar">{"".join(_filt)}</div>
    <div class="gal-grid">{"".join(_cards)}</div>
    <p class="gal-note">说明：样品图为工艺与结构参考，尺寸、材质（201 / 304 / 316）、表面处理均可按您的图纸调整；涉及客户私模的产品不公开展示。</p>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">器具定制能到什么程度</span>
      <span class="en">CAPABILITY</span>
      <p>不是只能做标准件——从材料、成形到表面，每一环都能按你的要求调。</p>
    </div>
    <div class="grid grid-3">
      <div class="card"><span class="num">01</span><h3>材质可选</h3><p>304 食品级（样品勺身带 SUS304 钢印）、316 耐盐雾耐酸碱、430 导磁适配电磁炉、201 成本更优，来料可提供材质报告。</p></div>
      <div class="card"><span class="num">02</span><h3>成形工艺</h3><p>冲压、拉伸、旋压、激光切割、氩弧焊、点焊、卷边，厚料薄料都能上，异形件开模打样。</p></div>
      <div class="card"><span class="num">03</span><h3>表面处理</h3><p>镜面抛光、拉丝、喷砂、电解、镀钛金色 / 黑色 / 玫瑰金，也可做磨砂防指纹。</p></div>
      <div class="card"><span class="num">04</span><h3>尺寸定制</h3><p>从拇指大的调料碟到直径 40cm 的盆，按图放样；公差按图纸要求控制，关键尺寸可全检。</p></div>
      <div class="card"><span class="num">05</span><h3>logo 与包装</h3><p>激光打标、蚀刻、压印三种上标方式；内盒、彩盒、说明卡按您的品牌做，出货前拍照确认。</p></div>
      <div class="card"><span class="num">06</span><h3>小批量也接</h3><p>常规款 100 件起，开模定制按模具费+数量核算，打样费确认大货后可抵货款。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">先见实物，再开模具</span>
      <span class="en">3D PRINTING PROTOTYPE</span>
      <p>图纸或方案一经确认，我们会先用 3D 打印把样品按 1:1 打出来——造型、比例、结构装配在开模之前就能亲手确认，改型只需改打印文件，不动模具、不花模具费。</p>
    </div>
    <div class="proto">
      <figure class="proto-lead">
        <img src="/images/process/3d-print-group.jpg" alt="3D 打印样品实拍：烛台、摆件、相框等按客户图纸 1:1 打印的白样">
        <figcaption>3D 打印白样实拍：烛台、摆件、相框、餐具……1:1 还原图纸造型</figcaption>
      </figure>
      <div class="proto-row">
        <figure>
          <img src="/images/process/3d-print-detail-1.jpg" alt="3D 打印样品细节：烛台托盘与珠链杆身成型效果" loading="lazy">
          <figcaption>异形曲面、串珠杆身照样清晰成型</figcaption>
        </figure>
        <figure>
          <img src="/images/process/3d-print-detail-2.jpg" alt="3D 打印样品细节：壁厚与底座比例与量产实物一致" loading="lazy">
          <figcaption>壁厚、底座比例与量产件一致</figcaption>
        </figure>
        <div class="proto-note">
          <b>为什么先打 3D 样？</b>
          <ul>
            <li><b>看得见摸得着</b>：屏幕上的效果图和实物是两回事，拿到手才能判断比例和握感</li>
            <li><b>改型零模具成本</b>：不满意只改打印文件，反复调整到满意再开模</li>
            <li><b>避免开模后返工</b>：结构、装配关系在白样阶段全部验证完</li>
            <li><b>交期更快</b>：3D 样 3–7 天到手，比直接开模试产快得多</li>
          </ul>
        </div>
      </div>
      <figure class="proto-lead">
        <img src="/images/process/metal-finish.jpg" alt="3D 打样确认后的不锈钢成品：镜面抛光电镀实拍" loading="lazy">
        <figcaption>白样确认后转入五金量产：镜面抛光 + 电镀，成品质感在打样阶段就能预判</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">从一张图到一批货</span>
      <span class="en">PROCESS</span>
    </div>
    <div class="steps">
      <div class="step"><b>发图 / 寄样</b><p>照片、手绘图、CAD 都行</p></div>
      <div class="step"><b>工艺评估</b><p>48 小时给方案与报价</p></div>
      <div class="step"><b>3D 打样确认</b><p>3–7 天出 1:1 白样，确认后开模</p></div>
      <div class="step"><b>批量生产</b><p>30% 定金排产</p></div>
      <div class="step"><b>验货发货</b><p>全检后物流直达</p></div>
    </div>
  </div>
</section>

<section class="section section--soft" id="inquiry">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start">
      <div>
        <div class="sec-head" style="text-align:left;margin-bottom:18px">
          <span class="bar">有样品或图纸？发过来</span>
          <span class="en">ENQUIRY</span>
          <p>写清用途、数量、材质要求即可，工艺问题我们帮你判断。</p>
        </div>
        <ul style="font-size:14.5px;color:var(--ink-2);line-height:2.2">
          <li>📱 电话 / 微信：<b>180 0275 8559</b>（微信同号，可直接发图）</li>
          <li>✉ 邮箱：<b>sales@osheaccessories.com</b></li>
          <li>🏭 地址：东莞市长安镇厦边社区大板地一路10号8幢</li>
          <li>🕘 周一至周六 08:30–18:30</li>
        </ul>
      </div>
      <div class="form">{form("内贸站询价 — 不锈钢器具定制", "/samples/")}</div>
    </div>
  </div>
</section>

<div class="pmodal" id="pmodal">
  <div class="pm-box">
    <button class="pm-close" type="button" aria-label="关闭">×</button>
    <div class="pm-head"><b id="pmName"></b><span id="pmCat"></span><span class="pm-count" id="pmCount"></span></div>
    <div class="pm-stage">
      <button class="pm-arrow pm-prev" type="button" aria-label="上一张">‹</button>
      <img id="pmImg" alt="">
      <button class="pm-arrow pm-next" type="button" aria-label="下一张">›</button>
    </div>
    <div class="pm-thumbs" id="pmThumbs"></div>
  </div>
</div>
<script>
{_gal_js}
</script>'''

page("samples/index.html", "样品展示 — 不锈钢餐具/厨具/器具定制实拍 | 欧奢五金",
     "欧奢五金不锈钢器具定制样品展示：多功能勺子、碗、储物罐、水壶、摆件、摆件花、烛台，白底主图+细节实拍，304/316 食品级材质，按图来样定制，100 件起。",
     samples_body, "/samples/",
     h1="样品展示", sub="不锈钢器具定制 · 白底主图 + 细节实拍 · 来图来样打样。")

# ═══════════════════════ 服务 ═══════════════════════
svc_body = f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">不只是生产，更是帮您把事办成</span>
      <span class="en">SERVICES</span><p>从一张图纸到一整批货，每个环节都有人对接。</p></div>
    <div class="grid grid-3">
      <div class="card"><span class="num">服务 01</span><h3>来图来样定制</h3><p>发 CAD 图、手绘图甚至一张照片都可以评估。工程师 48 小时内给出工艺建议、成本区间和打样时间。</p></div>
      <div class="card"><span class="num">服务 02</span><h3>快速打样</h3><p>有库存样 2–3 天寄出；定制样 15 天内完成并寄送。确认大货后样品费在货款中抵扣。</p></div>
      <div class="card"><span class="num">服务 03</span><h3>OEM / ODM 代工</h3><p>按您的品牌要求生产，包装印您的 logo，对外信息严格保密，可签保密协议。</p></div>
      <div class="card"><span class="num">服务 04</span><h3>第三方验货支持</h3><p>支持 SGS、BV 等第三方验货机构进厂抽检，也可保留留样供比对，质量责任说得清楚。</p></div>
      <div class="card"><span class="num">服务 05</span><h3>包装定制</h3><p>内盒、外箱、唛头按您的要求印刷，出货前拍照确认，避免装错混发。</p></div>
      <div class="card"><span class="num">服务 06</span><h3>售后保障</h3><p>质量客诉 24 小时内响应，补货、返工、退款按合同约定执行，不拖延不扯皮。</p></div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">订单是怎么跑起来的</span>
      <span class="en">PROCESS</span></div>
    <div class="steps">
      <div class="step"><b>询价</b><p>当天回复报价</p></div>
      <div class="step"><b>3D 打样</b><p>3–7 天出 1:1 白样</p></div>
      <div class="step"><b>定金</b><p>30% 排产</p></div>
      <div class="step"><b>生产</b><p>30 天内交货</p></div>
      <div class="step"><b>发货</b><p>全国物流直达</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">服务于多元市场</span>
      <span class="en">INDUSTRIES</span><p>不同行业对五金的要求差别很大，我们按场景推荐材质与工艺。</p></div>
    <div class="chips">
      <div class="chip">箱包手袋厂<small>女包 / 男包 / 旅行箱</small></div>
      <div class="chip">户外与军迷装备<small>登山包 / 战术包，推荐 316</small></div>
      <div class="chip">服装辅料公司<small>皮带扣 / 装饰扣 / 拉链</small></div>
      <div class="chip">医卫与母婴<small>卫生防护、无毒材质需求</small></div>
      <div class="chip">工具与劳保包<small>高强度受力部位定制</small></div>
      <div class="chip">宠物用品<small>牵引扣 / 调节扣，耐咬耐蚀</small></div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">批量下单怎么合作</span>
      <span class="en">B2B COOPERATION</span><p>专供批发商、贸易商、品牌方的大货条款，都写在明面上。</p></div>
    <div class="grid grid-2" style="margin-bottom:26px">
      <div class="card"><h3>对公结算，可开发票</h3><p>支持对公转账，可开增值税发票（专票 / 普票按您的需要）。合同、报价单、送货单齐全，财务对账不费劲。</p></div>
      <div class="card"><h3>欢迎实地验厂</h3><p>下单前可来东莞长安看车间、看设备、看现成货；也可委托第三方（SGS / BV 等）进厂验货。提前一天预约即可。</p></div>
      <div class="card"><h3>打样先确认再排产</h3><p>大货前必须先确认样品，样品留档，出货按样对照。避免"做出来和想的不一样"的扯皮。</p></div>
      <div class="card"><h3>老客户账期可谈</h3><p>首次合作 30% 定金 + 发货前付清；稳定合作后可谈账期与月结，具体以合同约定为准。</p></div>
    </div>
    <table class="tbl">
      <tr><th>订购数量</th><th>价格方式</th><th>配套服务</th></tr>
      <tr><td>100 – 999 件 / 条</td><td>页面示例价（标准价）</td><td>混色混码、包装印 logo</td></tr>
      <tr><td>1,000 – 4,999 件 / 条</td><td><b>批量价，按数量核价</b></td><td>专属跟单、分批交货可谈</td></tr>
      <tr><td>5,000 件 / 条以上</td><td><b>专属核价，价格更优</b></td><td>可谈账期、优先排产、留备品</td></tr>
    </table>
    <p style="font-size:13px;color:var(--muted);margin-top:12px">具体折扣按材质、工艺、数量综合核定，把需求发我们，当天给出阶梯报价单。</p>
  </div>
</section>
<section class="banner" style="background-image:linear-gradient(rgba(16,16,18,.55),rgba(16,16,18,.62)),url({_img('zip-ring.jpg')});background-size:cover;background-position:center"><div class="wrap"><h2>有图纸？发过来聊聊</h2><p>评估免费，报价透明，不合适也不打扰。</p><a class="btn btn-accent" href="/contact/">联系我们</a></div></section>'''
page("services/index.html", "定制服务 — 来图来样 | OEM代工 | 快速打样 | 欧奢五金",
     "欧奢五金定制服务：来图来样定制、OEM/ODM 代工、2–15 天打样、支持第三方验货、包装印 logo、24 小时客诉响应。",
     svc_body, "/services/",
     h1="服务", sub="来图来样定制 · OEM/ODM · 打样 · 验货 · 售后，一站对接。")

# ═══════════════════════ 关于 ═══════════════════════
about_body = f'''
<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center">
      <div>
        <span class="eyebrow">关于我们</span>
        <h2 style="font-size:26px;margin-bottom:16px">做了 12 年五金的东莞工厂</h2>
        <p style="font-size:15px;color:var(--ink-2)">欧奢（东莞）五金有限公司位于东莞市长安镇，专注箱包五金与不锈钢拉链生产 12 年。从铜件冲压、不锈钢精密铸造到拉链装配，主要工序都在自有车间完成——这就是我们能承诺"100 件起订、30 天交货、品质全检"的底气。</p>
        <p style="font-size:15px;color:var(--ink-2);margin-top:12px">我们不做"什么都接"的贸易商：只做五金和拉链，只按可验证的标准交付。客户寄来的样品我们会保留留样，出过的货能对得上账。</p>
      </div>
      <img src="/images/banner-assembly.jpg" alt="欧奢五金装配车间实拍" style="width:100%;height:320px;object-fit:cover;border-radius:4px">
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b>12 年</b><span>生产经验</span></div>
      <div class="stat"><b>100 件</b><span>起订量</span></div>
      <div class="stat"><b>30 天</b><span>大货交期</span></div>
      <div class="stat"><b>24 小时</b><span>客诉响应</span></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="mv">
      <div class="mv-card">
        <span class="en">Mission · 使命</span>
        <h3>让中小箱包厂用上"大厂品质"的五金</h3>
        <p>100 件也能下单，混色混码不设门槛。我们想把"起订量大、打样慢、交期不确定"从箱包行业的采购清单里划掉。</p>
      </div>
      <div class="mv-card">
        <span class="en">Vision · 愿景</span>
        <h3>做最可验证的箱包五金工厂</h3>
        <p>留样可查、验货欢迎、客诉当天响应。客户对我们最大的认可不是夸奖，而是把下一单放心地交过来。</p>
      </div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid grid-2">
      <div class="card"><h3>我们的承诺</h3><p>不展示没拿到的检测报告，不接做不到的交期，不报含水分的价格。能做就说能做，做不到就说做不到。</p></div>
      <div class="card"><h3>工厂信息</h3><p>欧奢（东莞）五金有限公司<br>地址：广东省东莞市长安镇厦边社区大板地一路10号8幢<br>欢迎客户实地看厂，提前一天预约即可。</p></div>
    </div>
  </div>
</section>
<section class="banner"><div class="wrap"><h2>欢迎来厂里坐坐</h2><p>看车间、看设备、看货比听人说一百句都实在。</p><a class="btn btn-accent" href="/contact/">预约看厂</a></div></section>'''
page("about/index.html", "关于我们 — 12年箱包五金源头工厂 | 欧奢（东莞）五金有限公司",
     "欧奢（东莞）五金有限公司：位于东莞长安，12 年箱包五金与不锈钢拉链生产经验，100 件起订，欢迎实地看厂。",
     about_body, "/about/",
     h1="关于欧奢", sub="源头工厂 · 只做五金和拉链 · 品质可验证。")

# ═══════════════════════ 博客 ═══════════════════════
blog_body = f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="bar">行业知识与选材干货</span>
      <span class="en">NEWS</span><p>五金怎么选、拉链怎么验、定制怎么避坑——每周更新。</p></div>
    <div class="grid grid-3">
      <div class="blog-item"><img class="blog-thumb" src="/images/cap-tumble.jpg" alt="振动研磨车间实拍"><div class="blog-body"><span class="date">即将上线</span><h3>箱包五金怎么选：铜的、钢的、锌合金的到底差在哪</h3><p>从重量、强度、成本三个维度对比常见材质，看完就会选。</p></div></div>
      <div class="blog-item"><img class="blog-thumb" src="/images/cap-polish.jpg" alt="打磨抛光工位实拍"><div class="blog-body"><span class="date">即将上线</span><h3>304 和 316 不锈钢差在哪？一张表看懂</h3><p>户外包、医卫包、海边用的包，材质选错就是客诉的开始。</p></div></div>
      <div class="blog-item"><img class="blog-thumb" src="/images/cap-sanding.jpg" alt="平面砂光车间实拍"><div class="blog-body"><span class="date">即将上线</span><h3>为什么你的拉链用半年就拉不动了</h3><p>拉链卡齿、锈死的真正原因，以及验收拉链该看哪几项。</p></div></div>
    </div>
  </div>
</section>
<section class="banner" style="background-image:linear-gradient(rgba(16,16,18,.6),rgba(16,16,18,.66)),url({_img('zip-dark.jpg')});background-size:cover;background-position:center"><div class="wrap"><h2>想看什么主题？</h2><p>关注我们的公众号或加微信，选题您说了算。</p><a class="btn btn-accent" href="/contact/">联系我们</a></div></section>'''
page("blog/index.html", "博客 — 五金选材与行业干货 | 欧奢五金",
     "欧奢五金博客：箱包五金选材、不锈钢知识、拉链验收与定制避坑指南，每周更新。",
     blog_body, "/blog/",
     h1="博客", sub="选材干货 · 行业知识 · 定制指南。")

# ═══════════════════════ 联系我们 ═══════════════════════
contact_body = f'''
<section class="section">
  <div class="wrap">
    <div class="contact-cards">
      <div class="cc">
        <div class="ic">📱</div>
        <b>电话 / 微信</b>
        <p class="big">180 0275 8559</p>
        <p>微信同号，加好友备注"询价"<br>周一至周六 08:30–18:30</p>
      </div>
      <div class="cc">
        <div class="ic">✉</div>
        <b>电子邮箱</b>
        <p class="big" style="font-size:14.5px">sales@osheaccessories.com</p>
        <p>图纸、样品照发这里，当天回复</p>
      </div>
      <div class="cc">
        <div class="ic">🏭</div>
        <b>工厂地址</b>
        <p>广东省东莞市长安镇<br>厦边社区大板地一路10号8幢</p>
        <p style="margin-top:6px">看厂请提前一天预约</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft" id="inquiry">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start">
      <div>
        <div class="sec-head" style="text-align:left;margin-bottom:18px">
      <span class="bar">留下需求，我们找您</span>
      <span class="en">ENQUIRY</span><p>也可以直接加微信或打电话，都能找到人。</p></div>
        <ul style="font-size:14.5px;color:var(--ink-2);line-height:2.2">
          <li>① 写清产品类型（铜五金 / 不锈钢五金 / 拉链）</li>
          <li>② 尽量带上规格、数量、使用场景</li>
          <li>③ 有图纸或样品照可发邮箱或微信</li>
          <li>④ 工作日当天回复报价与打样方案</li>
        </ul>
        <!-- 微信二维码：<img src="/images/wechat-qr.jpg" alt="微信二维码" width="150"> 生成二维码后取消注释 -->
      </div>
      <div class="form">{form("内贸站询价 — 联系我们页", "/contact/")}</div>
    </div>
  </div>
</section>'''
page("contact/index.html", "联系我们 — 电话/微信/邮箱 | 欧奢五金",
     "联系欧奢五金：电话/微信 180 0275 8559，邮箱 sales@osheaccessories.com，地址东莞市长安镇厦边社区大板地一路10号8幢，在线询价当天回复。",
     contact_body, "/contact/",
     h1="联系我们", sub="电话、微信、邮箱、在线表单，选您方便的方式。")

print("\n全部页面生成完毕")
