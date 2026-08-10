from __future__ import annotations

import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://elenalantsova0-hue.github.io/Fedor-Lantsov"
SITE_NAME = "Fedor Lantsov"
DATA_FILE = ROOT / "js" / "data" / "paintings.js"
CSS_FILES = [
    "reset.css", "variables.css", "typography.css", "layout.css",
    "navigation.css", "hero.css", "gallery.css", "artwork.css",
    "about.css", "forms.css", "footer.css", "animations.css",
    "responsive.css", "seo.css",
]
ROOT_PAGES = {
    "index.html": {
        "title": "Fedor Lantsov — Original Figurative Oil Paintings",
        "description": "Explore original figurative oil paintings, mythology art and portrait commissions by contemporary artist Fedor Lantsov.",
        "canonical": f"{BASE_URL}/",
        "image": f"{BASE_URL}/images/hero/hero.webp",
        "type": "website",
    },
    "collection.html": {
        "title": "Original Oil Painting Collection | Fedor Lantsov",
        "description": "Browse original figurative, mythology and portrait oil paintings by Fedor Lantsov, with dimensions, availability and acquisition details.",
        "canonical": f"{BASE_URL}/collection.html",
        "image": f"{BASE_URL}/images/hero/hero.webp",
        "type": "website",
    },
    "about.html": {
        "title": "About Figurative Artist Fedor Lantsov",
        "description": "Discover Fedor Lantsov’s contemporary figurative painting practice, classical atelier methods and approach to mythology and portrait art.",
        "canonical": f"{BASE_URL}/about.html",
        "image": f"{BASE_URL}/images/artist/fedor-lantsov.webp",
        "type": "profile",
    },
    "contact.html": {
        "title": "Contact & Private Art Inquiries | Fedor Lantsov",
        "description": "Contact the Fedor Lantsov atelier about original paintings, custom oil portrait commissions, gallery collaborations and acquisitions.",
        "canonical": f"{BASE_URL}/contact.html",
        "image": f"{BASE_URL}/images/hero/hero.webp",
        "type": "website",
    },
}

