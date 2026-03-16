import json
import random
import string
from pathlib import Path


class Bank:
    database='data.json'
    data=[]
    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("No such File exists")
    except Exception as err:
        print(f"an Exception occured as {err}")
    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spchar=random.choices("!@#$%^&*",k=1)
        id=alpha + num + spchar
        random.shuffle(id)
        return "".join(id)


    def Createaccount(self):
        info={
            "Name":input("Tell your Name :"),
            "Age" :int(input("Tell your Age :")),
            "Email" :input("Tell your Email :"),
            "Pin" : int(input("Tell your 4 digit Pin :")),
            "AccountNo":Bank.__accountgenerate(),
            "Balance":0
        }
        if info["Age"] < 18 or len(str(info["Pin"])) != 4:
            print("Sorry you cannot create your account")
        else:
            print("Account has been created Successfully")
            
        for i in info:
            print(f"{i}:{info[i]}")
        
        print("Please note down your account Number")
        Bank.data.append(info)
        Bank.__update()

    def Depositmoney(self):
        accnumber=input("Please Tell your account number")
        pin=int(input("Please entre your 4 digit account pin"))
        userdata=[i for i in Bank.data if i['AccountNo']==accnumber and i['Pin']==pin ]

        if userdata==False:
            print("No data Found")
        else:
            amount=int(input("How much you want to deposit"))
            if amount>10000 or amount<0:
                print("Sorry amount is too much you can deposit amount below 10000")
            else:
                #print(userdata)
                userdata[0]['Balance'] +=amount
                Bank.__update()
                print("Amount Deposited successfully")
    def Withdrawmoney(self):
        accnumber=input("Please Tell your account number")
        pin=int(input("Please entre your 4 digit account pin"))
        userdata=[i for i in Bank.data if i['AccountNo']==accnumber and i['Pin']==pin ]

        if userdata==False:
            print("No data Found")
        else:
            amount=int(input("How much you want to withdraw"))
            if userdata[0]['Balance']<amount:
                print("Sorry you do not have enough balance")
            else:
               # print(userdata)
                userdata[0]['Balance'] -=amount
                Bank.__update()
                print("Amount Withdrew successfully")
    def Showdetails(self):
        accnumber=input("Please Tell your account number")
        pin=int(input("Please entre your 4 digit account pin"))
        userdata=[i for i in Bank.data if i['AccountNo']==accnumber and i['Pin']==pin]
        print("Your Details are :\n\n")
        for i in userdata[0]:
            print(f"{i} :{userdata[0][i]}")

    def updatedetails(self):
        accnumber=input("Please Tell your account number")
        pin=int(input("Please entre your 4 digit account pin"))
        userdata=[i for i in Bank.data if i['AccountNo']==accnumber and i['Pin']==pin]

        if userdata==False:
            print("No such user found")
        else:
            print("You cannot change age,account number ,balance")
            print("Fill the  details for change or leave it empty if no change")
            newdata={
                "Name": input("Please tell new name or press enter :"),
                "Email":input("Please enter new email or press enter to skip :"),
                "Pin": input("Please enter new pin or press enter to skip :")
            }
            if newdata["Name"]=="":
                newdata["Name"]=userdata[0]["Name"]
            if newdata["Email"]=="":
                newdata["Email"]=userdata[0]["Email"]
            if newdata["Pin"]=="":
                newdata["Pin"]=userdata[0]["Pin"]

            newdata["Age"]=userdata[0]["Age"]
            newdata["AccountNo"]=userdata[0]["AccountNo"]
            newdata["Balance"]=userdata[0]["Balance"]

            if type(newdata["Pin"])==str:
                newdata["Pin"]=int(newdata["Pin"])

            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]
            Bank.__update()
            print("Details have been updated successfully")
    def delete(self):
        accnumber=input("Please Tell your account number")
        pin=int(input("Please entre your 4 digit account pin"))
        userdata=[i for i in Bank.data if i['AccountNo']==accnumber and i['Pin']==pin]

        if userdata ==False:
            print("Sorry no such data exists")
        else:
            check =input("Press y if you actaully want to delete or else press n : ")
            if check=='n' or check=='N':
                print("Bypassed")
            else:
                index=Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account Deleted successfully")
                Bank.__update()


user=Bank()
print("Press 1 for Creating an account")
print("Press2 for Depositing money in the bank")
print("Press 3 for Withdrawing the money")
print("Press 4 for Details")
print("Press 5 for Updating the details")
print("Press 6 for Deleting your account")

check=int(input("Tell your response :"))

if check==1:
    user.Createaccount()
if check==2:
    user.Depositmoney()
if check ==3:
    user.Withdrawmoney()
if check==4:
    user.Showdetails()
if check==5:
    user.updatedetails()
if check==6:
    user.delete()