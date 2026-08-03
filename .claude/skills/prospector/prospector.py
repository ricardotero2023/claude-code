#!/usr/bin/env python3
"""
Prospector: Scrape Google Maps leads via Apify → Airtable base con botón WhatsApp
Usage: python prospector.py --apify-key KEY --airtable-token TOKEN --niche NICHE --zone ZONE
"""
import argparse
import time
import sys
import requests

ACTOR_ID = "nwua9Gu5YrADL7ZDj"  # compass/crawler-google-places


# ─── Geocoding ────────────────────────────────────────────────────────────────

def geocode_zone(zone):
    """Devuelve (lat, lng, country_code) de la zona via Nominatim (OSM, sin key)."""
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": zone, "format": "json", "limit": 1, "addressdetails": 1},
            headers={"User-Agent": "prospector-skill/1.0"},
            timeout=10,
        )
        r.raise_for_status()
        results = r.json()
        if results:
            lat = float(results[0]["lat"])
            lng = float(results[0]["lon"])
            cc = results[0].get("address", {}).get("country_code", "").upper()
            return lat, lng, cc
    except Exception as e:
        print(f"   ⚠️  Geocoding falló ({e}), se scrapea sin coordenadas")
    return None, None, None


# ─── Apify ────────────────────────────────────────────────────────────────────

