
#Waktu sampling sistem
Ts = 

#Pembuatan blok-blok yang digunakan menggunakan fungsi

#Blok Integrator
def my_integrator(mylist, mytotal) :
	total = mytotal + (Ts)*(mylist[0] + mylist[1])/2
	#mylist[1] = mylist[0]
	return total

#Blok Limiter
def my_limiter(x, upper, lower) :
	a = x
	if (a>=upper) :
		a = upper
	
	if (a<=lower) :
		a = lower
	
	return a;
	
#Blok kontur tanjakan
def tanjakan(jarak) :
	if ((jarak >= 0) and (jarak < 5540)) :
		tanjak = 0
	elif ((jarak >= 5540) and (jarak < 6696)) :
		tanjak = 0.000865051903114188
	elif ((jarak >= 6696) and (jarak < 8033)) :
		tanjak = 0.0022
	elif ((jarak >= 8033) and (jarak < 9890)) :
		tanjak = -0.0038
	elif ((jarak >= 9890) and (jarak < 11750)) :
		tanjak = 0.0016
	elif ((jarak >= 11750) and (jarak < 13381)) :
		tanjak = -0.0012
	elif ((jarak >= 13381) and (jarak < 15145)) :
		tanjak = -0.0023
	elif ((jarak >= 15145) and (jarak < 18245)) :
		tanjak = 3.2258e-04
	elif ((jarak >= 18245) and (jarak < 19550)) :
		tanjak = 0.0031
	elif ((jarak >= 19550) and (jarak < 20935)) :
		tanjak = 0.0022
	elif ((jarak >= 20935) and (jarak < 22390)) :
		tanjak = 6.8729e-04
	elif ((jarak >= 22390) and (jarak < 24032)) :
		tanjak = -6.0901e-04
	elif ((jarak >= 24032) and (jarak < 26552)) :
		tanjak = 3.9683e-04
	elif ((jarak >= 26552) and (jarak < 33380)) :
		tanjak = 0.0
	elif ((jarak >= 33380) and (jarak < 43289)) :
		tanjak = -1.0092e-04
	elif ((jarak >= 43289) and (jarak < 47626)) :
		tanjak = -4.6115e-04
	elif ((jarak >= 47626) and (jarak < 56623)) :
		tanjak = -2.2230e-04
	elif ((jarak >= 56623) and (jarak < 62869)) :
		tanjak = 3.2020e-04
	elif ((jarak >= 62869) and (jarak < 69864)) :
		tanjak = 0.0010
	elif ((jarak >= 69864) and (jarak < 73774)) :
		tanjak = 0.0013
	elif ((jarak >= 73774) and (jarak < 80745)) :
		tanjak = 4.3035e-04
	elif ((jarak >= 80745) and (jarak < 84007)) :
		tanjak = 0.0046
	elif ((jarak >= 84007) and (jarak < 91643)) :
		tanjak = 0.0041
	elif ((jarak >= 91643) and (jarak < 97778)) :
		tanjak = 0.0028
	elif ((jarak >= 97778) and (jarak < 103070)) :
		tanjak = -0.0019
	elif ((jarak >= 103070) and (jarak < 109635)) :
		tanjak = 0.0087
	elif ((jarak >= 109635) and (jarak < 116871)) :
		tanjak = 0.0117
	elif ((jarak >= 116871) and (jarak < 120941)) :
		tanjak = 0.0076
	elif ((jarak >= 120941) and (jarak < 127164)) :
		tanjak = 0.0130
	elif ((jarak >= 127164) and (jarak < 132869)) :
		tanjak = 0.0123
	elif ((jarak >= 132869) and (jarak < 135946)) :
		tanjak = 0.0127
	elif ((jarak >= 135946) and (jarak < 140066)) :
		tanjak = 0.0126
	elif ((jarak >= 140066) and (jarak < 144711)) :
		tanjak = 0.0090
	elif ((jarak >= 144741) and (jarak < 151767)) :
		tanjak = 0.0130
	elif ((jarak >= 151767) and (jarak < 155134)) :
		tanjak = 0.0226
	elif ((jarak >= 0) and (jarak < 160000)) :
		tanjak = 0
	else :
		tanjak = 0
		
	return tanjak;

