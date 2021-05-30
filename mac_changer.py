#!/usr/bin/env python

import subprocess   #Possibilita utilizar comandos no terminal
import optparse   #Possibilita utilizar argumentos
import re   #

#Funcao que permite a utilizacao de argumentos na chamada do programa no terminal
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC adress")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC adress")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options


#Funcao que recebe 2 argumentos e realiza a mudanca do MAC adress
def change_mac(interface, new_mac):
    print("[+] Changing MAC adress for " + interface + " to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    # Comando que le o resultado do ifconfig
    resultados_ifconfig = subprocess.check_output(["ifconfig", interface])
    procura_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(resultados_ifconfig))
    if procura_mac:
        return procura_mac.group(0)
    else:
        print("[-] Could not read MAC adress")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC= " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was succesfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")

