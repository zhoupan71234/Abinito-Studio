import os


def gettxt():
    txt = open("requirements.txt", "r").readlines()
    return txt


libs = gettxt()
for lib in libs:
    lib = lib.strip('\n')
    os.system("pip install " + str(lib) + r" -i https://pypi.tuna.tsinghua.edu.cn/simple")
