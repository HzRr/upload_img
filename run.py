from pywebio import start_server
from pages.upload_img import upload_img

if __name__ == '__main__':
    start_server(
        applications=[upload_img],
        port=39003,
        host="0.0.0.0",
        debug=True
        )
