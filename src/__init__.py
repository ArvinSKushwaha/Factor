# from requests import *
# from random import choice
# from json import load


# with open('Factor.json', 'r') as f:
# 	json = load(f)
# 	intermediate_ip_count = json['intermediate_server_count']

# print(intermediate_ip_count)

# IPS = ['.'.join([str(n)]*4) for n in range(100)]

# def intermediate_ips():
# 	'''This function will choose "number" random IP addresses for use as intermediates
# 	Inputs:
# 	number: int
# 	Returns:
# 	ips: list
# 	'''

# 	NewIPs = []
# 	# for i in range(number):
# 	# 	NewIPs.append(choice(IPS))
# 	while len(NewIPs) < intermediate_ip_count:
# 		ip = choice(IPS)
# 		if(not ip in NewIPs):
# 			NewIPs.append(ip)
# 	return NewIPs
	
# print(intermediate_ips())