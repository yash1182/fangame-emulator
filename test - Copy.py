import time
import requests
import json
import websocket
import threading
import os
import jwt
from dhooks import Embed, Webhook
from urllib.parse import quote
questions = {}
embedColor = 0xFF6347
import datetime
embedUrl = "https://play-lh.googleusercontent.com/qTO_bSnkqmPFZ8k-vTFahIFDPl_iTyos_CMHVCRLq3RD78c30rQKT7S9yEdepLrRBw"
webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

users = {
    "yash":[ "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA4MGM3Y2YzNTNjY2U0NGI3ODdhOCIsIm1vYmlsZSI6Ijk2Njk3MDkxNzkiLCJmaXJzdE5hbWUiOiI5NioqKio5MTc5IiwiaWF0IjoxNjA5NjA4ODQ5fQ.Gv9VE8WXlMjoZz0Mt-C-tMchegxALx4Gv1WQ5Cg5mnk",
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTg1ZjA2YTFmNTJkMDY3YTc1NSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwiaWF0IjoxNjA5NTk2ODU0fQ.gMr3kFsRwiRD_Mx88BYKT1YauUwhQkYUP4Q9Vc-651M",
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA5Y2FiY2YzNTNjY2U0NGI3OGVkMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiJBc2hvayBHdXB0YSIsImlhdCI6MTYwOTYxNDc3OX0.NV2IFAfr3HmeIcLYoABT7siRC8_z1-SlVACOhIiEdww"
                    ],
            "abhi": [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTVhNDU3MzQ4N2ExNzZlMmI3ZGI5ZSIsIm1vYmlsZSI6Ijk3NzM4MzM5NzIiLCJmaXJzdE5hbWUiOiJQcmluY2UiLCJpYXQiOjE2MDk4NTI4OTB9.k0hXVINO3TfCH3gXbGLF4Eei_kPgFfoTLsT_bE-IMAk", #abhi-1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTI1ZjA2YTFmNTJkMDY3YTcxZSIsIm1vYmlsZSI6IjgwNzcyMTMyMDUiLCJmaXJzdE5hbWUiOiJBYmhpIiwiaWF0IjoxNjA5ODUzMTM0fQ.pRTnxvqEjvhVElbY3HPdoFS3A1OrPUUwnTooOe8biYA"
            ],
            "iza":[
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWFkNWFiZjA2YTFmNTJkMDY3Y2RlZCIsIm1vYmlsZSI6Ijk3MTE5ODY0ODciLCJmaXJzdE5hbWUiOiI5NyoqKio2NDg3IiwiaWF0IjoxNjA5Njc1MTQ1fQ.EczFpPU_nm-nIUXgbGmp_wn8Nnq5OJdem8TYtwYCD1o", #iza 1 
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjQ3Yzk1MWRkYWZmMDUwMDk0NmRlMCIsIm1vYmlsZSI6IjgzODM4MTQ3NjUiLCJmaXJzdE5hbWUiOiI4MyoqKio0NzY1IiwiaWF0IjoxNjA5ODU5NjIxfQ.pVvtwbD2kDNg48hwvnReThBrO8Zzz2SOWscEaZeR_7I", #iza 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg4ZmRiZjA2YTFmNTJkMDY3OWU2ZSIsIm1vYmlsZSI6IjcwMTE5MTgxOTYiLCJmaXJzdE5hbWUiOiI3MCoqKio4MTk2IiwiaWF0IjoxNjA5ODU5Njg0fQ.sR4IpeOWc9yIwZ1X7XZb-yIOmHK2iBqRMJ8M-e7pMw4", #iza 3
            ],
            "akash": [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjFlMmIyY2YzNTNjY2U0NGI3OWRkYyIsIm1vYmlsZSI6Ijk3NTM3OTIzNDkiLCJmaXJzdE5hbWUiOiI5NyoqKioyMzQ5IiwiaWF0IjoxNjA5ODM2MTk0fQ.MopqRg1hd5jEnsbuOSaP_aEkwQzN5i4Rp_59R2ZeJRQ", #akash 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5MGE0ZjA2YTFmNTJkMDY3OWVhZCIsIm1vYmlsZSI6IjcwMjQ4ODU3OTIiLCJmaXJzdE5hbWUiOiJDYXNhbm92YSIsImlhdCI6MTYwOTg1OTI0NH0._vKI7rDHJCNIfmz9WVQ6g6jk7Sbg4wjLHXYBE7lme60", #akash 2
            ],
            "shivang": [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5MGUzZjA2YTFmNTJkMDY3OWVjNSIsIm1vYmlsZSI6Ijc2OTM4MzAyODQiLCJmaXJzdE5hbWUiOiJqZXNzZSBwaW5rbWFuIiwiaWF0IjoxNjA5ODM2NzQwfQ.MDQg9osTGjNPTlqLK493AMNcV5BZz8vsTuOLkjTOqrE", #hopeless 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjFjZDU2Y2YzNTNjY2U0NGI3OWJhYyIsIm1vYmlsZSI6IjgxMDkxOTc3OTUiLCJmaXJzdE5hbWUiOiJzaGl2YW5nc2luZ2hjaGF1aGFuIiwiaWF0IjoxNjA5ODU0NjAwfQ.Fzrf1BSUivRL6h2M8e6KXkcYx3OGyTT-RcOuWlIMtlA", #hopeless 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjQ1MzA5ZWYwZWMwZWRkMWYyNzZlYSIsIm1vYmlsZSI6Ijk1ODQ4NzM1NTIiLCJmaXJzdE5hbWUiOiI5NSoqKiozNTUyIiwiaWF0IjoxNjA5ODU5MDY1fQ.dW-zFCFMRtGU0D8L7BMwAcK0tJL8EuC0m8rhfmagMsQ" #hopeless 3
            ],
            "silence": [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTU5YjlhMzQ4N2ExNzZlMmI3ZDk5NyIsIm1vYmlsZSI6Ijk5NjIwNTY3NTQiLCJmaXJzdE5hbWUiOiI5OSoqKio2NzU0IiwiaWF0IjoxNjA5ODU4MTUzfQ._z_a0NJTyj7XSrCR05uVrFZBylUFFA4-XcJT_BUdoug", #silence 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWI2ZjQ0ZWY4MGNkN2RhOGQ3N2EzNCIsIm1vYmlsZSI6Ijk5NjI5OTc1MzQiLCJmaXJzdE5hbWUiOiI5OSoqKio3NTM0IiwiaWF0IjoxNjA5ODU4MjI4fQ.af31zu8fNKS3rXdnltcL_LP7Bv2srLaSS-I9hWk4poM", #silence 2
            ]
    }