LANDINGS = {
    "figurative-oil-paintings": {
        "title": "Original Figurative Oil Paintings | Fedor Lantsov",
        "h1": "Original Figurative Oil Paintings",
        "description": "Explore original figurative oil paintings by Fedor Lantsov, combining classical realism, expressive light and contemporary human presence.",
        "filter": lambda p: p["category"] == "figurative",
        "copy": [
            "Fedor Lantsov’s figurative oil paintings combine close observation of the human form with the disciplined methods of the European atelier. Each work begins with structure: gesture, proportion, tonal balance and the direction of light. Layers of oil color then build atmosphere and depth, allowing the figure to emerge gradually rather than sit as a flat illustration on the surface.",
            "The collection moves between quiet portrait studies, myth-inspired compositions and more expressive scenes shaped by water, movement or dramatic shadow. Warm skin tones are often set against deep browns, marine blues or glowing reds. This contrast supports the emotional focus of each painting while preserving a clear, classical design.",
            "Every work shown here is an original oil painting rather than a print. Individual artwork pages include dimensions, year, technique, availability and detailed views. Collectors can request acquisition information directly from the studio, with worldwide free delivery offered for available paintings and a seven-day return period subject to the studio’s confirmed terms.",
        ],
    },
    "mythology-paintings": {
        "title": "Mythology & Goddess Oil Paintings | Fedor Lantsov",
        "h1": "Mythology & Goddess Paintings",
        "description": "Discover original mythology oil paintings inspired by Aphrodite, Demeter, Flora and Cleopatra, rendered through classical realism.",
        "filter": lambda p: p["category"] == "mythology" or "aphrodite" in p["slug"],
        "copy": [
            "Mythology gives Fedor Lantsov a visual language for exploring beauty, authority, transformation and the relationship between human presence and the natural world. These original oil paintings draw on figures such as Aphrodite, Demeter, Flora and Cleopatra without attempting literal historical reconstruction. The emphasis remains on light, gesture, atmosphere and the emotional character of the subject.",
            "Water, flowers, fruit, jewelry and drapery operate as compositional elements as much as narrative signs. Marine blues create movement around the Aphrodite series, while Demeter and Flora use earth colors and botanical forms. Cleopatra shifts toward warm gold, turquoise and architectural detail. Across the collection, classical realism provides structure while contemporary brushwork keeps the images immediate.",
            "Each painting is presented with its exact medium, dimensions, year and current status. Detailed photographs reveal the layered surface and handling of oil paint. These works are intended for collectors seeking Greek mythology art, goddess paintings and original figurative fine art with a distinctive contemporary voice.",
        ],
    },
    "portrait-paintings": {
        "title": "Original Portrait Oil Paintings | Fedor Lantsov",
        "h1": "Original Portrait Oil Paintings",
        "description": "View original portrait oil paintings by Fedor Lantsov, including classical studies and contemporary commissioned portrait examples.",
        "filter": lambda p: p["category"] == "portrait",
        "copy": [
            "The portrait paintings in this collection are built around attention, character and the changing relationship between light and expression. Fedor Lantsov uses oil on linen to develop subtle transitions across the face, hair and surrounding space. Rather than relying on photographic sharpness everywhere, selected edges soften into shadow so that the sitter’s presence remains the central focus.",
            "Some works are intimate studies, while others introduce symbolic or decorative elements. Warm earth colors, controlled chiaroscuro and restrained backgrounds connect the portraits to classical realism. At the same time, asymmetrical poses and contemporary color relationships prevent them from feeling like historical reproductions.",
            "Original portraits and custom commissions can be discussed directly with the atelier. Each artwork page includes dimensions, year, price or recorded price, availability and close detail views where provided. The collection is designed for buyers seeking hand-painted fine art portraiture rather than digital effects or printed reproductions.",
        ],
    },
    "original-oil-paintings": {
        "title": "Original Oil Paintings for Sale | Fedor Lantsov",
        "h1": "Original Oil Paintings for Sale",
        "description": "Browse available original oil paintings by Fedor Lantsov, including figurative art, mythology paintings and portraits on linen.",
        "filter": lambda p: p["available"],
        "copy": [
            "This selection brings together the original oil paintings currently available from Fedor Lantsov’s studio. The catalogue includes figurative compositions, mythology-inspired works and portrait studies, each painted individually on linen. No image in this section represents a print edition or digitally reproduced substitute for the original object.",
            "Artwork pages provide the information collectors need to compare works: exact dimensions, medium, year, price, availability, main photography and close detail images where available. The descriptions discuss visible composition, palette and technique, helping online visitors understand how each painting may function within a private collection or interior.",
            "Available works can be reserved through a private inquiry. The studio currently advertises worldwide free delivery and seven-day returns; final shipping timing, customs treatment and return eligibility should always be confirmed in writing before acquisition. Sold works remain visible as part of the artist’s catalogue and are clearly marked as acquired.",
        ],
    },
    "custom-oil-portraits": {
        "title": "Custom Oil Portrait from Photo | Fedor Lantsov",
        "h1": "Custom Oil Portrait Commissions",
        "description": "Commission a hand-painted custom oil portrait from a photograph, created on linen using traditional layered painting methods.",
        "filter": lambda p: p["slug"] == "custom-portrait",
        "copy": [
            "A custom oil portrait commission offers a way to transform a personal photographic reference into a unique hand-painted work. Fedor Lantsov develops each portrait on linen through drawing, tonal organization and layered oil color. The source photograph guides likeness, pose and essential character, while the final decisions about light, color and emphasis remain painterly.",
            "The example shown here demonstrates the studio’s interest in classical portrait lighting, restrained color and gradual transitions between illuminated form and shadow. A commission is not a printed photograph with a filter applied. It is an original physical painting, built through successive stages and adjusted for the scale and atmosphere of the intended setting.",
            "To request a portrait, contact the studio with a clear reference photograph, preferred dimensions, deadline and any important background information. Pricing currently begins within the range shown on the example artwork page. Final cost, schedule, delivery and revision expectations should be agreed before work begins. Because commissioned portraits are made for a specific client, return terms require separate written confirmation.",
        ],
    },
}


