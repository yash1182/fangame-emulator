import time
import requests
import json
import websocket
import threading
from dhooks import Embed, Webhook
import datetime
import jwt
import os
import random

cd = os.path.dirname(os.path.realpath(__file__))

embedColor = 0xFF6347

mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA4MGM3Y2YzNTNjY2U0NGI3ODdhOCIsIm1vYmlsZSI6Ijk2Njk3MDkxNzkiLCJmaXJzdE5hbWUiOiI5NioqKio5MTc5IiwiaWF0IjoxNjA5NjA4ODQ5fQ.Gv9VE8WXlMjoZz0Mt-C-tMchegxALx4Gv1WQ5Cg5mnk" #mummy 

tokens =(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTg1ZjA2YTFmNTJkMDY3YTc1NSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwiaWF0IjoxNjA5NTk2ODU0fQ.gMr3kFsRwiRD_Mx88BYKT1YauUwhQkYUP4Q9Vc-651M", #9301271210
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg4ZDEyZjA2YTFmNTJkMDY3OWUwYyIsIm1vYmlsZSI6Ijk4MjYxNDEyMDciLCJmaXJzdE5hbWUiOiJhbWl0IiwiaWF0IjoxNjA5OTE5MjY0fQ.ywUzJruJncXW47qs0xmg5AiZxk95ajqH3UaybbinHz0", #main number
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA5Y2FiY2YzNTNjY2U0NGI3OGVkMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiJBc2hvayBHdXB0YSIsImlhdCI6MTYwOTYxNDc3OX0.NV2IFAfr3HmeIcLYoABT7siRC8_z1-SlVACOhIiEdww", #ashok
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTVhNDU3MzQ4N2ExNzZlMmI3ZGI5ZSIsIm1vYmlsZSI6Ijk3NzM4MzM5NzIiLCJmaXJzdE5hbWUiOiJQcmluY2UiLCJpYXQiOjE2MDk4NTI4OTB9.k0hXVINO3TfCH3gXbGLF4Eei_kPgFfoTLsT_bE-IMAk", #abhi-1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTI1ZjA2YTFmNTJkMDY3YTcxZSIsIm1vYmlsZSI6IjgwNzcyMTMyMDUiLCJmaXJzdE5hbWUiOiJBYmhpIiwiaWF0IjoxNjA5ODUzMTM0fQ.pRTnxvqEjvhVElbY3HPdoFS3A1OrPUUwnTooOe8biYA", #abhi 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWFkNWFiZjA2YTFmNTJkMDY3Y2RlZCIsIm1vYmlsZSI6Ijk3MTE5ODY0ODciLCJmaXJzdE5hbWUiOiI5NyoqKio2NDg3IiwiaWF0IjoxNjA5Njc1MTQ1fQ.EczFpPU_nm-nIUXgbGmp_wn8Nnq5OJdem8TYtwYCD1o", #iza 1 
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjQ3Yzk1MWRkYWZmMDUwMDk0NmRlMCIsIm1vYmlsZSI6IjgzODM4MTQ3NjUiLCJmaXJzdE5hbWUiOiI4MyoqKio0NzY1IiwiaWF0IjoxNjA5ODU5NjIxfQ.pVvtwbD2kDNg48hwvnReThBrO8Zzz2SOWscEaZeR_7I", #iza 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg4ZmRiZjA2YTFmNTJkMDY3OWU2ZSIsIm1vYmlsZSI6IjcwMTE5MTgxOTYiLCJmaXJzdE5hbWUiOiI3MCoqKio4MTk2IiwiaWF0IjoxNjA5ODU5Njg0fQ.sR4IpeOWc9yIwZ1X7XZb-yIOmHK2iBqRMJ8M-e7pMw4", #iza 3
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjFlMmIyY2YzNTNjY2U0NGI3OWRkYyIsIm1vYmlsZSI6Ijk3NTM3OTIzNDkiLCJmaXJzdE5hbWUiOiI5NyoqKioyMzQ5IiwiaWF0IjoxNjA5ODM2MTk0fQ.MopqRg1hd5jEnsbuOSaP_aEkwQzN5i4Rp_59R2ZeJRQ", #akash 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5MGE0ZjA2YTFmNTJkMDY3OWVhZCIsIm1vYmlsZSI6IjcwMjQ4ODU3OTIiLCJmaXJzdE5hbWUiOiJDYXNhbm92YSIsImlhdCI6MTYwOTg1OTI0NH0._vKI7rDHJCNIfmz9WVQ6g6jk7Sbg4wjLHXYBE7lme60", #akash 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5MGUzZjA2YTFmNTJkMDY3OWVjNSIsIm1vYmlsZSI6Ijc2OTM4MzAyODQiLCJmaXJzdE5hbWUiOiJqZXNzZSBwaW5rbWFuIiwiaWF0IjoxNjA5ODM2NzQwfQ.MDQg9osTGjNPTlqLK493AMNcV5BZz8vsTuOLkjTOqrE", #hopeless 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjFjZDU2Y2YzNTNjY2U0NGI3OWJhYyIsIm1vYmlsZSI6IjgxMDkxOTc3OTUiLCJmaXJzdE5hbWUiOiJzaGl2YW5nc2luZ2hjaGF1aGFuIiwiaWF0IjoxNjA5ODU0NjAwfQ.Fzrf1BSUivRL6h2M8e6KXkcYx3OGyTT-RcOuWlIMtlA", #hopeless 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjQ1MzA5ZWYwZWMwZWRkMWYyNzZlYSIsIm1vYmlsZSI6Ijk1ODQ4NzM1NTIiLCJmaXJzdE5hbWUiOiI5NSoqKiozNTUyIiwiaWF0IjoxNjA5ODU5MDY1fQ.dW-zFCFMRtGU0D8L7BMwAcK0tJL8EuC0m8rhfmagMsQ", #hopeless 3
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTU5YjlhMzQ4N2ExNzZlMmI3ZDk5NyIsIm1vYmlsZSI6Ijk5NjIwNTY3NTQiLCJmaXJzdE5hbWUiOiI5OSoqKio2NzU0IiwiaWF0IjoxNjA5ODU4MTUzfQ._z_a0NJTyj7XSrCR05uVrFZBylUFFA4-XcJT_BUdoug", #silence 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWI2ZjQ0ZWY4MGNkN2RhOGQ3N2EzNCIsIm1vYmlsZSI6Ijk5NjI5OTc1MzQiLCJmaXJzdE5hbWUiOiI5OSoqKio3NTM0IiwiaWF0IjoxNjA5ODU4MjI4fQ.af31zu8fNKS3rXdnltcL_LP7Bv2srLaSS-I9hWk4poM", #silence 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZThjZWE4ZjA2YTFmNTJkMDY3YjQ2OCIsIm1vYmlsZSI6Ijk1NTAwODkxOTYiLCJmaXJzdE5hbWUiOiI5NSoqKio5MTk2IiwiaWF0IjoxNjEwMTE2MTAyfQ.oZxwC4JDanSD6eKP1iZnXfLr7svSyFs3S9qKTTFAlgA", #bobu 1 
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWNiYjZhZWY4MGNkN2RhOGQ3ODY1NiIsIm1vYmlsZSI6IjgzMjgzMTExNDYiLCJmaXJzdE5hbWUiOiI4MyoqKioxMTQ2IiwiaWF0IjoxNjEwMTE2MTc2fQ.aTtUlfh5A6kuzcBZIZYaUngv1IyqaFeGQXtYysej4zA" #bobu 2       
        )

