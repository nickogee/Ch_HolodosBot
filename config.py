

with open('TOKEN', 'r') as t_file:
    TOKEN = t_file.read()



USER = 'test'
PASS = 'hE4qo5jo'

BASE_URL = 'http://192.168.194.143/trade/'
HW_ROUTE = '/micromarket/get_wh/'

WH_GUID_MARKER = '@WH_GUID@'
MARK_Z_UP_ROUTE = f'/micromarket/mark_z_up/{WH_GUID_MARKER}'
MARK_UP_ROUTE = f'/micromarket/mark_up/{WH_GUID_MARKER}'
LEFTOVERS_SKU_ROUTE = f'/micromarket/leftovers_sku/{WH_GUID_MARKER}'
WRITE_OFF_ROUTE = '/micromarket/write_off/'
