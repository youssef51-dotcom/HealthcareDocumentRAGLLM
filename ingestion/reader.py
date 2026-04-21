import fitz
from collections import defaultdict

def collect_block_stats(doc):
    """
    Collects text frequency + vertical positions across all pages
    """
    text_positions = defaultdict(list)

    for page in doc:
        blocks = page.get_text("blocks")

        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            text = text.strip()

            if not text:
                continue

            text_positions[text].append((y0, y1))

    return text_positions

def detect_header_footer(text_positions, page_height, doc_len):
    headers = set()
    footers = set()

    for text, positions in text_positions.items():

        if len(positions) < max(2, doc_len * 0.3):
            continue  # must repeat across pages

        avg_y = sum((p[0] + p[1]) / 2 for p in positions) / len(positions)

        # header zone (top 10%)
        if avg_y < page_height * 0.12:
            headers.add(text)

        # footer zone (bottom 10%)
        if avg_y > page_height * 0.88:
            footers.add(text)

    return headers, footers

def remove_header_footer(blocks, headers, footers):
    cleaned = []

    for b in blocks:
        x0, y0, x1, y1, text, *_ = b
        text = text.strip()

        if text in headers or text in footers:
            continue

        cleaned.append(b)

    return cleaned


def detect_columns(page):
    """
    Simple heuristic:
    if text blocks are mostly split left/right → 2 columns
    else → 1 column
    """
    blocks = page.get_text("dict")["blocks"]

    x_positions = []

    for b in blocks:
        if "lines" not in b:
            continue
        x_positions.append(b["bbox"][0])

    if not x_positions:
        return 1

    mid = page.rect.width / 2

    left = sum(1 for x in x_positions if x < mid)
    right = sum(1 for x in x_positions if x >= mid)

    return 2 if left > 3 and right > 3 else 1


def extract_lines(pdf_path, mode="auto"):
    doc = fitz.open(pdf_path)
    lines = []

    for page_index, page in enumerate(doc):

        # --------------------------
        # COLUMN MODE
        # --------------------------
        if mode == "auto":
            col_mode = detect_columns(page)
        else:
            col_mode = 1 if mode == "1col" else 2

        mid = page.rect.width / 2

        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if "lines" not in b:
                continue

            x0, y0, x1, y1 = b["bbox"]

            text = ""
            sizes = []
            fonts = []

            # --------------------------
            # KEEP FONT EXTRACTION (FIX)
            # --------------------------
            for line in b["lines"]:
                for span in line["spans"]:
                    text += span["text"] + " "
                    sizes.append(span["size"])
                    fonts.append(span["font"])

            text = text.strip()
            if not text:
                continue

            item = {
                "text": text,
                "page": page_index,
                "x": x0,
                "y": y0,

                # 🔥 IMPORTANT (RESTORED)
                "font_size": max(sizes) if sizes else 0,
                "font": fonts[0] if fonts else ""
            }

            # --------------------------
            # COLUMN HANDLING (KEEP)
            # --------------------------
            if col_mode == 2:
                item["col"] = "left" if x0 < mid else "right"
            else:
                item["col"] = "full"

            lines.append(item)

    return lines

