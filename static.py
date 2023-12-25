#!/usr/bin/python3.4

''' **************************************************************** '''

import math
import matplotlib.pyplot as plt
import random

import numpy as np
import pandas as pd

''' **************************************************************** '''

class FLOW(object):
	def method(self, depth):
		#print('depth', round(abs(depth)))
		my_flow = random.randrange(-10, 10, 2)
		# my_flow = random.randrange(0, 10, 2)
		# return my_flow / 10
		if my_flow > 0:
			print('flow', my_flow)
		# return my_flow - 5
		# return 0.2
		return my_flow

flow = FLOW()

el_count  =  10    # количество элементов
cable_len =  100    # длина кабеля, метры
Ckt       =    0.02 # коэффициент касательной составляющей
Ckn       =    1.2  # коэффициент нормальной составляющей
Dk        =    0.01 # диаметр кабеля
ro        = 1025    # плотность воды
Vb        =    1.5  # скорость течения (уточнить - скорость потока относительно кабеля это, а не течение)
Gk        =    0    # остаточная плавучесть

Vb_lst = []
Fx_lst = []
Fy_lst = []
Fz_lst = []

for v in range(0, 30, 5):
	for x in range(-100, 100, 10):
		for y in range(-100, 100, 10):
			for z in range(-100, 100, 10):
				Vb_lst.append(v/10)
				Fx_lst.append(x)
				Fy_lst.append(y)
				Fz_lst.append(z)



in_array = list(range(0, 11))
in_array_1 = [0]*11


# массивы координат элементов

# прямой
x_k = list(range(0, el_count + 1))
y_k = list(range(0, el_count + 1))
z_k = list(range(0, el_count + 1))

# обратный
x_kn = list(range(0, el_count + 1))
y_kn = list(range(0, el_count + 1))
z_kn = list(range(0, el_count + 1))

''' **************************************************************** '''

def static(VB, FX, FY, FZ):
	
	global el_count
	global cable_len
	global Ckt
	global Ckn
	global Dk
	global ro
	global Vb
	global Gk



	global x_k
	global y_k
	global z_k


	# длина одного элемента
	''' dbl_dLk  '''
	el_len = cable_len / el_count

	# суммарные силы по осям от аппарата (с учётом гидродинамики и плавучести)
	# сила на ходовом конце кабеля

	# global Vb_lst
	# global Fx_lst
	# global Fy_lst
	# global Fz_lst


	# print(Vb_lst[5000000])
	# print(Fx_lst[5000000])
	# print(Fy_lst[5000000])
	# print(Fz_lst[5000000])

	Vb = VB
	Fx = FX
	Fy = FY
	Fz = FZ

	in_array[0] = el_count
	in_array[1] = cable_len
	in_array[2] = Ckt
	in_array[3] = Ckn
	in_array[4] = Dk
	in_array[5] = ro
	in_array[6] = Vb
	in_array[7] = Gk
	in_array[8] = Fx
	in_array[9] = Fy
	in_array[10] = Fz

	in_array_1[0] = el_count
	in_array_1[1] = cable_len
	in_array_1[2] = Ckt
	in_array_1[3] = Ckn
	in_array_1[4] = Dk
	in_array_1[5] = ro
	in_array_1[6] = Vb
	in_array_1[7] = Gk
	in_array_1[8] = Fx
	in_array_1[9] = Fy
	in_array_1[10] = Fz

	# print(in_array_1)

	# начальные координаты
	x_k[0] = 0
	y_k[0] = 0
	z_k[0] = 0
	
	# номер текущего отрезка
	cur_pos = 1

	while True:
	
		# 1 
	
		# результирующая сила - модуль
		# ходовой конец кабеля
		mod_F = math.sqrt(Fx ** 2 + Fy ** 2 + Fz ** 2)
	
		# направляющие косинусы
		Cos_Ax = Fx / mod_F
		Cos_Ay = Fy / mod_F
		Cos_Az = Fz / mod_F
	
		# 2
	
		# координаты элемента
		x_k[cur_pos] = x_k[cur_pos - 1] - el_len * Cos_Ax
		y_k[cur_pos] = y_k[cur_pos - 1] - el_len * Cos_Ay
		z_k[cur_pos] = z_k[cur_pos - 1] - el_len * Cos_Az
	
		# 3
		
		# знак направления
		if Cos_Ax >= 0:
			''' int_modCax '''
			mod_cax = 1
		else:
			mod_cax = -1

		# касательная составляющая




		# Vb = flow.method(y_k[cur_pos])

		if Vb >= 0:
			sgn = 1
		else:
			sgn = -1
		#print('x_k', x_k[cur_pos])



		Fkt = Ckt * Ckn * el_len * Dk * math.pi * ro * mod_cax * ((Vb * Cos_Ax) ** 2) / 2
	
		# нормальная составляющая
		Fkn = Ckn * el_len * Dk * ro * ((Vb * math.sqrt(1 - Cos_Ax ** 2)) ** 2) / 2
	
		# 4
		''' dbl_CosAxg ''' ''' dbl_CosAy ''' ''' dbl_CosAz '''
		Cos_Axg = -math.sqrt((Cos_Ay) ** 2 + (Cos_Az) ** 2)
		
		if Cos_Axg == 0:
		
			Cos_Ayg = 0	#	''' dbl_CosAyg '''
			Cos_Azg = 0	#	''' dbl_CosAzg '''
		
		else:
			
			Cos_Ayg = -Cos_Ax * Cos_Ay / Cos_Axg
			Cos_Azg = -Cos_Ax * Cos_Az / Cos_Axg
		
		# 5
		# силы
	
		Fx = Fx - Fkt * Cos_Ax + Fkn * Cos_Axg
	
		# комментарий по поводу смены знака
	
		Fy = Fy + Gk * el_len - Fkt * Cos_Ay + Fkn * Cos_Ayg
		Fz = Fz - Fkt * Cos_Az + Fkn * Cos_Azg
	
		# 6
	
		cur_pos += 1	# счётчик
	
		# условие выхода из цикла
		''' if cur_pos == el_count + 2: '''
		if cur_pos == el_count + 1:
			break
		
		####
	
	mod_F = math.sqrt(Fx ** 2 + Fy ** 2 + Fz ** 2)

	####
	
