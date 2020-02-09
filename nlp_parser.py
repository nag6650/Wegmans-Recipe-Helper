# Imports the Google Cloud client library
from google.cloud import language

from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

encoding_type = enums.EncodingType.UTF8


def ingredient_getter(ingredient_list):
    document = types.Document(
        content=ingredient_list,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document, encoding_type)
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

        print("\n")


def main():
    ingredient_getter(" 1/2. butter")


main()
