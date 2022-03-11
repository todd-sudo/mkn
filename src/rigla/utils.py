

async def chunks_regions(regions: list) -> list:
    regions1 = regions[0:10]
    regions2 = regions[10:20]
    regions3 = regions[20:40]
    regions4 = regions[40:50]
    regions5 = regions[50:62]
    return [regions1, regions2, regions3, regions4, regions5]
