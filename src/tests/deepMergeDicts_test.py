""" Merging dicts testing """
from grappa import expect
from src.index import deepMergeDicts

class TestDeepMergeDicts:
    def testMergingTwoEqualDictsShouldResultInOnlyOne(self):
        original = {"settings": {"error": {"account": "account"}}}
        toBeMerged = {"settings": {"error": {"account": "account"}}}
        deepMergeDicts(original, toBeMerged)

        toBeMerged | expect.to.equal(original)

    def testMergingLeavesWithDifferentKeysShouldJoin(self):
        original = {"settings": {"error": {"settings": "hello"}}}
        toBeMerged = {"settings": {"error": {"account": "account"}}}
        deepMergeDicts(original, toBeMerged)

        original | expect.to.equal({'settings': {'error': {'settings': 'hello', 'account': 'account'}}})

    def testMergingChildNodesWithDifferentKeysShouldJoin(self):
        original = {"settings": {"different": {"settings": "hello"}}}
        toBeMerged = {"settings": {"error": {"account": "account"}}}
        deepMergeDicts(original, toBeMerged)

        original | expect.to.equal({'settings': {'different': {'settings': 'hello'}, 'error': {'account': 'account'}}})

    def testMergingParentNodesWithDifferentKeysShouldJoin(self):
        original = {"settings": {"different": {"settings": "hello"}}}
        toBeMerged = {"parent": {"different": {"settings": "hello"}}}
        deepMergeDicts(original, toBeMerged)

        original | expect.to.equal({'settings': {'different': {'settings': 'hello'}}, 'parent': {'different': {'settings': 'hello'}}})
