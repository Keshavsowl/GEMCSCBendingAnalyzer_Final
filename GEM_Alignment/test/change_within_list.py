'''
This file reads a .list file or .txt file that already has name of files
line by line. All this file does is concatenates the string path name to
each file line by line.

--Towsifa Akhter
'''

f = open("singleMuonGun_11_3_4_2021_design.list", "r")

#print(f.read(10)) #print first 10 characters of the file

list_of_original_lines = f.readlines()
#list_of_new_lines = ["root://cms-xrd-global.cern.ch/" + line.strip() +"\n" for line in list_of_original_lines]

##the list and loop below writes the first 5 lines of a file into a new list
list_of_new_lines = []
for i in range(5):
  list_of_new_lines.append(list_of_original_lines[i])
##end of the writing first 5 lines


f1 = open("shortList_singleMuonGun_11_3_4_2021_design.list", "w")
f1.writelines(list_of_new_lines)
f1.close()
