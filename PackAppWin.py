import os, shutil, plistlib, time, sys

line = "--------------------------------------------------"
loc = ""

def quit():
    print("Goodbye! Have a good day!")
    os.system("pause")
    sys.exit()

def noline(string):
    print(string,end="")

def title(string):
    print(line)
    print("{:^50}".format(string))
    print(line)

def isfile(string):
    return os.path.isfile(string)

def clear():
    os.system("cls")

def copyfiles(sharedsupportloc):
    for f in neededfiles:
        noline("    Copying {}... ".format(f))

        shutil.copy(f, sharedsupportloc)
        print("Done.")

def checkfiles():
    clear()
    title("Checking Required Files...")
    loc = input("Please drag and drop the downloaded folder: ")
    print (loc)
    os.system("cd {}".format(loc))
    time.sleep(0.5)
    for f in neededfiles:
        if isfile(f) == False:
            print("Missing Files.")
            os.system("pause")
            sys.exit()
    time.sleep(1)

neededfiles = [r"./AppleDiagnostics.chunklist", r"./AppleDiagnostics.dmg", r"./BaseSystem.chunklist", r"./BaseSystem.dmg", r"./InstallESDDmg.pkg", r"./InstallInfo.plist"]

def editplist():
    fp = open(r"./InstallInfo.plist","rb")
    installinfo = plistlib.load(fp)
    del installinfo["Payload Image Info"]["chunklistURL"]
    del installinfo["Payload Image Info"]["chunklistid"]
    installinfo["Payload Image Info"]["URL"] = "InstallESD.dmg"
    installinfo["Payload Image Info"]["id"] = "com.apple.dmg.InstallESD"
    plistlib.dump(installinfo, open(r"./InstallInfo.plist", "wb"))

def BaseSystem():
    clear()

    title("Choose macOS Version")
    print("1: High Sierra")
    print("2: Mojave")
    print("Q: Quit")
    print("M: Main Menu")
    option = input("Please enter an option: ")
    version = ""
    diskname = ""
    if option == "1":
        version = "High Sierra"
        diskname = "OS X Base System"
    elif option == "2":
        version = "Mojave"
        diskname = "macOS Base System"
    elif option == "Q":
        quit()
    elif option == "M":
        mainmenu()
    else:
        SharedSupport()

    clear()

    title("Packing files to SharedSupport")

    noline("Making Directories... ")

    os.mkdir("SharedSupport")
    print("Done.")

    print("Copying files... ")

    copyfiles(r"./SharedSupport")
    print("Done.")

    noline("Editting InstallInfo.plist... ")

    os.chdir(r"./SharedSupport")
    editplist()
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done.")

    print("Extracting files from BaseSystem.dmg...")

    os.chdir(r"../")
    l7z = input("Please Drag and Drop the 7z.exe from your Program Files: ")
    os.system("{} x ../BaseSystem.dmg".format(l7z))
    print("Done.")

    noline("Moving files in place... ")
    shutil.move(r"./SharedSupport", r"./{}/Install macOS {}.app/Contents".format(diskname, version))
    print("Done.")

    noline("Deleting files... ")
    os.chdir(r"./{}".format(diskname))
    shutil.rmtree(r"./.vol")
    shutil.rmtree(r"./.HFS+ Private Directory Data_")
    shutil.rmtree(r"./[HFS+ Private Data]")
    print("Done.")

    print("All Done.")
    time.sleep(1)

    mainmenu()

def SharedSupport():
    clear()

    title("Packing files to SharedSupport")

    noline("Making Directories... ")
    os.mkdir("SharedSupport")
    print("Done.")

    print("Copying files... ")
    copyfiles(r"./SharedSupport")
    print("Done.")

    noline("Editting InstallInfor.plist... ")
    os.chdir(r"./SharedSupport")
    editplist()
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done")

    print("All Done.")
    time.sleep(1)

    mainmenu()

def mainmenu():
    clear()
    title("Main Menu")
    print("B: Pack files for creating a Full Installer")
    print("P: Pack files for convert the current Network Recovery Installer to a Full Installer (SharedSupport)")
    print("Q: Quit")
    option = input("Enter an option: ")
    if option == "Q" or option == "q":
        quit()
    elif option == "B" or option == "b":
        os.chdir(loc)
        BaseSystem()
    elif option == "P" or option == "p":
        os.chdir(loc)
        SharedSupport()
    else:
        mainmenu()

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    checkfiles()
    mainmenu()

if __name__ == "__main__":
    main()

os.system("pause")
