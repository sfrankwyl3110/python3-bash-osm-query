def reduce_dict_by_keys(original_dict: dict, keys_keep: list) -> dict:
    return {key: original_dict[key] for key in keys_keep if key in original_dict}


def max_key(input_dict: dict, key_max: str) -> dict:
    return max(input_dict, key=lambda x: x[key_max])


def list_to_csl(input_list: list) -> str:
    return ",".join(input_list)
