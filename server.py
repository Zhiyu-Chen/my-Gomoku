import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options


class Gomoku(object):
	records = []
	black = False
	white = False
	callbacks = []
	turn = 0 #when turn == 0, black play; when turn == 1, white play
	isOver = 0 # the game is not finished

	def register(self, callback):
		self.callbacks.append(callback)

	def unregister(self, callback):
		self.callbacks.remove(callback)

	def preventOverride(self,step):
		for point in self.records:
			if point[0] == step[0] and point[1] == step[1]:
				print "override !"
				return False

		return True

	def isWinHorizon(self,step):
		judge = []
		for record in self.records:
			if step[1] == record[1] and step[2] == record[2]:
				judge.append((record[0] - 25)/50)

		return self.isFive(judge)

	def isFive(self,judge):
		count = len(judge)
		if count < 5:
			return False
		judge.sort()
		for i in range(0,count):
			if (judge[i + 4] - judge[i]) == 4:
				return True

		return False



	def iswin(self,step):
		return self.isWinHorizon(step)


	def addmove(self,step):
		#if not override, draw it and add it to the record list
		if(self.preventOverride(step)): 
			self.records.append(step)
			#judge whether it is finished 
			if self.iswin(step):
				self.isOver = 1
				print "finished !"
			self.notifyCallbacks(step)
 
	def notifyCallbacks(self,step):
		for callback in self.callbacks:
			#waiting to be modified -> send 'isOver'
			callback(step)



class DetailHandler(tornado.web.RequestHandler):
	def get(self):
		if self.application.gomoku.black == False:
			self.application.gomoku.black = True
			player_id = 'black'
		else:
			self.application.gomoku.white = True
			player_id = 'white'

		self.render("client.html",player_id = player_id)
		#display thhe current situation
		pass

class PlayHandler(tornado.web.RequestHandler):
	def post(self):
		action = self.get_argument('action')
		player_id = self.get_argument('player_id')
		player_id = str(player_id)
		x = int(self.get_argument('x'))
		y = int(self.get_argument('y'))
		print type(x)
		if not player_id:
			self.set_status(400)
			return

		#judege whether the post question is legal (right player)
		if self.application.gomoku.turn == 0 and player_id == 'white': #black's turn but white's play
			return 
		elif self.application.gomoku.turn == 1 and player_id == 'black': #white's turn but black's play
			return
		else:
			#return the reaction to player
			if action == 'click':
				step = [x,y,self.application.gomoku.turn]

				if self.application.gomoku.turn == 0:
					self.application.gomoku.turn = 1
				else:
					self.application.gomoku.turn = 0

				#judge whether it is legal or not
				print "receive: " + str(step)
				self.application.gomoku.addmove(step)
			else:
				self.set_status(400)
			 
		
		

class StatusHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		self.application.gomoku.register(self.callback)
	
	def on_close(self):
		self.application.gomoku.unregister(self.callback)
	
	def on_message(self, message):
		pass
	
	def callback(self, step):
		#cast doubt
		#self.write_message('{"board":"%s"}' % str(record).decode('utf-8'))
		msg = [step, self.application.gomoku.isOver]
		self.write_message(str(msg).encode())


class Application(tornado.web.Application):
	def __init__(self):
		self.gomoku = Gomoku()
		
		handlers = [
			(r'/', DetailHandler),
			(r'/play/status',StatusHandler),
			(r'/play',PlayHandler),
		]
		
		settings = {
			'template_path': 'templates',
			'static_path': 'static'
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()

