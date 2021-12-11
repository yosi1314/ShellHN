import logging
from app.consts import validator_consts as vc, hm_utils_consts as hm


def _is_int(user_input):
    try:
        return int(user_input)
    except ValueError:
        print(vc.IS_INT_MSG)
        return False


def _is_in_range(user_input):
    if user_input <= hm.DEFAULT_LIMIT and user_input > hm.MIN_RESULTS:
        return user_input
    print(vc.IS_IN_RANGE_MSG)
    return False


_user_input_validations = [_is_int, _is_in_range]


def validate_user_input(answers, key, input_func, *input_func_params, **kwinput_func_params):
    attempt = 1
    while attempt <= 3:
        user_input = answers[key]
        for validator in _user_input_validations:
            user_input = validator(user_input)
            if user_input is False:
                break
        if user_input is False and attempt != 3:
            attempt += 1
            answers = input_func(*input_func_params, **kwinput_func_params)
        elif attempt == 2:
            print(vc.BAD_INPUT_MSG)
            logging.exception(vc.BAD_INPUT_LOG)
            raise SystemExit(vc.BAD_INPUT_LOG)
        else:
            return user_input
