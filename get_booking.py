import requests,json
Id = "BGDZ-070423"
Endpoint = "https://voyageur.checkfront.com/api/3.0/booking/"
url = f"{Endpoint}{Id}"
headers = {
  'Authorization': 'Basic M2RhNDNlMzI0YTE0NGM2MWIwZjdhZTM2MmI4ZWNhZGU1OTQyNTliYzo3NGViZjM2ZDYwNTAyOWQ3N2FmOGNmMjdjMWIzNmI0MTIyMzg4NDEwNGM4YWNkZTI1MDY5ZTU3OTZiYTg5NGZj',
  'Content-Type': 'application/json'
}
Booking_Name = json.loads(requests.request("GET", url, headers=headers).text).get('booking')
Get_Items = Booking_Name.get('items').values()
for GetName in Get_Items:
    Store_Booing_Name = GetName.get('name')
    Booking_Id = Booking_Name.get('id')
    # print(Booking_Id,Store_Booing_Name)


    url = f"{Endpoint}{Id}/guest"
    response = json.loads(requests.request("GET", url, headers=headers).text).get('guests').values()
    data = [i.get('fields') for i in response]
    Name = [i.get('guest_first_name') +" "+ i.get('guest_last_name') for i in data]
    Email =  [i.get('guest_first_name')]
    print(Name)
