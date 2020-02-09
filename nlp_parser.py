from google.cloud import language

from google.cloud.language import enums
from google.cloud.language import types
e_types = enums.Entity.Type

from scraping import scrape

# Instantiates client
client = language.LanguageServiceClient()
# Set encoding type for documents
encoding_type = enums.EncodingType.UTF8
# Unwanted entity types
bad_types = [e_types.NUMBER, e_types.DATE, e_types.ADDRESS, e_types.WORK_OF_ART]


def ingredient_getter(ingredient_list):
    entity_list = []
    document = types.Document(
        content=ingredient_list,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document, encoding_type)
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        if enums.Entity.Type(entity.type) not in bad_types:
            entity_list.append(entity.name)

        print("\n")
    return entity_list


def main():
    print(ingredient_getter(scrape("https://www.simplyrecipes.com/recipes/eggs_benedict/")))


main()
