""" Merging dictionaries while replacing leave's values testing """
from grappa import expect
from src.index \
    import intersectDictionaries,\
    checkDictionaryHasMoreThanOneValue,\
    checkValueIsNotADictionary,\
    checkValueIsDictionary


class TestIntersectDictionaries:
    def testMergingTwoDictsShouldResultInAChangeOfLeafValue(self):
        sanitized = {"settings": {"error": {"account": "account"}}}
        toBeMerged = {"settings": {"error": {"account": "Actual Leave Value"}}}
        intersectDictionaries(sanitized, toBeMerged)

        sanitized | expect.to.equal({'settings': {'error': {'account': 'Actual Leave Value'}}})

    def testMergingTwoDictsWithDifferentKeysShouldNotChangeSanitized(self):
        sanitized = {"settings": {"error": {"different": "account"}}}
        toBeMerged = {"settings": {"error": {"account": "Actual Leave Value"}}}
        intersectDictionaries(sanitized, toBeMerged)

        sanitized | expect.to.equal({"settings": {"error": {"different": "account"}}})

    def testDictionaryValueCheckerReturnsTrueWhenHavingValues(self):
        sanitized = {"settings": "One Value"}
        result = checkDictionaryHasMoreThanOneValue(sanitized)

        result | expect.to.be.true

    def testDictionaryValueCheckerReturnsFalseWhenHavingNoValues(self):
        sanitized = {}
        result = checkDictionaryHasMoreThanOneValue(sanitized)

        result | expect.to.be.false

    def testValueIsNotADictionary(self):
        sanitized = {"key": "Not A Dictionary Value"}
        result = checkValueIsNotADictionary(sanitized)

        result | expect.to.be.true

    def testShouldFailWhenValueIsADictionary(self):
        sanitized = {"key": {"anotherKey": "Not A Dictionary Value"}}
        result = checkValueIsNotADictionary(sanitized)

        result | expect.to.be.false

    def testValueIsADictionary(self):
        sanitized = {"key": {"anotherKey": "Not A Dictionary Value"}}
        for key in sanitized:
            result = checkValueIsDictionary(sanitized, key)

            result | expect.to.be.true

    def testShouldFailWhenValueIsNotADictionary(self):
        sanitized = {"key": "string"}
        for key in sanitized:
            result = checkValueIsDictionary(sanitized, key)

            result | expect.to.be.false

