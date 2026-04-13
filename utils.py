def bool_value(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() == "true"
    return bool(v)


def first_or_none(seq):
    return seq[0] if seq else None


def entity_name(entity):
    try:
        if hasattr(entity, "label") and entity.label:
            return str(entity.label[0])
    except Exception:
        pass
    return getattr(entity, "name", str(entity))


def format_list(items):
    items = list(items)
    if not items:
        return "None"
    return ", ".join(sorted(entity_name(x) for x in items))
