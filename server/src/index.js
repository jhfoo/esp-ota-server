const restify = require('restify'),
    server = restify.createServer(),
    corsM = require('restify-cors-middleware'),
    socketio = require('socket.io'),
    io = socketio.listen(server.server)

io.on('connection', (socket) => {
    console.log('New connection')
})

const cors = corsM({
    origins:['*']
})

server.pre(cors.preflight)
server.use(cors.actual)

server.listen(8088, function() {
  console.log('%s listening at %s', server.name, server.url)
})