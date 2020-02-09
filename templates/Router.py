"""
file: Router.py
event: Brick Hack 6
author: Albin Liang
Version: 0.1
Purpose: This will make the Wegman's API call to get a JSON List of all products from a generic food term name.
"""

import requests
from collections import OrderedDict

URLBEG = "https://api.wegmans.io/products/"
URLEND = "api-version=2018-10-18&subscription-key=c776a0f5153a4b5d8ac80f114e7ce3a1"
STORE = "25"

def getSkuRoute( prodName ):

    prodSearch = "search?query="
    quoteProdName = '"' + prodName + '"'

    url = URLBEG + prodSearch + quoteProdName + '&' + URLEND

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)


    obj = response.json()

    # print(json.dumps(obj, indent=4))

    # print(obj["results"])
    # print(type(obj["results"]))
    availSkuList = []

    for things in obj["results"]:

        #check availability in store
        avail = getAvailabilityRoute(things["sku"], STORE)
        if (avail): #add the available ones to a list
            availSkuList.append( things["sku"] )

    if(len(availSkuList)==0):
        return "No Availabilities"
    #for all the available ones append the price
    priceDict = {}
    for sku in availSkuList:
        price = getPricesRoute(sku, STORE)
        priceDict[sku] = price

    sortedPriceDict = OrderedDict(sorted(priceDict.items(), key = lambda kv:(kv[1], kv[0])))
    lowPriceTup = (next(iter(sortedPriceDict.items())))
    print(lowPriceTup[0])
    print(lowPriceTup[1])


def getAvailabilityRoute( skuNum, storeNum ):


        availSearch = "/availabilities/"

        url = URLBEG + str(skuNum) + availSearch + str(storeNum) + '?' + URLEND

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        obj = response.json()

        # print(json.dumps(obj, indent=4))
        # print(type(obj))
        for keys, values in obj.items():
            if (values == True):
                # availItemList.append(obj["sku"])
                return True;


def getPricesRoute(skuNum, storeNum):
    priceSearch = "/prices/"

    url = URLBEG + str(skuNum) + priceSearch + str(storeNum) + '?' + URLEND

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    obj = response.json()

    # print(json.dumps(obj, indent=4))
    # print(type(obj))
    return obj["price"]
            # availItemList.append(obj["sku"])


if __name__ == "__main__":

    test_term = input("Enter a food item\n")
    getSkuRoute(str(test_term))
    input("Close window to exit\n")