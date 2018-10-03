#!/usr/bin/env python2
from peeringdb import PeeringDB
import sys

asn_number = 46489
total_public_peers = 0
total_private_peers = 0
total_speed = 0
peers_without_ipv6 = []
speed_count ={"10000": 0, "20000": 0, "30000": 0, "50000":0, "100000":0,"200000":0,"300000":0}
unique_peer = []
total_unique_public_peers = 0
total_private_peers = 0

file_path   = "/var/www/html/as_report.txt"
seperator = "+------------------------------------------------------------------+\n"
header1 = "\nOrganization Details for AS%s\n\n" % str(asn_number)
header2 = "List of all the Public Peering Exchange Points for AS%s\n" % str(asn_number)
header3 = "Total number of Public Peering Exchange points\t\t:"
header4 = "Total number of Private Peering Exchange points\t\t:"
header5 = "\n\tExecutive Summary for AS%s\t\n\n" % str(asn_number)
header6 = "Total Unique Public Peerings\t\t\t\t:"
header7 = "Total Unique Peerings(Public and Private)\t\t:"
header8 =  "The total aggregate speed\t\t\t\t:"
header9 = "\nPublic Peers which do not have IPv6 address:\n"
file_open_error = "Run the script as root or superuser which has proper permissions"

class exchange_info():
	def __init__(self):
		pdb = PeeringDB()
		self.net_ixlan = pdb.type_wrap('netixlan')
		self.net = pdb.type_wrap('net')
		self.net_fac = pdb.type_wrap('netfac')
		assert self.net.get(1) == pdb.get('net',1)
		assert self.net_ixlan.all(asn=asn_number) == pdb.all('netixlan',asn=asn_number)
		assert self.net_fac.all(asn=asn_number) == pdb.all('netfac',asn=asn_number)
		try:
			self.fh = open(file_path, "w")
			self.fh.write("\n")
			self.fh.close()
		except  IOError:
			print file_open_error

	def write_org_summary(self):
		self.fh = open(file_path, "a")
		self.fh.write(header1+seperator)
		for exch in self.net.all(asn=asn_number)[0]:
			element = self.net.all(asn=asn_number)[0][exch]
			if element and not type(element)==int and not type(element)==bool:
				string_element = element.encode('utf-8')
			elif type(element)==int or type(element)==bool:
				string_element = str(element)
			self.fh.write(exch +"\t:\t"+string_element+"\n")
		self.fh.write(seperator+"\n\n")
		self.fh.close()

	def write_public_peers(self):
		self.fh = open(file_path, "a")
		self.fh.write(header2+seperator)
		global total_speed
		global total_public_peers
		global total_unique_public_peers
		for num,pexch in enumerate(self.net_ixlan.all(asn=asn_number)):
			name = pexch['name'].encode('utf-8')
			if(pexch['ipaddr4']):
				v4=pexch['ipaddr4'].encode('utf-8')
			else:
				v4 =""
			if(pexch['ipaddr6']):
				v6=pexch['ipaddr6'].encode('utf-8')
			else:
				v6=""
				peers_without_ipv6.append(name)	
			if name not in unique_peer:
				unique_peer.append(name)
			current_speed = pexch['speed']
			total_speed += current_speed
			try:
				speed_count[str(current_speed)] += 1
			except KeyError:
				continue
			self.fh.write("  Number :      " + str(num)+"\n")
			self.fh.write("  Name:         "+name+"\n")
			self.fh.write("  IPv4 Address: "+v4+"\n")
			self.fh.write("  IPv6 address: "+v6+"\n")
			self.fh.write("  Speed:        "+str(current_speed)+"\n")
			self.fh.write(seperator)
		total_public_peers = num + 1
		total_unique_public_peers = len(unique_peer)
		self.fh.write(seperator)
		self.fh.close()

	def count_private_peers(self):
		global total_private_peers
		for num,pexch in enumerate(self.net_fac.all(asn=asn_number)):
			name = pexch['name'].encode('utf-8')
			print name
			if name not in unique_peer:
				unique_peer.append(name)
		total_private_peers = num + 1

def main():
	cl = exchange_info()
	cl.write_org_summary()
	cl.write_public_peers()
	#cl.count_private_peers()
	file_handle = open(file_path, "a")
	file_handle.write(header5+seperator)
	file_handle.write(header3+str(total_public_peers)+"\n")
	#file_handle.write(header4+str(total_private_peers)+"\n")
	file_handle.write(header6+str(total_unique_public_peers)+"\n")
	#file_handle.write(header7+str(len(unique_peer))+"\n")
	file_handle.write(header8+str(total_speed)+"\n")
	for spd in speed_count:
		file_handle.write("The number of public Peering Exchange Points with speed of %sG is\t: " % spd + str(speed_count[spd])+"\n")
	file_handle.write(header9)
	for peer in set(peers_without_ipv6):
		file_handle.write(peer+"\n")
	file_handle.close()

if __name__ == "__main__":
	sys.exit(main())
