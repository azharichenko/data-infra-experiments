from googleapiclient.discovery import build

def get_keep_data():
    service = build('drive', 'v3')
    service.close()

if __name__ == "__main__":
    pass