#Blok kontur tikungan
# def tikungan(jarak_2) :
	
	# elif ((jarak_2 >= 140066) and (jarak_2 < 144711)) :
		# tikung = 0.0090
	# elif ((jarak_2 >= 144741) and (jarak_2 < 151767)) :
		# tikung = 0.0130
	# elif ((jarak_2 >= 151767) and (jarak_2 < 155134)) :
		# tikung = 0.0226
	# elif ((jarak_2 >= 0) and (jarak_2 < 160000)) :
		# tikung = 0
	# else :
		# tikung = 0
		
	# return tikung;
	
#Inisiasi variabel-variabel
a1 = [0.0, 0.0]
v1 = [0.0, 0.0]
s1 = 0.0
a2 = [0.0, 0.0]
v2 = [0.0, 0.0]
s2 = 0.0
a3 = [0.0, 0.0]
v3 = [0.0, 0.0]
s3 = 0.0	
Trac_force = 0.0
max_Trac_force = 
max_power = 
kf = 
	
while(True) :
	#Perhitungan gaya traksi
	if (Trac_force*v1[0]) <= (N*N/64) * max_power :
		Trac_force = ((N*0.125)*max_Trac_force) - (kf*v1[0])
	else :
		Trac_force = (N*N*0.01625) * max_power / v1[0]
			
	if (N < 0) :
		Trac_force = -1 * Trac_force
	
	#############Bagian Lokomotif#############
	#Pencarian gaya tanjakan dan tikungan
	f_tanjak1 = tanjakan(s1)*84
	
	#Perhitungan gaya total
	Force1 = Trac_force - f_adhesi1 - f_tanjak1 - (2.86+0.55*(10/84)*(v1[0]+0)**2/10) - 20685.4788*v1[0] - 7005073.41*s1 + 7005073.41*s2 + 20685.4788*v2[0]  #- f_tikung1
		
	#Perhitungan kinematika translasi	
	a1[0] = Force1*1.18894679432796e-05
	v1[0] = my_integrator(a1 , v1[0])
	v1[0] = my_limiter(v1[0], 33.3333333333333, -33.3333333333333)
	s1 = my_integrator(v1 , s1)
	a1[1] = a1[0]
	v1[1] = v1[0]
	
	
	#############Bagian Gerbong 1#############
	#Pencarian gaya tanjakan dan tikungan
	f_tanjak2 = tanjakan(s2)*30
	
	#Perhitungan gaya total
	Force2 = -(2.55+(v2[0]+0)**2/4000) + 20685.4788*v1[0] + 7005073.41*s1 - f_adhesi2 + 20685.4788*v3[0] + 7005073.41*s3 - 14010146.8200000*s2 - 41370.9576000000*v2[0] - f_tanjak2 #- f_tikung2
		
	#Perhitungan kinematika translasi	
	a2[0] = Force2*3.32137053087757e-05
	v2[0] = my_integrator(a2 , v2[0])
	v2[0] = my_limiter(v2[0], 33.3333333333333, -33.3333333333333)
	s2 = my_integrator(v2 , s2)
	a2[1] = a2[0]
	v2[1] = v2[0]
	
	#############Bagian Gerbong 2#############
	#Perhitungan gaya-gaya sebelum ditotal
	f_tanjak3 = tanjakan(s3)*30
	
	#Perhitungan gaya total
	Force3 = - (2.55+(v3[0]+0)**2/4000) - 20685.4788*v3[0] - 7005073.41*s3 + 7005073.41*s2 + 20685.4788*v2 - f_adhesi3 - f_tanjak3 #- f_tikung3
		
	#Perhitungan kinematika translasi	
	a3[0] = Force3*3.32137053087757e-05
	v3[0] = my_integrator(a3 , v3[0])
	v3[0] = my_limiter(v3[0], 33.3333333333333, -33.3333333333333)
	s3 = my_integrator(v3 , s3)
	a3[1] = a3[0]
	v3[1] = v3[0]
	
	
	
	
	
	
	
	
	
	
	
