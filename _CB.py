import re
import bs4 as bs 
import json
import Util

def get_start_urls():
    start_urls_cb = {'living':[ 
                            "https://www.crateandbarrel.com/furniture/sofas/1",
                            "https://www.crateandbarrel.com/furniture/sleeper-sofas/1",
                            "https://www.crateandbarrel.com/furniture/chairs/1",
                            "https://www.crateandbarrel.com/furniture/chaises/1",
                            "https://www.crateandbarrel.com/furniture/ottomans-and-cubes/1",
                            "https://www.crateandbarrel.com/furniture/benches/1",
                            "https://www.crateandbarrel.com/furniture/coffee-tables-and-side-tables/",
                            "https://www.crateandbarrel.com/furniture/media-stands-consoles/1",
                            "https://www.crateandbarrel.com/furniture/storage-cabinets/1",
                            "https://www.crateandbarrel.com/furniture/bar-cabinets-and-carts/1",
                            "https://www.crateandbarrel.com/furniture/chests-cabinets/1",
                            "https://www.crateandbarrel.com/furniture/tables/1",
                            "https://www.crateandbarrel.com/furniture/entryway-benches/1",
                            "https://www.crateandbarrel.com/furniture/wall-storages/1",
                            "https://www.crateandbarrel.com/furniture/coat-rack/1"
                        ],
                        'dining':[
                            "https://www.crateandbarrel.com/furniture/dining-tables/1",
                            "https://www.crateandbarrel.com/furniture/dining-chairs/1",
                            "https://www.crateandbarrel.com/furniture/barstools/1",
                            "https://www.crateandbarrel.com/furniture/chair-cushions/1",
                            "https://www.crateandbarrel.com/furniture/dining-benches/1",
                            "https://www.crateandbarrel.com/furniture/buffets-sideboards/1",
                            "https://www.crateandbarrel.com/furniture/dining-kitchen-storage/1"
                        ],
                        'bedroom':[
                            "https://www.crateandbarrel.com/furniture/beds/1",
                            "https://www.crateandbarrel.com/furniture/mattresses-foundations/1",
                            "https://www.crateandbarrel.com/furniture/nightstands/1",
                            "https://www.crateandbarrel.com/furniture/dressers-chests/1",
                            "https://www.crateandbarrel.com/furniture/armoires/1",
                            "https://www.crateandbarrel.com/furniture/bedroom-benches/1"
                        ],
                        'office':[
                            "https://www.crateandbarrel.com/furniture/desks/1",
                            "https://www.crateandbarrel.com/furniture/office-chairs/1",
                            "https://www.crateandbarrel.com/furniture/bookcases-cabinets/1",
                            "https://www.crateandbarrel.com/furniture/filing-cabinets-and-carts/1"
                        ],
                        'outdoor':[
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-patio-dining-furniture/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-patio-lounge-furniture/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-furniture-cushions/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-furniture-covers/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-furniture-cleaners/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-umbrellas/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-sectionals/1"
                        ],
                        'accessories':[
                            "https://www.crateandbarrel.com/decorating-and-accessories/decorative-pillows/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/outdoor-pillows/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/poufs/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/pillow-inserts/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/throws/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/candleholders/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/lanterns/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/candles/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/vases/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/baskets/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/botanicals-and-plants/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/sculpture/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/centerpiece-bowls/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/trays-platters/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/home-accents/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/fireplace-accessories/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/clocks/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/mirrors/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/frames/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/display-shelves-and-picture-ledges/1",
                            "https://www.crateandbarrel.com/furniture/mirrors/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/garden-and-patio-accessories/1",

                            # rugs
                            "https://www.crateandbarrel.com/rugs/all-rugs/1",
                            "https://www.crateandbarrel.com/rugs/outdoor-rugs/1",
                            "https://www.crateandbarrel.com/rugs/kitchen-and-entryway-rugs/1",
                            "https://www.crateandbarrel.com/rugs/floor-runners/1",
                            "https://www.crateandbarrel.com/bed-and-bath/bath-rugs/1",
                            "https://www.crateandbarrel.com/rugs/doormats/1",

                            #art
                            "https://www.crateandbarrel.com/decorating-and-accessories/prints/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/one-of-a-kind-art/1",
                            "https://www.crateandbarrel.com/decorating-and-accessories/wall-art/1",
                        ],
                        'lighting':[
                            "https://www.crateandbarrel.com/lighting/chandeliers-pendants/1",
                            "https://www.crateandbarrel.com/lighting/table-desk-lamps/1",
                            "https://www.crateandbarrel.com/lighting/floor-lamps/1",
                            "https://www.crateandbarrel.com/lighting/sconces/1",
                            "https://www.crateandbarrel.com/outdoor-furniture/outdoor-lighting/1",
                        ]
                        }

    return start_urls_cb