def scrape_leads(api_key, niche, zone, max_results):
    query = f"{niche} en {zone}"
    print(f"🔍 Scrapeando '{niche}' en '{zone}'...")

    lat, lng, country_code = geocode_zone(zone)
    if lat:
        print(f"   📍 {lat:.4f}, {lng:.4f} ({country_code})")
    else:
        print(f"   ⚠️  Sin coordenadas — los resultados podrían incluir otras zonas")

    payload = {
        "searchStringsArray": [query],
        "maxCrawledPlaces": max_results,
        "language": "es",
        "maxImages": 0,
        "maxReviews": 0,
        "includeHistogram": False,
        "includeOpeningHours": False,
        "includeWebResults": False,
    }
    if lat:
        payload["lat"] = lat
        payload["lng"] = lng
        payload["zoom"] = 12

    r = requests.post(
        f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs",
        params={"token": api_key},
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    run_id = r.json()["data"]["id"]
    print(f"   Run: {run_id}")

    while True:
        r = requests.get(
            f"https://api.apify.com/v2/actor-runs/{run_id}",
            params={"token": api_key},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()["data"]
        status = data["status"]
        count = data.get("stats", {}).get("itemCount", 0)
        print(f"   Estado: {status} | Leads: {count}", end="\r", flush=True)

        if status == "SUCCEEDED":
            print()
            break
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print()
            sys.exit(f"❌ Apify falló: {status}")
        time.sleep(8)

    r = requests.get(
        f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items",
        params={"token": api_key},
        timeout=60,
    )
    r.raise_for_status()
    leads = r.json()

    if country_code:
        before = len(leads)
        leads = [
            l for l in leads
            if (l.get("countryCode") or "").upper() == country_code
        ]
        removed = before - len(leads)
        if removed:
            print(f"   🗑️  {removed} leads de otros países descartados")

    print(f"✅ {len(leads)} leads de {zone}\n")
    return leads


# ─── Airtable ─────────────────────────────────────────────────────────────────

def get_workspace_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://api.airtable.com/v0/meta/bases", headers=headers, timeout=15)
    if r.status_code == 200:
        bases = r.json().get("bases", [])
        for base in bases:
            base_id = base.get("id")
            if not base_id:
                continue
            r2 = requests.get(f"https://api.airtable.com/v0/meta/bases/{base_id}", headers=headers, timeout=15)
            if r2.status_code == 200:
                wid = r2.json().get("workspaceId")
                if wid:
                    return wid
    raise SystemExit(
        "❌ No se pudo detectar workspace ID automáticamente.\n"
        "   Solución: abre airtable.com, entrá a tu workspace, mirá la URL\n"
        "   (formato: wspXXXXXXXX) y agregá --workspace-id 'wspXXXXXXXX' al comando."
    )


def _wa_formula():
    return (
        '"https://wa.me/" '
        '& SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({Teléfono}, "+", ""), " ", ""), "-", ""), "(", "") '
        '& "?text=Hola%2C%20hablo%20con%20" & SUBSTITUTE({Empresa}, " ", "%20") & "%3F"'
    )


def _base_fields():
    return [
        {"name": "Empresa",     "type": "singleLineText"},
        {"name": "Teléfono",    "type": "phoneNumber"},
        {"name": "Rating",      "type": "number",    "options": {"precision": 1}},
        {"name": "Reseñas",     "type": "number",    "options": {"precision": 0}},
        {"name": "Categoría",   "type": "singleLineText"},
        {"name": "Dirección",   "type": "singleLineText"},
        {"name": "Ciudad",      "type": "singleLineText"},
        {"name": "Web",         "type": "url"},
        {"name": "Google Maps", "type": "url"},
    ]


def create_base(token, name, workspace_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print(f"📋 Creando base '{name}'...")

    payload = {
        "name": name,
        "workspaceId": workspace_id,
        "tables": [{"name": "Leads", "fields": _base_fields()}],
    }
    r = requests.post("https://api.airtable.com/v0/meta/bases", headers=headers, json=payload, timeout=30)
    r.raise_for_status()

    data = r.json()
    base_id = data["id"]
    table_id = data["tables"][0]["id"]
    print(f"   Base ID: {base_id}")

    print(f"   Agregando campo WhatsApp...")
    field_url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields"
    wa_formula = _wa_formula()

    r = requests.post(field_url, headers=headers, json={
        "name": "WhatsApp",
        "type": "button",
        "options": {
            "label": "💬 Abrir WA",
            "style": {"backgroundColor": "greenDark1", "textColor": "white"},
            "action": {"type": "openUrl", "url": {"type": "formula", "formulaText": wa_formula}},
        }
    }, timeout=15)

    if r.status_code not in (200, 201):
        r = requests.post(field_url, headers=headers, json={
            "name": "WhatsApp",
            "type": "formula",
            "options": {"formula": wa_formula}
        }, timeout=15)
        if r.status_code not in (200, 201):
            print(f"   ⚠️  Campo WhatsApp no se pudo agregar: {r.text[:200]}")
        else:
            print(f"   ✅ Campo fórmula URL agregado (clickeable)")
    else:
        print(f"   ✅ Botón WhatsApp agregado")

    print()
    return base_id, table_id


def clean_phone(raw):
    if not raw:
        return ""
    return "".join(c for c in raw if c.isdigit() or c == "+")


def upload_records(token, base_id, table_id, leads):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    records = []
    for lead in leads:
        cat = lead.get("categoryName") or lead.get("category") or ""
        if not cat and lead.get("categories"):
            cat = lead["categories"][0] if isinstance(lead["categories"], list) else str(lead["categories"])

        phone_raw = lead.get("phoneUnformatted") or lead.get("phone") or ""

        fields = {
            "Empresa":   (lead.get("title") or "").strip(),
            "Teléfono":  clean_phone(phone_raw),
            "Categoría": cat,
            "Dirección": lead.get("address") or "",
            "Ciudad":    lead.get("city") or "",
        }
        if lead.get("totalScore") is not None:
            try:
                fields["Rating"] = round(float(lead["totalScore"]), 1)
            except (TypeError, ValueError):
                pass
        if lead.get("reviewsCount") is not None:
            try:
                fields["Reseñas"] = int(lead["reviewsCount"])
            except (TypeError, ValueError):
                pass
        if lead.get("website"):
            fields["Web"] = lead["website"]
        if lead.get("url"):
            fields["Google Maps"] = lead["url"]

        records.append({"fields": fields})

    print(f"⬆️  Subiendo {len(records)} registros...")
    total = 0
    for i in range(0, len(records), 10):
        batch = records[i : i + 10]
        r = requests.post(url, headers=headers, json={"records": batch}, timeout=30)
        if r.status_code != 200:
            print(f"\n   ⚠️  Error en batch {i}: {r.status_code} — {r.text[:200]}")
            continue
        total += len(batch)
        print(f"   Subidos: {total}/{len(records)}", end="\r", flush=True)
        time.sleep(0.2)

    print()
    return total


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Scrape leads → Airtable con botón WhatsApp")
    p.add_argument("--apify-key",       required=True,  help="Apify API token")
    p.add_argument("--airtable-token",  required=True,  help="Airtable personal access token")
    p.add_argument("--niche",           required=True,  help='Ej: "clínicas dentales"')
    p.add_argument("--zone",            required=True,  help='Ej: "Madrid"')
    p.add_argument("--max-results",     type=int, default=200)
    p.add_argument("--workspace-id",    default=None,   help="Airtable workspace ID (auto-detectado si se omite)")
    args = p.parse_args()

    base_name = f"Leads {args.niche.title()} {args.zone.title()}"

    leads = scrape_leads(args.apify_key, args.niche, args.zone, args.max_results)
    if not leads:
        sys.exit("❌ Apify no devolvió resultados. Probá con un nicho o zona diferente.")

    workspace_id = args.workspace_id or get_workspace_id(args.airtable_token)
    print(f"   Workspace: {workspace_id}")

    base_id, table_id = create_base(args.airtable_token, base_name, workspace_id)

    uploaded = upload_records(args.airtable_token, base_id, table_id, leads)

    print(f"\n✅ Listo! {uploaded}/{len(leads)} leads en '{base_name}'")
    print(f"🔗 https://airtable.com/{base_id}")
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 ÚLTIMO PASO: botón WhatsApp verde (30 seg en Airtable)
   La API de Airtable no permite crear botones programáticamente.

   1. Abrí la base → click en + al final de las columnas
   2. Tipo: Button
   3. Nombre del campo: WhatsApp
   4. Label del botón: WhatsApp
   5. Color: verde
   6. Action: Open URL → activar fórmula → pegar esto:

"https://wa.me/" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({{Teléfono}}, "+", ""), " ", ""), "-", ""), "(", "") & "?text=Hola%2C%20hablo%20con%20" & SUBSTITUTE({{Empresa}}, " ", "%20") & "%3F"

   7. Save 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")


if __name__ == "__main__":
    main()
