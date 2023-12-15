from django import template
from ..models import Author
from ..utils import get_mongo_db
from bson.objectid import ObjectId
import re


register = template.Library()


# def get_authors(id_):
#     db = get_mongo_db()
#     author = db.authors.find_one({'_id': ObjectId(id_)})
#     return author['fullname']


def get_authors(author_id):
    author = Author.objects.get(pk=author_id)
    return author.fullname

register.filter('author', get_authors)


def calculate_font_size(counter):
    return max(25 - 1.5*counter, 0)

register.filter('calculate_font_size', calculate_font_size)



def is_add_quote_page(path):
    return re.match(r'^/(\d+)?/?$', path) is not None


register.filter('is_add_quote_page', is_add_quote_page)