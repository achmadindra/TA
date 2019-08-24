#!/usr/bin/env python
import pika
import sys
import threading 
import time 

def RMQ () :
	
	credentials = pika.PlainCredentials('kantu','dopple21')
	parameters = pika.ConnectionParameters('167.205.66.21',5672,'/',credentials)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()

	channel.exchange_declare(exchange='Simulator_Kereta',
							 exchange_type='direct')
							 
	channel.queue_declare(queue='data_Traksi')
	channel.queue_declare(queue='data_Kecepatan')
	channel.queue_declare(queue='data_Percepatan')
	channel.queue_declare(queue='data_sudutRoll')
	channel.queue_declare(queue='data_sudutPitch')


	channel.queue_bind(exchange='Simulator_Kereta',
					   queue='data_Traksi',
					   routing_key='traksi')
					   
	channel.queue_bind(exchange='Simulator_Kereta',
					   queue='data_Kecepatan',
					   routing_key='kecepatan')

	channel.queue_bind(exchange='Simulator_Kereta',
					   queue='data_Percepatan',
					   routing_key='percepatan')
	
	channel.queue_bind(exchange='Simulator_Kereta',
					   queue='data_sudutRoll',
					   routing_key='roll')
	
	channel.queue_bind(exchange='Simulator_Kereta',
					   queue='data_sudutPitch',
					   routing_key='pitch')
					   
	kf=0.02
	max_traction=700000.0
	max_power=500000.0
	
	traction = 0.0
	velocity = 0.0
	
	while True :
		N = N_g
		if (traction*velocity) <= (N*N/64) * max_power :
			traction = ((N*0.125)*max_traction) - (kf*velocity)
		else :
			traction = (N*N*0.01625) * max_power / velocity
			
		if (N < 0) :
			traction = -1 * traction;
		
		method_frame, header_frame, body = channel.basic_get('data_Kecepatan')
		if method_frame:
			velocity = float(body)
			print velocity
			channel.basic_ack(method_frame.delivery_tag)
		
		channel.basic_publish(exchange='Simulator_Kereta',
							routing_key='traksi',
							body=str(traction) )
		
		
		
	connection.close()


def input2() :
	global N_g
	N_g = 1.0
	while True :
		x = input("Gaya traksi?")
		N_g = x
		

	
if __name__ == "__main__": #Menjalankan semua Threading 
		
	P1 = threading.Thread(target = RMQ, args = ())
	P3 = threading.Thread(target = input2, args = ())
	
	P1.start()
	P3.start()
	
	P1.join()
	P3.join()