from dataclasses import asdict as std_asdict


def asdict(obj):
    the_dict = {
        **std_asdict(obj),
        **{a: getattr(obj, a) for a in getattr(obj, "__serialize__", [])},
    }
    return the_dict
