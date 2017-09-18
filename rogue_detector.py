#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Rogue Access Point Detector
# version: 0.1
# author: anotherik (Ricardo Gonçalves)

import os, string, threading, sys, signal, time, Queue, multiprocessing
import modules.scanners.iwlist_network_monitor as iwlist_monitor
import modules.scanners.scapy_network_monitor as scapy_monitor
import modules.detectors.evil_twin_detector as detector1
import modules.actuators.createRogueAP as hive_mode
import modules.manage_interfaces as manage_interfaces
import modules.colors as colors

def print_info(info, type=0):
    if (type == 0):
        m = colors.get_color("OKBLUE")
    elif (type == 1):
        m = colors.get_color("OKGREEN")
    elif (type == 2):
        m = colors.get_color("WARNING")
    m += "[*] " + colors.get_color("ENDC") + colors.get_color("BOLD") + info + colors.get_color("ENDC")
    print(m)

def intro():
	print(colors.get_color("BOLD") +
	 "                               _    ____    ____       _            _     \n"+
	 " _ __ ___   __ _ _   _  ___   / \  |  _ \  |  _ \  ___| |_ ___  ___| |_ \n" +
	 "| '__/ _ \ / _` | | | |/ _ \ / _ \ | |_) | | | | |/ _ \ __/ _ \/ __| __| \n" +
	 "| | | (_) | (_| | |_| |  __// ___ \|  __/  | |_| |  __/ ||  __/ (__| |_ \n"+
	 "|_|  \___/ \__, |\__,_|\___/_/   \_\_|     |____/ \___|\__\___|\___|\__| \n "+
	 "          |___/                                                   v1.0\n"+
     "\t\t\t\tby Ricardo Gonçalves (@anotherik)\n"+ colors.get_color("ENDC"))

def usage():
	print_info("Usage: ./rogue_detector.py [option]")
	print("\nOptions:  -i interface\t\t -> the interface to monitor the network")
	print("\t  -p profile\t\t -> name of the profile to load")
	print("\t  -s scan_type\t\t -> name of scanning type (iwlist, scapy)")
	print("\t  -h hive_mode\t\t -> creates an AP")
	print("\t  -d deauth\t\t -> deauthenticates users from target AP")

def parse_args():
	intro()
	scanners = ["scapy", "iwlist"]
	scanner_type = ""
	profile, scan, hive, deauth = False, False, False, False

	if (len(sys.argv) < 4):
		usage()
		return

	# setting args
	for cmd in sys.argv:

		if (cmd == "-i"):
			global interface
			interface = sys.argv[sys.argv.index(cmd)+1]

		if (cmd == "-p"):
			profile_name = sys.argv[sys.argv.index(cmd)+1]
			if(os.path.isfile(profile_name+".txt")):
				profile = True
			else:
				print (colors.get_color("FAIL")+ "Profile selected does not exists!\n"+ colors.get_color("ENDC"))
				return
			
		if (cmd == "-s"):
			scan = True
			scanner_type = sys.argv[sys.argv.index(cmd)+1]

		if (cmd == "-h"):
			hive = True

		if (cmd == "-d"):
			deauth = True	

			
	if (scan):		
		if (scanner_type == "scapy"):
			manage_interfaces.change_mac(interface)
			manage_interfaces.enable_monitor(interface)
			try:
				if (profile):
					scapy_monitor.scapy_scan(interface, profile_name)
				else: 
					scapy_monitor.scapy_scan(interface)
			except Exception as e:
				print("Exception: %s" % e)
				return
		
		if (scanner_type == "iwlist"):
			try:
				if (profile):
					iwlist_monitor.scan(interface, profile_name)
				else:
					iwlist_monitor.scan(interface)
			except Exception as e:
				print("Exception: %s" %e)
				return

		if (scanner_type not in scanners):
			print (colors.get_color("FAIL")+ "Wrong module selected!\n"+ colors.get_color("ENDC"))
			usage()
			return

	if (hive):
		iface_hive = raw_input("Enter the Interface for the Hive: ")
		iface_hive = str(iface_hive)
		try:	
			manage_interfaces.enable_monitor(iface_hive)
			p = multiprocessing.Process(hive_mode.startRogueAP(iface_hive))
			p.start()
			p.join()
		except Exception as e:
			print("Exception: %s" % e)
			return
			# config a file to load the AP parameters
			# os.system("./createRogueAP.sh") # read params from config file


def main():
	parse_args()

if __name__ == '__main__':
	main()