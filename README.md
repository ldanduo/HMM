#隐马尔科夫模型进行中文分词
author : darrenan
created at : 2014-03-17

#模型训练
python HMM_train.py RenMinData.txt_utf8

* RenMinData.RenMinData_utf8 为人民日报已经人工分词的预料。

生成三个文件

* prob_start.py 为模型的初始概率
* prob_trans.py 为模型状态转移概率
* prob_emit.py 为发射概率

#测试模型效果
python HMM.py

#reference
* 维特比算法：http://zh.wikipedia.org/wiki/%E7%BB%B4%E7%89%B9%E6%AF%94%E7%AE%97%E6%B3%95
* https://github.com/fxsjy/finalseg
