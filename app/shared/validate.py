
from uuid import UUID

def _missing_key_error(key):
    return {'data': [],
            'reason': 'Missing key: {}'.format(key),
            'status_code': 1001}

def _empty_key_error(key):
    return {'data': [],
            'reason': 'Invalid value for key: {}'.format(key),
            'status_code': 1002}

def _invalid_uuid_error(value):
    return {'data': [],
            'reason': 'Malformed UUID: {} in URL'.format(value),
            'status_code': 1003}

def _evaluate(l, d, m):
    """
    validate existence of all keys in l
    validate data type of all values in d
    keys are mandatory or optional per m
    args:
        l: list of expected keys
        d: dict of actual keys, values
        m: boolean 
    """
    for e in l:
        if e not in d and m:
            return (True, _missing_key_error(e))
    for e in l:
        if e not in d:
            continue
        elif d[e] is None:
            return(True, _empty_key_error(e))
        elif isinstance(d[e], str) and len(d[e]) == 0:
            return(True, _empty_key_error(e))
        elif e.endswith('_id'):
            try:
                uuid = UUID(e)
            except ValueError as err:
                return(True, _invalid_uuid_error(e))
    return (False, d)

def evaluate_form(keys, form, mandatory=False):
    return _evaluate(keys, form, mandatory)

def evaluate_args(keys, form, mandatory=False):
    return _evaluate(keys, args, mandatory)

def evaluate_uuid(value):
    """
    validate value is a valid UUID
    args:
        value: UUID
    """
    try:
        uuid = UUID(value)
        return(False, value)
    except ValueError as e:
        return(True, _invalid_uuid_error(value))
