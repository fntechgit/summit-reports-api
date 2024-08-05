from graphene import ObjectType, String


class CustomDictionary(ObjectType):
    key = String()
    value = String()