# 1.2 billion = 1200000000
# if one files have 1 lak then total 12000 files.


# naming convention

# main dire = e
# subdirectories = 1,2,3,4,5,6,7,8,


# first write splitter for just one file

# out folder is in root/smiles/
def feed_splitter(huge_files_folder, root):

	if huge_files_folder[-1] != "/":
		huge_files_folder = huge_files_folder + "/"
	if root[-1] != "/":
		root = root + "/"
	
	files = getF(huge_files_folder,"files")

	for fil in files:

		current_file_path = huge_files_folder + fil
		cor_out_folder    = root + "/" + "smiles" + "/" + fil + "/"

		dir_check(cor_out_folder)
		dir_check(root + "/" + "logs" + "/" + "splitter" + "/")
		logs_path = root + "logs" + "/" + "splitter" + "/" + "split_logs.txt"
		file_if_not(logs_path)
		logs_dict = read_dict(logs_path)


		file_present = False

            if fol in logs_dict:
                # check whether file(i) is in it or not
                for i in logs_dict[fol]:
                    # if file found then continue
                    if i == fil:
                        file_present = True
                        continue
                if not file_present:
                    splitter(current_file_path, cor_out_folder)
                    # after parsing done, record in logs
                    ap_dict(logs_path, fol, fil, 1)
            else:
                # print("folder not there")
                splitter(current_file_path, cor_out_folder)
                ap_dict(logs_path, fol, fil, 0)


def splitter(huge_file_path, out_folder4pieces):

	# split files into pieces with 50k molecules each
	# close writing when modulo 50k == 0 or when end of file reached
	if out_folder4pieces[-1] != "/":
		out_folder4pieces = out_folder4pieces + "/"

	file_no = 1
	line_no = 0
	piece = ""

	with open (huge_file_path, 'r') as f:
		for line in f:
			piece += line + "\n"
			line_no += 1

			if line_no%50000 == 0:
				out_file_path = out_folder4pieces + str(file_no) + ".smi"
				file_if_not(out_file_path)
				with open(out_file_path, 'w', encoding="utf-8") as w:
					w.write(piece)
					piece = ""
					file_no += 1
		# possible when file ended but threshold of size not met, so now piece will not be ""
		# SO check, if piece is not "" then write to file,
		# nitpicking : what if file to be read was empty even then piece wil be ""
		# We dont care about that 

		if piece != "":
			out_file_path = out_folder4pieces + str(file_no) + ".smi"
				file_if_not(out_file_path)
				with open(out_file_path, 'w', encoding="utf-8") as w:
					w.write(piece)
					piece = ""

		


