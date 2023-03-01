from .models import Category

def menu_links(request):
    """
    Gets all of the category data in a variable
    Then in settings.py it is configured so that the menu links can be accessed in any template
    """
    links = Category.objects.all()
    return dict(links=links)
