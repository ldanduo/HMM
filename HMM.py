#!/usr/bin/python
#-*-coding:utf-8
import os
import sys
import pdb

def load_model(f_name):
    ifp = file(f_name, 'rb')
    return eval(ifp.read())

prob_start = load_model("prob_start.py")
prob_trans = load_model("prob_trans.py")
prob_emit = load_model("prob_emit.py")


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}] #tabular
    path = {}
    for y in states: #init
        V[0][y] = start_p[y] * emit_p[y].get(obs[0],0)
        path[y] = [y]
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            (prob,state ) = max([(V[t-1][y0] * trans_p[y0].get(y,0) * emit_p[y].get(obs[t],0) ,y0) for y0 in states if V[t-1][y0]>0])
            V[t][y] =prob
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def cut(sentence):
    #pdb.set_trace()
    prob, pos_list =  viterbi(sentence,('B','M','E','S'), prob_start, prob_trans, prob_emit)
    return (prob,pos_list)

if __name__ == "__main__":
    test_str = u"长春市长春节讲话。"
    prob,pos_list = cut(test_str)
    print test_str
    print pos_list
    test_str = u"他说的确实在理."
    prob,pos_list = cut(test_str)
    print test_str
    print pos_list

    test_str = u"毛主席万岁。"
    prob,pos_list = cut(test_str)
    print test_str
    print pos_list

    test_str = u"我有一台电脑。"
    prob,pos_list = cut(test_str)
    print test_str
    print pos_list
