"""
Generate printable attribute and relationship cards from the OFDS data model CSVs.

Reads:
  docs/reference/data_model/entities.csv
  docs/reference/data_model/<entity>/attributes.csv
  docs/reference/data_model/<entity>/relationships.csv
  codelists/{open,closed}/<name>.csv
  config.csv  (a template is written on first run if absent)

Writes:
  <entity>.html per entity (open in a browser, File → Print → Save as PDF)

Usage:
  python generate_cards.py [--columns N] [--cards-per-page N] [--output-dir DIR]
"""

import argparse
import csv
import re
from html import escape
from pathlib import Path

DATA_MODEL_DIR = Path("docs/reference/data_model")
CODELISTS_DIR = Path("codelists")
CONFIG_CSV = Path("config.csv")
CODELIST_PREVIEW_COUNT = 3
MARKDOWN_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def codelist_preview(codes):
    """Return the first CODELIST_PREVIEW_COUNT codes, with a trailing '...' entry if truncated."""
    preview = codes[:CODELIST_PREVIEW_COUNT]
    if len(codes) > CODELIST_PREVIEW_COUNT:
        preview = preview + [("...", "")]
    return preview


def md_to_html(text):
    """Escape HTML special characters and convert Markdown links to <a> tags."""
    return MARKDOWN_LINK_RE.sub(r'<a href="\2">\1</a>', escape(text))


def load_entities():
    with open(DATA_MODEL_DIR / "entities.csv") as f:
        return [row["name"] for row in csv.DictReader(f)]


def load_codelists():
    """Return a dict mapping codelist filename → list of (code, title) tuples."""
    codelists = {}
    for path in CODELISTS_DIR.rglob("*.csv"):
        with open(path) as f:
            codelists[path.name] = [(row["Code"], row.get("Title", "")) for row in csv.DictReader(f)]
    return codelists


def load_config():
    """Return a dict mapping (entity, key) → {"note": str, "exclude": bool}."""
    if not CONFIG_CSV.exists():
        return {}
    with open(CONFIG_CSV) as f:
        return {
            (row["entity"], row["key"]): {
                "note": row.get("note", ""),
                "exclude": row.get("exclude", "").strip().lower() == "true",
            }
            for row in csv.DictReader(f)
        }


def load_attributes(entity):
    with open(DATA_MODEL_DIR / entity.lower() / "attributes.csv") as f:
        return list(csv.DictReader(f))


def load_relationships(entity):
    with open(DATA_MODEL_DIR / entity.lower() / "relationships.csv") as f:
        return list(csv.DictReader(f))


def split_relationship_description(description):
    """Split 'Title: The description.' into (title, description)."""
    if ": " in description:
        title, desc = description.split(": ", 1)
        return title, desc
    return description, ""


def build_cards(entities, codelists, config):
    cards = []
    for entity in entities:
        for attr in load_attributes(entity):
            entry = config.get((entity, attr["path"]), {})
            if entry.get("exclude"):
                continue
            codelist_name = attr.get("codelist", "")
            cards.append({
                "type": "attribute",
                "entity": entity,
                "key": attr["path"],
                "title": attr["title"],
                "description": attr["description"],
                "note": entry.get("note", ""),
                "codelist": codelist_preview(codelists.get(codelist_name, []) if codelist_name else []),
                "cardinality": "",
            })
        for rel in load_relationships(entity):
            title, description = split_relationship_description(rel["description"])
            entry = config.get((entity, title), {})
            if entry.get("exclude"):
                continue
            cards.append({
                "type": "relationship",
                "entity": entity,
                "key": title,
                "title": title,
                "description": description,
                "note": entry.get("note", ""),
                "codelist": [],
                "cardinality": rel["cardinality"],
            })
    return cards


def render_card(card):
    entity = escape(card["entity"])
    title = escape(card["title"])
    description = "".join(
        f'<p class="card-text small">{md_to_html(p)}</p>'
        for p in card["description"].split(" | ")
    )
    note = md_to_html(card["note"])

    badge = ""
    if card["type"] == "relationship":
        badge = f' <span class="badge bg-secondary">{escape(card["cardinality"])}</span>'

    codelist_html = ""
    if card["codelist"]:
        items = "\n".join(
            f'        <li class="list-group-item py-1 small">'
            f'<strong>{escape(code)}</strong>'
            + (f" — {escape(title_str)}" if title_str else "")
            + "</li>"
            for code, title_str in card["codelist"]
        )
        codelist_html = f'      <ul class="list-group list-group-flush">\n{items}\n      </ul>\n'

    note_para = (
        f'        <p class="card-text text-muted fst-italic small">{note}</p>'
        if note else
        f'        <p class="card-text text-muted small">&nbsp;</p>'
    )

    return (
        f'    <div class="card h-100">\n'
        f'      <div class="card-header py-1 small">{entity}{badge}</div>\n'
        f'      <div class="card-body py-2">\n'
        f'        <h6 class="card-title">{title}</h6>\n'
        f'{description}\n'
        f'{note_para}\n'
        f'      </div>\n'
        f'{codelist_html}'
        f'    </div>'
    )


def render_html(cards, columns, cards_per_page, title=""):
    pages = [cards[i:i + cards_per_page] for i in range(0, len(cards), cards_per_page)]
    pages_html = []
    for page in pages:
        card_items = "\n".join(render_card(c) for c in page)
        pages_html.append(f'  <div class="card-page">\n{card_items}\n  </div>')
    body = "\n".join(pages_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <title>{title} — OFDS Data Model Cards</title>
  <style>
    .card-page {{
      display: grid;
      grid-template-columns: repeat({columns}, 1fr);
      gap: 1rem;
      margin-bottom: 2rem;
    }}
    @media print {{
      .card-page {{
        display: grid;
        grid-template-columns: repeat({columns}, 1fr);
        gap: 0.5rem;
        margin: 0;
        break-after: page;
        page-break-after: always;
      }}
      body {{ margin: 0; padding: 0.5cm; }}
      * {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}
    }}
  </style>
</head>
<body class="p-3">
{body}
</body>
</html>"""


def write_config_template(entities):
    """Write a config.csv template with all entity/key combinations and empty note/exclude columns."""
    rows = []
    for entity in entities:
        for attr in load_attributes(entity):
            rows.append({"entity": entity, "key": attr["path"], "note": "", "exclude": ""})
        for rel in load_relationships(entity):
            title, _ = split_relationship_description(rel["description"])
            rows.append({"entity": entity, "key": title, "note": "", "exclude": ""})
    with open(CONFIG_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["entity", "key", "exclude", "note"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created config template: {CONFIG_CSV} — set exclude=true to omit a card, add notes to the 'note' column.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate printable OFDS data model cards.")
    parser.add_argument("--columns", type=int, default=3, help="Grid columns per page (default: 3)")
    parser.add_argument("--cards-per-page", type=int, default=6, help="Cards per printed page (default: 6)")
    parser.add_argument("--output-dir", default=".", help="Directory for output HTML files (default: .)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    entities = load_entities()
    codelists = load_codelists()

    if not CONFIG_CSV.exists():
        write_config_template(entities)

    config = load_config()

    for entity in entities:
        cards = build_cards([entity], codelists, config)
        html = render_html(cards, args.columns, args.cards_per_page, title=entity)
        output_path = output_dir / f"{entity.lower()}.html"
        with open(output_path, "w") as f:
            f.write(html)
        print(f"Generated {len(cards)} cards → {output_path}")
