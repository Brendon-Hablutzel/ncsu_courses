def assert_dicts_equals(expected_dict, actual_dict):
    for key in expected_dict.keys():
        dict1_element = expected_dict[key]
        try:
            dict2_element = actual_dict[key]
        except KeyError:
            raise AssertionError(f"key {key} not found in second dictionary")

        assert dict1_element == dict2_element
