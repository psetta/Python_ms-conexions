# -*- coding: utf-8 -*-

import os
import re

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
			text_print = os.popen("ping "+ip).read()
		except:
			print "Imposible comprobar ping"
			text_print = ""
		ms = re.findall("Media.+",text_print)
		if ms:
			print "\t"+ms[0]
			log.write(">> "+line+"\n"+ms[0]+"\n")
		else:
			print "\tNon foi posible conectar"
	
log.close()
print "Finalizado"
raw_input()