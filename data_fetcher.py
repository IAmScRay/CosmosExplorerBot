from json import loads
import requests

from validator import Validator

API_URL = "http://IP:PORT"


class DataFetcher:

    def __init__(self):
        """DataFetcher gets the data from API server about **validator set**,
        **data** from validators & a **chain ID**.\n

        * ``update()`` method may be used to update the data periodically
        """
        self.chain_id = ""
        self.latest_block = ""
        self.val_set = {}
        self.max_active_set = 0

        self.update()

    def update(self):
        self._get_chain_id()
        self._get_latest_block()
        self._get_set()
        self._get_max_active_set()

    def _get_chain_id(self):
        """
            *Internal function*: **DO NOT USE THIS IN PRODUCTION ENVIRONMENT**!
        """
        url = API_URL + "/cosmos/base/tendermint/v1beta1/node_info"

        request = requests.get(url)
        response = loads(request.content)

        self.chain_id = response["default_node_info"]["network"]

    def _get_latest_block(self):
        """
            *Internal function*: **DO NOT USE THIS IN PRODUCTION ENVIRONMENT**!
        """

        url = API_URL + "/cosmos/base/tendermint/v1beta1/validatorsets/latest"

        request = requests.get(url)
        response = loads(request.content)

        self.latest_block = response["block_height"]

    def _get_set(self):
        """
            *Internal function*: **DO NOT USE THIS IN PRODUCTION ENVIRONMENT**!
        """

        url = API_URL + "/cosmos/staking/v1beta1/validators"

        request = requests.get(url)
        response = loads(request.content)

        for val_data in response["validators"]:
            validator = Validator(val_data)
            self.val_set[validator.get_moniker()] = validator

    def _get_max_active_set(self):
        """
            *Internal function*: **DO NOT USE THIS IN PRODUCTION ENVIRONMENT**!
        """

        url = API_URL + "/cosmos/staking/v1beta1/params"

        request = requests.get(url)
        response = loads(request.content)

        self.max_active_set = response["params"]["max_validators"]

    @staticmethod
    def _is_bonded(val):
        return val[1].status == "BOND_STATUS_BONDED"

    @staticmethod
    def _is_inactive(val):
        return val[1].status == "BOND_STATUS_UNBONDING" or val[1].status == "BOND_STATUS_UNBONDED"

    @staticmethod
    def _is_jailed(val):
        return val[1].jailed

    def get_chain_id(self):
        return self.chain_id

    def get_block_height(self):
        self._get_latest_block()
        return self.latest_block

    def get_max_active_set(self):
        return self.max_active_set

    def get_active_set(self):
        return list(filter(self._is_bonded, self.val_set.items()))

    def get_inactive_set(self):
        return list(filter(self._is_inactive, self.val_set.items()))

    def get_jailed_set(self):
        return list(filter(self._is_jailed, self.val_set.items()))

    def sorted_by_votes(self):
        return sorted(self.get_active_set(), key=lambda val: val[1].tokens, reverse=True)

    def get_by_moniker(self, moniker) -> Validator:
        return self.val_set[moniker]
