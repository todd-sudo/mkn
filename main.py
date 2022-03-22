import asyncio
import json

from src.coolblue.parser import run_parser_coolblue
from src.rigla.parser import run_parser_rigla
from src.rigla.categories import get_categories
# from src.tvoydom.parser.categories import get_categories
from src.tvoydom.parser.product import get_products
from src.tvoydom.parser.utils import format_categories


# async def main():
#     await run_parser_rigla()
#     print("#готоводело")
#
#
# if __name__ == '__main__':
#     asyncio.run(main())


def main():
    run_parser_coolblue()
    print("#готоводело")


if __name__ == '__main__':
    main()