def load_paintings() -> list[dict]:
    text = DATA_FILE.read_text(encoding="utf-8")
    payload = text.split("=", 1)[1].strip().removesuffix(";")
    return json.loads(payload)


def write_paintings(items: list[dict]) -> None:
    content = "// Generated from Painting Info.xlsx and verified local image paths.\n"
    content += "window.paintingsData = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n"
    DATA_FILE.write_text(content, encoding="utf-8")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def json_ld(data: object) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def excerpt(text: str, limit: int = 158) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    shortened = compact[:limit].rsplit(" ", 1)[0]
    return shortened.rstrip(".,;:") + "…"


def numeric_price(value: str) -> tuple[str, str | None]:
    nums = re.findall(r"[\d,]+", value)
    cleaned = [n.replace(",", "") for n in nums]
    if len(cleaned) >= 2:
        return cleaned[0], cleaned[1]
    return (cleaned[0] if cleaned else "0"), None


def normalize_and_optimize_images(items: list[dict]) -> None:
    responsive = ROOT / "images" / "responsive"
    responsive.mkdir(parents=True, exist_ok=True)
    for item in items:
        slug = item["slug"]
        old_main = ROOT / item["image"]
        new_main = ROOT / "images" / "paintings" / f"{slug}.webp"
        if old_main.exists() and old_main.resolve() != new_main.resolve():
            if new_main.exists():
                old_main.unlink()
            else:
                old_main.rename(new_main)
        if not new_main.exists():
            raise FileNotFoundError(new_main)
        item["image"] = f"images/paintings/{slug}.webp"
        with Image.open(new_main) as source:
            item["imageWidth"], item["imageHeight"] = source.size
            for width in (480, 900):
                target = responsive / f"{slug}-{width}.webp"
                save_variant(source, target, width)
        item["srcset"] = [
            f"images/responsive/{slug}-480.webp 480w",
            f"images/responsive/{slug}-900.webp 900w",
            f"images/paintings/{slug}.webp {item['imageWidth']}w",
        ]

        normalized_details = []
        detail_srcsets = []
        for index, old_rel in enumerate(item.get("details", []), start=1):
            old_detail = ROOT / old_rel
            new_detail = ROOT / "images" / "details" / f"{slug}-{index:02d}.webp"
            if old_detail.exists() and old_detail.resolve() != new_detail.resolve():
                if new_detail.exists():
                    old_detail.unlink()
                else:
                    old_detail.rename(new_detail)
            if not new_detail.exists():
                continue
            normalized_details.append(f"images/details/{slug}-{index:02d}.webp")
            with Image.open(new_detail) as source:
                width, height = source.size
                for target_width in (480, 900):
                    target = responsive / f"{slug}-detail-{index:02d}-{target_width}.webp"
                    save_variant(source, target, target_width)
            detail_srcsets.append({
                "width": width,
                "height": height,
                "srcset": [
                    f"images/responsive/{slug}-detail-{index:02d}-480.webp 480w",
                    f"images/responsive/{slug}-detail-{index:02d}-900.webp 900w",
                    f"images/details/{slug}-{index:02d}.webp {width}w",
                ],
            })
        item["details"] = normalized_details
        item["detailImages"] = detail_srcsets


def save_variant(source: Image.Image, target: Path, target_width: int) -> None:
    image = source.convert("RGB")
    width, height = image.size
    if width > target_width:
        target_height = round(height * target_width / width)
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, "WEBP", quality=82, method=6, optimize=True)


def css_links(prefix: str) -> str:
    return "\n".join(f'<link rel="stylesheet" href="{prefix}css/{name}">' for name in CSS_FILES)


