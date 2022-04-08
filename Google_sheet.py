from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "key_REM_LOL.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

#creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID de la google_sheet
id_googlesheet = "1GSFVRdKKlngaEL9oZ9V3qHwmw3fv6LOwtbDsnmFdAgo"

service = build("sheets", "v4", credentials=creds)

# On appel la googlesheet
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=id_googlesheet, range="Test_LOL!A1:N25").execute()
values = result.get("values", [])   # On recupere les valeurs de chaque case

# On affiche toutes les valeurs
print(values)

text = [["Coucou"], [19]]

request = sheet.values().update(spreadsheetId=id_googlesheet, range="Test_LOL!B11", valueInputOption="USER_ENTERED", body={"values":text}).execute()

