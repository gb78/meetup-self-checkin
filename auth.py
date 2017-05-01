import requests
import json
import getpass
import random
import daemon

baseURL="http://emjuizdefora.com/gdgjf/api/"

URLS={
'1':{'nome':'GDG','url':"http://emjuizdefora.com/gdgjf/api/"},
'2':{'nome':'GBG','url':"http://emjuizdefora.com/gbgjf/api/"},
'3':{'nome':'Cafe Digital','url':"http://cafedigitaljf.com.br/api/"}
}
#baseURLS=json.loads(URLS)

print "* * * * Self Check-in * * * * \n "
xgroup=raw_input("(1) GDG \n(2) GBG \n(3) Cafe Digital \n")

baseURL=URLS[xgroup]['url']
print baseURL

checkAuth=0;
while checkAuth<=0:
	xemail = raw_input("Email: ")
	xpassw  = getpass.getpass('Senha:')
	
	print "Autorizando..."
#	r = requests.post( baseURL + "autenticar/", { 'email' : xemail , 'password' : xpassw})
	r = requests.post( baseURL + "autenticar/", { 'email' : 'gb@nepopo.net' , 'password' : 'Gb6357_'})
	if r.status_code==200:
		checkAuth=1
		print "...ok"
	else:
		print r.text
	print '\n'

organizer=json.loads(r.text)
xname=organizer['pessoa']['nome']
xtoken=organizer['accessToken']

print "Organizer: "+xname+"\n";


#selecionar evento
r=requests.get(baseURL+"evento/1352", headers={ "X-TOKEN" : xtoken });
event=json.loads(r.text)
print event['titulo']+" Presentes: "+str(event['qtd_presentes'])+" | Inscritos: "+str(event['qtd_confirmados'])+"\n"

keep_running=1
while keep_running>0:
	#presenca
	checkID = raw_input("Passe a tag no leitor ou\ndigite seu email: ")
	if checkID=='0':
		keep_running=0
		print "\n"
	else:
		r=requests.post(baseURL+"inscricao/self_chekin/",  headers={"X-TOKEN":xtoken}, data={"evento":"1352","identificacao":checkID})
		presence=json.loads(r.text)

		if not presence.has_key('erro'):
			greetings=['Aloha','Welcome','Ola','Alo','Oi','Bienvenue']
			print random.choice(greetings)+" "+presence['nome']+"!"
		else:
			print "Cadastro inexistente... quem sois? "
		
		print "\n"




#print(r.text) #TEXT/HTML
#print(r.headers) #HEADERS
#print(r.status_code, r.reason) #HTTP
