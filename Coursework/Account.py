import hashlib
import json
import os

class Account:


    def __init__(self):
        # initialises starting values for file data
        self.data = {
            "username": "",
            "password": "",
            "money": 0
        }

        self.filename = ""


    def writeData(self):
        try:  # tries to create a new file
            with open(self.filename, "w") as file: # open the file and write all of the data in self.data
                json.dump(self.data, file)
            print("Data Saved")
        except:
            print("Error")


    def loadData(self):
        with open(self.filename, "r") as file: # open the file, then load all of the data as a dictionary
            data = json.load(file)
        return data["money"]


    def accessAccount(self, username, password, mode, money=0):
        self.filename = username.lower() + ".json" # path will be "username.json" to easily distinguish between users
        mode = mode.lower() # user can input save, Save, SAVE, etc. setting here means i dont have to use .lower() twice for loading as well

        self.data["username"] = username
        self.data["password"] = hashlib.sha256(password.encode()).hexdigest() #hashes password. encoded password is turned into a sha256 object, which is then deconstructed into a string by hexdigest
        self.data["money"] = money


        if os.path.exists(self.filename): # checks if theres already a file with the same path
            with open(self.filename, "r") as file: # if theres already an account, read the hashed password
                hashed_password = json.load(file)["password"]
            if self.data["password"] == hashed_password: # make sure the password matches

                if mode == "save": # if saving data, then save data
                    self.writeData() # then save new data - password protecting it will stop other users accessing data that isnt theirs
                elif mode == "load": # if loading data, load data
                    return self.loadData()
                else:
                    print("mode is invalid - check code")
            else:
                print("Incorrect Password")
        else: # if there isnt a file with that path, make a new one (no password check)
            print(f"creating new file with path - {os.path.abspath(self.filename)}")
            self.writeData() # same function as saving data but without a password check - cant pass as there is no password saved - no file yet.