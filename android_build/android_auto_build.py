import os
import shutil
import subprocess

# 打好的包的存放路径
targetFilepath = "/Users/xika/Desktop/打包文件"

# 友盟渠道号文件 老项目
__old_um_file_path = "/Users/xika/work/NovelProject/NovelProject/gradle.properties"
__old_project_root_path = "/Users/xika/work/NovelProject/NovelProject"

# 友盟渠道号文件  新项目
__new_um_file_path = "/Users/xika/Downloads/XS_Android-main/NovelComicsProject/gradle.properties"
__new_project_root_path = "/Users/xika/Downloads/XS_Android-main/NovelComicsProject"

# 表示当前打包的是新工程还是老工程，1 代表新工程，2 代表旧工程
current_state = 1

um_file_path = __new_um_file_path
project_root_path = __new_project_root_path


def read_line_txt(txt_path):
    with open(txt_path, "r", ) as file:
        return file.readlines()


def replace_lines_starting_with(file_path, old_prefix, new_prefix):
    lines = []

    # 读取文件并检查行以指定字符开头
    with open(file_path, "r", encoding="ISO-8859-1") as file:
        for line in file:
            if line.startswith(old_prefix):
                line = "UM_APP_CHANNEL=" + new_prefix + "\n"
            lines.append(line)

    # 将修改后的内容写回文件
    with open(file_path, "w", encoding="ISO-8859-1") as file:
        for line in lines:
            file.write(line)

    print(f"已将文件 {file_path} 中以 '{old_prefix}' 开头的行替换为 '{new_prefix}'。")


# 移动文件到指定文件夹
def __move_all_files_in_directory(src_directory, dst_directory):
    for filename in os.listdir(src_directory):
        src_file_path = os.path.join(src_directory, filename)
        dst_file_path = os.path.join(dst_directory, filename)

        if os.path.isfile(src_file_path):
            try:
                shutil.move(src_file_path, dst_file_path)
                print(f"文件 {src_file_path} 已成功移动到 {dst_file_path}")
            except Exception as e:
                print(f"移动文件 {src_file_path} 时出现错误：{e}")


# def delete_all_files_in_directory(directory):
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
#         if os.path.isfile(file_path):
#             try:
#                 os.remove(file_path)
#                 print(f"文件 {file_path} 已被删除。")
#             except Exception as e:
#                 print(f"删除文件 {file_path} 时出现错误：{e}")


def __build_and_sign_apk(channel, project_root):
    # 使用Gradle命令进行编译和打包
    gradle_cmd = f"gradlew assemble{channel.capitalize()}Release" if os.name == 'nt' else f"./gradlew assemble{channel.capitalize()}Release"

    # 执行Gradle命令
    try:
        process = subprocess.Popen(gradle_cmd, shell=True)
        process.wait()
    except Exception as e:
        print(f"{channel} 渠道打包过程出现错误：{e}")
        exit(1)

    # 检查APK文件是否生成
    output_dir = os.path.join(project_root, f"app/build/outputs/apk/{channel}/release")
    filelist = os.listdir(output_dir)
    if len(filelist) >= 2:
        print(f"{channel} 渠道 APK文件已生成：{filelist[0]}")
    else:
        print(f"{channel} 渠道 APK文件生成失败，请检查编译过程中的错误。")
        exit(1)
    apk_file = os.path.join(output_dir, filelist[0])
    if not os.path.exists(apk_file):
        print(f"{channel} 渠道 APK文件生成失败，请检查编译过程中的错误。")
        exit(1)

    __move_all_files_in_directory(output_dir, targetFilepath)

    # # 签名APK文件
    # signed_apk_file = os.path.join(output_dir, f"app-{channel}-release-signed.apk")
    #
    # signing_cmd = f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {key_store} -storepass {key_store_password} -keypass {key_password} {apk_file} {key_alias} -signedjar {signed_apk_file}"
    #
    # try:
    #     process = subprocess.Popen(signing_cmd, shell=True)
    #     process.wait()
    # except Exception as e:
    #     print(f"{channel} 渠道签名过程出现错误：{e}")
    #     exit(1)
    #
    # if os.path.exists(signed_apk_file):
    #     print(f"{channel} 渠道已签名的APK文件已生成：{signed_apk_file}")
    # else:
    #     print(f"{channel} 渠道签名APK文件生成失败，请检查签名过程中的错误。")
    #     exit(1)
    #
    # print(f"{channel} 渠道Android应用打包成功！")


# # 签名信息配置
# key_store = "/path/to/your/keystore.jks"
# key_alias = "your_key_alias"
# key_store_password = "your_keystore_password"
# key_password = "your_key_password"

# 追书大全
zhuishudaquan_channel = ["xiaomi_101", "baidu_tg104", "back_up101", "vivo_lr_3", "baidu_tg103", "baidu_tg102", "vivo",
                         "baidu_tg101"]

# 漫客阅读器
mkydq_channel = ["baidu_tg103", "baidu_tg102", "baidu_tg108", "baidu_tg1066", "oppo_tg106", "baidu_tg106",
                 "baidu_tg101"]

# 快搜阅读器
ksydq_channel = ["baidu_test", "topon_tg101", "mk_dl101", "back_up101", "ks_tg101", "douyin_tg101", "vivo", "oppo",
                 "baidu_tg101"]

# 小小追书
xxzs_channel = ["website", "lr_22", "vivo", "baidu_tg109", "oppo", "baidu_tg107", "baidu_tg106", "baidu_tg108",
                "baidu_tg105", "baidu_tg104", "baidu_tg103", "baidu_tg102", "baidu_lb101", "baidu_tg101"]
