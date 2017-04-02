import requests
from lxml import etree

URL_TITLE = 'https://ru.wikipedia.org/w/api.php?format=json&action=query&prop=categories&titles={title}'
URL_CATEGORY = 'https://ru.wikipedia.org/w/api.php?action=categorytree&format=json&category={category}&options=%7B%22mode%22%3A0%2C%22hideprefix%22%3A20%2C%22showcount%22%3Afalse%2C%22namespaces%22%3Afalse%7D&uselang=ru&formatversion=2'
URL_CATEGORY_REVERSE = 'https://ru.wikipedia.org/w/api.php?action=categorytree&format=json&category={category}&options=%7B%22mode%22%3A100%2C%22hideprefix%22%3A20%2C%22showcount%22%3Afalse%2C%22namespaces%22%3Afalse%7D&uselang=ru&formatversion=2'


def add_category(category, categories, stack):
    if category.find('Википедия:') == -1 and category not in categories:
        categories.add(category)
        stack.append(category)
        print(category)


def pop_category(stack):
    category = None
    try:
        category = stack.pop()
    except:
        pass
    return category


def get_title_categories(title):
    r = requests.get(URL_TITLE.format(title=title))
    import json
    j = json.loads(r.text)
    categories = set()
    stack = []
    for page in j['query']['pages'].values():
        for category in page['categories']:
            add_category(category['title'][10:], categories, stack)
    return categories


def get_categories_reverse(category):
    r = requests.get(URL_CATEGORY_REVERSE.format(category=category))
    text = '<html>' + r.text[25:-3].replace('\\n', '').replace('\\t', '').replace('\\', '') + '</html>'
    m = etree.fromstring(text).xpath("//a")
    result = []
    for i in m:
        result.append(i.text)
    return result


def get_categories_reverse2(category):
    categories = set()
    stack = []
    while category:
        r = get_categories_reverse(category)
        for category in r:
            add_category(category, categories, stack)
        category = pop_category(stack)
    return categories


def get_categories(category='Всё', depth=1):
    r = requests.get(URL_CATEGORY.format(category=category))
    text = '<html>' + r.text[25:-3].replace('\\n', '').replace('\\t', '').replace('\\', '') + '</html>'
    m = etree.fromstring(text).xpath("//a")
    result = []
    for i in m:
        result.append(i.text)
    return result


if __name__ == '__main__':
    categories = set()
    stack = []
    index = {}

    # title = 'Улица_Республики_(Тюмень)'
    # categories = get_title_categories(title)
    # result = set()
    # for category in categories:
    #     result.update(get_categories_reverse(category))
    root = 'Туризм'

    import entity

    obj = entity.Entity(root, [])
    index[obj.title] = obj

    while obj:
        result = get_categories(obj.title)

        for category in result:
            if category.find('Википедия:') == -1 and category not in index:
                child_entity = entity.Entity(category, [obj])
                index[category] = child_entity
                stack.append(child_entity)
                print(category)
        obj = pop_category(stack)






