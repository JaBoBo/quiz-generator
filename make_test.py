#!/usr/bin/python
# format: python take_test.py <input q/a database filename> <output test file name> num_answers_per_question num_qs_to_generate

# provide final answer key + scantron type

from os import system,name # used to clear screen in windows or linux
from random import randint # to randomize questions & answers


def read_test_file(filename): # reads in all questions/answers
					  # returns list of q/a's & total # of questions
	numitems = 0 ; testinput = [] ; firstline = True
	with open(filename) as f:
		while True:
			if firstline:
				firstline = False
				try:
					num_answers = int(f.readline())
				except:
					print "UH OH, FIRST LINE SHOULD BE # OF ANSWERS PER QUESTION"
					exit(0)
			wronglist = [] ; bad_num_wrongs = False
			question_in=f.readline() ; right_answer=f.readline()
			if not right_answer or not question_in: break
			question_in = question_in.rstrip() ; right_answer = right_answer.rstrip()
			for ctr in range(num_answers-1):
				add_wrong=f.readline()
				if not add_wrong: bad_num_wrongs = True ; break
				add_wrong = add_wrong.rstrip()
				wronglist.append(add_wrong)
			if bad_num_wrongs: break
			testinput.append([question_in,right_answer,wronglist])
			numitems += 1
		f.close()
	return testinput, numitems

def pick_n_shuffle_qs(original_list,num_qs): # shuffles all questions
				     # returns orignal_list, shuffled (answers not shuffled)
	def one_rand(list_size):
		xyz = randint(0,list_size-1)
		while xyz in covered_items: # keep generating until not in used_list
			xyz = one_rand(list_size)
		return xyz
	newlist = [] # format: [ [<question>,answernum, [ans1,ans2,ans3,ans4],[q2,...] ]
	covered_items = []
	for i in range(num_qs):
#	for i in range(len(original_list)):
		next_question = one_rand(len(original_list))
		newlist.append(original_list[next_question])
		covered_items.append(next_question)
	return newlist

def shuffle_answers(finlist): # takes in shuffled q's
			      # returns list w/ shuffled q's & a's
			      # return format: [[<question>,<right answer index>,[<all answers>]],...]
	def rand_answer(list_size):
		xyz = randint(0,list_size-1)
		while xyz in covered_answers: # keep generating until not in used_list
			xyz = rand_answer(list_size)
		return xyz
	full_test = []
	for eachq in finlist:
		covered_answers = []
		shuffled = []
		answer_list = eachq[2] # make unshuffled answer list - last entry will be correct one before shuffle
		answer_list.append(eachq[1])
		for i in range(len(answer_list)):
			next_answer = rand_answer(len(answer_list))
			covered_answers.append(next_answer)
			if next_answer == len(answer_list)-1:
				right_answer = len(shuffled) # randomly selected the correct one
			shuffled.append(answer_list[next_answer])
		full_test.append([eachq[0],right_answer,shuffled])
	return full_test

def display_test_key(complete_test_list):
	for eachitem in complete_test_list:
		print "Question: " + eachitem[0]
		for eachanswer in eachitem[2]:
			print chr(65 + eachitem[2].index(eachanswer)) + ") " + eachanswer
		print "Correct Answer: " + chr(65 + eachitem[1]) + ") " + eachitem[2][eachitem[1]]
		print

def make_test_key_file(complete_test_list,outfilename):
	f = open(outfilename,'w') # open/create new file
	for eachitem in complete_test_list:
		f.write("Question: " + eachitem[0] + "\n")
		for eachanswer in eachitem[2]:
			f.write(chr(65 + eachitem[2].index(eachanswer)) + ") " + eachanswer + "\n")
		f.write("Correct Answer: " + chr(65 + eachitem[1]) + ") " + eachitem[2][eachitem[1]] + "\n")
		f.write("\n")
	f.close()

