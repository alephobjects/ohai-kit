from django import template
register = template.Library()

@register.filter
def columnize(item_list, period):
    """
    Take a list of items [1, 2, 3, 4, 5, 6, 7] and break it up into
    sub lists of some arbitrary period [[1, 2, 3, 4], [5, 6, 7]].
    """
    columns = []
    ct = 0
    for item in item_list:
        if ct % period == 0:
            columns.append([])
        columns[-1].append(item)
        ct += 1

    return columns

