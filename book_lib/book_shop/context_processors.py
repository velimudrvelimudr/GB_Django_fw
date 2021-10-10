
def user_book_count(request):
    """ добавляет в контекст количество книг в библиотеке пользователя """

    user_count = None

    if request.user.is_authenticated:
        user_count = request.user.user_count

    return {
        'user_count':user_count
    }
