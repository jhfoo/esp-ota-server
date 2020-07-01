const Router = require('restify-router').Router,
    router = new Router()

router.add('/device', require('./device'))
router.add('/devicegroup', require('./DeviceGroup'))

function ping(req, res, next) {
    res.send('pong')
    next()
}

router.get('/ping', ping)

module.exports = router