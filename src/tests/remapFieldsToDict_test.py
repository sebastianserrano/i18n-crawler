""" List to dict conversion testing """
from grappa import expect
from src.index import remapFieldsToDict

class TestRemapFieldsToDict:
    def testDictIsInRightShape(self):
        array = ['editProduct', 'error', 'settings']
        result = remapFieldsToDict(array)

        result | expect.to.equal({'editProduct': {'error': {'settings': 'settings'}}})

    def testResultIsADict(self):
        array = ['editProduct', 'error', 'settings']
        result = remapFieldsToDict(array)

        result | expect.to.be.a('dict')