# 天天追书
ttzs_channel = ["oppo", "zs_dl101", "gmcs", "vivo"]

# 小小阅读
xxyuedu_channel = ["oppo", "xx_dl101", "vivo", "baidu_tg101"]

# 追书大师
zsds_channel = ["website", "vivo_lr_26", "oppo_lr_26", "lr_25", "baidu_tg1011", "dub_al00", "baidu_tg109",
                "baidu_tg102", "baidu_tg104", "baidu_tg108", "free_market101", "free_vivo101", "baidu_tg107",
                "baidu_tg106", "oppo", "vivo", "baidu_tg101"]
# 书香之家
sxhome_channel = ["qita_market", "baidu", "xiaomi", "oppo", "vivo", "baidu_tg101"]

# 笔趣阁极速版
biquge_lite_channel = ["website", "cz_tg101", "gm_tg102", "gm_tg101", "bixin_baidu", "mh66_website", "fission6_h5",
                       "fission6", "douyin_tg101", "kuaishou_tg101", "baidu_tg101", "oppo"]

new_project = {"mkydq": mkydq_channel, "ksydq": ksydq_channel, "xxzs": xxzs_channel, "ttzs": ttzs_channel,
               "xxyuedu": xxyuedu_channel, "zhuishudaquan": zhuishudaquan_channel, "zsds": zsds_channel,
               "sxhome": sxhome_channel, "biquge_lite": biquge_lite_channel
               }

# 值得阅读
zhideyuedu_channel = ["lr_388", "baidu_tg105", "baidu_tg104", "zhide_360", "baidu_tg103", "market_tg102",
                      "market_tg101", "baidu_dl101", "baidu_tg101", "website"]

# 阅读神器
yuedudashi_channel = ["vivo_lr_390", "lr_390", "vivo", "baidu_tg106", "baidu_tg104", "baidu_tg105", "baidu_tg103",
                      "market_tg101", "ydsq_sj101", "baidu_tg102", "ydsq_dl101", "baidu_tg_liebian101", "tx_yyb",
                      "baidu_tg101", "website"]

# 天天读书
ttds_channel = ["website", "baidu_tg102", "vivo", "baidu_tg104", "baidu_tg105", "baidu_tg103", "market_tg101",
                "huawei_tg101", "baidu_dl101", "baidu_tg360", "baidu_tg101", "ttds", "zhide_360"]
# 点点阅读
diandian_channel = ["baidu_tg102", "baidu_tg106", "baidu_tg105", "zhide_360", "baidu_tg103", "market_tg102",
                    "market_tg101", "huawei_tg101", "baidu_tg101", "ddyd_yyb"]
# 旧疯狂阅读
newfkyd_channel = ["baidu_tg104", "huawei", "baidu_tg103", "vivo", "baidu_tg101", "install_tg101", "baidu_tg102",
                   "baidu_lb101", "market_tg102", "sougou101", "huawei101", "fkyd_yyb"]
# 旧疯狂阅读
oldfkyd_channel = ["website", "vivo", "baidu_tg104", "baidu_tg103", "baidu_dl101", "market_tg101", "market_tg102"]

# 全民小说
qmxs_channel = ["website", "lr_389", "vivo", "baidu_tg105", "baidu_tg104", "qihu360", "baidu_tg103", "market_tg101",
                "test", "baidu_dl101", "baidu_tg101"]

# 开始阅读
ksyd_channel = ["market_tg101", "lr_390", "vivo_lr_389", "lr_389", "vivo", "zhide_360", "c_test", "baidu_tg104",
                "baidu_dl101", "baidu_tg103", "baidu_tg101", "website"]

# 肥猫阅读
fmyd_channel = ["oppo_tg101", "oppo_tg106", "baidu_tg106", "baidu_string", "baidu_int", "baidu_tg103", "oppo_tg107",
                "baidu_tg102", "baidu_tg104", "baidu_tg101"]

bqgfanshu_channel = ["oppo", "vivo", "baidu_tg101"]

old_project = {"zhideyuedu": zhideyuedu_channel, "yuedudashi": yuedudashi_channel, "ttds": ttds_channel,
               "diandian": diandian_channel, "newfkyd": newfkyd_channel, "oldfkyd": oldfkyd_channel,
               "qmxs": qmxs_channel, "ksyd": ksyd_channel, "fmyd": fmyd_channel, "bqgfanshu": bqgfanshu_channel}


# app包
# appname = "bqgfanshu"
# # 渠道列表
# channels = read_line_txt("/Users/xika/PycharmProjects/androidbuild/um.txt")
# for channel in channels:
#     replace_lines_starting_with(__new_project_root_path, "UM_APP_CHANNEL", channel)
#     __build_and_sign_apk(appname, __old_project_root_path)


def run_project():
    __build_new_project()
    __build_old_project()


# 打新工程包
def __build_new_project():
    global current_state
    current_state = 1
    __build_project(new_project)


# 打老工程包
def __build_old_project():
    global current_state
    current_state = 2
    __build_project(old_project)


def __build_project(app_dict):
    if current_state == 1:
        um_file_path = __new_um_file_path
        project_root_path = __new_project_root_path
    else:
        um_file_path = __old_um_file_path
        project_root_path = __old_project_root_path

    # 进入项目根目录
    os.chdir(project_root_path)

    for key in app_dict:
        app_name = key
        channel_list = app_dict[key]
        for channel_name in channel_list:
            replace_lines_starting_with(um_file_path, "UM_APP_CHANNEL", channel_name)
            __build_and_sign_apk(app_name, project_root_path)


run_project()
