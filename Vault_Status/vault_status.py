import os
import json

v_host = [line.strip() for line in open('vault_host.txt','r')]

for v in v_host:
	vault_init = ''
	vault_seal = ''
	vault_ver = ''
	vault_clus = ''
	stat = os.popen('curl -s --insecure https://%s:8200/v1/sys/seal-status' %v).read()
	data = stat.split(",")
	for i in data:
		if "initialized" in i:
			vault_init = i
		if "sealed" in i:
			vault_seal = i
		if "version" in i:
			vault_ver = i
		if "cluster_name" in i:
			vault_clus = i
	print("%s, %s, %s, %s, %s" %(v,vault_init,vault_seal,vault_ver,vault_clus))