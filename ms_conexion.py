#Test de conectividad con servidores

import os
import re
import sys
import socket
import threading

#String, string => int(ms) / None
def ping(ip,so):
	if so in ("Windows","Linux"):
		if so == "Windows":
			ping_text = os.popen("ping "+ip).read()
			ms = re.findall("Media =(.+)ms",ping_text)
		elif so == "Linux":
			ping_text = os.popen("ping -c 4 "+ip).read()
			line_ms = re.findall("mdev =(.+)ms",ping_text)
			if line_ms:
				ms = re.findall("\d+\.\d+/(\d+\.\d+)/",line_ms[0])
			else:
				return None
		if len(ms)>=1:
			return float(ms[0])
		else:
			return None
	else:
		return None

#String, string, dict, string => None
def ping_thread(ip,so,dict,i):
	ms = ping(ip,so)
	if ms:
		dict[i] = ms

#None => String / False
def sistema_operativo():
	if os.name == "posix":
		return "Linux"
	elif os.name == "nt":
		return "Windows"
	else:
		return False
	
#String => Boolean
def valid_address(ip):
	try:
		socket.inet_aton(ip)
		return True
	except:
		return False

#None => String
def cargar_archivo(ruta_archivo=False):
	if ruta_archivo:
		if os.path.isfile(ruta_archivo):
			archivo = open(ruta_archivo,"r")
		elif os.path.isfile(ruta_archivo+".txt"):
			archivo = open(ruta_archivo+".txt","r")
		else:
			print("No existe el archivo")
			exit()
	else:
		while not ruta_archivo:
			try:
				ruta_archivo = input("\nArchivo de datos de servidores: ")
			except:
				exit()
			if os.path.isfile(ruta_archivo):
				archivo = open(ruta_archivo,"r")
			elif os.path.isfile(ruta_archivo+".txt"):
				archivo = open(ruta_archivo+".txt","r")
			else:
				ruta_archivo = False
				print("No existe el archivo")
	texto_archivo = archivo.read()
	archivo.close()
	nombre_archivo = ruta_archivo.split(".")[0]
	return nombre_archivo,texto_archivo

#List (of list) => None (print)
def print_table(lineas,rows=0,dict_ms=False):
	rows = len(lineas) if not rows else rows
	n_cols = max(len(line) for line in lineas)
	n_rows = len(lineas)
	tam_cols = [max(len(line[cn]) for line in lineas if len(line)>cn) 
				for cn in range(n_cols)]
	lineas = [[e for e in line]+["" for i in range(n_cols-len(line))] 
				for line in lineas]
	if dict_ms:
		tam_col_ms = 11
		tam_file = sum(tam_cols)+n_cols+tam_col_ms
	else:
		tam_file = sum(tam_cols)+n_cols
	print("\n"+"-"*tam_file)
	for i in range(n_cols):
		if i==0:
			print(("{0:^"+str(tam_cols[i])+"}").format(i),end="")
		else:
			print(("|{0:^"+str(tam_cols[i])+"}").format(i),end="")
	if dict_ms:
		print(("|{0:^"+str(tam_col_ms)+"}").format("ms"),end="")
	print()
	for line in lineas[:min(rows,len(lineas))]:
		print("-"*tam_file)
		for cn in range(len(line)):
			if cn==0:
				print(("{0:^"+str(tam_cols[cn])+"}").format(line[cn]),end="")
			else:
				print(("|{0:^"+str(tam_cols[cn])+"}").format(line[cn]),end="")
		if dict_ms:
			ip = [e for e in line if valid_address(e)][0]
			print(("|{0:^"+str(tam_col_ms)+"}").format(str(dict_ms[ip])),end="")
		print()
	print("-"*tam_file)
	if len(lineas) > rows:
		print(("{0:^"+str(tam_cols[0])+"}").format("..."))
		print("-"*tam_file)
		
#List => dict
def test_conectividad(addresses,so):
	dict_addresses = {ip:None for ip in addresses}
	threads = []
	for ip in addresses:
		thread = threading.Thread(target=ping_thread, 
					args=(ip,so,dict_addresses,ip))
		threads.append(thread)
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	return dict_addresses
	
#List, dict => file
def create_file(lineas, dict_ms, name):
	nid = 1
	file_name = name+"_"+str(nid)+"_log.log"
	while os.path.isfile(file_name):
		nid += 1
		file_name = name+"_"+str(nid)+"_log.log"
	file = open(file_name,"w")
	for line in lineas:
		ip_line = [e for e in line if valid_address(e)][0]
		if dict_ms[ip_line]:
			text_linea = "\t".join(line)+"\t=>\t"+str(dict_ms[ip_line])+"ms\n"
		else:
			text_linea = "\t".join(line)+"\t=>\t"+str(dict_ms[ip_line])+"\n"
		file.write(text_linea)
	file.close()
	print("\nLog '{}' creado.".format(file_name))
	
#MAIN. #None => file (print)
def main():
	so = sistema_operativo()
	if so:	
		print("### Test Conectividad ###")
		if len(sys.argv)>=2:
			arg_archivo = sys.argv[1]
			nombre_archivo, texto_archivo = cargar_archivo(arg_archivo)
		else:
			nombre_archivo, texto_archivo = cargar_archivo()
		separador_linea = "\t"
		lineas = texto_archivo.strip().split("\n")
		lineas = [l.split(separador_linea) for l in lineas]
		lineas = [line for line in lineas if any(valid_address(e) for e in line)]
		addresses = [[e for e in line if valid_address(e)][0] for line in lineas]
		if any(addresses):
			print_table(lineas,4)
			test = False
			while not test:
				try:
					test = input("\nRealizar Test de Conectividad (Y/N): ").upper()
				except:
					return None
				if any(test == e for e in ("Y","YES","S","SI","SÍ")):
					print("\nTest de Conectividad en proceso....")
					dict_ms = test_conectividad(addresses,so)
					print_table(lineas,dict_ms=dict_ms)
					create_file(lineas,dict_ms,nombre_archivo)
				elif any(test == e for e in ("N","NO")):
					return None
				else:
					test = False
		else:
			print("No se encontraron direcciones IP en el archivo")
	else:
		print("Sistema operativo inválido")

if __name__ == "__main__":
	main()