def root_nav(prefix: str = "") -> str:
    return f'''<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header" id="site-header"><div class="container navigation">
<a class="brand" href="{prefix}index.html">Fedor Lantsov<span>Fine Art · Atelier</span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" aria-label="Open navigation"><span class="nav-toggle-lines" aria-hidden="true"></span></button>
<nav aria-label="Primary navigation"><ul class="nav-links" id="primary-navigation">
<li><a class="nav-link" data-page="index" href="{prefix}index.html">Home</a></li>
<li><a class="nav-link" data-page="collection" href="{prefix}collection.html">Collection</a></li>
<li><a class="nav-link" data-page="about" href="{prefix}about.html">About</a></li>
<li><a class="nav-link" data-page="contact" href="{prefix}contact.html">Contact</a></li>
</ul></nav><a class="button nav-cta" href="{prefix}contact.html">Private Inquiry</a>
</div></header>'''


def footer(prefix: str = "") -> str:
    return f'''<footer class="site-footer"><div class="container"><div class="footer-grid">
<div><a class="brand" href="{prefix}index.html">Fedor Lantsov<span>Fine Art · Atelier</span></a><p class="footer-brand-copy">Classical figurative painting shaped by European atelier tradition, mythology and the study of light.</p></div>
<div><h2 class="footer-title">Explore</h2><ul class="footer-links"><li><a href="{prefix}collection.html">Collection</a></li><li><a href="{prefix}about.html">About the artist</a></li><li><a href="{prefix}contact.html">Private inquiries</a></li></ul></div>
<div><h2 class="footer-title">Collections</h2><ul class="footer-links"><li><a href="{prefix}figurative-oil-paintings/">Figurative paintings</a></li><li><a href="{prefix}mythology-paintings/">Mythology paintings</a></li><li><a href="{prefix}portrait-paintings/">Portrait paintings</a></li><li><a href="{prefix}custom-oil-portraits/">Portrait commissions</a></li></ul></div>
</div><div class="footer-bottom"><p>© <span data-current-year></span> Fedor Lantsov. All rights reserved.</p><p>Original works · International enquiries</p></div></div></footer>'''


def scripts(prefix: str = "", include_gallery: bool = False) -> str:
    names = ["navigation.js", "animations.js", "lazyload.js", "app.js"]
    if include_gallery:
        names.insert(0, "gallery.js")
    return "\n".join(f'<script src="{prefix}js/{name}" defer></script>' for name in names)


def picture(item: dict, prefix: str, css_class: str, eager: bool = False) -> str:
    src = prefix + "images/responsive/" + item["slug"] + "-900.webp"
    srcset = ", ".join(prefix + part for part in item["srcset"])
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (
        f'<img class="{css_class}" src="{esc(src)}" srcset="{esc(srcset)}" '
        f'sizes="(max-width: 760px) 100vw, 50vw" width="{item["imageWidth"]}" '
        f'height="{item["imageHeight"]}" loading="{loading}" decoding="async"{priority} '
        f'alt="{esc(item["title"])} — original oil painting by Fedor Lantsov">'
    )


def card(item: dict, prefix: str = "", heading: str = "h2") -> str:
    benefits = ""
    if item["available"]:
        benefits = '<ul class="painting-benefits" aria-label="Purchase terms"><li>Worldwide free delivery</li><li>7-day returns accepted</li></ul>'
    return f'''<article class="painting-card reveal {'is-wide' if item.get('wide') else ''}" data-category="{esc(item['category'])}" data-available="{str(item['available']).lower()}">
<a class="painting-link" href="{prefix}artworks/{quote(item['slug'])}/" aria-label="View {esc(item['title'])}">
<div class="painting-canvas {esc(item['paintClass'])} ratio-{item['widthCm']}x{item['heightCm']}">{picture(item, prefix, 'painting-image')}<span class="canvas-badge">{esc(item['size'])}</span></div>
<div class="painting-info"><{heading} class="painting-title">{esc(item['title'])}</{heading}><p class="painting-meta">{esc(item['medium'])} · {esc(item['size'])} · {item['year']}</p><span class="painting-status {'is-sold' if not item['available'] else ''}">{'Available' if item['available'] else 'Acquired'}</span>{benefits}</div>
</a></article>'''


