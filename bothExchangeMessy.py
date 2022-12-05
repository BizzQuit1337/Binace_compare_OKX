#########################Imports###############################
from binance.client import AsyncClient, Client
from dotenv import load_dotenv
from pyokx import OKXClient, Publicdata
import asyncio
import pandas as pd
import re

#################
#CLEAN ME BASTARD
#theme : Dark
#DO IT 
#########################Functions############################

##Functino to save to excel 
def saveExcel(dict, fileName, sheetName):
    try:
        df = pd.DataFrame.from_dict(dict)
        df.to_excel(fileName, sheet_name=sheetName)
    except:
        df = pd.DataFrame.from_dict(dict, orient='index')
        df.to_excel(fileName, sheet_name=sheetName)

##Function to compare two exchanges info
def compare(dict_okx, dict_binance):
    list_binance = []
    list_okx = []
    match_list = []
    compare = []
    binance_counter = 0
    for i in range(0, len(dict_okx)):
        okx_clean = dict_okx['instId'][i].replace('-','')
        list_okx.append(okx_clean)
    for i in range(0, len(dict_binance)):
        binance_clean = dict_binance[i]['symbol'].replace('_','')
        list_binance.append(binance_clean)   
    
    for i in list_binance: 
        okx_counter = 0
        for j in list_okx:
            okx_counter += 1
            if i == j:
                match_list.append([binance_counter, okx_counter])
        binance_counter += 1
    
    for i in match_list:
        data = {
            'symbol':dict_binance[i[0]]['symbol'],
            'binance_tick_size':dict_binance[i[0]]['tickSize'],
            'okx_tick_size':dict_okx['tickSz'][i[1]],
            'difference':float(dict_binance[i[0]]['tickSize'])-float(dict_okx['tickSz'][i[1]])
        }
        compare.append(data)
    
    return compare
#########################Creating Clients######################

#read information from env, this is for okx
load_dotenv()

##Keys for binance exchange
api_key_binance = "hZpG8LnDticj1hA3uplW6hxOvrqPatoSjaGTiXgolUmejwArROlFN1X3lPZzE0q6"
api_secret_binace = "3prGUaWoL6UF9hVJ3YGhSebJZZ335lxO6Ll0Rfi1ZXws8gyn4fycf830Elpzg6ax"

##Keys for okx exchange
api_key_okx = 'e35f24ed-741a-4771-86ef-2ec7353bac12'
api_secret_okx = '8625839F2F22AC2A171DB1F0169B6BBB'
api_passphrase_okx = 'nya2jra9ryv5JMG*pyk'

##Creating the okx client 
okx_client = OKXClient(
    key = api_key_okx,
    secret = api_secret_okx,
    passphrase = api_passphrase_okx
)

##Creating the binance client
binace_client = Client(api_key_binance, api_secret_binace, testnet=True)

#########################Collecting Metadata######################

##Collecting binance data
binance_data_raw = binace_client.futures_coin_exchange_info()

##Collecting okx data
instruments_okx = Publicdata(okx_client)
okx_data_raw = instruments_okx.get_instruments('FUTURES')

#########################Cleaning data######################

##Cleaning binance data
binance_data_dict = binance_data_raw['symbols']
binance_data_clean = []
for i in range(0,len(binance_data_dict)):
    binance_data_cleaning = binance_data_dict[i]['filters'][0]
    binance_data_clean.append(binance_data_cleaning)

##Combining filter zero with symbol
#Need a for loop to loop through both lists and pull dicts from each 

tickSymbol = []
for i in range(0, len(binance_data_raw['symbols'])):
    #For function would have smaller dictionary get required entry appended
    symbolTicksize = {
        'symbol': binance_data_raw['symbols'][i]['symbol'],
        'minPrice': binance_data_clean[i]['minPrice'],
        'maxPrice': binance_data_clean[i]['maxPrice'],
        'filterType': binance_data_clean[i]['filterType'],
        'tickSize': binance_data_clean[i]['tickSize']
    }
    tickSymbol.append(symbolTicksize)

##Cleaning okx data
okx_data_clean = okx_data_raw.to_df()

#########################Saving to excel######################
saveExcel(tickSymbol, 'Metadata_Binance.xlsx', 'binanceMeta') #Specific filter from the binance full data
saveExcel(binance_data_dict, 'Metadata_Binance(symbols).xlsx', 'binanceMeta') #Full data
saveExcel(okx_data_clean, 'Metadaya_OKX.xlsx', 'okxMeta') #full data

#########################Comparing data######################
saveExcel(compare(okx_data_clean.to_dict(), tickSymbol), 'test.xlsx', 'test')
#compare(okx_data_clean, binance_data_clean)
