# content of test_sample.py
from src import index

class Testi18nRegex:
    def testI18nMatchesIsolatedLine(self):
        line = 'i18n.t("settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        assert match

    def testRegularLine(self):
        lineOne = 'messages: [i18n.t("productSync.error")],'
        lineTwo = 'content: i18n.t("settings.expiryBanner.updateRMSKey"),'

        matchOne = index.checkI18nExistance(lineOne)
        matchTwo = index.checkI18nExistance(lineTwo)

        assert match

    def testI18nWithMultipleParameters(self):
        line = 'string += i18n.t("settings.expiryBanner.titleDays", daysToExpiry) + " "'
        match = index.checkI18nExistance(line)
        assert match

    def testI18nDoesNotMatchWithoutOpeningParenthesis(self):
        line = 'i18n.t"settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        assert not match

    def testI18nDoesNotMatchWithoutClosingParenthesis(self):
        line = 'i18n.t("settings.expiryBanner.expired"'
        match = index.checkI18nExistance(line)
        assert not match

    def testI18nDoesNotMatchWithoutOpeningQuotes(self):
        line = 'i18n.t(settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        assert not match

    def testI18nDoesNotMatchWithoutClosingQuotes(self):
        line = 'i18n.t("settings.expiryBanner.expired)'
        match = index.checkI18nExistance(line)
        assert not match

    def testI18nDoesNotMatchWithoutOpeningNecessaryi18n_tCall(self):
        line = '("settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        assert not match
