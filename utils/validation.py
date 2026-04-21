def format_pydantic_errors(errors) -> str:
    messages = []

    for err in errors:
        location = ".".join([str(loc) for loc in err["loc"]])
        msg = err["msg"]

        messages.append(f"{location}: {msg}")

    return "\n".join(messages)