import requests,json,datetime,configparser
Get_Current_Date = str(datetime.datetime.now()).split(' ')[0]
config = configparser.ConfigParser()
config.read('config.ini')
Authorization = config.get('API_SECURITY', 'Autorization')
Refresh_Token = config.get('API_SECURITY', 'Refresh_Token')

def Get_Booking_Records():
    # Get Today All Booking
    Endpoint = "https://voyageur.checkfront.com/api/3.0/booking"
    Booking_url = f"{Endpoint}?start_date=2023-04-13"
    # url = f"{Endpoint}?start_date={Get_Current_Date}"
    headers = {'Content-Type': 'application/json','Authorization': f'Basic {Authorization}'}
    response = json.loads(requests.request("GET", Booking_url, headers=headers).text).get('booking/index').values()
    for Id in response:
      # Get Booking Guest
      Customer_Name = Id.get('customer_name')
      url = f"{Endpoint}/{Id.get('code')}/guest"
      Get_Guests = json.loads(requests.request("GET", url, headers=headers).text).get('guests')
      if len(Get_Guests)>0:
        print("yessssssssssssssssss")
        count = 1
        if len(Get_Guests)>0:
            data = Get_Guests.values()
            for fields in data:
                Checkfront_Records = fields.get('fields')
                try:
                    Guest_Name = Checkfront_Records.get('guest_first_name')+" "+ Checkfront_Records.get('guest_last_name')
                except:
                    Guest_Name = "None"
                try:
                    Guest_Email = Checkfront_Records.get('guest_email')
                except:
                    Guest_Email = "None"
                try:
                    Age = Checkfront_Records.get('age')
                except:
                    Age = "None"
                try:
                    Allergies = Checkfront_Records.get('allergies')
                except:
                    Allergies = "None"
                try:
                    Dietary_restrictions = Checkfront_Records.get('dietary_restrictions')[0]
                except:
                    Dietary_restrictions ="None"
                try:
                    Health_information_and_medical =  Checkfront_Records.get('health_information_and_medical')
                except:
                    Health_information_and_medical = "None"
                try:
                    Boot_size = Checkfront_Records.get('boot_size')
                except:
                    Boot_size = 0
                try:
                    height = Checkfront_Records.get('height')
                except:
                    height = 0
                yield {"Booking Id":Id.get('code'),"Guest Name":Guest_Name,"Guest Email":Guest_Email,"Age":Age,"Allergies":Allergies,"Dietary Restrictions":Dietary_restrictions,"Health_information_and_medical":Health_information_and_medical,"Boot size":Boot_size,"Height":height},Customer_Name
                count+=1
      else:
        print("No Guests")


def Tokens():
    Client_Id = "319825298674-c35ao8adpg083egpl1jkfseekni6fs8u.apps.googleusercontent.com"
    Cleint_Secret = "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"
    url = f"https://oauth2.googleapis.com/token?grant_type=refresh_token&client_id={Client_Id}&client_secret={Cleint_Secret}&refresh_token={Refresh_Token}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    Access_Token_Here = json.loads(requests.request("POST", url, headers=headers).text).get('access_token')
    return Access_Token_Here

def get_files(token):
    headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
    url = "https://www.googleapis.com/drive/v3/files"
    payload = json.dumps({
    "title": "My new document",
    "mimeType": "application/vnd.google-apps.document"
    })
    Get_Id = json.loads(requests.request("POST", url, headers=headers, data=payload).text).get('id')
    return Get_Id

def Rename_File_Name(Google_Doc_Id):
    headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
    url = f"https://www.googleapis.com/drive/v3/files/{Google_Doc_Id}"
    Get_Customer_Name = [i[1] for i in Get_Booking_Records()] # Booking Customer Name
    # payload = json.dumps({"name": Get_Customer_Name[0]})
    payload = json.dumps({"name": "New Eva Test Records"})
    Get_File_Name = json.loads(requests.request("PATCH", url, headers=headers, data=payload).text).get('name')
    return Get_File_Name

def Search_File_Name(Get_File_Name,Store_Booking_Records):
    headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
    Search_Url = f"""https://www.googleapis.com/drive/v3/files?key=AIzaSyBayxpIXIr72V5mp1L31SQGTege1ZLORs0&q=name%3D%27{Get_File_Name}%27"""
    response_Search = json.loads(requests.request("GET", Search_Url, headers=headers).text).get('files')
    if len(response_Search) <=1:
        print("yessssssssssssssss")
        for checkfront_rec in Store_Booking_Records:
            Get_Search_Id= response_Search[0].get('id')
            url = f"https://docs.googleapis.com/v1/documents/{Get_Search_Id}:batchUpdate"
            payload = json.dumps({
            "requests": [
                {
                "insertText": {
                    "location": {
                    "index": 1
                    },
                    "text":"\n" +checkfront_rec[0].get('Booking Id') + "\n" + checkfront_rec[0].get('Guest Name') + "\n" + checkfront_rec[0].get('Guest Email')+ "\n" + checkfront_rec[0].get('Age') + "\n"+ checkfront_rec[0].get('Allergies')+ "\n" + checkfront_rec[0].get('Dietary Restrictions')+ "\n" + checkfront_rec[0].get('Health_information_and_medical')+ "\n" + str(checkfront_rec[0].get('Boot size'))+ "\n" + str(checkfront_rec[0].get('Height')) 
                }
                }
            ]
            })
            response = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
if __name__ == '__main__':
    Store_Booking_Records = Get_Booking_Records()
    token = Tokens()
    Google_Doc_Id = get_files(token)
    Rename_File = Rename_File_Name(Google_Doc_Id)
    Get_File_Name = Search_File_Name(Rename_File,Store_Booking_Records)