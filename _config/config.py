
from .encrypter import Enc
import os
from getpass import getpass
from datetime import datetime as dt
import logging
from logging import getLogger, StreamHandler, Formatter

def get_date_str_ymd():
    return dt.now().strftime('%Y%m%d')

def get_date_str_ymdhms():    
    return dt.now().strftime('%Y/%m/%d %H:%M:%S')

class config:
    __enc = Enc()
    def __init__(self,delimita=":::",):
        self.data = {
        "loglevel"  :50,
        "encrypt"   :0,
        "workdir"   :0,
        "data_path" : f"{os.getcwd()}\\data",
        "log_path" : f"{os.getcwd()}\\log",
        }
        self.delimita = delimita
        self.setting_path = os.path.join(self.data['data_path'] , "setting.data")
        self.logger = getLogger(__name__)
        self.log_name = os.path.join(self.data['log_path'],__name__+".log")
        os.makedirs(self.data['data_path'],exist_ok=True)
        os.makedirs(self.data['log_path'],exist_ok=True)
        self.read_key()
        # set loglevel
        self.logger.setLevel(self.data['loglevel'])
        # Streamハンドラクラスをインスタンス化
        st_handler = logging.StreamHandler()
        # Fileハンドラクラスをインスタンス化
        fl_handler = logging.FileHandler(filename=self.log_name, encoding="utf-8")
        # Logフォーマットを設定
        handler_format = Formatter('[ %(levelname)s %(asctime)s] %(message)s')
        # インスタンス化したハンドラをそれぞれログ太郎に渡す
        self.logger.addHandler(st_handler)
        self.logger.addHandler(fl_handler)
        self.logger.setFormatter(handler_format)
    
    def read_key(self):
        if os.path.exists(self.setting_path)==False:
            self.write_data()
            return
        tmp_data = open(self.setting_path,"r",encoding="utf-8").read().split("\n")
        tmp_data = [td.rstrip('"').lstrip('"').split('"'+self.delimita+'"') for td in tmp_data]
        for td in tmp_data:
            if len(td)<2:
                continue
            if td[0]=="KEY":
                continue
            try:
                self.data[td[0]] = int(td[1])
            except:
                self.data[td[0]] = td[1]
    
    def set_data(self,key,value):
        self.data[key] = value
    
    def get_data(self,key):
        try:
            return self.data[key]
        except:
            self.data[key] = 0
            return self.data[key]
    
    def del_data(self,key):
        self.data.pop(key)
        self.write_data()
    
    def write_data(self):
        tmp_data = f"KEY{self.delimita}VALUE\n"
        for key in self.data.keys():
            tmp_data += f'"{key}"{self.delimita}"' + str(self.data[key]) + '"\n'
        open(self.setting_path,"w",encoding="utf-8").write(tmp_data)
    
    def set_id(self,id_line,pwd_line):
        self.data["id"] = self.__enc.encrypt(id_line)
        self.data["pwd"]  = self.__enc.encrypt(pwd_line)
        self.write_data()
    
    def get_id(self):
        if self.data["id"]:
            return  self.__enc.decrypt(self.data["id"]),self.__enc.decrypt(self.data["pwd"])
        else:
            return None,None
    
    def del_id(self):
        self.del_data("id")
        self.del_data("pwd")
    
    def write_log(self,text,type=-1,species=""):
        log_species = {
            0:"DEBUG",
            1:"INFO",
            2:"WARNING",
            3:"ERROR",
            4:"CRITICAL",
        }
        if type > -1:
            species = log_species[type]
        if species == "DEBUG":
            self.logger.debug(text)
        elif species == "INFO":
            self.logger.info(text)
        elif species == "WARNING":
            self.logger.warning(text)
        elif species == "ERROR":
            self.logger.error(text)
        elif species == "CRITICAL":
            self.logger.critical(text)
    