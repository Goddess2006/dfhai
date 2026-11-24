#!/usr/bin/env python3
"""Newsletter prin Brevo API v3: liste, draft de campanie, test, programare, trimitere.

Cheia: variabila de mediu BREVO_API_KEY (Brevo → SMTP & API → API Keys). Niciodată în repo.

  python3 brevo.py lists
  python3 brevo.py senders
  python3 brevo.py create --name "NL 2026-12-01" --subject "..." --preview "..." \
        --html out/newsletter-brevo.html --list 3 --sender-email office@decoflair.ro --sender-name "Deco & Flair"
  python3 brevo.py test --id 42 --to adresa@exemplu.ro
  python3 brevo.py schedule --id 42 --at 2026-12-02T09:30:00+02:00
  python3 brevo.py send-now --id 42 --yes        # trimite efectiv: doar după acordul explicit al omului
  python3 brevo.py stats --id 42

Doar biblioteca standard Python.
"""
import argparse, json, os, sys, urllib.request, urllib.error

API = "https://api.brevo.com/v3"


def call(method, path, body=None):
    key = os.environ.get("BREVO_API_KEY")
    if not key:
        sys.exit("Lipsește BREVO_API_KEY.")
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method=method, headers={
        "api-key": key, "accept": "application/json", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {"status": resp.status}
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {path}\n{e.read().decode(errors='replace')[:2000]}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lists"); sub.add_parser("senders")
    c = sub.add_parser("create")
    for k in ("--name", "--subject", "--html", "--sender-email"):
        c.add_argument(k, required=True)
    c.add_argument("--sender-name", default="Deco & Flair")
    c.add_argument("--preview", default="")
    c.add_argument("--list", type=int, action="append", required=True)
    c.add_argument("--reply-to")
    t = sub.add_parser("test"); t.add_argument("--id", type=int, required=True); t.add_argument("--to", action="append", required=True)
    s = sub.add_parser("schedule"); s.add_argument("--id", type=int, required=True); s.add_argument("--at", required=True)
    n = sub.add_parser("send-now"); n.add_argument("--id", type=int, required=True); n.add_argument("--yes", action="store_true")
    st = sub.add_parser("stats"); st.add_argument("--id", type=int, required=True)
    a = ap.parse_args()

    if a.cmd == "lists":
        out = call("GET", "/contacts/lists?limit=50")
        for l in out.get("lists", []):
            print(f"{l['id']:>5}  {l.get('uniqueSubscribers', l.get('totalSubscribers', '?')):>7}  {l['name']}")
    elif a.cmd == "senders":
        print(json.dumps(call("GET", "/senders"), indent=1, ensure_ascii=False))
    elif a.cmd == "create":
        body = {
            "name": a.name, "subject": a.subject, "previewText": a.preview,
            "sender": {"name": a.sender_name, "email": a.sender_email},
            "htmlContent": open(a.html, encoding="utf-8").read(),
            "recipients": {"listIds": a.list},
        }
        if a.reply_to:
            body["replyTo"] = a.reply_to
        out = call("POST", "/emailCampaigns", body)
        print(f"Draft creat: id={out.get('id')} (netrimis). Următorul pas: test.")
    elif a.cmd == "test":
        call("POST", f"/emailCampaigns/{a.id}/sendTest", {"emailTo": a.to})
        print("Test trimis la:", ", ".join(a.to))
    elif a.cmd == "schedule":
        call("PUT", f"/emailCampaigns/{a.id}", {"scheduledAt": a.at})
        print(f"Campania {a.id} programată la {a.at}.")
    elif a.cmd == "send-now":
        if not a.yes:
            sys.exit("Refuz fără --yes: trimiterea către toată lista nu se poate anula.")
        call("POST", f"/emailCampaigns/{a.id}/sendNow")
        print(f"Campania {a.id} a pornit.")
    elif a.cmd == "stats":
        out = call("GET", f"/emailCampaigns/{a.id}?statistics=globalStats")
        print(json.dumps({"name": out.get("name"), "status": out.get("status"),
                          "stats": out.get("statistics", {}).get("globalStats")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
