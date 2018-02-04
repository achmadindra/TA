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
def filter11_pitch(x, koef):
	
	
	
	return x
	

#inisialisasi variabel penyimpan nilai output dan input dari filter
#variabel x_a menunjukkan x[n-a] untuk n adalah sampling ke-n
in22_surge = 0.0
in22_surge_1 = 0.0
in22_surge_2 = 0.0
in22_surge_3 = 0.0

out22_surge = 0.0
out22_surge_1 = 0.0
out22_surge_2 = 0.0
out22_surge_3 = 0.0

in22_sway = 0.0
in22_sway_1 = 0.0
in22_sway_2 = 0.0
in22_sway_3 = 0.0

out22_sway = 0.0
out22_sway_1 = 0.0
out22_sway_2 = 0.0
out22_sway_3 = 0.0

in12_surge = 0.0
out12_surge = 0.0
out12_surge_1 = 0.0
out12_surge_2 = 0.0

in12_sway = 0.0
out12_sway = 0.0
out12_sway_1 = 0.0
out12_sway_2 = 0.0

in11_roll = 0.0
out11_roll = 0.0
out11_roll_1 = 0.0

in11_pitch = 0.0
out11_pitch = 0.0
out11_pitch_1 = 0.0

i = 1 #Variabel pointer dari file
file = open('track_data.txt','w') #Membuka file external yang berisi data track kereta api 

#Motion Cueing
while True:

	#******Baca data percepatan dan lokasi kereta dari Rabbit MQ******
	in_asway #input Percepatan  sway
	in_asurge #input Percepatan surge
	
	
	#******Baca data, harus perhatikan posisi!!!*******
	line = file.readline(i)
	data_track = line.split
	in_pitch = float(data_track[0]) #input sudut pitch
	in_roll = float(data_track[1]) #input sudut roll
	
	#******Translational channel******
	#Scale and Limit, ubah in_asway dan in_asurge menjadi in22_sway dan in22_sway
	in22_sway =
	in22_surge = 
	
	#Filter highpass W22
	out22_surge = -*out22_surge_3 - *out22_surge_2 - out22_surge_1 +  in22_surge_3 + *in22_surge_2 + in22_surge_1 + in22_surge
	in22_surge_3 = in22_surge_2
	in22_surge_2 = in22_surge_1
	in22_surge_1 = in22_surge
	out22_surge_3 = out22_surge_2
	out22_surge_2 = out22_surge_1
	out22_surge_1 = out22_surge
	
	out22_sway = -*out22_sway_3 - *out22_sway_2 - out22_sway_1 +  in22_sway_3 + *in22_sway_2 + in22_sway_1 + in22_sway
	in22_sway_3 = in22_sway_2
	in22_sway_2 = in22_sway_1
	in22_sway_1 = in22_sway
	out22_sway_3 = out22_sway_2
	out22_sway_2 = out22_sway_1
	out22_sway_1 = out22_sway
	
	#integrator menjadi posisi simulator
	
	
	#******Coordination channel******
	#Scale and Limit
	in12_sway =
	in12_surge =
	
	#Filter lowpass W12
	out12_surge = out12_surge_2 - out12_surge_1 + in12_surge
	out12_surge_2 = out12_surge_1
	out12_surge_1 = out12_surge
	
	out12_sway = out12_sway_2 - out12_sway_1 + in12_sway
	out12_sway_2 = out12_sway_1
	out12_sway_1 = out12_sway
	
	#Ubah agar menjadi rotasi dengan menggunakan arcsin(a/g) -------- Penggunaan fungsi asin() pada pyton harus dalam bentuk radian ---------
	out12_roll = 
	out12_pitch =
	
	#******Rotational channel******
	#Scale and Limit
	
	#Filter highpass W11
	out11_surge = out11_surge_1 + in11_surge
	out11_surge_1 = out11_surge
	
	out11_sway = out11_sway_1 + in11_sway
	out11_sway_1 = out11_sway
	
	#Perlu integrator? input dari dinamika apa saja?
	
	#Perhitungan sudut roll dan pitch simulator (penjumlahan dari rotational (hasil integral?) dan coordination channel)
	out_roll = out12_roll +
	out_pitch = out12_pitch +
	
	
	
	i = i+1
	
file.close()