import numpy as np
import pandas as pd
import os
from os import walk
from sklearn import preprocessing

PATH = '/home/darth/Desktop/pandas'

col_names = ['duration', 'service', 'src_bytes', 'dest_bytes', 'count', 'same_srv_rate',
			'serror_rate', 'srv_serror_rate', 'dst_host_count', 'dst_host_srv_count',
			'dst_host_same_src_port_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
			'flag', 'ids_detection', 'malware_detection', 'ashula_detection', 'label', 'src_ip_add',
			'src_port_num', 'dst_ip_add', 'dst_port_num', 'start_time', 'protocol']

cols_to_std = ['duration', 'src_bytes', 'dest_bytes', 'count',
				'same_srv_rate', 'serror_rate', 'srv_serror_rate',
				'dst_host_count', 'dst_host_srv_count',
				'dst_host_same_src_port_rate', 'dst_host_serror_rate',
				'dst_host_srv_serror_rate', 'src_port_num',
				'dst_port_num', 'start_time']

cols_to_index = ['ashula_detection', 'dst_ip_add', 'flag', 'ids_detection', 'label',
					'malware_detection', 'protocol', 'service', 'src_ip_add']

def main():
	# get all the CSV files in the PATH dir
	files = list_files(path=PATH)

	# create empty df, where dfs shall be appended
	df = pd.DataFrame(dtype=str)

	# append the dfs from each file to the data df
	for file in files:
		df = df.append(pd.read_csv(filepath_or_buffer=file, names=col_names, engine='python'))
	
	df['start_time'] = df['start_time'].apply(lambda time: int(time.split(':')[0]) +
											(int(time.split(':')[1]) * (1 / 60)) +
											(int(time.split(':')[2]) * (1 / 3600)))

	df[cols_to_index] = df[cols_to_index].apply(preprocessing.LabelEncoder().fit_transform)
	df[cols_to_std] = preprocessing.StandardScaler().fit_transform(df[cols_to_std])
	
	print(df)

def list_files(path):
	file_list = []
	for (dirpath, dirnames, filenames) in walk(path):
		file_list.extend(os.path.join(dirpath, filename) for filename in filenames)
	return file_list

if __name__ == '__main__':
	main()