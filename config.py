import os


try:
    # docker build -t choco_holodos --build-arg token=token_string ./
    TOKEN = os.environ['TOKEN']
except KeyError:
    print('Не установлено значение переменной окружения TOKEN')
      
# with open('TOKEN', 'r') as t_file:
# with open('Ch_HolodosBot/TOKEN', 'r') as t_file:
    # TOKEN = t_file.read()


try:
    # docker build -t choco_holodos --build-arg pass_1c=hE4qo5jo ./
    PASS_1C = os.environ['PASS_1C']
except KeyError:
    print('Не установлено значение переменной окружения PASS_1C')
      

# USER = 'test'
USER = 'bot_Holodos'
# PASS = 'hE4qo5jo'
PASS = PASS_1C

# BASE_URL = 'http://192.168.194.143/trade/'
BASE_URL = 'https://192.168.100.5:8443/trade/'

HW_ROUTE = '/micromarket/get_wh/'
WH_GUID_MARKER = '@WH_GUID@'
MARK_Z_UP_ROUTE = f'/micromarket/mark_z_up/{WH_GUID_MARKER}'
MARK_UP_ROUTE = f'/micromarket/mark_up/{WH_GUID_MARKER}'
LEFTOVERS_SKU_ROUTE = f'/micromarket/leftovers_sku/{WH_GUID_MARKER}'
WRITE_OFF_ROUTE = '/micromarket/write_off/'
INVENTORY_RESULT_ROUTE = '/micromarket/inventory/'
