import inspect


def get_class_members(cls):
    members = inspect.getmembers(cls, lambda member: not inspect.isroutine(member))
    return [member for member in members if not member[0].startswith('__')]


def create_validator(*keys, _or=False):
    def validator(_dict):
        if not isinstance(_dict, dict):
            return False
        conds = ((key in _dict) for key in keys)
        return any(conds) if _or else all(conds)
    return validator


valid_book_object = create_validator('name', 'price', 'isbn')

valid_put_request_data = create_validator('name', 'price')

valid_patch_request_data = create_validator('name', 'price', _or=True)
