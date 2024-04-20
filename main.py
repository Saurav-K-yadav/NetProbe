import pandas as pd
import numpy as np
import os
import signal
import time
import getpass
import subprocess
from blockip import blockip
from collections import Counter
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense,Layer
from keras.layers import Attention, Input
import keras.backend as K
from tensorflow.keras.backend import squeeze,softmax,dot,expand_dims,tanh
from tensorflow.keras.backend import sum as sums
from keras.models import load_model

blockedips=set()

def run_shell_script(script_path):
    try:
        subprocess.run(["bash", script_path], check=True)
        print("Shell script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def format_3d(df):
    X = np.array(df)
    return np.reshape(X, (X.shape[0], X.shape[1], 1))

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

fields=['src_port', 'dst_port',
       'protocol','flow_duration', 'flow_byts_s', 'flow_pkts_s',
       'fwd_pkts_s', 'bwd_pkts_s', 'tot_fwd_pkts', 'tot_bwd_pkts',
       'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max',
       'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std',
       'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean',
       'bwd_pkt_len_std', 'pkt_len_max', 'pkt_len_min', 'pkt_len_mean',
       'pkt_len_std', 'pkt_len_var', 'fwd_header_len', 'bwd_header_len', 'flow_iat_mean',
       'flow_iat_max', 'flow_iat_min', 'flow_iat_std', 'fwd_iat_tot',
       'fwd_iat_max', 'fwd_iat_min', 'fwd_iat_mean', 'fwd_iat_std',
       'bwd_iat_tot', 'bwd_iat_max', 'bwd_iat_min', 'bwd_iat_mean',
       'bwd_iat_std', 'fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags',
       'bwd_urg_flags', 'fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt',
       'psh_flag_cnt', 'ack_flag_cnt', 'urg_flag_cnt', 'ece_flag_cnt',
       'down_up_ratio', 'pkt_size_avg', 'init_fwd_win_byts',
       'init_bwd_win_byts', 'active_max', 'active_min', 'active_mean',
       'active_std', 'idle_max', 'idle_min', 'idle_mean', 'idle_std',
       'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'bwd_byts_b_avg', 'bwd_pkts_b_avg',
       'fwd_blk_rate_avg', 'bwd_blk_rate_avg', 'fwd_seg_size_avg',
       'bwd_seg_size_avg', 'cwe_flag_count', 'subflow_fwd_pkts',
       'subflow_bwd_pkts', 'subflow_fwd_byts', 'subflow_bwd_byts']
labels = {
    '0': "Benign",
    '1': "Golden_eye",
    '2': "slow_http",
    '3': "vsi",
}

def detect_anomaly(csv_path, model):
    # Read data
    data = pd.read_csv(csv_path)
    source_ip = data['src_ip']
    data = data[fields]

    # Handle special values
    dataset = data.replace('Infinity', '0')
    dataset = dataset.replace(np.inf, '0')
    dataset['flow_pkts_s'] = pd.to_numeric(dataset['flow_pkts_s'])
    dataset['flow_byts_s'] = pd.to_numeric(dataset['flow_byts_s'].fillna(0))

    # Make predictions
    predictions = model.predict(format_3d(data))
    predictions = np.argmax(predictions, axis=1)
  
    # Count predictions
    label_counts = Counter(predictions)
    #print(label_counts)
    time.sleep(3)
    max_count = 0
    max_model=''
    for label, count in label_counts.items():
        tlabel = labels[str(label)]
        print(f"{tlabel}: {count}")
        if count > max_count:
            max_count = count
            max_model = tlabel

    print(f"Model with maximum predictions: {max_model} ({max_count} predictions)")

    # Store anomalies
    unique_ips = set()  # To store unique IPs
    anomalies = []
    if(max_model!='Benign'):
        for i in range(len(predictions)):
            if predictions[i] != "Benign" and labels[str(predictions[i])] == max_model:
                ip = source_ip[i]
                if ip not in unique_ips:  # Check if IP is already seen
                    unique_ips.add(ip)
                    anomalies.append((ip, labels[str(predictions[i])]))

    # Print the results
    print('Source IP | Anomaly')
    print('===================')
    for ip, anomaly in anomalies:
        blockedips.add(ip)
        print(f"{ip} | {anomaly}")
    blockip(blockedips)

def main():
	model = load_model('ModelvsiLstm.keras', custom_objects={'AttentionLayer': AttentionLayer})
	while(1):
		run_shell_script('./newscript.sh')
		time.sleep(5)
		while(os.path.getsize('test.csv') ==0):
			run_shell_script('./newscript.sh')
			time.sleep(5)
		detect_anomaly('test.csv', model)
		
		
if __name__=='__main__':
	main()

	
        
        
        
        
        
        
        
