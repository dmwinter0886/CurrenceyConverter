# write your code here!
import requests
import json


class ConiCoin:
    def __init__(self):
        self.currencyRates = {}

    def convert_to_international_currency(self, currencyCode, convertedCurrencyCode):
        currencyCode = currencyCode.lower()
        convertedCurrencyCode = convertedCurrencyCode.lower()
        preConvertedAmount = float(input())
        currencyRate = self.get_currency_rate(currencyCode, convertedCurrencyCode)
        convertedAmount = preConvertedAmount * currencyRate
        print('You received {:.2f} {}'.format(convertedAmount, convertedCurrencyCode.upper()))

    def cache_usd_and_eur_rates(self, currencyToConvert):
        currencyToConvert = currencyToConvert.lower()
        response = requests.get('http://www.floatrates.com/daily/{}.json'.format(currencyToConvert))
        rates = json.loads(response.text)
        usdRate = rates.get('usd', False)
        eurRate = rates.get('eur', False)
        self.currencyRates['usd'] = usdRate['rate'] if usdRate else 1
        self.currencyRates['eur'] = eurRate['rate'] if eurRate else 1

    def get_currency_rate(self, currencyCode, convertedCurrencyCode):
        currencyCode = currencyCode.lower()
        print('Checking the cache...')
        currencyRate = self.currencyRates.get(convertedCurrencyCode, -1)
        if currencyRate > 0:
            print('Oh! It is in the cache!')
        else:
            print('Sorry, but it is not in the cache!')
            response = requests.get('http://www.floatrates.com/daily/{}.json'.format(currencyCode))
            rates = json.loads(response.text)
            self.currencyRates[convertedCurrencyCode] = rates[convertedCurrencyCode]['rate']
        return self.currencyRates[convertedCurrencyCode]


money = ConiCoin()
currencyCode = input()
convertedCurrencyCode = input()
money.cache_usd_and_eur_rates(currencyCode)
while convertedCurrencyCode != '':
    money.convert_to_international_currency(currencyCode, convertedCurrencyCode)
    convertedCurrencyCode = input()