class FanGameUser:
    def __init__(self,authToken=None):
        self.authToken = authToken
        if self.authToken:
            userInfo = jwt.decode(self.authToken, options={"verify_signature": False},algorithms=["HS256"])
            self.number = userInfo['mobile']
            self.firstName = userInfo['firstName']
            self.userId = userInfo['id']
            self.prize = 0
    def __str__(self):
        js = {"number":self.number,"name":self.firstName,"userId":self.userId}
        return json.dumps(js)
    def setPrize(self,amount:int=0):
        self.prize = amount
        

class PrizeCalculator:
    def __init__(self,winnerDetails:list=[],date:datetime=datetime.datetime.now().date()):
        self.date = date
        self.winnerDetails = winnerDetails
        self.users = {}
        for user in users.items():
            self.users[user[0]] = [FanGameUser(authToken) for authToken in user[1]]
    def calculate(self):
        for user,accounts in self.users.items():
            for account in accounts:
                for winner in self.winnerDetails:
                    if winner['userId'] == account.userId:
                        account.setPrize(winner['totalAmount'])
                        break
    def display(self):
        print(f"Prize Distribution for {self.date}")
        for user,accounts in self.users.items():
            totalAmount = 0
            for account in accounts:
                totalAmount+=account.prize
            print(f"{user}: {totalAmount}")

if __name__ == "__main__":
    cd = os.path.dirname(os.path.realpath(__file__))
    with open(cd+r"\jan 2.json","r+",encoding="utf8") as f:
        winnerDetails = json.load(f)
    calculator = PrizeCalculator(winnerDetails)
    calculator.calculate()
    calculator.display()
    