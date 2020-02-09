"""
file: nlp_parser.py
event: Brick Hack 6
author: Ethan Howes
Purpose: Finds "food" entities within
ingredients text scraped from website
"""

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

e_types = enums.Entity.Type

# Instantiates client
client = language.LanguageServiceClient()
# Set encoding type for documents
encoding_type = enums.EncodingType.UTF8
# Unwanted entity types
bad_types = [e_types.NUMBER, e_types.DATE, e_types.ADDRESS, e_types.WORK_OF_ART, e_types.EVENT,
             e_types.LOCATION, e_types.PRICE, e_types.PHONE_NUMBER]

# Unwanted words
bad_words = ["Ingredients", "ingredients", "teaspoon", "tablespoon", "garnish", "main", "Dash", "dash",
             "Blender", "blender", "package", "Package", "kind", "Kind", "Cup", "cup", "more", "More",
             "size", "Size", "little", "Little", "pound", "Pound", "foil", "Foil", "stick", "Stick",
             "choice", "Choice", "store", "Store", "store-bought", "Store-bought", "home-made",
             "Home-made", "pieces", "Pieces", "total", "Total", "head", "Head", "slices", "Slices",
             "english", "English"]

# Words we don't want to take out
good_words = ["lime", "Lime", "jalapenos", "Jalapenos", "red peppers", "green peppers", "yellow peppers",
              "mayonnaise", "English muffins", "english muffins", "Hollandaise", "hollandaise", "grapes",
              "Grapes","thyme", "Thyme", "pepper", "Pepper", "honey", "Honey", "turkey", "Turkey", "ham",
              "Ham"]


def noise_remover(ingredient_list):
    """ Filters out unwanted words"""
    ingredients_parsed = ingredient_list.split(" ")
    good_ingredients = []
    for w in ingredients_parsed:
        if w not in bad_words:
            good_ingredients.append(w)
    return " ".join(good_ingredients)


def ingredient_getter(ingredient_list):
    """Calls functions necessary to remove noise in text, sets
    aside 'good' words that should be kept, and analyses the final
    text for entities to return final food entity list"""
    ingredient_list = noise_remover(ingredient_list)

    entity_list = []

    # Keep words in the good list
    for w in ingredient_list.split(" "):
        if w in good_words:
            entity_list.append(w)

    document = types.Document(
        content=ingredient_list,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document, encoding_type)
    # Perform entity analysis
    for entity in response.entities:

        if enums.Entity.Type(entity.type) not in bad_types:
            entity_list.append(entity.name)

    entity_list = list(dict.fromkeys(entity_list))
    return entity_list
