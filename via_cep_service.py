import requests
import configparser


class ViaCEPService:
    def __init__(self, config_file="config.ini"):
        self.base_url = self.load_base_url(config_file)

    def load_base_url(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config["viacep"]["BASE_URL"]

    def get_address_info(self, cep):
        try:
            response = requests.get(f"{self.base_url}/{cep}/json/")

            if response.status_code != 200:
                return
            
            data = response.json()
            return data

        except requests.exceptions.RequestException as req_err:
            return {"error": f"API CEP - Request error: {req_err}"}

        except Exception as err:
            return {"error": f"API CEP - An error occurred: {err}"}
