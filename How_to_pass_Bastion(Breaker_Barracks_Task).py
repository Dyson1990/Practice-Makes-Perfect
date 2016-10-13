# -*- coding:utf-8 -*-  
"""
@Version: ??
@Author: Dyson
@Contact: Weaver1990@163.com
@File: Bastion_Bow.py
@Time: 2016/10/13 15:46
@Instruction：其实可以不用将点坐标引入矩阵，这里主要是为了练习numpy
暂时没有考虑两条线重合的情况
"""
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"
import numpy as np
import itertools
log_obj = set_log.Logger('Bastion_Bow.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('Bastion_Bow.log', if_cleanup = True)  # 是否需要在每次运行程序前清空Log文件


def build_array(points_list):
	location_arr = np.array(points_list)
	# log_obj.debug2("位置矩阵：" + arr_points)
	max_row, max_col = [np.max(np.hsplit(location_arr, 2)[0]), np.max(
			            np.hsplit(location_arr, 2)[1])]
	# log_obj.debug("max_row：%d，max_col：%d" % (max_row, max_col))
	arr = np.zeros([max_row, max_col], dtype=int)
	for point in points:
		arr[point[0]-1, point[1]-1] = 1 # 假定计算行列时，第一列（行）号为1
	return  arr

def build_choices(points_list):
	points_arr = build_array(points_list)
	choices_list = []
	# 将新生成的01矩阵中所有的行列向量列举出来
	col_vec_list = np.hsplit(points_arr, int(points_arr.shape[1]))
	row_vec_list = np.vsplit(points_arr, int(points_arr.shape[0]))
	for point in points_list:
		point = [point[0]-1,point[1]-1]
		# 找出目标点对应的行列向量
		row_vec = row_vec_list[point[0]]
		col_vec = col_vec_list[point[1]]
		# 看看目标点的行列向量是不是零向量
		if len(row_vec.nonzero()[0])> 1: # 如果向量中有两个以上的点
			l = []
			for i in xrange(len(row_vec.nonzero()[0])):
				# 存入向量中，点的坐标
				l.append([point[0], row_vec.nonzero()[1][i]])
			if l not in choices_list:
				choices_list.append(l)
		if len(col_vec.nonzero()[0]) > 1:
			l = []
			for i in xrange(len(col_vec.nonzero()[0])):
				l.append([col_vec.nonzero()[0][i], point[1]])
			if l not in choices_list:
				choices_list.append(l)
			
		# 找出所有斜线方向的向
		l1 = []
		l2 = []
		for point2 in points_list:
			point2 = [point2[0] - 1, point2[1] - 1]
			# ‘/’这个方向上的
			if sum(point) == sum(point2):
				l1.append(list(point2))

			# ‘\’这个方向上的
			if abs(point[0]-point[1]) == abs(point2[0]-point2[1]):
				l2.append(list(point2))
		l1.sort()
		l2.sort()
		if l1 not in choices_list:
			choices_list.append(l1)
		if l1 not in choices_list:
			choices_list.append(l2)
	return choices_list

def find_the_choice(points_list, num=10):
	choices_map = list(build_choices(points_list))
	for t in itertools.combinations_with_replacement(choices_map, r=num):
		# 列举所有5条直线的组合
		sample = ([[0, 2], [0, 4], [0, 6]], [[0, 2], [2, 2]], [[0, 6], [2, 6]],
		   [[0, 6], [1, 5]], [[2, 8], [3, 7]])
		# 计数器
		d = {}
		for l1 in t:
			for l2 in l1:
				str0 = str(l2)
				if str0 not in d.keys():
					d[str0] = 0
				d[str0] += 1
		if len(d) == len(points_list) and min(d.values()) > 1:
			print "Bingo !!! :" , t
	
if __name__ == '__main__':
	"""
	   1   2   3   4   5   6   7   8   9
	  ___________________________________
	1|   |   | X |   | X |   | X |   |   |
	2|   | X |   | X |   | X |   | X |   |
	3| X |   | X |   |   |   | X |   | X |
	4|   |   |   |   |   |   |   | X |   |
	5|   |   |   |   | X |   |   |   |   |
	
	   0   1   2   3   4   5   6   7   8
	  ___________________________________
	0|   |   | X |   | X |   | X |   |   |
	1|   | X |   | X |   | X |   | X |   |
	2| X |   | X |   |   |   | X |   | X |
	3|   |   |   |   |   |   |   | X |   |
	4|   |   |   |   | X |   |   |   |   |
	"""
	points = [(1, 3), (1, 5), (1, 7), (2, 2), (2, 4), (2, 6), (2, 8), (3, 1),
	          (3, 3), (3, 7), (3, 9), (4, 8), (5, 5)]
	# points_map = build_array(points)
	"""
	[[0 0 1 0 1 0 1 0 0]
	 [0 1 0 1 0 1 0 1 0]
	 [1 0 1 0 0 0 1 0 1]
     [0 0 0 0 0 0 0 1 0]
     [0 0 0 0 1 0 0 0 0]]
	"""
	# choices_map = build_choices(points)
	# build_choices(points)
	find_the_choice(points,num=10)
	
