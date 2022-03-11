import pprint # used for testing -- can be removed when complete
import yfinance as yf



def getStockPrice(msg):
    # Strip $ from front of user message
    stockString = str(msg).split("$")[1]
    

    try:
        stockObject = (yf.Ticker(stockString.upper()))
        # pprint will display formatted stockObject
        #pprint.pprint(stockObject.info)
        symbol = stockObject.info['symbol']
        currentPrice = stockObject.info['currentPrice']
        currency = stockObject.info['currency']
        closePrice = stockObject.info['previousClose']
        dollarChange = currentPrice - closePrice
        percentChange = (dollarChange / closePrice) * 100
        stockDict = {
            'symbol': symbol,
            'currentPrice': currentPrice,
            'currency': currency,
            'closePrice': closePrice,
            'dollarChange': dollarChange,
            'percentChange': percentChange,
            'shortName' : stockObject.info['shortName'],
            'logo': stockObject.info['logo_url']
        }
        # print("dollarChange " + str(round(dollarChange, 2)))
        # print("percentChange " + str(round(percentChange, 2)))
        return stockDict
    
    # Certain stocks have different key values, so we catch KeyError exception

    except KeyError:
        try:
            stockObject = (yf.Ticker(stockString.upper()))
            symbol = stockObject.info['symbol']
            currentPrice = stockObject.info['regularMarketPrice']
            currency = stockObject.info['currency']
            closePrice = stockObject.info['regularMarketPreviousClose']
            dollarChange = stockObject.info['regularMarketChange']
            percentChange = (stockObject.info['regularMarketChangePercent']) * 100

            stockDict = {
                'symbol': symbol,
                'currentPrice': currentPrice,
                'currency': currency,
                'closePrice': closePrice,
                'dollarChange': dollarChange,
                'percentChange': percentChange,
                'shortName' : stockObject.info['shortName'],
                'logo': stockObject.info['logo_url']
        }
            return stockDict
        except: 
            # If stock is still not found return error string
            return "STOCK_NOT_FOUND"
