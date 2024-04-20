from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense,Layer
from keras.layers import Attention, Input
import keras.backend as K
from tensorflow.keras.backend import squeeze,softmax,dot,expand_dims,tanh
from tensorflow.keras.backend import sum as sums
from collections import Counter
from keras .models import load_model
from GetData import load_file,format_3d,preprocess_dataset
import pandas as pd
import numpy as np

class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        et = squeeze(tanh(dot(x, self.W) + self.b), axis=-1)
        at = softmax(et)
        at = expand_dims(at, axis=-1)
        output = x * at
        return sums(output, axis=1)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])


def GraphPlot(hist):
    plt.plot(hist.history['accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(hist.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train'], loc='upper left')
    plt.show()
    print(model.metrics_names)


PACKET_THRESHOLD = 150

# Function to capture packets and write them to a pcap file
def capture_packets(packet_count):
    # Capture packets
    packets = sniff(count=packet_count)
    
    # Generate a unique file name for the pcap file based on the current timestamp
    file_name = "capture.pcap"
    
    # Write packets to a pcap file
    wrpcap(file_name, packets)
    
labels = {
    '0': "BENIGN",
    '1': "DrDoS_DNS",
    '2': "DrDoS_LDAP",
    '3': "DrDoS_MSSQL",
    '4': "DrDoS_NTP",
    '5': "DrDoS_NetBIOS",
    '6': "DrDoS_SNMP",
    '7': "DrDoS_SSDP",
    '8': "DrDoS_UDP",
    '9': "LDAP",
    '10': "MSSQL",
    '11': "NetBIOS",
    '12': "Portmap",
    '13': "Syn",
    '14': "UDP",
    '15': "UDP-lag",
    '16': "UDPLag",
    '17': "WebDDoS"
}

def __main__():
	#while(1):
		# Define the sudo password
		# sudo_password = ""
		# # Define the tcpdump command
		# command = "sudo -s tcpdump -c 50 -w capture.pcap"

		# Run the command using subprocess
		# process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		# stdout, stderr = process.communicate(input=(sudo_password + '\n').encode())
		#capture_packets(PACKET_THRESHOLD)
		# Check for any errors
		# if stderr:
		# 	print("Error:", stderr.decode())
		# else:
		# 	print("Command executed successfully.")	
		print("Command executed successfully.")	
		data_file_path = './flows.csv'
		model_file_path = 'transfer_model_saturday.keras'
		model = load_model(model_file_path,custom_objects={'AttentionLayer':AttentionLayer})
		data=load_file(data_file_path)
		data=preprocess_dataset(data)
		data=format_3d(data)
		print('Preprocessing Done')
		predictions=model.predict(data.astype(np.float32))
		print('prediction done Now couting labels')
		predicted_labels=[]
		for prediction in predictions:
			index=np.argmax(prediction)
			label=labels[str(index)]
			predicted_labels.append(label)
		label_counts=Counter(predicted_labels)
		for label,count in label_counts.items():
			print(f"{label}:{count}")
		#time.sleep(4)

if __name__=="__main__":
	__main__()
