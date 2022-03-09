from src.rigla.parser import get_products_rigla
from src.rigla.categories import get_categories
# from src.tvoydom.parser.categories import get_categories
from src.tvoydom.parser.product import get_products
from src.tvoydom.parser.utils import format_categories


def main():
    get_products_rigla()


if __name__ == '__main__':
    main()
