import pika
import multiprocessing as MP
import math
import time 		#Library Waktu  
import serial	 	#Library Serial Communication 
from pymodbus.client.sync import ModbusSerialClient as ModbusClient 



def dinamika_MC (pitch_m,roll_m,surge_m,sway_m):
	# RMQ environment Setup
	# credentials = pika.PlainCredentials('kantu','dopple21')
	# parameters = pika.ConnectionParameters('192.168.43.220',5672,'/',credentials)
	# connection = pika.BlockingConnection(parameters)
	# channel = connection.channel()
	
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange='Simulator_Kereta',
							 exchange_type='direct')
	
	channel.queue_declare(queue='data_level')
#	channel.queue_declare(queue='data_kecepatan')
	
	channel.queue_bind(exchange='amq.topic',
					   queue='data_level',
					   routing_key='level')
	
	# channel.queue_bind(exchange='Simulator_Kereta',
					   # queue='data_kecepatan',
					   # routing_key='kecepatan')
	#Waktu sampling sistem
	Ts = 0.036

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
		
		return a
	
	
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

	#Variabel perhitungan
	count = 0
	mass = 200000.0
	acceleration = [0.0, 0.0]
	velocity = [0.0, 0.0]
	position = 0	
	Trac_force = Trac_force_hehe =  0.0
	max_Trac_force = 350000.0
	max_power = 1491400.0
	#mass = 90000.0
	kf = 0.21
	N = 0.0;
	f_adhesi1 = 168
	#file1 = open('dinamika_a_v_x.txt','w')
	
	#Variabel filter
	in22_surge = 0.0
	in22_surge_1 = 0.0
	in22_surge_2 = 0.0
	in22_surge_3 = 0.0
	in22_surge_4 = 0.0

	out22_surge = 0.0
	out22_surge_1 = 0.0
	out22_surge_2 = 0.0
	out22_surge_3 = 0.0
	out22_surge_4 = 0.0

	in22_sway = 0.0
	in22_sway_1 = 0.0
	in22_sway_2 = 0.0
	in22_sway_3 = 0.0
	in22_sway_4 = 0.0

	out22_sway = 0.0
	out22_sway_1 = 0.0
	out22_sway_2 = 0.0
	out22_sway_3 = 0.0
	out22_sway_4 = 0.0

	in12_surge = 0.0
	in12_surge_1 = 0.0
	in12_surge_2 = 0.0
	in12_surge_3 = 0.0
	in12_surge_4 = 0.0

	out12_surge = 0.0
	out12_surge_1 = 0.0
	out12_surge_2 = 0.0
	out12_surge_3 = 0.0
	out12_surge_4 = 0.0

	in12_sway = 0.0
	in12_sway_1 = 0.0
	in12_sway_2 = 0.0
	in12_sway_3 = 0.0
	in12_sway_4 = 0.0

	out12_sway = 0.0
	out12_sway_1 = 0.0
	out12_sway_2 = 0.0
	out12_sway_3 = 0.0
	out12_sway_4 = 0.0

	in11_roll = 0.0
	in11_roll_1 = 0.0
	in11_roll_2 = 0.0
	in11_roll_3 = 0.0
	in11_roll_4 = 0.0

	out11_roll = 0.0
	out11_roll_1 = 0.0
	out11_roll_2 = 0.0
	out11_roll_3 = 0.0
	out11_roll_4 = 0.0

	in11_pitch = 0.0
	in11_pitch_1 = 0.0
	in11_pitch_2 = 0.0
	in11_pitch_3 = 0.0
	in11_pitch_4 = 0.0

	out11_pitch = 0.0
	out11_pitch_1 = 0.0
	out11_pitch_2 = 0.0
	out11_pitch_3 = 0.0
	out11_pitch_4 = 0.0

	#Variabel penyimpan nilai integrator/akumulator
	v_surge = v_sway = v_surge_1 = v_sway_1 = 0.0
	pos_surge = pos_sway = 0.0

	#Variabel penyimpan nilai output coordination channel
	out_roll_coor = 0.0
	out_pitch_coor = 0.0

	# i = 1 #Variabel pointer dari file
	#file = open('track_data.txt','w') #Membuka file external yang berisi data track kereta api 

	#Variabel rate limiter
	rate_limit_up = 0.2
	rate_limit_down = -0.2

	count = -1
	while(True) :
		calculation = 0
		
		method_frame1, header_frame1, body1 = channel.basic_get('data_level')
		if method_frame1:
			N = float(body1)
			calculation = 1
			channel.basic_ack(method_frame1.delivery_tag)
			
		if calculation == 1 :
			time_now = time.time()
			count = count + 1
			#print (abs(Trac_force)*abs(velocity[0]))
			#print ((N*N/64) * max_power)
			if (N == 0.0) :
				Trac_force = 0.0
			else :
				if ((abs(Trac_force)*abs(velocity[0])) < ((N*N*0.01625) * max_power)):
					Trac_force = ((abs(N)*0.125)*max_Trac_force) - (kf*abs(velocity[0])) 
				else :
					Trac_force = (N*N*0.01625) * max_power / abs(velocity[0])
						
			if (N < 0) :
				Trac_force = -1 * Trac_force
			
			#print ("level Traksi"+str(N))
			#print ("gaya traksi"+str(Trac_force))
			#v_hehe = v_hehe + 1
			#Look-up nilai pitch dari track kereta
			if (count> 50000):
				pitch = 0
			else :
				pitch = 0
			
			#############Bagian Lokomotif#############
			#Pencarian gaya tanjakan dan tikungan
			f_tanjak1 = 0 #tanjakan(s1)*84
			
			#Perhitungan gaya total
			#Perhitungan percepatan dengan dinamika sederhana
			#Force = (Gaya traksi - Gaya gesek udara - m*g*sin(sudut kemiringan)) / massa
			#Gaya gesek udara = 0.5 * massa jenis udara* v^2 * koefisien gesekan
			pitch = 0 #3.14/6.0
			if velocity[0] >= 0 :
				acceleration[0] = (Trac_force - (0.5*1.184*velocity[0]*velocity[0]*0.9*9.61) - mass*0.98*(math.sin(pitch)))/mass
			else :
				acceleration[0] = (Trac_force + (0.5*1.184*velocity[0]*velocity[0]*0.9*9.61) - mass*0.98*(math.sin(pitch)))/mass
			#print ("akselerasi"+str(acceleration[0]))	
			
			#Perhitungan kecepatan dan posisi
			velocity[0] = velocity[0] + (Ts)*(acceleration[0]+acceleration[1])/2
			velocity[0] = my_limiter(velocity[0], 27.78, -27.78)
			if ((velocity[0] == 27.78) or (velocity[0] == -27.78)) :
				acceleration[0] = 0.0
		#	print ("kecepatan"+str(velocity[0])+"\n")
			
			position = position + (Ts)*(velocity[0]+velocity[1])/2
			velocity[1] = velocity[0]
			acceleration[1] = acceleration[0]
			#file1.write(str(acceleration[0])+'\t'+ str(velocity[0])+'\t'+str(Trac_force)+'\t'+str((abs(Trac_force)*abs(velocity[0])))+'\t'+str(((N*N*0.01625) * max_power))+'\n')			
			count = count+1
			

			#Motion Cueing
			in_surge = acceleration[0]
			in_pitch = pitch
			in_roll = 0
			in_sway = 0

			
			#******Translational channel******
			#Scale and Limit, ubah in_asway dan in_asurge menjadi in22_sway dan in22_sway
			in22_surge = in_surge*1
			in22_sway = in_sway*1
				
			if in22_sway<-1.3 :
				in22_sway = -1.3
			elif in22_sway>1.3 :
				in22_sway = 1.3
			else :
				in22_sway = in22_sway
			
			if in22_surge<-1.8 :
				in22_surge = -1.8
			elif in22_surge>1.8 :
				in22_surge = 1.8
			else :
				in22_surge = in22_surge
			
			#Filter highpass W22
			#Metode biliner : out22_surge = -(-0.960580095921472)*out22_surge_3 - 2.92110855188490*out22_surge_2 - (-2.96052837624337)*out22_surge_1 +  (-0.980277128006217)*in22_surge_3 + 2.94083138401865*in22_surge_2 + (-2.94083138401865)*in22_surge_1 + (0.980277128006217)*in22_surge
			#Metode butter : out22_surge = -0.903102267248853*out22_surge_4 -(-3.70444311831844)*out22_surge_3 - 5.69943427173562*out22_surge_2 - (-3.89809122104887)*out22_surge_1 + 0.950316929896987*in22_surge_4+ (-3.80126771958795)*in22_surge_3 + 5.70190157938192*in22_surge_2 + (-3.80126771958795)*in22_surge_1 + (0.950316929896987)*in22_surge
			#Metode bilinier 20 rad/s : out22_surge = -0.949078714507875*out22_surge_4 -(-3.84591570088674)*out22_surge_3 - 5.84457504630847*out22_surge_2 - (-3.94773790403574)*out22_surge_1 +0.974206710358677*in22_surge_4+ (-3.89682684143471)*in22_surge_3 + 5.84524026215206*in22_surge_2 + (-3.89682684143471)*in22_surge_1 + (0.974206710358677)*in22_surge
			#Metode butter 10 ms : out22_surge = -0.592354664504642*out22_surge_4 -(-2.67875163325157)*out22_surge_3 - 4.56543574113814*out22_surge_2 - (-3.47779077111533)*out22_surge_1 +0.769645800625606*in22_surge_4+ (-3.07858320250242)*in22_surge_3 + 4.61787480375363*in22_surge_2 + (-3.07858320250242)*in22_surge_1 + (0.769645800625606)*in22_surge
			#Metode butter 36 ms :
			out22_surge = -0.144993530748619*out22_surge_4 -(-0.849445567682487)*out22_surge_3 - 1.96176693814036*out22_surge_2 - (-2.13504958640504)*out22_surge_1 +0.380703476436032*in22_surge_4+ (-1.52281390574413)*in22_surge_3 + 2.28422085861619*in22_surge_2 + (-1.52281390574413)*in22_surge_1 + (0.380703476436032)*in22_surge
			in22_surge_4 = in22_surge_3
			in22_surge_3 = in22_surge_2
			in22_surge_2 = in22_surge_1
			in22_surge_1 = in22_surge
			out22_surge_4 = out22_surge_3
			out22_surge_3 = out22_surge_2
			out22_surge_2 = out22_surge_1
			out22_surge_1 = out22_surge
			
			#Metode bilinier out22_sway = -(-0.978034598453367)*out22_sway_3 - 2.95605489488688*out22_sway_2 - (-2.97802029582270)*out22_sway_1 +  (-0.989013723645370)*in22_sway_3 + 2.96704117093611*in22_sway_2 + (-2.96704117093611)*in22_sway_1 + 0.989013723645368*in22_sway
			#Metode butter : out22_sway = -0.903102267248853*out22_sway_4 -(-3.70444311831844)*out22_sway_3 - 5.69943427173562*out22_sway_2 - (-3.89809122104887)*out22_sway_1 + 0.950316929896987*in22_sway_4 + (-3.80126771958795)*in22_sway_3 + 5.70190157938192*in22_sway_2 + (-3.80126771958795)*in22_sway_1 + 0.950316929896987*in22_sway
			#Metode bilinier 20 rad/s out22_sway = -0.592354664504642*out22_sway_4 -(-2.67875163325157)*out22_sway_3 - 4.56543574113814*out22_sway_2 - (-3.47779077111533)*out22_sway_1 + 0.769645800625606*in22_sway_4 + (-3.07858320250242)*in22_sway_3 + 4.61787480375363*in22_sway_2 + (-3.07858320250242)*in22_sway_1 + 0.769645800625606*in22_sway
			#Metode butter 36 ms
			out22_sway = -0.144993530748619*out22_sway_4 -(-0.849445567682487)*out22_sway_3 - 1.96176693814036*out22_sway_2 - (-2.13504958640504)*out22_sway_1 + 0.380703476436032*in22_sway_4 + (-1.52281390574413)*in22_sway_3 + 2.28422085861619*in22_sway_2 + (-1.52281390574413)*in22_sway_1 + 0.380703476436032*in22_sway
			in22_sway_4 = in22_sway_3
			in22_sway_3 = in22_sway_2
			in22_sway_2 = in22_sway_1
			in22_sway_1 = in22_sway
			out22_sway_4 = out22_sway_3
			out22_sway_3 = out22_sway_2
			out22_sway_2 = out22_sway_1
			out22_sway_1 = out22_sway
			
			#integrator menjadi kecepatan simulator
			v_surge = v_surge + (Ts)*(out22_surge+out22_surge_1)/2
			v_sway = v_sway + + (Ts)*(out22_sway+out22_sway_1)/2
			
			#integrator menjadi posisi simulator
			pos_surge = pos_surge + (Ts)*(v_surge+v_surge_1)/2
			pos_sway = pos_sway + (Ts)*(v_sway+v_sway_1)/2
			
			#update nilai kecepatan
			v_surge_1 = v_surge
			v_sway_1 = v_sway
			
			#******Coordination channel******
			#Scale and Limit
			in12_surge = in_surge*0.9
			in12_sway = in_sway*0.9
			
			#Penambahan efek belokan
			left_turn = right_turn = 0
			
			#if 3000 <= count <= 6000 :
				# left_turn = 1
	
				
			if (left_turn==1) :
				in12_sway = in12_sway - (velocity[0]*velocity[0]*5000)
			elif (left_turn==2) :
				in12_sway = in12_sway - (velocity[0]*velocity[0]*1000)
			elif (left_turn==3) :
				in12_sway = in12_sway - (velocity[0]*velocity[0]*500)
			elif (left_turn==4) :
				in12_sway = in12_sway - (velocity[0]*velocity[0]*400)
			elif (right_turn==1) :
				in12_sway = in12_sway + (velocity[0]*velocity[0]*5000)
			elif (right_turn==2) :
				in12_sway = in12_sway + (velocity[0]*velocity[0]*1000)
			elif (right_turn==3) :
				in12_sway = in12_sway + (velocity[0]*velocity[0]*500)
			elif (right_turn==4) :
				in12_sway = in12_sway + (velocity[0]*velocity[0]*400)
			else :
				in12_sway = in12_sway
			
			if in12_sway<-10 :
				in12_sway = -10
			elif in12_sway>10 :
				in12_sway = 10
			else :
				in12_sway = in12_sway
			
			if in12_surge<-10 :
				in12_surge = -10
			elif in12_surge>10 :
				in12_surge = 10
			else :
				in12_surge = in12_surge
			
			#Filter lowpass W12
			#Metode butter : out12_surge = -0.752804997893585*out12_surge_4 -(-3.22480441374259)*out12_surge_3 - 5.18840245279824*out12_surge_2 - (-3.71628187421257)*out12_surge_1 + 7.57267104144893e-06*in12_surge_4 + 3.02906841657957e-05*in12_surge_3 + 4.54360262486936e-05*in12_surge_2 + 3.02906841657957e-05*in12_surge_1 + 7.57267104144893e-06*in12_surge
			#Metode biliner : out12_surge = -0.999608555186179*out12_surge_2 - (-1.99472627971748)*out12_surge_1 + 0.00122056886717570*in12_surge_2 +0.00244113773435140*in12_surge_1 + 0.00122056886717570*in12_surge
			#metode butter 20 Hz out12_surge = -0.592354664504640*out12_surge_4 -(-2.67875163325157)*out12_surge_3 - 4.56543574113813*out12_surge_2 - (-3.47779077111533)*out12_surge_1 + 7.80000797422770e-05*in12_surge_4 + 0.000312000318969108*in12_surge_3 + 0.000468000478453662*in12_surge_2 + 0.000312000318969108*in12_surge_1 + 7.80000797422770e-05*in12_surge
			#metode butter 36 ms
			out12_surge = -0.145014752693752*out12_surge_4 -(-0.849551302857080)*out12_surge_3 - 1.96195423929353*out12_surge_2 - (-2.13518185567314)*out12_surge_1 + 0.00763973959106680*in12_surge_4 + 0.0305589583642672*in12_surge_3 + 0.0458384375464008*in12_surge_2 + 0.0305589583642672*in12_surge_1 + 0.00763973959106680*in12_surge
			out12_surge_4 = out12_surge_3
			out12_surge_3 = out12_surge_2
			out12_surge_2 = out12_surge_1
			out12_surge_1 = out12_surge
			in12_surge_4 = in12_surge_3
			in12_surge_3 = in12_surge_2
			in12_surge_2 = in12_surge_1
			in12_surge_1 = in12_surge
			
			#Metode butter out12_sway = -0.716643737543780*out12_sway_4 -(-3.10507663902639)*out12_sway_3 - 5.05585341868038*out12_sway_2 - (-3.66719629364101)*out12_sway_1 + 1.40139722980132e-05*in12_sway_4 + 5.60558891920526e-05*in12_sway_3 + 8.40838337880789e-05*in12_sway_2 + 5.60558891920526e-05*in12_sway_1 + 1.40139722980132e-05*in12_sway
			#Metode bilinier : out12_sway = - 0.984921636858626*out12_sway_2 - (-1.97816694867345)*out12_sway_1 + 0.00168867204629486*in12_sway_2 + 0.00337734409259083*in12_sway_1 + 0.00168867204629519*in12_sway
			#Netode butter 10 ms : out12_sway = -0.592354664504640*out12_sway_4 -(-2.67875163325157)*out12_sway_3 - 4.56543574113813*out12_sway_2 - (-3.47779077111533)*out12_sway_1 + 7.80000797422770e-05*in12_sway_4 + 0.000312000318969108*in12_sway_3 + 0.000468000478453662*in12_sway_2 +0.000312000318969108*in12_sway_1 + 7.80000797422770e-05*in12_sway
			#Metode butter 36 ms
			out12_sway = -0.145014752693752*out12_sway_4 -(-0.849551302857080)*out12_sway_3 - 1.96195423929353*out12_sway_2 - (-2.13518185567314)*out12_sway_1 + 0.00763973959106680*in12_sway_4 + 0.0305589583642672*in12_sway_3 + 0.0458384375464008*in12_sway_2 + 0.0305589583642672*in12_sway_1 + 0.00763973959106680*in12_sway
			out12_sway_4 = out12_sway_3
			out12_sway_3 = out12_sway_2
			out12_sway_2 = out12_sway_1
			out12_sway_1 = out12_sway
			in12_sway_4 = in12_sway_3
			in12_sway_3 = in12_sway_2
			in12_sway_2 = in12_sway_1
			in12_sway_1 = in12_sway
			
			
			#Ubah agar menjadi rotasi dengan menggunakan arcsin(a/g) -------- Penggunaan fungsi asin() pada pyton harus dalam bentuk radian ---------
			if (out12_sway>1) :
				out12_roll = 1.57
			else :
				if (out12_sway<-1) :
					out12_roll = -1.57
				else :
					out12_roll = math.asin(out12_sway/9.8)
			
			if (out12_surge>1) :
				out12_pitch = 1.57
			else :
				if (out12_surge<-1) :
					out12_pitch = -1.57
				else :
					out12_pitch = math.asin(out12_surge/9.8)
				
			#Rate Limiter
			rate_roll = (out12_roll-out_roll_coor)/(Ts)
			rate_pitch = (out12_pitch-out_pitch_coor)/(Ts)
			
			if rate_roll>rate_limit_up :
				out_roll_coor = (Ts)*rate_limit_up + out_roll_coor
			elif rate_roll<rate_limit_down :
				out_roll_coor = (Ts)*rate_limit_down + out_roll_coor
			else :
				out_roll_coor = out12_roll
			
			if rate_pitch>rate_limit_up :
				out_pitch_coor = (Ts)*rate_limit_up + out_pitch_coor
			elif rate_pitch<rate_limit_down :
				out_pitch_coor = (Ts)*rate_limit_down + out_pitch_coor
			else :
				out_pitch_coor = out12_pitch
			
			#******Rotational channel******
			#Scale and Limit
			if in_roll<-0.2 :
				in11_roll = -0.2
			elif in_roll>0.2 :
				in11_roll = 0.2
			else :
				in11_roll = in_roll
			
			if in_pitch<-1 :
				in11_pitch = -1
			elif in_pitch>1 :
				in11_pitch = 1
			else :
				in11_pitch = in_pitch
			
			#Filter lowpass W11	
			#Metode butter : out11_pitch = -0.910211320832731*out11_pitch_4 -(-3.72646892562956)*out11_pitch_3 - 5.72218913832976*out11_pitch_2 - (-3.90592993040290)*out11_pitch_1 + 1.00195626746846e-07*in11_pitch_4 + (4.00782506987385e-07)*in11_pitch_3 + 6.01173760481077e-07*in11_pitch_2 + (4.00782506987385e-07)*in11_pitch_1 + 1.00195626746846e-07*in11_pitch
			#Metode bilinier : out11_pitch = - (-0.965557342137982)*out11_pitch_1 + (0.0172213289310090)*in11_pitch_1 + 0.0172213289310090*in11_pitch
			#Metode butter 10 ms out11_pitch = -0.624309524597209*out11_pitch_4 -(-2.79070006755009)*out11_pitch_3 - 4.69717049318745*out11_pitch_2 - (-3.52994147688130)*out11_pitch_1 + 5.24045845791965e-05*in11_pitch_4 + (0.000209618338316786)*in11_pitch_3 + 0.000314427507475179*in11_pitch_2 + (0.000209618338316786)*in11_pitch_1 + 5.24045845791965e-05*in11_pitch
			#Metode butter 36 ms
			out11_pitch = -0.177437034697608*out11_pitch_4 -(-1.00752178167038)*out11_pitch_3 - 2.23500049743655*out11_pitch_2 - (-2.31921994719526)*out11_pitch_1 + 0.00535598770428241*in11_pitch_4 + (0.0214239508171296)*in11_pitch_3 + 0.0321359262256945*in11_pitch_2 + (0.0214239508171296)*in11_pitch_1 + 0.00535598770428241*in11_pitch
			out11_pitch_4 = out11_pitch_3
			out11_pitch_3 = out11_pitch_2
			out11_pitch_2 = out11_pitch_1
			out11_pitch_1 = out11_pitch
			in11_pitch_4 = in11_pitch_3
			in11_pitch_3 = in11_pitch_2
			in11_pitch_2 = in11_pitch_1
			in11_pitch_1 = in11_pitch
			
			#Metode butter :
			#out11_roll = -0.790353945979528*out11_roll_4 -(-3.34726193634964)*out11_roll_3 - 5.32182353393364*out11_roll_2 - (-3.76485705728338)*out11_roll_1 + 3.65539250921088e-06*in11_roll_4 + (1.46215700368435e-05)*in11_roll_3 + 2.19323550552653e-05*in11_roll_2 + (1.46215700368435e-05)*in11_roll_1 + 3.65539250921088e-06*in11_roll
			#out11_roll = -(-0.835219367028832)*out11_roll_3 - 2.65594728274520*out11_roll_2 - (-2.82006032902489)*out11_roll_1 + 8.34483364351990e-05*in11_roll_3 + (0.000250345009305597)*in11_roll_2 + 0.000250345009305597*in11_roll_1 + (8.34483364351990e-05)*in11_roll
			#Metode bilinier : out11_roll = - (-0.915370503524090)*out11_roll_1 + (0.0423147482379549)*in11_roll_1 + 0.0423147482379549*in11_roll
			#Metode butter 10 ms : out11_roll = -0.304904941514000*out11_roll_4 -(-1.57676238600480)*out11_roll_3 - 3.12465607675697*out11_roll_2 - (-2.82855504855157)*out11_roll_1 + 0.00151522398216295*in11_roll_4 + (0.00606089592865182)*in11_roll_3 + 0.00909134389297773*in11_roll_2 + (0.00606089592865182)*in11_roll_1 + 0.00151522398216295*in11_roll
			#Metode butter 36 ms
			out11_roll = -0.0179526472148710*out11_roll_4 -(0.0256563080856837)*out11_roll_3 - 0.490733981575289*out11_roll_2 - (0.122003773226983)*out11_roll_1 + 0.103521669381427*in11_roll_4 + (0.414086677525707)*in11_roll_3 + 0.621130016288560*in11_roll_2 + (0.414086677525707)*in11_roll_1 + 0.103521669381427*in11_roll
			out11_roll_4 = out11_roll_3
			out11_roll_3 = out11_roll_2
			out11_roll_2 = out11_roll_1
			out11_roll_1 = out11_roll
			in11_roll_4 = in11_roll_3
			in11_roll_3 = in11_roll_2
			in11_roll_2 = in11_roll_1
			in11_roll_1 = in11_roll
			
			#Perhitungan sudut roll dan pitch simulator (penjumlahan dari rotational dan coordination channel)
			out_roll = out_roll_coor + out11_roll
			out_pitch = out_pitch_coor + out11_pitch
			
			#Proses penulisan file
			#file.write(str(out22_surge) + '\t' + str(out22_sway) + '\t' + str(v_surge) + '\t' + str(out11_pitch) + '\t' + str(pos_surge) + '\t' + str(pos_sway) + '\t' + str(out_roll) + '\t' + str(out_pitch) + '\t' + str(in_sway)+ '\t' + str(in_roll)+ '\t' + str(out_roll_coor)+ '\t' + str(out11_roll)+ '\t' + str(out_pitch_coor)+ '\t' + str(out11_pitch)  +'\n')
			#time.sleep(2.37)
			#print ("%s milisecond " %((time.time()-start_time)*1000))
		
			roll_m.value = -1 * out_roll
			pitch_m.value = -1 * out_pitch
			surge_m.value = pos_surge
			sway_m.value = pos_sway
			#file1.write(str(pitch_m.value)+'\t'+ str(surge_m.value)+'\n') #print(time.time()-t)
			print (time.time()-time_now)
		
