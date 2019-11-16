""" Regex testing """
from grappa import expect
from src import index

class Testi18nRegex:
    def testI18nMatchesIsolatedLine(self):
        line = 'i18n.t("settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.true

    def testRegularLine(self):
        lines = ['messages: [i18n.t("productSync.error")],',
                 'content: i18n.t("settings.expiryBanner.updateRMSKey"),']

        results = [bool(index.checkI18nExistance(x)) for x in lines]
        results | expect.to_not.contain(False)

    def testI18nWithMultipleParameters(self):
        line = 'string += i18n.t("settings.expiryBanner.titleDays", daysToExpiry) + " "'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.true

    def testI18nDoesNotMatchWithoutOpeningParenthesis(self):
        line = 'i18n.t"settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.false

    def testI18nDoesNotMatchWithoutClosingParenthesis(self):
        line = 'i18n.t("settings.expiryBanner.expired"'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.false

    def testI18nDoesNotMatchWithoutOpeningQuotes(self):
        line = 'i18n.t(settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.false

    def testI18nDoesNotMatchWithoutClosingQuotes(self):
        line = 'i18n.t("settings.expiryBanner.expired)'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.false

    def testI18nDoesNotMatchWithoutOpeningNecessaryi18n_tCall(self):
        line = '("settings.expiryBanner.expired")'
        match = index.checkI18nExistance(line)
        bool(match) | expect.to.be.false
