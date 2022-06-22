"""
This is a telegram bot that interprets messages that update orca scan. This is going to be a doozy, good luck you
creatin

This bot should interpret a message in the following format:

Shop Name
Product, qty
Product, qty
etc

The catch is that the product will be spelt wrong 99% of the time and shop name will be wrong 20% of the time.
You have to implement a spell checker for this to run smoothly.

The warehouse after i make this bot be like:
               T~~
               |
              /"\
      T~~     |'| T~~
  T~~ |    T~ WWWW|
  |  /"\   |  |  |/\T~~
 /"\ WWW  /"\ |' |WW|
WWWWW/\| /   \|'/\|/"\
|   /__\/]WWW[\/__\WWWW
|"  WWWW'|I_I|'WWWW'  |
|   |' |/  -  \|' |'  |
|'  |  |LI=H=LI|' |   |
|   |' | |[_]| |  |'  |
|   |  |_|###|_|  |   |
'---'--'-/___\-'--'---'



"""
from urllib.request import urlopen

import telebot
import difflib
import json
import requests
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context
key = '2140236127:AAGJoBZNy3q0TFf3_HA4pCbUFO-mkLUwBBs'
bot = telebot.TeleBot(key)

stores = {'Melbourne': ('https://api.orcascan.com/sheets/Txhxp42BtVloqrAQ', 'https://api.orcascan.com/sheets/HC4_95-2H4HIFJKT/json'),
          'Doncaster': ('https://api.orcascan.com/sheets/Txhxp42BtVloqrAQ', 'https://api.orcascan.com/sheets/HC4_95-2H4HIFJKT/json'),
          'North Lakes': ('https://api.orcascan.com/sheets/sKJ1rrgi2hdxKrDx', 'https://api.orcascan.com/sheets/gpQkhBOk3o8QH7XZ/json'),
          'Carindale' : ('https://api.orcascan.com/sheets/vPcKkkA90tDIx18G', 'https://api.orcascan.com/sheets/woTFl2oT8zT0VZBF/json'),
          'Chermside': ('https://api.orcascan.com/sheets/O779uuMXkV0GCaHk', 'https://api.orcascan.com/sheets/cHBPvtvmbR9vsBUU/json'),
          'Pacific Fair' : ('https://api.orcascan.com/sheets/ttGY2HoDTDvtJaVv', 'https://api.orcascan.com/sheets/wzfBl3iOq_d-LCAp/json'),
          'Robina' : ('https://api.orcascan.com/sheets/YvgHv8WxeE9d1kb6', 'https://api.orcascan.com/sheets/40T1Nr0snq9PS6La/json'),
          'Garden City' : ('https://api.orcascan.com/sheets/wTIcFPnxEJEzNvNl', 'https://api.orcascan.com/sheets/1HR5vMX1jxLXBS5h/json'),
          'Flower Precinct' : ('https://api.orcascan.com/sheets/Kqsg2034doQTSoZw', 'https://api.orcascan.com/sheets/1HR5vMX1jxLXBS5h/json'),
          'Warehouse' : ('https://api.orcascan.com/sheets/rlMKQCLWBN3LniQk', 'https://api.orcascan.com/sheets/pHOaJ1fFZgnSBJMs/json')}