def motor1 (pitch_m,roll_m) :
	client2= ModbusClient(method = "ascii", port="COM10",timeout=0.002, stopbits = 1, bytesize = 8, parity = 'N', baudrate = 115200)
	servo = "ServoOn" #Perintah mengaktifkan Servo
	if (servo == "ServoOn"):
		path5value = (0x0011, 0x0000) #Perintrol register aktif untuk kontrol Input
		speedpath6 = client2.write_registers(0x0216, path5value, unit = 0x007f)
	
		valueservo = (0x0001, 0x0000) #Perintah register servo On
		setservo = client2.write_registers(0x0214, valueservo, unit = 0x007f)
	else :
		path5value = (0x0111, 0x0000) #perintah register non-aktif untuk kontrol input
		valueservo = (0x0101, 0x0000) #perintah non-aktif servo (Servo off)
	
		speedpath6 = client2.write_registers(0x0216, path5value, unit = 0x007f)
		setservo = client2.write_registers(0x0214, valueservo, unit = 0x007f)

	def split (num) :
		if (num < 0) :
			temp = abs(num)
			temp = temp^0xFFFFFFFF
			temp = temp+1
		else :
			temp = num
		return ( temp & 0xFFFF, temp >> 16)
    
	while True :
		time_now = time.time()
		angle_puu = int((pitch_m.value - roll_m.value) * 100000 * 60 * 4/ (2*3.14))
		# print(angle)
		angle_hex = split(angle_puu) 
		# print(angle_puu)
		# print (angle_hex)
		value = (0x0012, 0x0004)
		anglepath1 = client2.write_registers(0x0606, angle_hex, unit = 0x007f)
		anglepath2 = client2.write_registers(0x0604, value, unit = 0x007f)
		startpath = client2.write_registers(0x050e, split(1), unit = 0x007f)
		#print "motor1 = " + str( time.time()-time_now)

