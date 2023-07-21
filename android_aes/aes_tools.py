import os.path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64


# AES加密
def aes_cbc_encrypt(msg):
    key = "Pxga!h*e4@T8xfOm".encode('utf-8')
    iv = b"E&z!EHGLd$fli*8R"

    cipher = AES.new(key, AES.MODE_CBC, iv)

    msg = msg.encode('utf-8')
    encrypted_msg = cipher.encrypt(pad(msg, AES.block_size))

    return base64.b64encode(encrypted_msg).decode('utf-8')


def read_line_txt(txt_path):
    with open(txt_path, "r", ) as file:
        return file.readlines()


if __name__ == "__main__":
    lins = []
    # 返回当前文件的父目录
    current_path = os.path.dirname(os.path.realpath(__file__))
    name = os.path.join(current_path, "baidu.txt")
    path = os.path.join(current_path, "baidu1.txt")
    channels = read_line_txt(name)
    for channel in channels:
        list_ids = channel.split()
        print(list_ids)
        if len(list_ids) == 0:
            break
        app_name = list_ids[0] + "__" + list_ids[1]
        appid = aes_cbc_encrypt(list_ids[-4])
        api_key = aes_cbc_encrypt(list_ids[-3])
        secret_key = aes_cbc_encrypt(list_ids[-2])
        sn = aes_cbc_encrypt(list_ids[-1] + "-" + list_ids[-4])

        current_line = app_name + "     appid=" + appid + "     api_key=" + api_key + "     secret_key=" + secret_key + "       sn=" + sn + "\n"
        lins.append(current_line)
    with open(path, "w", ) as file:
        file.writelines(lins)