''' **************************************************************** '''

def visual():
	
	'''
	http://nbviewer.ipython.org/github/whitehorn/Scientific_graphics_in_python/blob/master/P1%20Chapter%201%20Pyplot.ipynb
	'''
	
	global x_k
	global y_k
	global z_k
	
	
	
	fig = plt.figure()   # Создание объекта Figure
	
	fig = plt.figure(1,(28,16))   # Создание объекта Figure
	
	#plt.scatter(1.0, 1.0)   # scatter - метод для нанесения маркера в точке (1.0, 1.0)
	plt.scatter(0, 0)
	a = len(x_k) - 1
	plt.scatter(x_k[a], y_k[a])




	print (fig.axes)  
	
	#plt.savefig('fig1')
	
	for i in range(0,len(x_k)):
		
		#plt.scatter(1000*x_k[i], 1000*y_k[i],10)
		plt.scatter(x_k[i], y_k[i], 10)

	#plt.savefig("fig2")
	
	plt.show()

''' **************************************************************** '''

def saver(Vb, Fx, Fy, Fz, i):



	# np.save("output.npy", in_array_1)


	df = pd.DataFrame(x_k + y_k + z_k)
	# df.to_csv("files/" + str(Vb) + "_" + str(Fx) + "_" + str(Fy) + "_" + str(Fz) + "_" + 'out.csv', index=False, header=False)
	df.to_csv("files/" + str(i) + "_" + 'out.csv', index=False, header=False)
	df = pd.DataFrame(in_array)
	# df.to_csv("files/" + str(Vb) + "_" + str(Fx) + "_" + str(Fy) + "_" + str(Fz) + "_" + 'in.csv', index=False, header=False)
	df.to_csv("files/" + str(i) + "_" + 'in.csv', index=False, header=False)


# для запуска из консоли
if __name__ == '__main__':


	# i =6479999
	# print(len(Vb_lst))
	# len(Vb_lst)
	for i in range(0,len(Vb_lst)):
		if Fx_lst[i] == 0 and Fy_lst[i] == 0 and Fz_lst[i] == 0:
			print("0, 0, 0")
			# print(len(Vb_lst))
		else:
			static(Vb_lst[i], Fx_lst[i], Fy_lst[i], Fz_lst[i])
			saver(Vb_lst[i], Fx_lst[i], Fy_lst[i], Fz_lst[i], i)

	# visual()

