from .reader import extract_lines
from .layout import sort_lines
from .headings import detect_headings
from .builder import build_sections, remove_non_clinical
from .chunker import build_rag_chunks


def extract_pdf_structure(pdf_path, mode="auto"):
    lines = extract_lines(pdf_path, mode=mode)

    headings = detect_headings(lines)

    sorted_lines = sort_lines(lines)

    sections = build_sections(sorted_lines, headings)

    cleaned_sections = remove_non_clinical(sections)

    chunked_sections = build_rag_chunks(cleaned_sections)

    return {
        "sections": chunked_sections
    }