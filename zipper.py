import sys
import zipfile
from os import chdir, getcwd, listdir, mkdir, walk
from os.path import basename, isdir, join
from shutil import make_archive


def main(args):
    loc_is_wd = False
    loc_given = True if len(args) > 0 else False

    zipping = True if input("Zip (z) or UnZip (u)? ") == "z" else False
    subfolders = False  # Default
    if not zipping:  # Check sub-folders from working directory
        subfolders = True if input("Check Sub-Folders? (y/n) ") == "y" else \
            False

    if not loc_given:
        print("Current Working Directory: " + getcwd())
        loc_is_wd = True if input("Is this the root director of interest? ("
                                  "y/n)") == "y" else False
    else:
        print("Zipper Called From: " + args[0])
        loc_given = True if input("Is this the root directory of interest? "
                                  "(y/n)") == "y" else False
        try:
            chdir(args[0])
        except FileNotFoundError:
            print("Sorry!  That directory didn't seem to work.")
            loc_given = False

    while True and not loc_is_wd and not loc_given:
        path = input("Path of root directory of interest? ")
        try:
            chdir(path)
            break  # Leaves While loop, as proper directory entered
        except FileNotFoundError:
            print("Cannot find directory '" + path + "'")
            print("Please try again")
            continue

    print("WD: " + getcwd())
    correct_dir = True if input("Correct WD? (y/n) ") == "y" else False

    if correct_dir:
        all_files = []
        if subfolders:
            file_walk = walk(getcwd())
            for root, dirs, files in file_walk:
                for file in files:
                    all_files.append(join(root, file))
        else:
            all_files = listdir(getcwd())
        dirs = []
        zips = []
        for item in all_files:
            if isdir(item):
                dirs.append(item)
            else:  # Check if it is a zip
                if basename(item).split(".")[1] == "zip":
                    zips.append(item)

        print("Directories to " + ("Zip" if zipping else "UnZip"))
        if zipping:
            for item in dirs:
                print(item)
        else:
            for item in zips:
                print(item)
    else:
        main()
        pass

    proceed = True if input("Correct? (y/n) ") == "y" else False
    if proceed:
        if zipping:
            do_zip(dirs)
        else:
            do_unzip(zips, path)
    else:
        main()
    pass


def do_zip(dirs):
    for d in dirs:
        make_archive(basename(d), "zip", d)
    print("Done")
    pass


def do_unzip(dirs, path):
    for d in dirs:
        zip_file = zipfile.ZipFile(d)
        split_path = d.split("\\")
        st_name = split_path[split_path.__len__() - 3]
        out_path = path + "/" + st_name
        mkdir(out_path)
        zip_file.extractall(out_path)
    pass


main(sys.argv[1:])
