#Koefisien-Koefisien Filter
#a11_pitch = []
#b11_pitch = []
#a12_pitch = []
#b12_pitch = []
#a22_pitch = []
#b22_pitch = []

#a11_pitch = []
#b11_pitch = []
#a12_pitch = []
#b12_pitch = []
#a22_pitch = []
#b22_pitch = []

#Filter11 untuk pitch dan surge
#def filter11_pitch(x, koef):
	
	
	
#return x
	

#inisialisasi variabel penyimpan nilai output dan input dari filter
#variabel x_a menunjukkan x[n-a] untuk n adalah sampling ke-n
import math

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
file = open('track_data.txt','w') #Membuka file external yang berisi data track kereta api 

#Motion Cueing
for x in range(0, 10000) :

	in_surge = in_sway = 10
	# in12_surge = in12_sway = 
	in_pitch = in_roll = 0.25
	
	# #******Baca data percepatan dan lokasi kereta dari Rabbit MQ******
	# in_asway #input Percepatan  sway
	# in_asurge #input Percepatan surge
	
	
	# #******Baca data, harus perhatikan posisi!!!*******
	# line = file.readline(i)
	# data_track = line.split
	# in_pitch = float(data_track[0]) #input sudut pitch
	# in_roll = float(data_track[1]) #input sudut roll
	
	#******Translational channel******
	#Scale and Limit, ubah in_asway dan in_asurge menjadi in22_sway dan in22_sway
	in_surge = in_surge*0.45
	in_sway = in_sway*0.35
	
	if in_sway<-1.3 :
		in22_sway = -1.3
	elif in_sway>1.3 :
		in22_sway = 1.3
	else :
		in22_sway = in_sway
	
	if in_surge<-1.8 :
		in22_surge = -1.8
	elif in_surge>1.8 :
		in22_surge = 1.8
	else :
		in22_surge = in_surge
	
	#Filter highpass W22
	out22_surge = -(-0.960580095921472)*out22_surge_3 - 2.92110855188490*out22_surge_2 - (-2.96052837624337)*out22_surge_1 +  (-0.980277128006217)*in22_surge_3 + 2.94083138401865*in22_surge_2 + (-2.94083138401865)*in22_surge_1 + (0.980277128006217)*in22_surge
	in22_surge_4 = in22_surge_3
	in22_surge_3 = in22_surge_2
	in22_surge_2 = in22_surge_1
	in22_surge_1 = in22_surge
	out22_surge_4 = out22_surge_3
	out22_surge_3 = out22_surge_2
	out22_surge_2 = out22_surge_1
	out22_surge_1 = out22_surge
	
	out22_sway = -(-0.978034598453367)*out22_sway_3 - 2.95605489488688*out22_sway_2 - (-2.97802029582270)*out22_sway_1 +  (-0.989013723645370)*in22_sway_3 + 2.96704117093611*in22_sway_2 + (-2.96704117093611)*in22_sway_1 + 0.989013723645368*in22_sway
	in22_sway_4 = in22_sway_3
	in22_sway_3 = in22_sway_2
	in22_sway_2 = in22_sway_1
	in22_sway_1 = in22_sway
	out22_sway_4 = out22_sway_3
	out22_sway_3 = out22_sway_2
	out22_sway_2 = out22_sway_1
	out22_sway_1 = out22_sway
	
	#integrator menjadi kecepatan simulator
	v_surge = v_surge + (0.002)*(out22_surge+out22_surge_1)/2
	v_sway = v_sway + + (0.002)*(out22_sway+out22_sway_1)/2
	
	#integrator menjadi posisi simulator
	pos_surge = pos_surge + (0.002)*(v_surge+v_surge_1)/2
	pos_sway = pos_sway + (0.002)*(v_sway+v_sway_1)/2
	
	#update nilai kecepatan
	v_surge_1 = v_surge
	v_sway_1 = v_sway
	
	#******Coordination channel******
	#Scale and Limit
	in_surge = in_surge*0.3
	in_sway = in_sway*0.2
	
	if in_sway<-0.5 :
		in12_sway = -0.5
	elif in_sway>0.8 :
		in12_sway = 0.8
	else :
		in12_sway = in_sway
	
	if in_surge<-1.2 :
		in12_surge = -1.2
	elif in_surge>1.2 :
		in12_surge = 1.2
	else :
		in12_surge = in_surge
	
	#Filter lowpass W12
	out12_surge = -0.752804997893585*out12_surge_4 -(-3.22480441374259)*out12_surge_3 - 5.18840245279824*out12_surge_2 - (-3.71628187421257)*out12_surge_1 + 7.57267104144893e-06*in12_surge_4 + 3.02906841657957e-05*in12_surge_3 + 4.54360262486936e-05*in12_surge_2 + 3.02906841657957e-05*in12_surge_1 + 7.57267104144893e-06*in12_surge
	out12_surge_4 = out12_surge_3
	out12_surge_3 = out12_surge_2
	out12_surge_2 = out12_surge_1
	out12_surge_1 = out12_surge
	in12_surge_4 = in12_surge_3
	in12_surge_3 = in12_surge_2
	in12_surge_2 = in12_surge_1
	in12_surge_1 = in12_surge
	
	out12_sway = -0.716643737543780*out12_sway_4 -(-3.10507663902639)*out12_sway_3 - 5.05585341868038*out12_sway_2 - (-3.66719629364101)*out12_sway_1 + 1.40139722980132e-05*in12_sway_4 + 5.60558891920526e-05*in12_sway_3 + 8.40838337880789e-05*in12_sway_2 + 5.60558891920526e-05*in12_sway_1 + 1.40139722980132e-05*in12_sway
	out12_sway_4 = out12_sway_3
	out12_sway_3 = out12_sway_2
	out12_sway_2 = out12_sway_1
	out12_sway_1 = out12_sway
	in12_sway_4 = in12_sway_3
	in12_sway_3 = in12_sway_2
	in12_sway_2 = in12_sway_1
	in12_sway_1 = in12_sway
	
	#Ubah agar menjadi rotasi dengan menggunakan arcsin(a/g) -------- Penggunaan fungsi asin() pada pyton harus dalam bentuk radian ---------
	out12_roll = math.asin(out12_sway/9.8)
	out12_pitch = math.asin(out12_surge/9.8)
	
	#Rate Limiter
	rate_roll = (out12_roll-out_roll_coor)/(0.002)
	rate_pitch = (out12_pitch-out_roll_coor)/(0.002)
	
	if rate_roll>0.2 :
		out_roll_coor = (0.002)*0.2 + out_roll_coor
	elif rate_roll<-0.2 :
		out_roll_coor = (0.002)*(-0.2) + out_roll_coor
	else :
		out_roll_coor = out12_roll
	
	if rate_pitch>0.2 :
		out_pitch_coor = (0.002)*0.2 + out_pitch_coor
	elif rate_pitch<-0.2 :
		out_pitch_coor = (0.002)*(-0.2) + out_pitch_coor
	else :
		out_pitch_coor = out12_pitch
	
	#******Rotational channel******
	#Scale and Limit
	if in_roll<-0.2 :
		in22_roll = -0.2
	elif in_roll>0.2 :
		in22_roll = 0.2
	else :
		in22_roll = in_roll
	
	if in_pitch<-0.2 :
		in22_pitch = -0.2
	elif in_pitch>0.2 :
		in22_pitch = 0.2
	else :
		in22_pitch = in_pitch
	
	#Filter highpass W11
	out11_roll = -0.910211320832731*out11_roll_4 -(-3.72646892562956)*out11_roll_3 - 5.72218913832976*out11_roll_2 - (-3.90592993040290)*out11_roll_1 + 1.00195626746846e-07*in11_roll_4 + 4.00782506987385e-07*in11_roll_3 + 6.01173760481077e-07*in11_roll_2 + 4.00782506987385e-07*in11_roll_1 + 1.00195626746846e-07*in11_roll
	out11_roll_4 = out11_roll_3
	out11_roll_3 = out11_roll_2
	out11_roll_2 = out11_roll_1
	out11_roll_1 = out11_roll
	in11_roll_4 = in11_roll_3
	in11_roll_3 = in11_roll_2
	in11_roll_2 = in11_roll_1
	in11_roll_1 = in11_roll
	
	out11_pitch = -0.790353945979528*out11_pitch_4 -(-3.34726193634964)*out11_pitch_3 - 5.32182353393364*out11_pitch_2 - (-3.76485705728338)*out11_pitch_1 + 3.65539250921088e-06*in11_pitch_4 + 1.46215700368435e-05*in11_pitch_3 + 2.19323550552653e-05*in11_pitch_2 + 1.46215700368435e-05*in11_pitch_1 + 3.65539250921088e-06*in11_pitch
	out11_pitch_4 = out11_pitch_3
	out11_pitch_3 = out11_pitch_2
	out11_pitch_2 = out11_pitch_1
	out11_pitch_1 = out11_pitch
	in11_pitch_4 = in11_pitch_3
	in11_pitch_3 = in11_pitch_2
	in11_pitch_2 = in11_pitch_1
	in11_pitch_1 = in11_pitch
	
	#Perlu integrator? input dari dinamika apa saja?
	
	#Perhitungan sudut roll dan pitch simulator (penjumlahan dari rotational (hasil integral?) dan coordination channel)
	out_roll = out_roll_coor + out11_roll
	out_pitch = out_pitch_coor + out11_pitch
	
	#Proses penulisan file
	file.write(str(out22_surge) + '\t' + str(out22_sway) + '\t' + str(v_surge) + '\t' + str(v_sway) + '\t' + str(pos_surge) + '\t' + str(pos_sway) + '\t' + str(out_roll) + '\t' + str(out_pitch) +'\n')
	
file.close()