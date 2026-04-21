import re

MEDICAL_HEADINGS = {
    "abstract", "introduction", "methods", "materials and methods",
    "results", "discussion", "conclusion", "references",
    "case report", "clinical presentation", "discussion and conclusion"
}

def is_numbered(text):
    return bool(re.match(r"^(\d+(\.\d+)*)\s+\w+", text))


def is_heading(text, font_size, body_size, font):
    score = 0

    if is_numbered(text):
        score += 4

    if font_size > body_size + 1:
        score += 3

    if 3 < len(text.split()) < 12:
        score += 2

    if "Bold" in font:
        score += 2

    if len(text) < 90:
        score += 1

    if text.lower().strip() in MEDICAL_HEADINGS:
        score += 5

    return score >= 5


def detect_headings(lines):
    sizes = [l["font_size"] for l in lines if l["font_size"] > 0]
    body_size = sorted(sizes)[len(sizes)//2] if sizes else 0

    headings = []

    for l in lines:
        if is_heading(l["text"], l["font_size"], body_size, l["font"]):
            headings.append(l)

    return headings


def detect_title(lines):
    page1 = [l for l in lines if l["page"] == 0]
    if not page1:
        return "Unknown"

    return max(page1, key=lambda x: x["font_size"])["text"]