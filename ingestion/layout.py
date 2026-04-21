def sort_lines(lines):
    """
    Ensures correct reading order for:
    - 1 column
    - 2 column
    """

    def key(x):
        # 2-column: left column first, then right
        col_priority = 0 if x.get("col") == "left" else 1
        return (x["page"], col_priority, x["y"])

    return sorted(lines, key=key)