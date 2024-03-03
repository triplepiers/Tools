# Copyright (c) 2023 SeaBee
# 
# 功能说明：在当前工作路径下生成一个 JSON 文件，包含 Zotero 下的所有 PDF 文件名及其路径
#
# 使用说明：更改 baseDir 即可切换遍历的路径，更改 outputFileName 即可更改输出文件名称
#         运行命令 python app.py -g 即可生成 JSON 文件
#
# TODO：
# - 更科学的菜单
# - 更正常的 show() 格式（分页？）
# - 更自动的 baseDir 查找方式（？）

import os
from time import asctime
from json import load
from sys import argv

class ZoteroSeeker:

    def __init__(self, baseDir, outputFileName):
        self.baseDir = baseDir
        self.outputFileName = outputFileName
        return

    def gen(self):

        def printFile(fileName, path):
            nonlocal outputFile
            nonlocal cnt

            if cnt == 0:
                outputFile.write('\t\t{\n')
            else:
                outputFile.write(',\n\t\t{\n')

            outputFile.write(f'\t\t\t"name": "{fileName}",\n')
            outputFile.write(f'\t\t\t"path": "{os.path.join(path, fileName)}"\n')
            outputFile.write('\t\t}')

            cnt += 1

            return

        # isValid ?
        if not os.path.exists(self.baseDir):
            print(f"[ZoteroSeeker]: Error - baseDir [{self.baseDir}] doesn't exists!")
            return
        
        # init
        cnt = 0

        with open(self.outputFileName, "w") as outputFile:
            
            # print head
            outputFile.write('{\n')
            outputFile.write(f'\t"time": "{asctime()}",\n')
            outputFile.write('\t"data": [\n')

            # walk through (only PDF)
            subDirs = os.listdir(self.baseDir)
            for subDir in subDirs:
                path = os.path.join(self.baseDir, subDir)
                if os.path.isdir(path):
                    files = os.listdir(path)
                    for f in files:
                        if f.endswith(".pdf"):
                            printFile(f, path)

            # print tail       
            outputFile.write('\n\t]\n}\n')

        print(f'[ZoteroSeeker]: [{cnt}] files found. You can find the list @{self.outputFileName}.')

    def clean(self):
        if os.path.exists(self.outputFileName):
            os.remove(self.outputFileName)
        print(f'[ZoteroSeeker]: Successfully cleaned [{self.outputFileName}] !')

    def show(self):
        
        # has Gened?
        if not os.path.exists(self.outputFileName):
            print(f"[ZoteroSeeker]: Error - please run 'seeker.gen()' first!")
            return

        # open and read
        with open(self.outputFileName) as outputFile:
            all_data = load(outputFile)
            # parsing
            print(f'[ZoteroSeeker]: Updated @ {all_data["time"]}')

def printMenu():
    print("              - Supported options are as follows:\n")
    print("                '-c': Clean the outputFile\n")
    print("                '-g': Generate/Update the outputFile\n")
    print("                '-s': Show the outputFile\n")
    print("                '-h': Print the HELP menu\n")

if __name__ == "__main__":

    baseDir = "/Users/shen/Zotero/storage"
    outputFileName = "Zotero.json"

    print(f"[ZoteroSeeker]: Hello, welcome to use ZoteroSeeker!\n")

    # isFirst?
    if not os.path.exists(outputFileName):   
        print("              - Please change the value of 'baseDir'")
        print("                (which should end with 'Zotero/storage')\n")

    # check option
    if len(argv) > 1:
        option = argv[1]
        seeker = ZoteroSeeker(baseDir, outputFileName)
        if option == "-c":
            seeker.clean()
        elif option == "-g":
            seeker.gen()
        elif option == "-s":
            seeker.show()
        elif option == "-h":
            printMenu()
        else:
            print(f"[ZoteroSeeker]: Error - Illegal option '{option}'!")
    else:
        printMenu()