from django import template

register = template.Library()

@register.filter(name='hum_bool')
def hum_bool(b):
    """ Выводит булевы переменные (True/False) в удобочитаемом виде. """
    # Пример использования в шаблоне admin_app/user_info.html.

    if isinstance(b, bool):
        return 'ДА' if b else 'НЕТ'
    else:
        return b