def seo_head(title: str, description: str, canonical: str, image_url: str, og_type: str = "website", extra_ld: list[dict] | None = None, robots: str = "index,follow,max-image-preview:large") -> str:
    tags = f'''<!-- SEO:START -->
<meta name="robots" content="{robots}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(image_url)}">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(image_url)}">
<link rel="manifest" href="{BASE_URL}/manifest.webmanifest">'''
    if extra_ld:
        tags += "\n" + "\n".join(json_ld(item) for item in extra_ld)
    return tags + "\n<!-- SEO:END -->"


def replace_seo_block(text: str, block: str) -> str:
    text = re.sub(r"\n?<!-- SEO:START -->.*?<!-- SEO:END -->\n?", "\n", text, flags=re.S)
    return text.replace("</head>", block + "\n</head>")


def replace_div_contents(text: str, opening_tag: str, content: str) -> str:
    """Replace one div's inner HTML while respecting nested div elements."""
    start = text.index(opening_tag)
    content_start = text.index(">", start) + 1
    depth = 1
    token_pattern = re.compile(r"<div\b|</div>", re.I)
    for match in token_pattern.finditer(text, content_start):
        if match.group(0).lower().startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return text[:content_start] + "\n" + content + "\n" + text[match.start():]
    raise ValueError(f"Unclosed div: {opening_tag}")


def update_root_pages(items: list[dict]) -> None:
    website_ld = {
        "@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME,
        "url": f"{BASE_URL}/", "inLanguage": "en",
    }
    person_ld = {
        "@context": "https://schema.org", "@type": "Person", "name": "Fedor Lantsov",
        "url": f"{BASE_URL}/about.html", "image": f"{BASE_URL}/images/artist/fedor-lantsov.webp",
        "jobTitle": "Figurative Painter",
    }
    item_list_ld = {
        "@context": "https://schema.org", "@type": "ItemList", "name": "Fedor Lantsov Painting Collection",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{BASE_URL}/artworks/{p['slug']}/", "name": p["title"]}
            for i, p in enumerate(items)
        ],
    }
    for filename, meta in ROOT_PAGES.items():
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"<title>.*?</title>", f"<title>{esc(meta['title'])}</title>", text)
        text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(meta["description"])}">', text)
        extra = []
        if filename == "index.html":
            extra = [website_ld, person_ld]
        elif filename == "about.html":
            extra = [person_ld]
        elif filename == "collection.html":
            extra = [item_list_ld]
        text = replace_seo_block(text, seo_head(meta["title"], meta["description"], meta["canonical"], meta["image"], meta["type"], extra))
        if "seo.css" not in text:
            text = text.replace('<link rel="stylesheet" href="css/responsive.css">', '<link rel="stylesheet" href="css/responsive.css">\n  <link rel="stylesheet" href="css/seo.css">')
        path.write_text(text, encoding="utf-8")

    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    cards = "\n".join(card(p) for p in items[:6])
    text = replace_div_contents(text, '<div class="paintings-grid" data-gallery data-limit="6">', cards)
    text = replace_footer(text, "")
    index.write_text(text, encoding="utf-8")

    collection = ROOT / "collection.html"
    text = collection.read_text(encoding="utf-8")
    cards = "\n".join(card(p) for p in items)
    text = replace_div_contents(text, '<div class="paintings-grid" data-gallery aria-live="polite">', cards)
    text = replace_footer(text, "")
    collection.write_text(text, encoding="utf-8")

    for filename in ("about.html", "contact.html"):
        path = ROOT / filename
        text = replace_footer(path.read_text(encoding="utf-8"), "")
        if filename == "contact.html":
            text = text.replace("Under €5,000", "Under $5,000").replace("€5,000–€10,000", "$5,000–$10,000").replace("€10,000–€20,000", "$10,000–$20,000").replace("€20,000+", "$20,000+")
        path.write_text(text, encoding="utf-8")

    legacy = ROOT / "artwork.html"
    text = legacy.read_text(encoding="utf-8")
    text = replace_seo_block(text, seo_head("Artwork Redirect | Fedor Lantsov", "Legacy artwork route.", f"{BASE_URL}/collection.html", f"{BASE_URL}/images/hero/hero.webp", robots="noindex,follow"))
    text = re.sub(r'\n<link rel="canonical" href="[^"]+">', "", text)
    if "seo.css" not in text:
        text = text.replace('<link rel="stylesheet" href="css/responsive.css">', '<link rel="stylesheet" href="css/responsive.css">\n  <link rel="stylesheet" href="css/seo.css">')
    text = replace_footer(text, "")
    legacy.write_text(text, encoding="utf-8")


