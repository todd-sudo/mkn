

def get_categories(categories: list):
    try:
        category1 = categories[0]
    except IndexError:
        category1 = ""
    try:
        category2 = categories[1]
    except IndexError:
        category2 = ""
    try:
        category3 = categories[2]
    except IndexError:
        category3 = ""
    try:
        category4 = categories[3]
    except IndexError:
        category4 = ""
    try:
        category5 = categories[4]
    except IndexError:
        category5 = ""

    return category1, category2, category3, category4, category5
