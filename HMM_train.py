#!/usr/bin/python
#-*-coding:utf-8
import sys
import math
import pdb
state_M = 4
word_N = 0

A_dic = {}
B_dic = {}
Count_dic = {}
Pi_dic = {}
word_set = set()
state_list = ['B','M','E','S']
line_num = -1

INPUT_DATA = "RenMinData.txt_utf8"
PROB_START = "prob_start.py"
PROB_EMIT = "prob_emit.py"
PROB_TRANS = "prob_trans.py"


def init():
    global state_M
    global word_N
    for state in state_list:
        A_dic[state] = {}
        for state1 in state_list:
            A_dic[state][state1] = 0.0
    for state in state_list:
        Pi_dic[state] = 0.0
        B_dic[state] = {}
        Count_dic[state] = 0

def getList(input_str):
    outpout_str = []
    if len(input_str) == 1:
        outpout_str.append('S')
    elif len(input_str) == 2:
        outpout_str = ['B','E']
    else:
        M_num = len(input_str) -2
        M_list = ['M'] * M_num
        outpout_str.append('B')
        outpout_str.extend(M_list)
        outpout_str.append('S')
    return outpout_str

def Output():
    start_fp = file(PROB_START,'w')
    emit_fp = file(PROB_EMIT,'w')
    trans_fp = file(PROB_TRANS,'w')

    print "len(word_set) = %s " % (len(word_set))
    for key in Pi_dic:
        '''
        if Pi_dic[key] != 0:
            Pi_dic[key] = -1*math.log(Pi_dic[key] * 1.0 / line_num)
        else:
            Pi_dic[key] = 0
        '''
        Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
    print >>start_fp,Pi_dic

    for key in A_dic:
        for key1 in A_dic[key]:
            '''
            if A_dic[key][key1] != 0:
                A_dic[key][key1] = -1*math.log(A_dic[key][key1] / Count_dic[key])
            else:
                A_dic[key][key1] = 0
            '''
            A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
    print >>trans_fp,A_dic

    for key in B_dic:
        for word in B_dic[key]:
            '''
            if B_dic[key][word] != 0:
                B_dic[key][word] = -1*math.log(B_dic[key][word] / Count_dic[key])
            else:
                B_dic[key][word] = 0
            '''
            B_dic[key][word] = B_dic[key][word] / Count_dic[key]

    print >> emit_fp,B_dic
    start_fp.close()
    emit_fp.close()
    trans_fp.close()


def main():
    if len(sys.argv) != 2:
        print >> stderr,"Usage [%s] [input_data] " % (sys.argv[0])
        sys.exit(0)
    ifp = file(sys.argv[1])
    init()
    global word_set
    global line_num
    for line in ifp:
        line_num += 1
        if line_num % 10000 == 0:
            print line_num

        line = line.strip()
        if not line:continue
        line = line.decode("utf-8","ignore")

        word_list = []
        for i in range(len(line)):
            if line[i] == " ":continue
            word_list.append(line[i])
        word_set = word_set | set(word_list)


        lineArr = line.split(" ")
        line_state = []
        for item in lineArr:
            line_state.extend(getList(item))
        #pdb.set_trace()
        if len(word_list) != len(line_state):
            print >> sys.stderr,"[line_num = %d][line = %s]" % (line_num, line.endoce("utf-8",'ignore'))
        else:
            for i in range(len(line_state)):
                if i == 0:
                    Pi_dic[line_state[0]] += 1
                    Count_dic[line_state[0]] += 1
                else:
                    A_dic[line_state[i-1]][line_state[i]] += 1
                    Count_dic[line_state[i]] += 1
                    if not B_dic[line_state[i]].has_key(word_list[i]):
                        B_dic[line_state[i]][word_list[i]] = 0.0
                    else:
                        B_dic[line_state[i]][word_list[i]] += 1
    Output()
    ifp.close()
if __name__ == "__main__":
    main()
