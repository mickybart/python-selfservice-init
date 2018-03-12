from selfservice.config import Config
from selfservice.app import App

# secret.json file example :
#
# {
#     "provisions" : { "list" : "https://<url>/%s/%s" }
# }
#
secrets = Config.load_json("secret.json")

config = Config(secrets["provisions"]["list"])

# OR
#
# Custom config ?
#
# from config import CustomConfig
# config = CustomConfig(secrets["provisions"]["list"])

App(config).run()
