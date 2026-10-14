"""Build KinAlert's scam search pages into site/scams/<slug>/index.html.

Run from the site folder:  python3 tools/build_scam_pages.py
Facts per page must come from official sources (GOV.UK, DVLA, Royal Mail, UK Finance). Source list is kept in SOURCES.
"""
import html
import json
from pathlib import Path

SITE = "https://kinalert.co.uk"
OUT = Path(__file__).resolve().parent.parent / "scams"

LOGO = ('<svg width="30" height="30" viewBox="0 0 30 30" aria-hidden="true"><rect width="30" height="30" rx="9" fill="#0e6b4f"/>'
        '<path d="M15 6.8l7 2.8v5.4c0 4.3-3 7.4-7 8.6-4-1.2-7-4.3-7-8.6V9.6l7-2.8z" fill="#fff"/>'
        '<path d="M11.6 15.2l2.4 2.4 4.4-4.6" fill="none" stroke="#0e6b4f" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

REPORT_FRAUD = "If you've lost money, call your bank straight away, then report it to Report Fraud (formerly Action Fraud) at reportfraud.police.uk or on 0300 123 2040."

PAGES = [
    {
        "slug": "royal-mail-scam-text",
        "title": "Royal Mail scam text: is it real? Check it free",
        "h1": "Got a Royal Mail text asking you to pay a fee?",
        "desc": "Fake Royal Mail texts say a parcel is held until you pay a small fee. Check yours free, see the red flags and what to do.",
        "lead": "Scam texts pretending to be Royal Mail are common. They usually say a parcel is on hold and ask you to pay a small fee through a link. Paste yours below to check it.",
        "from": "Text from an unknown number",
        "example": "Royal Mail: Your parcel is on hold due to an unpaid shipping fee of £1.45. Pay now to avoid return: royalmail-redeliver-uk.com",
        "flags": ["A small fee (often around £1–£3) to “release” or redeliver a parcel", "A link to a web address that isn't royalmail.com", "Pressure: pay today or the parcel goes back", "It arrived from a normal mobile number"],
        "todo": ["Don't click the link or enter card details.", "Check any real parcel yourself at royalmail.com/track-your-item using the tracking number from the sender.", "Send a screenshot of the text to reportascam@royalmail.com, and forward the text to 7726 for free.", REPORT_FRAUD],
        "faq": [("Does Royal Mail ever text about fees?", "Treat any text asking you to pay through a link with suspicion. Royal Mail says not to click the link or enter details in texts like this, and to check tracking on its own website."), ("I already paid. What now?", "Call your bank straight away using the number on the back of your card, so they can try to stop the payment and block your card.")],
    },
    {
        "slug": "hmrc-scam-text",
        "title": "HMRC tax refund scam text: is it real? Check it free",
        "h1": "Got a text from “HMRC” about a tax refund?",
        "desc": "HMRC never tells you about a tax rebate by text. Check a suspicious HMRC message free, see the red flags and how to report it.",
        "lead": "Fake HMRC messages promise a tax refund or threaten a fine, then send you to a link that steals your card or bank details. Paste yours below to check it.",
        "from": "Text claiming to be HMRC",
        "example": "HMRC: You are due a tax refund of £326.40. Claim before midnight: hmrc-refund-gov.co",
        "flags": ["A tax refund you weren't expecting", "A deadline like “claim before midnight”", "A link that isn't gov.uk", "Asking for card or bank details to “receive” the refund"],
        "todo": ["Don't click the link or reply.", "Forward suspicious HMRC texts to 60599 (network rates apply), and HMRC emails to phishing@hmrc.gov.uk, then delete them.", "Check your tax yourself by signing in at gov.uk, not through a link in a message.", REPORT_FRAUD],
        "faq": [("Does HMRC text about tax refunds?", "No. GOV.UK says HMRC will never send notifications of a tax rebate, or ask you to share personal or payment information, by text message."), ("What if it came by email?", "HMRC only emails about rebates or asks for details from addresses ending in hmrc.gov.uk. Forward anything suspicious to phishing@hmrc.gov.uk.")],
    },
    {
        "slug": "dvla-scam-text",
        "title": "DVLA scam text: vehicle tax refund or fine? Check it free",
        "h1": "Got a text from “DVLA” about a refund or unpaid tax?",
        "desc": "DVLA doesn't send texts about vehicle tax refunds. Check a suspicious DVLA message free and see what to do.",
        "lead": "Fake DVLA texts claim you're owed a vehicle tax refund, or that your tax has failed, and send you to a fake site. Paste yours below to check it.",
        "from": "Text claiming to be DVLA",
        "example": "DVLA: Your vehicle tax payment failed. To avoid a £1000 fine update your details at dvla-vehicletax.uk",
        "flags": ["A refund you didn't ask for, or a threat of a big fine", "A link that isn't gov.uk", "Asking you to “update” or “confirm” bank details", "Urgent wording to rush you"],
        "todo": ["Don't click the link or enter any details.", "Check your vehicle tax yourself on gov.uk.", "Forward the text to 7726 for free.", REPORT_FRAUD],
        "faq": [("Does DVLA text about tax refunds?", "No. DVLA has warned: “we don't send text messages about vehicle tax refunds.” Delete the message and don't click the link."), ("I clicked the link. What now?", "If you didn't enter anything, close the page. If you entered card or bank details, call your bank straight away.")],
    },
    {
        "slug": "hi-mum-scam",
        "title": "“Hi Mum” scam: new number from your child? Check it free",
        "h1": "Got a “Hi Mum, this is my new number” message?",
        "desc": "The Hi Mum scam pretends to be your child on a new number and asks for money. Check the message free and learn the warning signs.",
        "lead": "Scammers message parents pretending to be their son or daughter on a new number, then ask for money for an urgent bill. Paste the message below to check it.",
        "from": "WhatsApp or text from an unknown number",
        "example": "Hi Mum, I dropped my phone in the toilet, this is my new number. Can you help me pay a bill today? I'll pay you back tomorrow x",
        "flags": ["A new number with a story about a lost or broken phone", "They avoid a normal phone call", "An urgent bill, usually paid to a “friend's” account", "Voice notes can now be faked with AI, so a voice isn't proof"],
        "todo": ["Don't send money or bank details.", "Call your child on their old, normal number, or ask something only they would know.", "If it's a scam, block the number and forward texts to 7726.", REPORT_FRAUD],
        "faq": [("How much do people lose?", "UK banks say victims usually lose up to around £3,000, but some parents have sent far more over several payments."), ("Can they fake my child's voice?", "Yes. Banks have warned that scammers use AI to create voice notes. Always check by calling the normal number.")],
    },
    {
        "slug": "safe-account-scam",
        "title": "“Safe account” scam call from your bank? Check it free",
        "h1": "Your “bank” called and told you to move your money?",
        "desc": "Banks never ask you to move money to a safe account. Learn how the safe account scam works and check a suspicious message free.",
        "lead": "A caller says they're from your bank or the police, that your account is at risk, and that you must move your money to a “safe account”. There is no such thing. Describe what happened below to check it.",
        "from": "Phone call from “your bank”",
        "example": "Call from my bank: they said there is fraud on my account and I need to move my savings to a new safe account today.",
        "flags": ["You're told to move money to keep it safe", "They say it's urgent and to keep it secret, even from bank staff", "The number on your phone looks like your bank's (numbers can be faked)", "They ask for a code that's just been texted to you"],
        "todo": ["Hang up. Your bank will never ask you to move money to a safe account.", "Call 159 to reach your real bank safely, ideally from a different phone.", "Never share codes texted to you, or install apps a caller asks for.", REPORT_FRAUD],
        "faq": [("What is 159?", "159 is a free number that connects you to your own bank's fraud team, so you know you're talking to the real bank."), ("Will I get my money back?", "Since October 2024, UK banks must refund most victims of this kind of push-payment fraud, up to £85,000. Call your bank straight away.")],
    },
    {
        "slug": "whatsapp-add-my-number-scam",
        "title": "“Add my number on WhatsApp” scam calls: what to do",
        "h1": "Getting calls asking you to “add my number on WhatsApp”?",
        "desc": "Automated calls asking you to add a number on WhatsApp are the first step of a scam. Find out why and check suspicious messages free.",
        "lead": "Lots of UK phones are getting automated calls saying “can you add my number on WhatsApp?”. It moves you onto WhatsApp, past phone spam filters, where fake jobs and money requests follow. Paste anything that follows below to check it.",
        "from": "Call from an unknown mobile",
        "example": "Hello. Can you please add my number on WhatsApp? I want to talk to you.",
        "flags": ["A recorded voice or bot, not someone you know", "Calls that hang up after the message", "Then: job offers, investment tips, or requests for money on WhatsApp"],
        "todo": ["Don't add the number or reply.", "Hang up and block the number.", "Turn on WhatsApp two-step verification so no one can take over your account.", REPORT_FRAUD],
        "faq": [("What happens if I add the number?", "Reports describe fake job and task scams, WhatsApp account takeovers and requests for money."), ("How do I stop the calls?", "Block each number. On iPhone you can also turn on Settings → Phone → Silence Unknown Callers.")],
    },
    {
        "slug": "ai-voice-clone-scam",
        "title": "AI voice clone scam: a call from your child asking for money?",
        "h1": "Got a panicked call from your child asking for money?",
        "desc": "Scammers can copy a voice with AI from a few seconds of video. Learn how the AI voice clone scam works, how to set a family safe word, and check messages free.",
        "lead": "Scammers can copy someone's voice with AI from just a few seconds of a video posted online. They call a parent or grandparent sounding like their child, crying and asking for money right now. Here's how to spot it, and how a family safe word stops it.",
        "from": "Phone call or voice note that sounds like your child or grandchild",
        "example": "Call from my son, crying. He said he crashed the car and needs me to send £2,000 to the other driver now, and not to tell his dad.",
        "flags": ["Panic and urgency: an accident, arrest or emergency, and money needed right now", "“Don't tell Mum/Dad” or other requests for secrecy", "Payment to someone else's account, gift cards or crypto", "The voice sounds right, but the call came out of nowhere and they won't let you call back"],
        "todo": ["Ask for your family safe word. If they can't say it, hang up.", "Call them back on the number you already have saved, not the one that called you.", "Don't send money while you're on the call, however upset they sound.", REPORT_FRAUD],
        "faq": [("How do I pick a family safe word?", "Choose a short, random word or phrase that's easy to remember but isn't online: not a pet's name, birthday or anything on social media. Agree it face to face and don't text it."), ("How common is this?", "In a 2024 survey for Starling Bank, 28% of UK adults said they thought they'd been targeted by an AI voice cloning scam in the past year, and 46% had never heard of it."), ("Can they really copy a voice that easily?", "Yes. Starling Bank warns that a voice can be copied from as little as three seconds of audio, often taken from videos people post online.")],
    },
]

SOURCES = [
    "GOV.UK: Report suspicious HMRC emails, texts and calls (60599, phishing@hmrc.gov.uk, no tax rebate texts)",
    "DVLA: 'we don't send text messages about vehicle tax refunds'",
    "Royal Mail scam protection (reportascam@royalmail.com, royalmail.com/track-your-item)",
    "GOV.UK Dec 2025: Report Fraud replaces Action Fraud (reportfraud.police.uk, 0300 123 2040)",
    "UK Finance / PSR: mandatory APP reimbursement since Oct 2024",
    "Starling Bank Safe Phrases, 18 Sep 2024 (Mortar Research, 3,000+ UK adults): 28% think targeted, 46% never heard of it, 3 seconds of audio",
    "Independent Jul 2026: Hi Mum losses usually up to £3,000; Santander on AI voice notes",
]


def page(p: dict) -> str:
    e = html.escape
    faq_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "KinAlert", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Scams", "item": SITE + "/scams/"},
            {"@type": "ListItem", "position": 3, "name": p["h1"], "item": f"{SITE}/scams/{p['slug']}/"}]}]}
    related = "".join(f'<li><a href="/scams/{o["slug"]}/">{e(o["h1"])}</a></li>' for o in PAGES if o is not p)
    flags = "".join(f"<li>{e(f)}</li>" for f in p["flags"])
    todo = "".join(f"<li>{e(t)}</li>" for t in p["todo"])
    todo = todo.replace("reportfraud.police.uk", '<a href="https://www.reportfraud.police.uk/">reportfraud.police.uk</a>').replace("0300 123 2040", '<a href="tel:03001232040">0300 123 2040</a>').replace("159 ", '<a href="tel:159">159</a> ')
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    return f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])} | KinAlert</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{SITE}/scams/{p['slug']}/">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['desc'])}">
<meta property="og:image" content="{SITE}/assets/og.jpg"><meta property="og:url" content="{SITE}/scams/{p['slug']}/">
<meta property="og:type" content="article"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/pages.css">
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
</head><body>
<header class="wrap top"><a class="brand" href="/">{LOGO} KinAlert</a><a href="/#family">For families</a></header>
<main class="wrap">
<p class="crumbs"><a href="/">KinAlert</a> / <a href="/scams/">Scams</a></p>
<h1>{e(p['h1'])}</h1>
<p class="lead">{e(p['lead'])}</p>
<div data-kinalert-checker data-example="{e(p['example'])}"></div>
<h2>What this scam usually looks like</h2>
<div class="example"><small>{e(p['from'])}</small>{e(p['example'])}</div>
<h2>Red flags</h2><ul class="flags">{flags}</ul>
<h2>What to do</h2><ol class="todo">{todo}</ol>
<h2>Questions</h2>{faq}
<div class="cta"><strong style="font-size:22px">Worried about your mum or dad?</strong><p>We're building KinAlert for families: they forward anything odd to one WhatsApp number, and you get a text if it's a scam. <a href="/#family">Join the waitlist (coming soon)</a>.</p></div>
<h2>Other scams going round</h2><ul class="related">{related}</ul>
</main>
<footer class="wrap">KinAlert's checker is an AI check and can be wrong. If money is involved, call your bank on 159. <a href="/business/">For businesses</a> · <a href="/privacy/">Privacy</a> · <a href="mailto:hello@kinalert.co.uk">hello@kinalert.co.uk</a> · © 2026 KinAlert.</footer>
<script src="/assets/checker-widget.js?v=2" defer></script>
</body></html>
"""


def hub() -> str:
    e = html.escape
    items = "".join(f'<li><a href="/scams/{p["slug"]}/"><strong>{e(p["h1"])}</strong></a><br><span style="color:#4a5568">{e(p["desc"])}</span></li>' for p in PAGES)
    return f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Common UK scams and how to spot them | KinAlert</title>
<meta name="description" content="The scam texts, calls and WhatsApps going round the UK right now, with red flags, what to do, and a free checker.">
<link rel="canonical" href="{SITE}/scams/"><meta property="og:title" content="Common UK scams and how to spot them"><meta property="og:description" content="The scam texts, calls and WhatsApps going round the UK right now, with red flags and a free checker."><meta property="og:image" content="{SITE}/assets/og.jpg"><meta property="og:url" content="{SITE}/scams/"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/pages.css"></head><body>
<header class="wrap top"><a class="brand" href="/">{LOGO} KinAlert</a><a href="/#check">Check a message</a></header>
<main class="wrap"><h1>Scams going round the UK right now</h1>
<p class="lead">How each one works, the red flags, and what to do. Not sure about a message? <a href="/#check">Check it free</a>.</p>
<ul class="related" style="gap:22px">{items}</ul></main>
<footer class="wrap"><a href="/business/">For businesses</a> · <a href="/privacy/">Privacy</a> · <a href="mailto:hello@kinalert.co.uk">hello@kinalert.co.uk</a> · © 2026 KinAlert.</footer></body></html>
"""


def main() -> None:
    for p in PAGES:
        d = OUT / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(p), encoding="utf-8")
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(hub(), encoding="utf-8")
    TODAY = __import__("datetime").date.today().isoformat()
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
               f"  <url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod></url>", f"  <url><loc>{SITE}/scams/</loc><lastmod>{TODAY}</lastmod></url>", f"  <url><loc>{SITE}/business/</loc><lastmod>{TODAY}</lastmod></url>", f"  <url><loc>{SITE}/privacy/</loc><lastmod>{TODAY}</lastmod></url>"]
    sitemap += [f"  <url><loc>{SITE}/scams/{p['slug']}/</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES]
    sitemap.append("</urlset>")
    (OUT.parent / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print(f"built {len(PAGES)} pages + hub + sitemap")


if __name__ == "__main__":
    main()
