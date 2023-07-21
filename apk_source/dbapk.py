import os
import shutil

# 待处理的 APK 文件夹路径
apk_folder_path = os.path.dirname(os.path.realpath(__file__))
# 签名 APK 文件
keystore_path = os.path.join(apk_folder_path, "targe.keystore")
alias = "kkmfxs"
key_password = "3QJNiSXx6WQJ1u8w"

m_new_icon_file = os.path.join(apk_folder_path, "m_app_logo.png")
h_new_icon_file = os.path.join(apk_folder_path, "h_app_logo.png")
x_new_icon_file = os.path.join(apk_folder_path, "x_app_logo.png")
xx_new_icon_file = os.path.join(apk_folder_path, "xx_app_logo.png")
xxx_new_icon_file = os.path.join(apk_folder_path, "xxx_app_logo.png")


def start(new_app_name, apk_folder):
    # 遍历 APK 文件夹下的所有 APK 文件
    for file_name in os.listdir(apk_folder):
        if file_name.endswith(".apk"):
            # 解压 APK 文件
            apk_path = os.path.join(apk_folder, file_name)
            temp_folder = os.path.join(apk_folder, "temp")
            os.system("apktool d {} -o {}".format(apk_path, temp_folder))

            # 替换应用名称
            manifest_path = os.path.join(temp_folder, "AndroidManifest.xml")
            with open(manifest_path, "r") as f:
                content = f.read()
            content = content.replace('android:label="@string/app_name', 'android:label="{} '.format(new_app_name))
            with open(manifest_path, "w") as f:
                f.write(content)

            # 替换图标文件
            m_icon_folder = os.path.join(temp_folder, "res/mipmap-mdpi")
            for sub_folder in os.listdir(m_icon_folder):
                src_file = os.path.join(m_icon_folder, sub_folder)
                if os.path.exists(src_file):
                    dest_file = os.path.join(m_icon_folder, sub_folder)
                    shutil.move(src_file, dest_file)
                    shutil.copy(m_new_icon_file, src_file)

            h_icon_folder = os.path.join(temp_folder, "res/mipmap-hdpi")
            for sub_folder in os.listdir(h_icon_folder):
                src_file = os.path.join(h_icon_folder, sub_folder)
                if os.path.exists(src_file):
                    dest_file = os.path.join(h_icon_folder, sub_folder)
                    shutil.move(src_file, dest_file)
                    shutil.copy(h_new_icon_file, src_file)

            x_icon_folder = os.path.join(temp_folder, "res/mipmap-xhdpi")
            for sub_folder in os.listdir(x_icon_folder):
                src_file = os.path.join(x_icon_folder, sub_folder)
                if os.path.exists(src_file):
                    dest_file = os.path.join(x_icon_folder, sub_folder)
                    shutil.move(src_file, dest_file)
                    shutil.copy(x_new_icon_file, src_file)

            xx_icon_folder = os.path.join(temp_folder, "res/mipmap-xxhdpi")
            for sub_folder in os.listdir(xx_icon_folder):
                src_file = os.path.join(xx_icon_folder, sub_folder)
                if os.path.exists(src_file):
                    dest_file = os.path.join(xx_icon_folder, sub_folder)
                    shutil.move(src_file, dest_file)
                    shutil.copy(xx_new_icon_file, src_file)

            xxx_icon_folder = os.path.join(temp_folder, "res/mipmap-xxxhdpi")
            for sub_folder in os.listdir(xxx_icon_folder):
                src_file = os.path.join(xxx_icon_folder, sub_folder)
                if os.path.exists(src_file):
                    dest_file = os.path.join(xxx_icon_folder, sub_folder)
                    shutil.move(src_file, dest_file)
                    shutil.copy(xxx_new_icon_file, src_file)

            # 重新打包 APK 文件
            new_apk_path = os.path.join(apk_folder, "{}_new.apk".format(file_name[:-4]))
            os.system("apktool b {} -o {}".format(temp_folder, new_apk_path))

            build_cmd = (
                f'jarsigner -verbose -keystore "{keystore_path}" -storepass {key_password} '
                f'-keypass {key_password} "{new_apk_path}" {alias}'
            )
            os.system(build_cmd)

            # 删除临时文件夹
            shutil.rmtree(temp_folder)


if __name__ == "__main__":
    start("爱读不读", apk_folder_path)
    pass
