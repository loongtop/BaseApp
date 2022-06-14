

def get_choice_text(title, field):
    """
    When defining a column in the component,
    if the choice wants to display Chinese information, just call this method.
    :param title:
    :param field:
    :return:
    """
    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        method = f"get_{field}_display"
        return getattr(obj, method)()

    return inner