def getPrice(soup):
    tmp_original = soup.select("div.shop-bar-right-product-info span.regPrice")[0].string

    tmp_sale = soup.select("div.shop-bar-right-product-info span.salePrice")
    if len(tmp_sale) > 0: 
        tmp_sale = tmp_sale[0].string
    else:
        tmp_sale = tmp_original
        
    # print tmp_original
    # print tmp_sale

    original = re.search('\d+([.,]\d+)+', tmp_original).group(0)
    sale = re.search('\d+([.,]\d+)+', tmp_sale).group(0)
    original = original.replace(',', '')
    sale = sale.replace(',', '')

    return float(original), float(sale)


def getImageUrl(soup):
    tmp_images = ["https:"+e['src'] for e in soup.select('div.showcase-thumbnail  div.slick-slide img')]

    tmp_images = tmp_images[::-1]

    imageUrls = [e.replace('wid=60&hei=60', 'wid=1060&hei=1060') for e in tmp_images]
    imageUrlsSmall = [e.replace('wid=60&hei=60', 'wid=500&hei=500') for e in tmp_images]
    thumbImage = imageUrls[0].replace('wid=1060&hei=1060', 'wid=350&hei=350')

    return imageUrls, imageUrlsSmall, thumbImage

def get_nav_title(soup):
    nav_list = []
    tmp_list = soup.select("ul.breadcrumb-list li a")
    nav_list = [e.text for e in tmp_list]
    return nav_list

# download products
def downloadProduct(html, url, outfile, categoryName, search_dic, category_id):
    print "[ DM_info ] " + url

    soup = bs.BeautifulSoup(html, 'html.parser')
    try:
        item = {}
        item['storeName'] = "crateandbarrel"


        item['storeId'] = '365'
        item['productUrl'] = url
        
        item['originalPrice'], item['salePrice'] = getPrice(soup)
        item['title'] = soup.select_one("h1.shop-bar-product-title").string.strip()


        description = soup.select_one('div[data-module="description"]')
        if description is not None:
            description = description['data-description']
        else:
            description = soup.select_one("div.tabpanel div").text
        item['description'] = re.sub('(<(/)?div>)?', '', description).strip()

        tmp_dim = ''.join(e.text for e in soup.select('div.dimensions-details p'))

        item['width'], item['depth'], item['height'] = Util.dimension_helper(tmp_dim)
        item['dimensionsString'] = tmp_dim

        item['imageUrls'], item['imageUrlsSmall'], item['thumbImageUrl'] = getImageUrl(soup)
        # item['processedImageUrls'] = Util.aws_image_url_helper(item['imageUrls'])

        # get the key words from title and subcategory
        titlelower = item['title'].lower()
        title = re.sub(r'[^a-zA-Z ]', '', titlelower)
        item['keywords'] = title.split()

        # # add keyword for holiday
        # keyword_holiday = response.meta.get('dm_keyword_holiday')
        # if len(keyword_holiday) > 1:
        #     item['keywords'].append(unicode(keyword_holiday))
        #     item['keywords'].append(u'holiday')

        # item['color'] = getColor()
        item['address'] = "301 Santana Row, San Jose CA, 95128"
        sku = soup.select_one("span.shop-bar-sku-number")
        if sku is not None:
            item['sku'] = sku.string


        item['categoryName'] = categoryName
        item['categoryId'] = category_id[item['categoryName']]

        # generate subcategory
        candidates = get_nav_title(soup) + item['keywords']
        item['subCategoryName'] = Util.getSubcategory(candidates, search_dic, item['categoryName'])
        item['subCategoryId'] = category_id[item['categoryName']+'|'+item['subCategoryName']]

        print item['title'] + " is done"
        json.dump(item, outfile)
        outfile.write(',\n')
    except Exception as e:
        print e
        print "err happened when downloading products from " + url