def process_test_file(fname,fnameout,num_qs):
	test_list, num_questions =  read_test_file(fname)
	new_test_list = pick_n_shuffle_qs(test_list,num_qs) # remember to include new entry for correct answer
	finished_test_list = shuffle_answers(new_test_list)
	display_test_key(finished_test_list)
	make_test_key_file(finished_test_list,fnameout)


#### MAIN ####
filein='QUIZ.DAT.WITHNUMAS'
fileout='generated_tests/version3quiz.txt'
num_qs=12 # desired number of questions
#main_menu(filein,fileout,num_as,num_qs,'')
process_test_file(filein,fileout,num_qs)



####################################### FUTURE STUFF BELOW MOVED TO GET OUT OF THE WAY
#######################################
#######################################
#######################################
def clearscreen():
	system('cls' if name == 'nt' else 'clear')
def show_help():
	print "Insert Help Info Here"
def main_menu(intest,outtest,answernum,numgen,err_msg):
	clearscreen()
	h='#'*80
	hline = h + '\n'
#	hline = '##############################################################################\n'
	print hline ; print '            TEST GENERATOR MAIN MENU\n'; print hline; print
	print 'Test Input File: ' + intest + '    # of Answers per Question: ' + str(answernum)
	print 'Test Output File: ' + outtest + '   # of Test Questions to Generate: ' + str(numgen)
# left/right columnize
	print
	print '1)  Generate Test from File'
# redo menu to import q's from file -or- enter manually; then another to generate a test
	print '2)  Manually Enter Test Q&As'
# consider using database
	print '3)  Change Test Input File'
	print '4)  Change Test Output File'
# add warning for overwrite
	print '5)  Change # of Answers per Question in Q&As'
	print '6)  Change # of Test Questions to Generate'
	print '7)  View Test Output File'
	print '8)  Exit'

# 1) Create/Load/Edit Test Question Database
#### 1) Select existing or new DB
#### 2) View Q&As
#### 3) Add Q&As
#### 4) Modify Q&As
#### 5) Delete Q&As
#### 6) Exit Sub-Menu
# 2) Test & Answer Key Ops
#### 1) Generate (Make text & db file - test & key) - steps include # of Qs & # of mltpl chc answrs
#### 2) Load existing (Db or text?)
#### 3) Print Test
#### 4) Print Answer Key
#### 5) Exit Sub-Menu
# 3) Exit
	print; print hline ; print
	if err_msg:
		print '******' + err_msg; print
		err_msg = ''
	else: print; print
	response = raw_input('Selection: ')
	if response == '1':
# check valid/existing intest filename
# check valid outtest filename, verify overwrite if exists
# check valid answernum
# check valid num of questions to generate vs. total num of questions
# if bad, generate proper err_msg
# if good, process
		process_test_file(intest,outtest,answernum,numgen) # remember to error check
	elif response == '2':
		pass
	elif response == '3':
		pass
	elif response == '4':
		pass
	elif response == '5':
		aperq_entered = raw_input('Enter # of Answers per Question in Q&As: ')
		if aperq_entered.isdigit():
			temp_aperq = int(aperq_entered)
			if temp_aperq >= 2:
				answernum = temp_aperq
			else:
				err_msg = 'Invalid Entry for # of Answers per Question in Q&As. (Valid: 2-9)'
		else:
			err_msg = 'Invalid Entry for # of Answers per Question in Q&As. (Valid: 2-9)'
	elif response == '6':
		num_qs_to_generate = raw_input('Enter # of Test Questions to Generate: ')
		if num_qs_to_generate.isdigit():
			temp_numgen = int(num_qs_to_generate)
			if temp_numgen > 0:
				numgen = temp_numgen
			else:
				err_msg = 'Invalid Entry for # of Test Questions to Generate.'
		else:
			err_msg = 'Invalid Entry for # of Test Questions to Generate.'
	elif response == '7':
		pass
	elif response == '8':
		exit(0)
	else:
		main_menu(intest,outtest,answernum,numgen,"Improper Selection!!!!! Try Again.")
	main_menu(intest,outtest,answernum,numgen,err_msg)
