import requests

url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
response = requests.get(url)

devises = response.json()  # Salva a resposta em formato JSON na variável `cotacoes`

#print(devises)


#Dictionnaire des taux de change des devises - 07/11
ugly_devises = {'USDBRL': {'code': 'USD', 'codein': 'BRL', 'name': 'Dólar Americano/Real Brasileiro',
                           'high': '5.8618', 'low': '5.634', 'varBid': '0.0049', 'pctChange': '0.09',
                           'bid': '5.6832', 'ask': '5.6852', 'timestamp': '1730995850', 'create_date':
                               '2024-11-07 13:10:50'},

                'EURBRL': {'code': 'EUR', 'codein': 'BRL', 'name': 'Euro/Real Brasileiro',
                           'high': '6.1501', 'low': '6.079', 'varBid': '0.0432', 'pctChange': '0.71',
                           'bid': '6.1331', 'ask': '6.1411', 'timestamp': '1730995841', 'create_date':
                               '2024-11-07 13:10:41'},

                'BTCBRL': {'code': 'BTC', 'codein': 'BRL', 'name': 'Bitcoin/Real Brasileiro',
                           'high': '433977', 'low': '421715', 'varBid': '5031', 'pctChange': '1.18',
                           'bid': '431223', 'ask': '431426', 'timestamp': '1730995856', 'create_date':
                               '2024-11-07 13:10:56'}}

#print(ugly_devises)