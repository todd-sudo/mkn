import asyncio
import json

from src.rigla.parser import run_parser
from src.rigla.categories import get_categories
# from src.tvoydom.parser.categories import get_categories
from src.tvoydom.parser.product import get_products
from src.tvoydom.parser.utils import format_categories


async def main():
    await run_parser()


if __name__ == '__main__':
    asyncio.run(main())
