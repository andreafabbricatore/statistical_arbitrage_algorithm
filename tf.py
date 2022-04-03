def f(x):
    return x.price


def bid_ask(a_ask, b_ask, a_bid, b_bid):
    if max(a_bid, key=f).price > max(b_bid, key=f).price:
        bid = max(a_bid, key=f)
    else:
        bid = max(b_bid, key=f)
    if min(a_ask, key=f).price < min(b_ask, key=f).price:
        ask = min(a_ask, key=f)
    else:
        ask = min(b_ask, key=f)
    return bid, ask


def buy_side(ask, a_ask, b_ask): #return true if yuo have to buy a and false if you have to buy b
    return ask.price == a_ask[0].price


def is_opportunity(ask, bid):
    return bid.price > ask.price

    

def check_volume(volume, instrument, positions):
    if instrument == 'PHILIPS_A':
        if volume + positions['PHILIPS_A'] > 250 or positions['PHILIPS_B'] - volume < -250:
            volume = min(250 - positions['PHILIPS_A'], positions['PHILIPS_B'] + 250)
        return volume
    else:
        if volume + positions['PHILIPS_B'] > 250 or positions['PHILIPS_A'] - volume < -250:
            volume = min(250 - positions['PHILIPS_B'], positions['PHILIPS_A'] + 250)
        return volume
    

    