shop_names = ['Melbourne', 'North Lakes', 'Carindale', 'Chermside', 'Pacific Fair', 'Robina', 'Garden City', 'Flower Precinct', 'Warehouse']
warehouse = ('https://api.orcascan.com/sheets/rlMKQCLWBN3LniQk', 'https://api.orcascan.com/sheets/pHOaJ1fFZgnSBJMs/json')
productos = [
    "ROSES 25",
    "CARNATION ST",
    "M CARN BUNCH",
    "SP CHRYS BUNCH",
    "NATIVE BUNCH",
    "SPIDER CHRYS",
    "STATTICE BUNCH",
    "LILLIES BUNCH",
    "WHITE BB",
    "VIBURNUM BUNCH",
    "SUNFLOWERS",
    "HANG GLASS",
    "WHITE PAPER",
    "HESSIAN PAPER",
    "FLORAL GLUE",
    "DELLO MANO BROWNIE",
    "SPARKLING WINE FULL",
    "RED WINE SMALL",
    "SPARKLING WINE SMALL",
    "ROSE WINE",
    "PACARI",
    "COTTON",
    "DRIED SORGHUM",
    "SPRAY ROSES",
    "PEARL BRACELET",
    "SNAPBANDS",
    "RIBBON HAMPERS & BLOSSOM WHITE",
    "RIBBON HAMPERS & BLOSSOM BLACK",
    "WAX",
    "CAFETAL COFFEE",
    "DIFFUSER SMALL",
    "TEA",
    "CANDLES",
    "LEPTOS BURGUNDY QUEEN",
    "BESOS DE PAN",
    "RICE FLOWER",
    "MINI BOTTLE BRUSH",
    "BERZELIA",
    "SPARKLING APPLE JUICE L",
    "SPARKLING APPLE JUICE M",
    "ROSITA HATBOX SMALL",
    "SQUARE ROSITA BOX",
    "DRAWER BOX",
    "SUITCASE",
    "ROSITA HATBOX BIG",
    "ROSITA PRINTING CARDS",
    "ROSITA PRINTING CARDS",
    "SUITCASE",
    "DRAWER BOX",
    "HYPERICUM",
    "RAINBOW CHRYS",
    "COLORED POM",
    "COLOR SPIDER",
    "COLOURED BB",
    "RAINBOW ROSES",
    "MURRAYA BUNCH",
    "GUM BUNCH",
    "MAGNOLIA BUNCH",
    "PROTEA 1X STEM",
    "PIN CUSHION",
    "THRYP",
    "BROWN PAPER",
    "CELLOPHANE",
    "ROSITA PAPER LARGE",
    "MASON JAR",
    "HAMPER CRATE",
    "TEDDY BEAR",
    "OASIS BOX",
    "TWINE",
    "WIRE BOX",
    "WATER TUBES",
    "BOUQUET BOX",
    "RED WINE FULL",
    "FLORAL CARDS",
    "PINS FOR BUTTONHOLE",
    "FLORAL TAPE",
    "AEROSOL MIX COLORS",
    "CARDBOARD BOXES",
    "TEA TREE",
    "COFFEE CHOC",
    "JAM",
    "DIFFUSER BIG",
    "ESPRESSO CUP",
    "CAKES",
    "CHEESE",
    "DIAMOND PIN",
    "SCISSORS",
    "BLUSING POSIES",
    "Thin Wire",
    "WOODEN CRATES",
    "GLASS CYLINDER VASE",
    "PEPPER JAM",
    "BALSAMIC",
    "ON THE SIDE. CHEESE ACCOMPANIMENTS",
    "SEA SALT RUB",
    "RIBBON FOR CORSAGES",
]
@bot.message_handler("readme")
def readme(message):
    # get the store name from the message
    try:
        products = []
        msg = (message.text)
        msg = msg.split('\n')
        store = difflib.get_close_matches(msg[1], shop_names, 1)[0]
        print(store)
        # get that store's webhook in
        url = stores[store][0]
        response_url = urlopen(stores[store][1])
        data_json_url = json.loads(response_url.read())
        response_ware = urlopen(warehouse[1])
        data_json_ware = json.loads(response_ware.read())
        for i in msg[2:]:
            i = i.split(',')
            product = difflib.get_close_matches(i[0].upper(), productos, 1, 0.4)[0]
            print(product)
            amount = int(i[1].strip())
            print(amount)
            products.append((product, amount))
    except IndexError as e:
        print(e)
        bot.reply_to(message, "Could not send to orca, pleases remember to send messages in the format: \n Shop \n Product, qty \n Product, qty \n etc")
        return
    # send orca request
    # should remove product from warehouse and send to store.
    for prod in products:
        if str(store) != "Warehouse":
            for j in data_json_ware:
                if j["Name"] == prod[0]:
                    outof = requests.post(warehouse[0], data={"___orca_action": "update", "Barcode": j["Barcode"], "Name": j["Name"],
                                                    "Description": j["Description"], "Quantity in stock": (int(j["Quantity in stock"]) - prod[1]),
                                                    "QTY per Bunch": j["QTY Per Bunch"], "Price per stem": j["Price per stem"]})
                    print(outof.text)
        for k in data_json_url:
            # print(k["Name"], product)
            if k["Name"] == prod[0]:
                into = requests.post(url, data={"___orca_action": "update", "Barcode": k["Barcode"], "Name": k["Name"],
                                                "Description": k["Description"], "Quantity in stock": (int(k["Quantity in stock"]) + prod[1]),
                                                "QTY per Bunch": k["QTY Per Bunch"], "Price per stem": k["Price per stem"]})
                print(into.text)


    bot.reply_to(message, "Updated")

bot.polling()

