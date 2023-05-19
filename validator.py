from datetime import datetime
import math


class Validator:

    def __init__(self, data: dict):

        self.operator_address = data["operator_address"]
        self.jailed = data["jailed"]
        self.status = data["status"]
        self.tokens = math.floor(int(data["tokens"]) / (10 ** 18))
        self.description = data["description"]
        self.commission = str(math.floor(float(data["commission"]["commission_rates"]["rate"]) * 100))
        self.max_commission = str(math.floor(float(data["commission"]["commission_rates"]["max_rate"]) * 100))
        self.change_rate = str(math.floor(float(data["commission"]["commission_rates"]["max_change_rate"]) * 100))

        date_iso = data["commission"]["update_time"].split("T")[0]
        self.last_commission_update = str(datetime.strptime(date_iso, "%Y-%m-%d").strftime("%m.%d.%Y"))

    def get_moniker(self):
        return self.description["moniker"]

    def get_operator_address(self):
        return self.operator_address

    def get_voting_power(self):
        return self.tokens

    def get_details(self):
        return self.description["details"]

    def get_website(self):
        return self.description["website"]

    def get_commission(self):
        return self.commission

    def get_max_commission(self):
        return self.max_commission

    def get_change_rate(self):
        return self.change_rate

    def get_last_commission_update(self):
        return self.last_commission_update

    def __str__(self):
        return "Validator[moniker={},valoper={}]".format(self.get_moniker(), self.operator_address)
