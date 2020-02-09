"""
file: Router.py
event: Brick Hack 6
author: Albin Liang
Version: 0.1
Purpose: This will make the Wegman's API call to get a JSON List of all products from a generic food term name.
"""

import requests
import json
import time
import functools
from collections import OrderedDict

URLBEG = "https://api.wegmans.io/products/"
APIVERSION = "api-version=2018-10-18&subscription-key="
APIKEY = "bfe5e563c583455bb5d648e755550000"
URLEND = APIVERSION + APIKEY
STORE = "25"

# @functools.lru_cache(maxsize=128)
def getItemRoute( prodName ):
    """

    :param prodName:
    :return:
    """

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
    resultsList = obj["results"]
    # for result in resultsList:
        # GET_COUNT += 1
        # if (GET_COUNT > 90):
        #     APIKEY = key_rotator.next_key(key_rotator.KEYCHAIN)
        #     GET_COUNT = 0
        # avail = getAvailabilityRoute(result["sku"], STORE)
        # if (avail == True):
        #     availSkuList.append(result["sku"])
    if (len(resultsList) > 15):
        for i in range(0, 15, 1):

            # randomItem = random.choice(resultsList)
            # check availability in store
            # avail = getAvailabilityRoute(randomItem["sku"], STORE)
            avail = getAvailabilityRoute(resultsList[i]["sku"], STORE)
            if (avail==True): #add the available ones to a list
                availSkuList.append(resultsList[i]["sku"])
    else:
        for results in resultsList:
            avail = getAvailabilityRoute(results["sku"], STORE)
            if (avail==True): #add the available ones to a list
                availSkuList.append(results["sku"])




    if(len(availSkuList)==0):
        unavailDict = { "name" : "No availabilities at this location" }
        print(unavailDict)
        return unavailDict

    #for all the available ones append the price
    priceDict = {}
    for sku in availSkuList:
    #     GET_COUNT += 1
    #     if (GET_COUNT > 90):
    #         APIKEY = key_rotator.next_key(key_rotator.KEYCHAIN)
    #         GET_COUNT = 0
        price = getPricesRoute(sku, STORE)
        if price != "error":
            priceDict[sku] = price


    if(len(priceDict)==0):
        unavailDict = { "name" : "No prices available" }
        print(unavailDict)
        return unavailDict



    sortedPriceDict = OrderedDict(sorted(priceDict.items(), key = lambda kv:(kv[1], kv[0])))
    print(sortedPriceDict)
    lowPriceTup = (next(iter(sortedPriceDict.items())))

    lowestPrice = lowPriceTup[1]
    lowestSku = lowPriceTup[0]

    #get location info and get the individual values
    # GET_COUNT += 1
    # if (GET_COUNT > 90):
    #     APIKEY = key_rotator.next_key(key_rotator.KEYCHAIN)
    #     GET_COUNT = 0
    infoLoc = getLocRoute(lowestSku, STORE)

    lowestAisle = infoLoc[0]
    lowestSide = infoLoc[1]
    lowestShelf = infoLoc[2]

    for result2 in obj["results"]:
        # check availability in store
        if (result2["sku"] == lowestSku):  # add the available ones to a list
            lowestName = result2["name"]

    #create the finalized dictionary with name, price, and location(aisle,side,shelf)
    itemKeyNames = ["name", "price", "aisle", "aisleSide", "shelf"]
    itemKeyValues = [lowestName, lowestPrice, lowestAisle, lowestSide, lowestShelf]

    item_dict = dict(zip(itemKeyNames, itemKeyValues))


    return item_dict

def getAvailabilityRoute( skuNum, storeId ):
    """

    :param skuNum:
    :param storeId:
    :return:
    """
    availSearch = "/availabilities/"

    url = URLBEG + str(skuNum) + availSearch + str( storeId ) + '?' + URLEND

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    obj = response.json()

    try:
        return(obj["isAvailable"])
    except Exception:
        return None




def getPricesRoute(skuNum, storeId):
    """

    :param skuNum:
    :param storeId:
    :return:
    """
    priceSearch = "/prices/"

    url = URLBEG + str(skuNum) + priceSearch + str(storeId) + '?' + URLEND

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    obj = response.json()
    # print(json.dumps(obj, indent=4))
    # print(type(obj))
    # return obj["price"]
            # availItemList.append(obj["sku"])

    try:
        return obj["price"]
    except Exception:
        return "error"

def getLocRoute(skuNum, storeId):
    """

    :param skuNum:
    :param storeId:
    :return:
    """
    locations = "/locations/"

    url = URLBEG + str(skuNum) + locations + storeId + '?' + URLEND

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    obj = response.json()

    try:
        aisleNum = obj["locations"][0]["name"]
    except Exception:
        aisleNum = None

    try:
        aisleSide = obj["locations"][0]["aisleSide"]
    except Exception:
        aisleSide = None
    try:
        shelfNum = obj["locations"][0]["shelfNumber"]
    except Exception:
        shelfNum = None

    locInfo = (aisleNum, aisleSide, shelfNum)

    return locInfo
#
# if __name__ == "__main__":
#     test_term = input("Enter a food item\n")
#     start_time = time.time()
#     print(getItemRoute(test_term))
#     end_time = time.time()
#     print(end_time-start_time)


    # getSkuRoute("cheddar cheese")
    # getSkuRoute("ham")
