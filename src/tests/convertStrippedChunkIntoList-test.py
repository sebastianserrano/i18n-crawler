""" Regex testing """
from grappa import expect
from src.index import convertStrippedChunkIntoList

class TestConvertStrippedChunkIntoList:
    def testFunctionExtractsWordsSeparatedByDot(self):
        line = 'editProduct.genre.error'
        result = convertStrippedChunkIntoList(line)

        result | expect.to.contain('editProduct', 'genre', 'error')

    def testExtractionIsInRightOrder(self):
        line = 'editProduct.genre.error'
        result = convertStrippedChunkIntoList(line)

        result | expect.to.start_with.items('editProduct', 'genre', 'error')

    def testExtractionFailsWhenIsNotInRightOrder(self):
        line = 'editProduct.genre.error'
        result = convertStrippedChunkIntoList(line)

        result | expect.not_to.start_with.items('genre', 'error', 'editProduct')
