# -*- coding: utf-8 -*-

import os
import re

if os.name == "posix":
	sistema_operativo = "Linux"
else:
	sistema_operativo = "Windows"

print u"::Introduce o nome do arquivo cos datos dos servidores:"
name_arq = raw_input(">> ")
arq = open(name_arq,"r")

texto_arq = arq.read()

arq.close()

arq_lineas = texto_arq.split("\n")
for line in arq_lineas:
	print line.split("\t")

print u"::Introduce o número da columna donde están as IPs:"
n_column = raw_input(">> ")
n_column = int(n_column)

log = open("ping_servers_log.txt","w")

for line in arq_lineas:
	columns = line.split("\t")
	if len(columns) > n_column:
		ip = columns[n_column]
	else:
		ip = ""
	if ip:
		print "== "+line
		try:
			print "\tFacendo ping "+ip+"..."
			if sistema_operativo == "Windows":
				text_print = os.popen("ping "+ip).read()
			else:
				text_print = os.popen("ping -c 4 "+ip).read()
		except:
			print "Imposible comprobar ping"
			text_print = ""
		if sistema_operativo == "Windows":
			ms = re.findall("Media.+",text_print)
		else:
			line_ms = re.findall("mdev.+",text_print)
			if line_ms:
				ms = re.findall("(\d+\.\d+)",line_ms[0])
			else:
				ms = ""
		if ms:
			if sistema_operativo == "Windows":
				print "\t"+ms[0]
			else:
				print "\tMedia = "+ms[0]+"ms"
			log.write(">> "+line+"\n"+ms[0]+"\n")
		else:
			print "\tNon foi posible conectar"
	
log.close()
print "Finalizado"
raw_input()