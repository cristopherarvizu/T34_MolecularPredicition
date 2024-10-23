from django import template

register = template.Library()

@register.filter
def truncate_chars(value, max_length=10):
    """
    Truncates a string to a specified number of characters and adds an ellipsis if necessary.
    """
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value
