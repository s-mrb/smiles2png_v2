import ntpath
from os import walk, path
from pathlib import Path
import os
from cairosvg import svg2png




def dir_check(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# 2nd way
# def dir_check(path):
#     if not os.path.exists(path):
#         os.makedirs(path)


# here read_dict is used to read log files, make sure to keep all logs
# with same format so that you can reuse this function
def read_dict(path):
    dic = {}
    with open(path,'r') as f:
        key = ""
        for line in f:
            if line[0:5] == "_key_":
                key = (line.split())[1]
            else:
                temp = {key:line.split()}
                dic.update(temp)
        return dic

    # for line in file:
    #     line_offset.append(offset)
    #     offset += len(line)


def get_append_pos(path, key):
    with open(path,'r') as f:
        while True:
            # read line and move cursor to start of next line, but could be read in next while loop!!
            line = f.readline()

            if line == '':
                break
            if line[0:5] == "_key_":
                if (line.split())[1] == key:
                    # move cursor to start of **line after next line**,
                    # print()
                    f.readline()

                    # Why -1 works????
                    #
                    # The newline character is a single(typically 8 - bit) character.It's represented in program source
                    # (either in a character literal or in a string literal) by the two-character sequence \n . So '\n
                    # ' is a character constant representing a single character, the newline character

                    return f.tell() - 1
    return


def ap_dict(path, key, value, folder):
    # folder is boolean, 0 if key absent else 1
    if folder == 0:
        with open(path, 'a') as f:
            f.write("\n_key_ " + key + "\n" + value +" ")
            return
    pos = get_append_pos(path, key)

    c_last = ""

    with open (path, 'r') as f:
        f.seek(pos)
        c_last = f.read()

    # Note you can not use append below because
    # cause if first time if it is
    # _key_   gdb_11_2
    # gdb_11_2.txt
    #
    # then second time it will be
    # gdb_11_2.txt    gdb_11_3.txt    gdb_11_2.txt
    #
    # Why, because you r keeping line number to copy rest but using seek to write, so if you want to use append
    # then keep record of posiiton of index where to append
    #
    with open(path, 'a') as f:

        f.seek(pos)
        f.write(value + " " + c_last)



def file_if_not(p):
    if not os.path.exists(p):
        open(p, 'a').close()


def getF(directory, x="both"):
    # x could be "files" or "folders" or "both"

    folders = []
    for f in walk(directory):
        folders.extend(f)

    if x == "folders":
        return folders[1]
    if x == "files":
        return folders[2]
    else:
        return folders[1], folders[2]


def path_leaf(path):
    head, tail = ntpath.split(path)

    # if name ends with \\ then tail won't return anything
    # return tail or ntpath.basename(head)

    # since you dont want to return in case its not file
    return tail

def parse_r_obabel(read_path, write_path):
    # Parser for babel svg

    # NOTE below string also include \n, to add \n at end you must enter on last line
    start = """<svg version="1.1" id="topsvg"
    xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:cml="http://www.xml-cml.org/schema" x="0" y="0" width="256" height="256" viewBox="0 0 100 100">
    <title> - Open Babel Depiction</title>
    <rect x="0" y="0" width="100" height="100" fill="white"/>
    <g transform="translate(0,0)">
    """

    fil = 'fill="rgb(0,0,0)"'
    strke = 'stroke="rgb(0,0,0)"'
    strke_width = 'stroke-width="1"'

    # NOTE : anything added to above str is added on new line



    st = ""
    out = ""
    smile_done = False
    end = False
    finish = False
    space = " "
    width = 'width="100"'
    height = 'height="100"'

    test_c = 0
    dim_flag = False
    b_check = False
    s_check = False

    file = path_leaf(read_path)

    with open(read_path, 'r', encoding="utf-8") as f:
        for i in range(7):
            next(f)
        for line in f:
            if line[0:4] == "</g>" or end:

                end = True

                line_split = line.split()
                for token in line_split:
                    if token[0] == ">":
                        id = "db: " + file + " id: " + token[1:]
                        st = st + "</g>" + "\n" + "</svg>" + "\n"
                        st = id + "\n" + '"""' + "\n" + start + st + '"""' + "\n"
                        out = out + st
                        st = ""
                        smile_done = True
                        end = False

            if end:
                continue

            if smile_done:
                if not end:
                    smile_done = False
                    finish = True
                    continue
            if finish:
                finish = False
                continue

            token_list = []
            for s in line.split():
                if s[-1] == ">":
                    b_check = True

                if (2 <= len(s)):
                    if s[-2] == "/":
                        s_check = True

                if s[0:6] == "width=":
                    s = width
                if s[0:7] == "height=":
                    s = height
                if s[0:7] == "stroke=":
                    s = strke
                if s[0:13] == "stroke-width=":
                    s = strke_width
                if s[0:5] == "fill=":
                    s = fil
                if b_check:
                    b_check = False
                    if s_check:
                        s_check = False
                        if s[-2] != "/":
                            s = s + "/>"
                    elif s[-1] != ">":
                        s = s + ">"

                token_list.append(s)

            temp = ""
            for t in range(len(token_list) - 1):
                temp += token_list[t] + " "

            # sometimes list will  be empty
            if token_list:
                temp += token_list[-1] + "\n"

            token_list = []

            st = st + temp

    with open(write_path, 'w') as f:
        f.write(out)

# parse raw svg of obabel into form receivable to svg2png converter
def feed_parser(root):
    folders = getF(root, "folders")
    g = getF(root + "\\" + folders[2])

    if len(folders) == 0:
        raise Exception("Empty directory!")

    if len(folders) == 1:
        raise Exception("Two folders missing!")

    if len(folders) == 2:
        raise Exception("One folders missing!")

    r_obabel = ""
    r_png = ""
    p_obabel = ""

    flag = {"r_obabel": 0, "p_obabel": 0, "r_png": 0}

    for f in folders:
        if f == "r_obabel":
            r_obabel = root + f + "\\"
            flag["r_obabel"] = 1
        if f == "p_obabel":
            p_obabel = root + f + "\\"
            flag["p_obabel"] = 1
        if f == "r_png":
            r_png = root + f + "\\"
            flag["r_png"] = 1

    labels = list(flag.values())

    name = ""

    if not labels[0]:
        raise Exception("r_obabel folder not named properly!")
    if not labels[1]:
        raise Exception("p_obabel folder not named properly!")
    if not labels[2]:
        raise Exception("r_png folder not named properly")

    # Reading r_obabel

    # get folders
    r_obabel_folders = getF(r_obabel, "folders")

    # Read
    for fol in r_obabel_folders:

        # current folder address
        current_folder_dir = r_obabel + fol + "\\"

        # corresponding out folder for this folder
        corr_out_folder_dir = p_obabel + fol + "\\"

        # files in current folder
        files = getF(current_folder_dir, "files")

        # do parsing of each file
        for fil in files:

            # complete path of current file
            file_path = current_folder_dir + fil

            dir_check(corr_out_folder_dir)

            # corresponding out file path
            # before passing file to parser make output folder if don't exist
            out_path = corr_out_folder_dir + fil

            # read log
            # if logs folder not present then make one
            dir_check(root + "logs" + "\\" + "parser\\")
            logs_path = root + "logs" + "\\" + "parser" + "\\" + "p_logs.txt"
            file_if_not(logs_path)
            logs_dict = read_dict(logs_path)

            # call parser for this file only if it is not parsed already
            # parser
            # if folder is in logs file
            # flag for file presence
            file_present = False

            if fol in logs_dict:
                # check whether file(i) is in it or not
                for i in logs_dict[fol]:
                    # if file found then continue
                    if i == fil:
                        file_present = True
                        continue
                if not file_present:
                    parse_r_obabel(file_path, out_path)
                    # after parsing done, record in logs
                    ap_dict(logs_path, fol, fil, 1)
            else:
                # print("folder not there")
                parse_r_obabel(file_path, out_path)
                ap_dict(logs_path, fol, fil, 0)






def png_maker(current_file_path, cor_out_folder):
    input = current_file_path

    name = ""
    code = ""
    code_flag = False

    with open(current_file_path, 'r') as smiles:
        for line in smiles:
            if line[0:3] == "db:":
                tok = line.split()
                db = tok[1].split('.')[0]
                no = tok[3]
                name = db + "_" + no
                continue

            if line[0:3] == '"""':
                if code_flag:
                    code_flag = False

                    dir_check(cor_out_folder)
                    svg2png(bytestring=code,
                            write_to=cor_out_folder + name + ".png")

                    code = ""
                    name = ""
                    continue

            if line[0:3] == '"""':
                code_flag = True
                continue

            if code_flag:
                code += line




def feed_png_maker(root):
    folders = getF(root, "folders")
    g = getF(root + "\\" + folders[2])

    if len(folders) == 0:
        raise Exception("Empty directory!")

    if len(folders) == 1:
        raise Exception("Two folders missing!")

    if len(folders) == 2:
        raise Exception("One folders missing!")

    r_obabel = ""
    r_png = ""
    p_obabel = ""

    flag = {"r_obabel": 0, "p_obabel": 0, "r_png": 0}

    for f in folders:
        if f == "r_obabel":
            r_obabel = root + f + "\\"
            flag["r_obabel"] = 1
        if f == "p_obabel":
            p_obabel = root + f + "\\"
            flag["p_obabel"] = 1
        if f == "r_png":
            r_png = root + f + "\\"
            flag["r_png"] = 1

    labels = list(flag.values())

    name = ""

    if not labels[0]:
        raise Exception("r_obabel folder not named properly!")
    if not labels[1]:
        raise Exception("p_obabel folder not named properly!")
    if not labels[2]:
        raise Exception("r_png folder not named properly")

    name = ""
    code = ""
    code_flag = False

    folders = getF(p_obabel, "folders")

    for fol in folders:

        current_folder_dir = p_obabel + fol + "\\"
        files = getF(current_folder_dir, "files")

        for fil in files:

            current_file_path = current_folder_dir + fil
            cor_out_folder = r_png + fol + "\\"

            # read log
            # if logs folder not present then make one
            dir_check(root + "logs" + "\\" + "png_maker\\")
            logs_path = root + "logs" + "\\" + "png_maker" + "\\" + "c_logs.txt"
            file_if_not(logs_path)
            logs_dict = read_dict(logs_path)

            # call png_maker for this file only if it is not done already
            # parser
            # if folder is in logs file
            # flag for file presence
            file_present = False

            if fol in logs_dict:
                # check whether file(i) is in it or not
                for i in logs_dict[fol]:
                    # if file found then continue
                    if i == fil:
                        file_present = True
                        continue
                if not file_present:
                    png_maker(current_file_path, cor_out_folder)
                    # after parsing done, record in logs
                    ap_dict(logs_path, fol, fil, 1)
            else:
                # print("folder not there")
                png_maker(current_file_path, cor_out_folder)
                ap_dict(logs_path, fol, fil, 0)
