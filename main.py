import tf
from optibook.synchronous_client import Exchange
import time

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

e = Exchange()
a = e.connect()


def get_data():
    a = e.get_last_price_book('PHILIPS_A')
    b = e.get_last_price_book('PHILIPS_B')
    a_ask = a.asks
    b_ask = b.asks
    a_bid = a.bids
    b_bid = b.bids
    return a_ask, b_ask, a_bid, b_bid
    
trades = dict()
i = -1

while True:
    a_ask, b_ask, a_bid, b_bid = get_data()

    try:
       bid, ask = tf.bid_ask(a_ask, b_ask, a_bid, b_bid)
    except:
        continue
    
    buy_a = tf.buy_side(ask, a_ask, b_ask)

    if tf.is_opportunity(ask, bid):
        volume = min(ask.volume, bid.volume)
        positions = e.get_positions()
        i += 1
        diff = bid.price - ask.price
        
        if buy_a:
            volume = tf.check_volume(volume, 'PHILIPS_A', positions)
            if volume > 0:
                e.insert_order('PHILIPS_B', price=bid.price, volume=volume, side='ask', order_type='ioc')
                e.insert_order('PHILIPS_A', price=ask.price, volume=volume, side='bid', order_type='ioc')
                trades[i] = [buy_a, volume, diff]
        
        if not buy_a:
            volume = tf.check_volume(volume, 'PHILIPS_B', positions)
            if volume > 0:
                e.insert_order('PHILIPS_B', price=ask.price, volume=volume, side='bid', order_type='ioc')
                e.insert_order('PHILIPS_A', price=bid.price, volume=volume, side='ask', order_type='ioc')
                trades[i] = [buy_a, volume, diff]
    
    d = trades.copy()
    for t in d:
        positions = e.get_positions()
        a_ask, b_ask, a_bid, b_bid = get_data()
        volume = d[t][1]
        if not d[t][0]:
            try:
                ask_price = min(a_ask, key=tf.f).price
                bid_price = max(b_ask, key=tf.f).price
                diff_now = abs(ask_price - bid_price)
            except:
                continue
            if diff_now < d[t][2]:
                volume = tf.check_volume(volume, 'PHILIPS_A', positions)
                if volume > 0:
                    e.insert_order('PHILIPS_B', price=bid_price, volume=volume, side='ask', order_type='ioc')
                    e.insert_order('PHILIPS_A', price=ask_price, volume=volume, side='bid', order_type='ioc')
                    trades[t][1] = trades[t][1] - volume
                    if trades[t][1] == 0:
                        del trades[t]
        else:
            try:
                ask_price = min(b_ask, key=tf.f).price
                bid_price = max(a_bid, key=tf.f).price
                diff_now = abs(ask_price - bid_price)
            except:
                continue
            if diff_now < d[t][2]:
                volume = tf.check_volume(volume, 'PHILIPS_B', positions)
                if volume > 0:
                    e.insert_order('PHILIPS_B', price=ask_price, volume=volume, side='bid', order_type='ioc')
                    e.insert_order('PHILIPS_A', price=bid_price, volume=volume, side='ask', order_type='ioc')
                    trades[t][1] = trades[t][1] - volume
                    if trades[t][1] == 0:
                        del trades[t]
                 
        
    