def replace_footer(text: str, prefix: str) -> str:
    return re.sub(r'<footer class="site-footer">.*?</footer>', footer(prefix), text, flags=re.S)


def product_schema(item: dict) -> dict:
    low, high = numeric_price(item["price"])
    offer: dict = {
        "@type": "Offer" if high is None else "AggregateOffer",
        "url": f"{BASE_URL}/artworks/{item['slug']}/",
        "priceCurrency": item["currency"],
        "availability": "https://schema.org/InStock" if item["available"] else "https://schema.org/OutOfStock",
        "itemCondition": "https://schema.org/NewCondition",
    }
    if high is None:
        offer["price"] = low
    else:
        offer["lowPrice"] = low
        offer["highPrice"] = high
        offer["offerCount"] = 1
    return {
        "@context": "https://schema.org", "@type": "Product",
        "name": item["title"], "description": item["description"],
        "image": [f"{BASE_URL}/{path}" for path in [item["image"], *item.get("details", [])]],
        "sku": item["slug"], "brand": {"@type": "Person", "name": "Fedor Lantsov"},
        "material": item["medium"], "category": item["category"],
        "productionDate": str(item["year"]),
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Width", "value": item["widthCm"], "unitCode": "CMT"},
            {"@type": "PropertyValue", "name": "Height", "value": item["heightCm"], "unitCode": "CMT"},
        ],
        "offers": offer,
    }


