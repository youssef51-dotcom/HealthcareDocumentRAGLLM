def build_sections(lines, headings):
    """
    Builds sections purely from headings.
    No title assumption.
    """

    heading_set = set(h["text"] for h in headings)

    sections = []
    current = None

    for l in lines:
        text = l["text"]

        # if this line is a heading → start new section
        if text in heading_set:
            current = {
                "heading": text,
                "content": "",
                "page": l["page"] + 1
            }
            sections.append(current)

        else:
            # attach content to last heading
            if current:
                current["content"] += text + " "

    return sections

def remove_non_clinical(sections):
    """
    Removes reference/bibliography/appendix sections from extracted sections.
    """

    BAD_HEADINGS = [
        "references",
        "bibliography",
        "reference",
        "literature cited",
        "acknowledgements",
        "acknowledgments",
        "appendix", "conflict", "funding", "author"
    ]

    cleaned = []

    for sec in sections:
        heading = sec["heading"].lower().strip()

        # check if heading matches unwanted sections
        if any(bad in heading for bad in BAD_HEADINGS):
            continue

        cleaned.append(sec)

    return cleaned