def motor2 (pitch_m,roll_m) :
	client2= ModbusClient(method = "ascii", port="COM8",timeout=0.002, stopbits = 1, bytesize = 8, parity = 'N', baudrate = 115200)
	servo = "ServoOn" #Perintah mengaktifkan Servo
    
	if (servo == "ServoOn"):
		path5value = (0x0011, 0x0000) #Perintrol register aktif untuk kontrol Input
		speedpath6 = client2.write_registers(0x0216, path5value, unit = 0x007f)
	
		valueservo = (0x0001, 0x0000) #Perintah register servo On
		setservo = client2.write_registers(0x0214, valueservo, unit = 0x007f)

	else :
		path5value = (0x0111, 0x0000) #perintah register non-aktif untuk kontrol input
		valueservo = (0x0101, 0x0000) #perintah non-aktif servo (Servo off)
	
		speedpath6 = client2.write_registers(0x0216, path5value, unit = 0x007f)
		setservo = client2.write_registers(0x0214, valueservo, unit = 0x007f)

	def split (num) :
		if (num < 0) :
			temp = abs(num)
			temp = temp^0xFFFFFFFF
			temp = temp+1
		else :
			temp = num
		return ( temp & 0xFFFF, temp >> 16)
    
	while True :
		time_now = time.time()
		angle_puu = int((pitch_m.value + roll_m.value) * 100000 * 60 * 4 / (2*3.14))
		# print(angle)
		angle_hex = split(angle_puu) 
		# print(angle_puu)
		# print (angle_hex)
		value = (0x0012, 0x0004)
		anglepath1 = client2.write_registers(0x0606, angle_hex, unit = 0x007f)
		anglepath2 = client2.write_registers(0x0604, value, unit = 0x007f)
		startpath = client2.write_registers(0x050e, split(1), unit = 0x007f)
		#print "motor2 = " + str( time.time()-time_now)

