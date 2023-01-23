"""
Example of a class that acts like a string, but can have additional references.
Essentially makes use of customly overloaded comparison functions
"""


class EntityToken:
    text: str
    entity_ref: str

    def __init__(self, text: str, entity_ref: str):
        self.text = text
        self.entity_ref = entity_ref

    def __eq__(self, other):
        if isinstance(other, EntityToken):
            # Could be changed to accommodate only matching on entity_ref, too.
            return self.text == other.text and self.entity_ref == other.entity_ref
        elif isinstance(other, str):
            return self.text == other
        else:
            raise NotImplementedError(f"Comparison between EntityToken and {type(other)} not defined!")


if __name__ == '__main__':
    tup1 = (EntityToken("Peter", "ENT01"), "is", "tall")
    tup2 = ("Peter", "is", "tall")
    tup3 = ("Peter", "is", "small")
    tup4 = (EntityToken("Peter", "ENT02"), "is", "tall")
    tup5 = (EntityToken("Frank", "ENT01"), "is", "tall")

    print(tup1 == tup2)
    print(tup1 == tup3)
    print(tup1 == tup4)
    print(tup1 == tup5)