def breadcrumb_schema(item: dict | None = None, landing_name: str | None = None, landing_slug: str | None = None) -> dict:
    elements = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
        {"@type": "ListItem", "position": 2, "name": "Collection", "item": f"{BASE_URL}/collection.html"},
    ]
    if item:
        elements.append({"@type": "ListItem", "position": 3, "name": item["title"], "item": f"{BASE_URL}/artworks/{item['slug']}/"})
    elif landing_name and landing_slug:
        elements.append({"@type": "ListItem", "position": 3, "name": landing_name, "item": f"{BASE_URL}/{landing_slug}/"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


def generate_artwork_pages(items: list[dict]) -> None:
    output_root = ROOT / "artworks"
    output_root.mkdir(exist_ok=True)
    for item in items:
        page_dir = output_root / item["slug"]
        page_dir.mkdir(parents=True, exist_ok=True)
        canonical = f"{BASE_URL}/artworks/{item['slug']}/"
        title = f"{item['title']} — Original Oil Painting | Fedor Lantsov"
        description = excerpt(item["description"])
        main = picture(item, "../../", "artwork-image", eager=True)
        detail_cards = []
        for index, detail in enumerate(item.get("detailImages", []), start=1):
            src = f"../../images/responsive/{item['slug']}-detail-{index:02d}-900.webp"
            srcset = ", ".join("../../" + part for part in detail["srcset"])
            detail_cards.append(f'''<figure class="detail-card reveal"><img class="detail-image" src="{esc(src)}" srcset="{esc(srcset)}" sizes="(max-width:760px) 100vw, 33vw" width="{detail['width']}" height="{detail['height']}" loading="lazy" decoding="async" alt="{esc(item['title'])} — painting detail {index}"><figcaption>{['Brushwork detail','Glaze depth','Tonal structure'][min(index-1,2)]}</figcaption></figure>''')
        related = [p for p in items if p["slug"] != item["slug"] and p["category"] == item["category"]][:3]
        related_html = "\n".join(card(p, "../../", "h3") for p in related)
        status = "Available" if item["available"] else "Acquired"
        price_label = "Acquisition price" if item["available"] else "Recorded price"
        schema = [product_schema(item), breadcrumb_schema(item=item)]
        html_page = f'''<!DOCTYPE html><html lang="en" data-page="artwork"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(description)}"><title>{esc(title)}</title>
<link rel="icon" href="../../favicon.ico" sizes="any"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
{css_links('../../')}
{seo_head(title, description, canonical, f"{BASE_URL}/{item['image']}", 'product', schema)}
</head><body>{root_nav('../../')}<main id="main-content">
<section class="page-hero"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../../index.html">Home</a><span>›</span><a href="../../collection.html">Collection</a><span>›</span><span aria-current="page">{esc(item['title'])}</span></nav><p class="section-label">{esc(item['category'].title())} · {item['year']}</p><h1 class="section-title"><em>{esc(item['title'])}</em></h1></div></section>
<section class="section"><div class="container"><div class="artwork-layout"><figure class="artwork-frame reveal"><div class="artwork-visual {esc(item['paintClass'])} ratio-{item['widthCm']}x{item['heightCm']}">{main}<span class="canvas-badge">{esc(item['size'])}</span></div><figcaption class="visually-hidden">{esc(item['title'])}, {esc(item['medium'])}, {esc(item['size'])}, {item['year']}</figcaption></figure>
<div class="artwork-copy reveal"><p class="section-label">Original artwork</p><h2 class="visually-hidden">Artwork information</h2><p class="artwork-meta">{esc(item['medium'])} · {esc(item['size'])} · {item['year']}</p><p class="artwork-description">{esc(item['description'])}</p><p class="artwork-price"><span>{price_label}</span>{esc(item['price'])}<small>{status}</small></p><ul class="artwork-benefits"><li>Worldwide free delivery</li><li>7-day returns accepted for eligible original works</li></ul><a class="button" href="../../contact.html?artwork={quote(item['slug'])}">Request information</a></div></div>
{f'<div class="detail-grid">{"".join(detail_cards)}</div>' if detail_cards else ''}
</div></section>
{f'<section class="section section-dark"><div class="container"><div class="section-head"><div><p class="section-label">Explore more</p><h2 class="section-title">Related <em>Works</em></h2></div></div><div class="paintings-grid">{related_html}</div></div></section>' if related_html else ''}
</main>{footer('../../')}{scripts('../../')}</body></html>'''
        (page_dir / "index.html").write_text(html_page, encoding="utf-8")


def generate_landing_pages(items: list[dict]) -> None:
    for slug, meta in LANDINGS.items():
        selected = [p for p in items if meta["filter"](p)]
        page_dir = ROOT / slug
        page_dir.mkdir(exist_ok=True)
        canonical = f"{BASE_URL}/{slug}/"
        image = f"{BASE_URL}/{selected[0]['image']}" if selected else f"{BASE_URL}/images/hero/hero.webp"
        list_ld = {
            "@context": "https://schema.org", "@type": "ItemList", "name": meta["h1"],
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE_URL}/artworks/{p['slug']}/", "name": p["title"]} for i, p in enumerate(selected)],
        }
        cards = "\n".join(card(p, "../") for p in selected)
        copy = "\n".join(f"<p>{esc(paragraph)}</p>" for paragraph in meta["copy"])
        page = f'''<!DOCTYPE html><html lang="en" data-page="collection"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(meta['description'])}"><title>{esc(meta['title'])}</title><link rel="icon" href="../favicon.ico" sizes="any"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">{css_links('../')}{seo_head(meta['title'], meta['description'], canonical, image, 'website', [list_ld, breadcrumb_schema(landing_name=meta['h1'], landing_slug=slug)])}</head><body>{root_nav('../')}<main id="main-content"><section class="page-hero"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>›</span><a href="../collection.html">Collection</a><span>›</span><span aria-current="page">{esc(meta['h1'])}</span></nav><p class="section-label">Curated collection</p><h1 class="section-title">{esc(meta['h1'])}</h1><p class="lead">{esc(meta['description'])}</p></div></section><section class="section"><div class="container"><div class="seo-copy reveal">{copy}</div><div class="section-head"><div><p class="section-label">Selected artworks</p><h2 class="section-title">Explore the <em>Collection</em></h2></div></div><div class="paintings-grid">{cards or '<p class="empty-state">New works will be added soon.</p>'}</div></div></section></main>{footer('../')}{scripts('../')}</body></html>'''
        (page_dir / "index.html").write_text(page, encoding="utf-8")


def generate_support_files(items: list[dict]) -> None:
    urls = [
        f"{BASE_URL}/", f"{BASE_URL}/collection.html", f"{BASE_URL}/about.html", f"{BASE_URL}/contact.html",
        *[f"{BASE_URL}/{slug}/" for slug in LANDINGS],
        *[f"{BASE_URL}/artworks/{p['slug']}/" for p in items],
    ]
    today = date.today().isoformat()
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for url in urls:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{esc(url)}</loc>")
        sitemap.append(f"    <lastmod>{today}</lastmod>")
        if "/artworks/" in url:
            slug = url.rstrip("/").split("/")[-1]
            item = next(p for p in items if p["slug"] == slug)
            sitemap.extend([
                "    <image:image>", f"      <image:loc>{esc(BASE_URL + '/' + item['image'])}</image:loc>",
                f"      <image:title>{esc(item['title'])}</image:title>", f"      <image:caption>{esc(excerpt(item['description'], 240))}</image:caption>", "    </image:image>",
            ])
        sitemap.append("  </url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    manifest = {
        "name": "Fedor Lantsov Fine Art", "short_name": "Fedor Lantsov", "start_url": "./",
        "display": "standalone", "background_color": "#0a0907", "theme_color": "#0a0907",
        "icons": [{"src": "favicon.ico", "sizes": "64x64", "type": "image/x-icon"}],
    }
    (ROOT / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    not_found = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="The requested page could not be found. Explore the original painting collection by Fedor Lantsov or return to the homepage."><meta name="robots" content="noindex"><title>Page Not Found | Fedor Lantsov</title><link rel="icon" href="favicon.ico">{css_links('')}</head><body>{root_nav('')}<main id="main-content"><section class="page-hero seo-error"><div class="container"><p class="section-label">404</p><h1 class="section-title">Page <em>Not Found</em></h1><p class="lead">The requested page does not exist. Continue to the painting collection or return home.</p><div class="hero-actions"><a class="button" href="collection.html">View collection</a><a class="button button-secondary" href="index.html">Return home</a></div></div></section></main>{footer('')}{scripts('')}</body></html>'''
    (ROOT / "404.html").write_text(not_found, encoding="utf-8")


def update_javascript() -> None:
    gallery = r'''(() => {
  const root = document.querySelector('[data-gallery]');
  if (!root) return;
  const staticCards = [...root.querySelectorAll('.painting-card')];
  const buttons = document.querySelectorAll('[data-filter]');
  const applyFilter = filter => {
    staticCards.forEach(card => {
      const show = filter === 'all' || card.dataset.category === filter || (filter === 'sold' && card.dataset.available === 'false');
      card.hidden = !show;
    });
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    buttons.forEach(item => item.setAttribute('aria-pressed', 'false'));
    button.setAttribute('aria-pressed', 'true');
    applyFilter(button.dataset.filter);
  }));
  applyFilter('all');
})();
'''
    (ROOT / "js" / "gallery.js").write_text(gallery, encoding="utf-8")
    legacy = r'''(() => {
  const requested = new URLSearchParams(location.search).get('id');
  if (!requested || !window.paintingsData) return;
  const painting = window.paintingsData.find(item => item.slug === requested || String(item.id) === requested);
  if (painting) location.replace(`artworks/${encodeURIComponent(painting.slug)}/`);
})();
'''
    (ROOT / "js" / "artwork.js").write_text(legacy, encoding="utf-8")


def main() -> None:
    items = load_paintings()
    normalize_and_optimize_images(items)
    write_paintings(items)
    update_javascript()
    update_root_pages(items)
    generate_artwork_pages(items)
    generate_landing_pages(items)
    generate_support_files(items)
    print(f"SEO build complete: {len(items)} artworks, {len(LANDINGS)} landing pages")


if __name__ == "__main__":
    main()