def motor3 (surge_m) :
	client2= ModbusClient(method = "ascii", port="COM11",timeout=0.002, stopbits = 1, bytesize = 8, parity = 'N', baudrate = 115200)
	servo = "ServoOn" #Perintah mengaktifkan Servo
    
	if (servo == "ServoOn"):
		path5value = (0x0011, 0x0000) #Perintrol register aktif untuk kontrol Input
		speedpath6 = client2.write_registers(0x0216, path5value, unit = 0x007f)
	
		valueservo = (0x0001, 0x0000) #Perintah register servo On
		setservo = client2.write_registers(0x0214, valueservo, unit = 0x007f)

	else :
		path5value = (0x0111, 0x0000) #perintah register non-aktif untuk kontrol input
		valueservo = (0x0101, 0x0000) #perintah non-aktif servo (Servo off)
	
		speedpath6 = client2.write_registers(0x0216, path5value, unit = 0x007f)
		setservo = client2.write_registers(0x0214, valueservo, unit = 0x007f)

	def split (num) :
		if (num < 0) :
			temp = abs(num)
			temp = temp^0xFFFFFFFF
			temp = temp+1
		else :
			temp = num
		return ( temp & 0xFFFF, temp >> 16)
    
	while True :
		time_now = time.time()
		angle_puu = int(surge_m.value * 100000 * 120   / (2*3.14))
		# print(angle)
		angle_hex = split(angle_puu) 
		# print(angle_puu)
		# print (angle_hex)
		value = (0x0012, 0x0007)
		anglepath1 = client2.write_registers(0x0606, angle_hex, unit = 0x007f)
		anglepath2 = client2.write_registers(0x0604, value, unit = 0x007f)
		startpath = client2.write_registers(0x050e, split(1), unit = 0x007f)
		#print "motor3s = " + str( time.time()-time_now)

if __name__ == "__main__": #Menjalankan semua Threading 
		
	roll_m = MP.Value ('d',0.0)
	pitch_m = MP.Value ('d',0.0)
	surge_m = MP.Value ('d',0.0)
	sway_m = MP.Value ('d',0.0) 
	
	
	P1 = MP.Process (target = dinamika_MC, args = (pitch_m,roll_m,surge_m,sway_m))
	P3 = MP.Process (target = motor1, args = (pitch_m,roll_m))
	P4 = MP.Process (target = motor2, args = (pitch_m,roll_m))
	P5 = MP.Process (target = motor3, args = (surge_m,))
	
	
	P1.start()
	P3.start()
	P4.start()
	P5.start()
	
	P1.join()
	P3.join()
	P4.join()
	P5.join()
		
#Inisialisasi semua variabel x dan y agar 0
#Loop selama menerima input x