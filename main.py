import json
from server import WebServer

host = '0.0.0.0'
port = 3333

server = WebServer(host, port)

lobbys = []

def refrash(content):
	data = json.loads(content)
	lobby = [lobby for lobby in lobbys if lobby['lobby_name'] == data['lobby']]

	if lobby:
		idx = lobbys.index(lobby[0])
		
		if lobbys[idx]['color'] == data['color'][0] and lobbys[idx]['move']:
			move_data = lobbys[idx]['move']
			fen_data = lobbys[idx]['fen']
			
			return '{"cod": "ok", "move": '+json.dumps(move_data)+', "fen": '+json.dumps(fen_data)+'}'
		else:
			return '{"cod": "void"}'
	else:
		return '{"cod": "erro"}'

def move(content):
	data = json.loads(content)
	lobby = [lobby for lobby in lobbys if lobby['lobby_name'] == data['lobby']]

	if lobby:
		idx = lobbys.index(lobby[0])
		lobbys[idx]['move'] = data['move']
		lobbys[idx]['fen'] = data['fen']
		if lobbys[idx]['color'] == 'w':
			lobbys[idx]['color'] = 'b'
		else:
			lobbys[idx]['color'] = 'w'

		print(data['move'])
		print(data['fen'])
		return '{"cod": "ok"}'
	else:
		return '{"cod": "erro"}'

def enter(content):
	data = json.loads(content)
	lobby = [lobby for lobby in lobbys if lobby['lobby_name'] == data]
	print("lobby:")
	print(lobbys)
	if not lobby:
		lobbys.append({
			'lobby_name': data,
			'move': '',
			'fen': '',
			'color': 'w',
			'players': 1
			})
		return '{"cod": "ok", "color": "w"}'
	else:
		if lobby[0]['players'] > 2:
			return '{"cod": "erro", "color": ""}'
		else:
			idx = lobbys.index(lobby[0])
			lobbys[idx]['players'] += 1  
			return '{"cod": "ok", "color": "b"}'

	return '{"ok": "ok"}'

server.router('nextMove', move)
server.router('enter', enter)
server.router('refrash', refrash)

server.startServer()



