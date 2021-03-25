
# Parser for babel svg



import os
from os import walk
read_path = ""
out_path  = "/content/drive/My Drive/DataSets/Chemistry/test/b/"
walked = []


# NOTE below string also include \n, to add \n at end you must enter on last line
start = """<svg version="1.1" id="topsvg"
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:cml="http://www.xml-cml.org/schema" x="0" y="0" width="256" height="256" viewBox="0 0 100 100">
<title> - Open Babel Depiction</title>
<rect x="0" y="0" width="100" height="100" fill="white"/>
<g transform="translate(0,0)">
"""


fil = 'fill="rgb(0,0,0)"'
strke='stroke="rgb(0,0,0)"'
strke_width='stroke-width="1"'


# NOTE : anything added to above str is added on new line


for (all) in walk(read_path):
    walked.extend(all)

filenames = walked[2]
st = ""
out = ""
smile_done =False
end = False
finish = False
space = " "
width ='width="100"'
height = 'height="100"'

test_c = 0
dim_flag = False
b_check = False
s_check = False

for file in filenames:
    with open ( read_path+file , 'r') as f:
        for i in range(7):
            next(f)
        for line in f:
            if line[0:4]=="</g>" or end:

                end = True

                line_split = line.split()
                for token in line_split:
                    if token[0]==">":
                        id = "db: " + file + " id: " + token[1:]
                        st = st +  "</g>" + "\n" + "</svg>" + "\n"
                        st = id  + "\n" + '"""' +"\n"+ start + st + '"""' + "\n"
                        out = out + st
                        st = ""
                        smile_done =True
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


            token_list=[]
            for s in line.split():
                if s[-1]==">":
                    b_check =True

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
                            s = s+"/>"
                    elif s[-1] != ">":
                        s = s + ">"




                token_list.append(s)

            temp = ""
            for t in range(len(token_list)-1):

                temp += token_list[t] + " "

            # sometimes list will  be empty
            if token_list:
                temp += token_list[-1]+"\n"


            token_list=[]



            st = st + temp


    with open ( out_path+"p_"+file , 'w') as f:
        f.write(out)























# Parsed_obabel2png
from cairosvg import svg2png

import os
from os import walk

# input = /content/drive/My Drive/DataSets/Chemistry/test/a/
# output = /content/drive/My Drive/DataSets/Chemistry/test/b/

files = []
for (all) in os.walk('/content/drive/My Drive/DataSets/Chemistry/test/a/'):
  files.extend(all)

files = files[2]
name = ""
code = ""
code_flag = False
print(files)
for f in files:
  path = '/content/drive/My Drive/DataSets/Chemistry/test/a/'+f
  print(path)
  with open(path,'r') as smiles:
    for line in smiles:
      if line[0:3]=="db:":
        tok = line.split()
        db  = tok[1].split('.')[0]
        no  = tok[3]
        name = db + "_" + no
        print(name)
        continue

      if line[0:3]=='"""':
          if code_flag:
              code_flag = False
              # code = '"""\n' + code + '"""'
              # print(code)
              svg2png(bytestring=code, write_to='/content/drive/My Drive/DataSets/Chemistry/test/b/'+name+".png")

              # with open(output+name+".txt",'w') as g:
              #     g.write(code)
              # print(code)
              # exit(0)
              code = ""
              name = ""
              continue


      if line[0:3]=='"""':
          code_flag = True
          continue

      if code_flag:
          code += line








# directories
root =  "C:\\test\\"
























