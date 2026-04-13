def get_class(onto, name):
    """
    Robust class lookup by class name or label.
    This avoids crashes where getattr(onto, 'RegularPlayer') returns None.
    """
    target = name.strip().lower()

    for cls in onto.classes():
        if getattr(cls, "name", "").lower() == target:
            return cls

        if hasattr(cls, "label"):
            for lbl in cls.label:
                if str(lbl).strip().lower() == target:
                    return cls

    return None


def all_instances(onto, class_name):
    cls = get_class(onto, class_name)
    return list(cls.instances()) if cls else []


def find_by_name_or_label(instances, user_text):
    target = user_text.strip().lower()

    for inst in instances:
        if getattr(inst, "name", "").lower() == target:
            return inst

        if hasattr(inst, "label"):
            for lbl in inst.label:
                if str(lbl).strip().lower() == target:
                    return inst

    return None


def get_player(onto, name):
    return find_by_name_or_label(all_instances(onto, "Player"), name)


def get_space(onto, name):
    return find_by_name_or_label(all_instances(onto, "Space"), name)


def get_group(onto, name):
    return find_by_name_or_label(all_instances(onto, "PropertyGroup"), name)
