import requests
from requests.auth import HTTPBasicAuth
from config import PASS, USER, BASE_URL, HW_ROUTE, MARK_Z_UP_ROUTE, MARK_UP_ROUTE, LEFTOVERS_SKU_ROUTE, WH_GUID_MARKER,\
                    WRITE_OFF_ROUTE, INVENTORY_RESULT_ROUTE
from abc import abstractmethod, ABC
import base64


class Source1C(ABC):
    def __init__(self):
        self.auth = None
        self.route = None
        self.route_2 = None
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
        response = requests.get(f"{self.base_url}hs{self.route}", auth=self.auth, verify=False)
        if response.status_code == 200:
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

        resp_mark_z_up = self.get_mark_z_up()

        if resp_mark_z_up.status_code == 200:
            resp_mark_up = self.get_mark_up()
            if resp_mark_up.status_code == 200:
                return f'Обновлены остатки: {resp_mark_up.text}'
            else:
                return f'Не удалось обновить остатки по складу {self.selected_wh["Name"]}'
        else:
            return f'Не удалось создать заказы по складу {self.selected_wh["Name"]}'

    def get_mark_z_up(self):
        return requests.get(f"{self.base_url}hs{self.route.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth, verify=False)

    def get_mark_up(self):
        return requests.get(f"{self.base_url}hs{self.route_2.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth, verify=False)


class WriteOff(Source1C):
    def __init__(self):
        super().__init__()
        self.auth = HTTPBasicAuth(USER, PASS)
        self.route = LEFTOVERS_SKU_ROUTE
        self.route_2 = WRITE_OFF_ROUTE
        self.base_url = BASE_URL
        self.res_list = None
        self.category_list = None
        self.goods_list = None
        self.goods_name_list = None
        self.photo = []

    def get_response(self):

        response = requests.get(f"{self.base_url}hs{self.route.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth, verify=False)
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
        b64_enc = base64.b64encode(downloaded_file)
        b64_msg = b64_enc.decode('utf-8')

        self.photo.append(b64_msg)

    def post_write_off(self, wh_guid, count):
        data_dict = {
            "wh_guid": wh_guid,
            "good_guid": self.selected_good['GUID'],
            "feature_guid": self.selected_good['GUID_feature'],
            "count": count,
            "photo_hash": self.photo[0]
        }

        headers = {"Content-Type": "application/JSON;  charset=utf-8"}
        response = requests.post(url=f"{self.base_url}hs{self.route_2}", json=data_dict, auth=self.auth, headers=headers, verify=False)
        return response.text


class Inventory(Source1C):
    def __init__(self):
        super().__init__()
        self.auth = HTTPBasicAuth(USER, PASS)
        self.route = LEFTOVERS_SKU_ROUTE
        self.route_2 = INVENTORY_RESULT_ROUTE
        self.base_url = BASE_URL
        self.res_list = None
        self.goods_list = []
        self.invent_goods_list = []

    def get_response(self):
        response = requests.get(f"{self.base_url}hs{self.route.replace(WH_GUID_MARKER, self.selected_wh['GUID'])}", auth=self.auth, verify=False)
        if response.status_code == 200:
            self.res_list = response.json()
        return

    def pop_next_category(self):
        return self.res_list.pop().values()

    def post_inv_result(self):
        data_dict = {
            "wh_guid": self.selected_wh['GUID'],
            "result": self.invent_goods_list,
        }

        headers = {"Content-Type": "application/JSON;  charset=utf-8"}
        response = requests.post(url=f"{self.base_url}hs{self.route_2}", json=data_dict, auth=self.auth, headers=headers, verify=False)
        return response.text
