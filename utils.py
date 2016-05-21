def parse_enum_into_dict(enum_class):
    translate_dict = {}
    for enum in enum_class:
        translate_dict[enum.name] = enum
    return translate_dict
