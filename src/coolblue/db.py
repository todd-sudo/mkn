import sqlite3


def get_cursor_db():
    con = sqlite3.connect('./coolblue.db')

    cur = con.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS product (
            Competitor text,
            CompetitorDetail text,
            SKU text,
            Name text,
            Category1 text,
            Category2 text,
            Category3 text,
            Category4 text,
            Category5 text,
            PriceSaving text,
            PriceBase text,
            AvailableOnline text,
            DeliveryTime text,
            DeliveryCost text,
            Brand text,
            Url text,
            ImageUrl text,
            Description text
        )
        '''
    )
    con.commit()
    print("таблица создана")
    # con.close()
    return cur, con