friendsToken = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWM4NzdhZWY4MGNkN2RhOGQ3N2ZlNCIsIm1vYmlsZSI6Ijc4OTgyOTY5MDYiLCJmaXJzdE5hbWUiOiJIZWlzZW5iZXJnIiwiaWF0IjoxNjA5ODMwNzc4fQ._bDcvHK-2DGfpwtqLE4g0V6fHWPmFy-YgQSU2JiOQ80", #sagar 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA4YjBlY2YzNTNjY2U0NGI3ODg2OSIsIm1vYmlsZSI6Ijg3NzAyOTczMjAiLCJmaXJzdE5hbWUiOiJGYW5nYW1lIiwiaWF0IjoxNjA5ODMwOTEwfQ.kuC_M3J_3p8fsEqWRpCCgnMVD14cyqe6VtOp8lJrTRo", #sagar 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTlkNTA0ZjA2YTFmNTJkMDY3YmNmZiIsIm1vYmlsZSI6Ijg4MjE4ODg4MTEiLCJmaXJzdE5hbWUiOiJhbnNodWwgc2hhcm1hIiwiaWF0IjoxNjA5NjE1MzAzfQ.IeMBeBrng6UQHqDaITeXJ5waYaek28L47yUNF-jnYL0", #yashc
        )

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
            ],
            "goodboi":[
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZThjZWE4ZjA2YTFmNTJkMDY3YjQ2OCIsIm1vYmlsZSI6Ijk1NTAwODkxOTYiLCJmaXJzdE5hbWUiOiI5NSoqKio5MTk2IiwiaWF0IjoxNjEwMTE2MTAyfQ.oZxwC4JDanSD6eKP1iZnXfLr7svSyFs3S9qKTTFAlgA",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWNiYjZhZWY4MGNkN2RhOGQ3ODY1NiIsIm1vYmlsZSI6IjgzMjgzMTExNDYiLCJmaXJzdE5hbWUiOiI4MyoqKioxMTQ2IiwiaWF0IjoxNjEwMTE2MTc2fQ.aTtUlfh5A6kuzcBZIZYaUngv1IyqaFeGQXtYysej4zA"
            ]
    }

