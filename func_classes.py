import requests
from requests.auth import HTTPBasicAuth
from config import PASS, USER, BASE_URL, HW_ROUTE, MARK_Z_UP_ROUTE, MARK_UP_ROUTE, LEFTOVERS_SKU_ROUTE, WH_GUID_MARKER,\
                    PHOTO_PATH
from abc import abstractmethod, ABC


class Source1C(ABC):
    def __init__(self):
        self.auth = None
        self.route = None
        self.base_url = None
        self.selected_wh = None
        self.selected_good = None

    @abstractmethod
    def get_response(self):
        pass


class WareHouses(Source1C):
    def __init__(self):
        super().__init__()
        self.auth = HTTPBasicAuth(USER, PASS)
        self.route = HW_ROUTE
        self.base_url = BASE_URL
        self.wh_name_list = None
        self.wh_dict_list = None

    def get_response(self):
        response = requests.get(f"{self.base_url}hs{self.route}", auth=self.auth)
        self.wh_dict_list = response.json()
        self.wh_name_list = [i['Name'] for i in self.wh_dict_list]
        return

class UpdateBalance(Source1C):
    def __init__(self):
        super().__init__()
        self.auth = HTTPBasicAuth(USER, PASS)
        self.route = MARK_Z_UP_ROUTE
        self.route_2 = MARK_UP_ROUTE
        self.base_url = BASE_URL

    def get_response(self):

        response_1 = requests.get(f"{self.base_url}hs{self.route.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth)

        if response_1.status_code == 200:
            response_2 = requests.get(f"{self.base_url}hs{self.route_2.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth)
            if response_2.status_code == 200:
                return f'Обновлены остатки: {response_2.text}'
            else:
                return f'Не удалось обновить остатки по складу {self.selected_wh["Name"]}'
        else:
            return f'Не удалось создать заказы по складу {self.selected_wh["Name"]}'


class WriteOff(Source1C):
    def __init__(self):
        super().__init__()
        self.auth = HTTPBasicAuth(USER, PASS)
        self.route = LEFTOVERS_SKU_ROUTE
        self.base_url = BASE_URL
        self.res_list = None
        self.category_list = None
        self.goods_list = None
        self.goods_name_list = None
        self.photo = []

    def get_response(self):

        response = requests.get(f"{self.base_url}hs{self.route.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth)
        if response.status_code == 200:
            self.res_list = response.json()
        return

    def set_category_list(self):
        self.category_list = [i['CategoryName'] for i in self.res_list]
        return

    def set_goods_lists(self, category_name):
        for category_dict in self.res_list:
            if category_dict['CategoryName'] == category_name:
                self.goods_list = category_dict['Array']
                self.goods_name_list = [i['Name'] for i in self.goods_list]
                break
        return

    def set_selected_good(self, good_name):
        for i in self.goods_list:
            if i['Name'] == good_name:
                self.selected_good = i
                break
        return

    def save_photo(self, name, downloaded_file):
        full_name = f'{PHOTO_PATH}{name}'
        with open(full_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        self.photo.append(full_name)


