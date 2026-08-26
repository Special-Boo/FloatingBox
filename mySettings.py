import os, pickle

class Settings:
    def __init__(self, NM_file, default_settings = {}, DIR_savefolder = "pkls/settings"):
        self.default_settings = default_settings
        self.data = {}
        self.NM_file = NM_file
        self.DIR_savefolder = DIR_savefolder
        self.PATH_FILE = self.get_path_file()
        self.load()

    def get_path_file(self):
        return self.DIR_savefolder + "/" + self.NM_file + '.pkl'

    def check_existence(self):
        if not os.path.exists(self.DIR_savefolder):
            os.makedirs(self.DIR_savefolder)
            
        if not os.path.exists(self.PATH_FILE):
            with open(self.PATH_FILE,'wb') as file:
                pickle.dump(self.default_settings,file)

    def load(self):
        self.check_existence()
        
        with open(self.PATH_FILE, 'rb') as file:
            SS = pickle.load(file)

        self.data = SS

        return SS

    def save(self):

        with open(self.PATH_FILE,'wb') as file:
            pickle.dump(self.data,file)

    def __setitem__(self,key,data):
        self.data[key] = data

    def __getitem__(self,key):
        return self.data[key]