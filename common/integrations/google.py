
from googleapiclient.discovery import build


def get_keep_data():
    service = build('keep', 'v1')
    service.close()

if __name__ == "__main__":
    get_keep_data()