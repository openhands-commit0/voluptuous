import typing
from voluptuous import Invalid, MultipleInvalid
from voluptuous.error import Error
from voluptuous.schema_builder import Schema
MAX_VALIDATION_ERROR_ITEM_LENGTH = 500

def humanize_error(data, validation_error: Invalid, max_sub_error_length: int=MAX_VALIDATION_ERROR_ITEM_LENGTH) -> str:
    """Provide a more helpful + complete validation error message than that provided automatically
    Invalid and MultipleInvalid do not include the offending value in error messages,
    and MultipleInvalid.__str__ only provides the first error.
    """
    if isinstance(validation_error, MultipleInvalid):
        return '\n'.join(sorted(
            humanize_error(data, sub_error, max_sub_error_length)
            for sub_error in validation_error.errors
        ))

    path = validation_error.path
    value = data

    # Walk the path to find the value
    for step in path:
        if isinstance(value, (list, tuple)):
            value = value[step]
        else:
            value = value.get(step, 'N/A')

    # Truncate value if too long
    str_value = str(value)
    if len(str_value) > max_sub_error_length:
        str_value = str_value[:max_sub_error_length] + '...'

    # Build the error message
    path_str = ' @ data[%s]' % ']['.join(repr(p) for p in path) if path else ''
    error_type = ' for ' + validation_error.error_type if validation_error.error_type else ''
    
    return '%s%s (got %r)%s' % (
        validation_error.error_message,
        error_type,
        str_value,
        path_str
    )