firstRankUsers = []


webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

def publish(message):
    return
    webhook.send(message)

class MainControllerAlreadyExistsError(Exception):
    pass

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
                        prize = winner['totalAmount']
                        if not prize:
                            prize = 0
                        account.setPrize(prize)
                        break
    def display(self):
        print(f"Prize Distribution for {self.date}")
        for user,accounts in self.users.items():
            totalAmount = 0
            for account in accounts:
                totalAmount+=account.prize
            print(f"{user}: {totalAmount}")    

#===================================================================
class Emulator:
    counts = 0
    mainController = None
    def __init__(self,authToken=None,isMain=False,isFriend=False):
        if Emulator.mainController:
            if isMain:
                raise MainControllerAlreadyExistsError
        self.authToken = authToken
        self.eventId = None
        self.sessionId = None
        self.cookies = None
        self.pingInterval = 0
        self.pingTimeout = 0
        self.isMain = isMain
        self.isFriend = isFriend
        self.wrongAnswerCount = 0
        if self.isMain is True:
            Emulator.mainController = self
        if self.authToken != None:
            Emulator.counts+=1
            self.Id = Emulator.counts
            userInfo = jwt.decode(self.authToken, options={"verify_signature": False},algorithms=["HS256"])
            self.number = userInfo['mobile']
            self.firstName = userInfo['firstName']
            self.userId = userInfo['id']
        self.ws = None
        self.winPrize = 0
        self.winnerDetails = {}
        self.questions = {}

    def __str__(self):
        js = {f"emulatorId":self.Id,"number":self.number,"name":self.firstName,"userId":self.userId,"isMain":self.isMain}
        return json.dumps(js)
    def setEventId(self,eventId)->None:
        self.eventId = eventId
    def setAuthToken(self,authToken)->None:
        self.authToken = authToken
    def getEvents(self):
        url = "https://api.fangame.live/event/getEvents?page=undefined"
        headers = {"accept":"application/json, text/plain, */*"}
        response = requests.get(url).json()
        events = response['upcomingEvents']
        event = events[0]   
        eventName = event['eventName']
        print(f"Starting Emulators for {eventName}")
        eventId = event['_id']
        return eventId
    def getEventDetails(self,eventId):
        url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
        headers = {"accept":"application/json, text/plain, */*"}
        response =requests.get(url,headers=headers).json()
        return response
    def getSession(self):
        url = f"https://api.fangame.live/socket.io/?token={self.authToken}&EIO=3&transport=polling"
        response = requests.get(url)
        cookies = response.cookies
        self.cookies = dict(cookies)['io']
        response = json.loads(response.text[4:])
        self.sessionId = response['sid']
        self.pingInterval = response['pingInterval']
        self.pingTimeout = response['pingTimeout']
        url = f"{url}&sid={self.sessionId}"
        headers = {"cookie":f"io={self.cookies}"}
        response=requests.get(url,headers=headers).text
        #print(response)
        payload = '42:42["joinEvent","'+self.eventId+'"]'
        response= requests.post(url,headers=headers,data=payload).text
        #print(response)
        response= requests.get(url,headers=headers).text
        print(response)

    def getLeaks(self,eventId,countNumber=1):
        time.sleep(1)
        currentQuestionNumber = self.questions.get("questionNumber")
        response = self.getEventDetails(eventId)
        print(response)
        lastQuestionDetails = response['eventDetails']['lastQuestionDetails']
        questionNumber = lastQuestionDetails['number']
        if questionNumber==0:
            return
        if currentQuestionNumber!= questionNumber and questionNumber!=0:
            if countNumber>5:
                return
            time.sleep(1)
            self.getLeaks(eventId,countNumber+1)
            return
        question = lastQuestionDetails['question']
        options = lastQuestionDetails['options']
        correctAnswerOption = lastQuestionDetails['answer']
        embed = Embed(title=f"{question}")
        correctAnswer = options[correctAnswerOption-1]
        print(f"Correct Answer:\n{correctAnswerOption}) {correctAnswer}")
        embed.add_field(name="Correct Answer:",value=f"{correctAnswerOption}) {correctAnswer}")
        webhook.send(embed=embed)
        return correctAnswerOption , lastQuestionDetails['qid']

    def walletDetails(self):
        url = "https://api.fangame.live/user/wallet/walletDetails"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers).json()
        details = response['walletDetails']
        withdrawableBalance = details['withdrawableBalance']
        totalBalance = details['totalBalance']
        allCreditBalance = details['allCreditBalance']
        return details

    def cashout(self):
        amount = self.walletDetails()['withdrawableBalance']
        if amount ==0:
            print("You have insufficent Balance.")
            return {"message":"You have insufficent Balance."}
        url = "https://api.fangame.live/user/wallet/withdrawal"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        payload = {"withdrawalAmount":amount}
        response = requests.post(url,headers=headers,json=payload).json()
        print(response['msg'])
        return {"message":response['msg']}

    def transactionDetails(self):
        url = "https://api.fangame.live/user/transactionHistory?"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers).json()
        transactions = response['transactions']
        for transaction in transactions:
            totalAmount = transaction['totalAmount']
            type = transaction['type']
            print(f"{type}: {totalAmount}")
            print("==================")

    def prizeCalculator(self,winnerDetails:list):
        for winner in winnerDetails:
            if winner['mobile'] == self.number:
                self.winnerDetails = winner
                break
        self.winPrize = self.winnerDetails['totalAmount']
        

    def submitAnswer(self,qid,correct):
        #if self.isMain is False and self not in firstRankUsers:
        #    time.sleep(2)
        #second = random.choice((8,9))
        payload = "42"+ json.dumps(["submitAnswer",{"qid":qid,"option":int(correct),"seconds":9}],separators = (",", ":"))
        if self not in firstRankUsers:
            second = random.choice((8,9))
            '''if random.choice([True,False]) == True and self.wrongAnswerCount<2:
                options = [1,2,3,4]
                options.remove(int(correct))
                correct = random.choice([options])
                self.wrongAnswerCount+=1'''
            payload = "42"+ json.dumps(["submitAnswer",{"qid":qid,"option":int(correct),"seconds":second}],separators = (",", ":"))
        self.ws.send(payload)
        msg= f"Emulator Id {self.Id}: Submitted Answer!"
        print(msg)
        publish(msg)

    def connect(self):
        self.getSession()
        if not self.sessionId:
            print("Session missing!")
            return
        #====================================================#
        #isOpen = False
        def pingTask(ws):
            while True:
                time.sleep(5)
                ws.send("2")
        def on_open(ws):
            if self.isMain is True:
                msg = "Main Controller Connected!"
                print(msg)
                publish(msg)
            else:
                msg = f"Emulator Account Id {self.Id} Connected!"
                print(msg)
                publish(msg)
            ws.send("2probe")
            ws.send("5")
            t2=threading.Thread(target=pingTask,args=(ws,))
            t2.start()
        def on_error(ws,error):
            msg = f"Emulator Id {self.Id} error: {str(error)}"
            print(msg)
            publish(msg)
        def on_close(ws):
            msg = f"Emulator Id {self.Id}: Connection Closed!"
            print(msg)
            publish(msg)
        def on_message(ws,message):
            if message=="3":
                return
            print(message)
            message = message[2:]
            message = json.loads(message)
            if message[0] == "agoraChannelToken":
                return
            if message[0] == "newQuestion":
                data = message[1]
                qid = data["qid"]
                questionNumber = data['number']
                question = data['question']
                embed = Embed(title=f"{question}",color=embedColor)
                webhook.send(embed=embed)
                self.questions['question'] = question
                self.questions['questionNumber'] = questionNumber
            if message[0]=="options":
                options = message[1]
                self.questions['options'] = options
                question = self.questions['question']
                embed = Embed(title=f"{question}",color=embedColor)
                optionNumber = 1
                for option in options:
                    embed.add_field(name=f"Option {optionNumber}:",value=f"{option}",inline=False)
                    optionNumber+=1
                webhook.send(embed=embed)
                correct,qid = self.getLeaks(self.eventId)
                try:
                    self.submitAnswer(qid,correct)
                    for emu in emus:
                        threading.Thread(target = emu.submitAnswer, args = [qid, correct]).start()
                except Exception as e:
                    print(e)
                    webhook.send(str(e))
            if message[0] == "totalScores":
                totalScores = message[1]
                with open(f"{cd}\{datetime.datetime.now().date()}.json","w+") as f:
                    json.dump(totalScores,f)
                print("successfully dumped today's winner details")
                ws.close()
                for emu in emus:
                    threading.Thread(target = emu.ws.close).start()

                return
        #====================================================#
        url = f"wss://api.fangame.live/socket.io/?token={self.authToken}&EIO=3&transport=websocket&sid={self.sessionId}"
        headers = {"cookie":f"io={self.cookies}"}
        if self.isMain is True:
            self.ws = websocket.WebSocketApp(url,header=headers,on_message = on_message,on_error = on_error,on_close = on_close)
        else:
            self.ws = websocket.WebSocketApp(url,header=headers,on_error = on_error,on_close = on_close)
        self.ws.on_open = on_open
        self.ws.run_forever(ping_interval=self.pingInterval,ping_timeout=self.pingTimeout)

emus = [Emulator(token) for token in tokens]


def start(eventId=None):
    if not eventId:
        eventId = Emulator().getEvents()
    for emu in emus:
        emu.setEventId(eventId)
    threads = [threading.Thread(target=emu.connect) for emu in emus]
    for thread in threads:
        thread.start()

def getFirstRank():
    global firstRankUsers
    while len(firstRankUsers)!=3:
        firstRankUsers.append(random.choice(emus))

if __name__ == "__main__":
    #'''
    random.shuffle(emus)
    eventId = Emulator().getEvents()
    mainController = Emulator(mainControllerToken,isMain=True)
    mainController.setEventId(eventId)
    #mainController.cashout()
    mainThread = threading.Thread(target=mainController.connect)
    mainThread.start()
    print(mainController)
    getFirstRank()
    for emu in emus:
        print(emu)
        #emu.cashout()
    start(eventId)
    '''
    cd = os.path.dirname(os.path.realpath(__file__))
    date = datetime.datetime.now().date()
    date = "2021-01-16"
    with open(cd+rf"\{date}.json","r+",encoding="utf8") as f:
        winnerDetails = json.load(f)
    calculator = PrizeCalculator(winnerDetails)
    calculator.calculate()
    calculator.display()
    #'''


    
