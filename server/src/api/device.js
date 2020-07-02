const Router = require('restify-router').Router,
    router = new Router(),
    // requestIp = require('request-ip'),
    errors = require('restify-errors'),
    sqlite3 = require('sqlite3').verbose(),
    db = new sqlite3.Database('db/main.db', sqlite3.OPEN_CREATE | sqlite3.OPEN_READWRITE),
    DeviceMgrClass = require('../lib/DeviceMgr'),
    DeviceMgr = DeviceMgrClass.singleton,
    DeviceGroupMgrClass = require('../lib/DeviceGroupMgr'),
    DeviceGroupMgr = DeviceGroupMgrClass.singleton

DeviceMgrClass.setDefaultDatabase(db)
DeviceGroupMgrClass.setDefaultDatabase(db)
console.log(DeviceMgrClass.getDefaultDatabase())

async function initDatabase() {
    const tables = ['users', 'devices']

    console.log('Init database')
    for (let i = 0; i < tables.length; i++) {
        let TableName = tables[i]
        try {
            let ret = await new Promise((resolve, reject) => {
                db.each("select count(*) as total from sqlite_master where type = 'table' and name='" + TableName + "'", (err, row) => {
                    if (err) {
                        console.error(err)
                    } else {
                        if (row.total === 0) {
                            // create table
                            createDbTable(db, TableName)
                        }
                    }
                }, (err, rows) => {
                    if (err) {
                        reject(err)
                    } else {
                        resolve(rows)
                    }
                })
            })
        } catch (err) {
            console.error('ERROR: %s', err)
        }
    }
}


function createDbTable(db, TableName) {
    console.log('Creating table %s', TableName)
    switch (TableName) {
        case 'devices':
            DeviceMgr.createTable()
            break
    }
}

router.get('/clear', clearDevices)
function clearDevices(req, res, next) {
    try {
        DeviceMgr.clearTable()
        res.send('OK')
        next()
    } catch (err) {
        next(new errors.NotFoundError(err.message))
    }
}

router.get('/clean', cleanDevices)
function cleanDevices(req, res, next) {
    try {
        DeviceMgr.cleanTable()
        res.send('OK')
        next()
    } catch (err) {
        next(new errors.NotFoundError(err.message))
    }
}

router.get('/list', listDevices)
async function listDevices(req, res, next) {
    try {
        res.send(await DeviceMgr.getDevices())
        next()
    } catch (err) {
        console.error(err)
        next(new errors.NotFoundError(err.message))
    }

}

router.post('/register', registerDevice)
async function registerDevice(req, res, next) {
    let group = await DeviceGroupMgr.getByToken(req.body.GroupToken)
    if (!group) {
        return next(new errors.NotFoundError('Invalid group token'))
    } 

    try {
        if (await DeviceMgr.isDeviceIdExist(req.body.id)) {
            await DeviceMgr.update({
                id: req.body.id,
                LastKnownIp: req.connection.remoteAddress,
                FreeStorageKB: 'FreeStorageKB' in req.body ? req.body.FreeStorageKB : -1,
                LastPing: Math.floor(Date.now()/ 1000)
            })
        } else {
            await DeviceMgr.registerDevice({
                id: req.params.DeviceId,
                LastKnownIp: req.connection.remoteAddress,
                FreeStorageKB: req.params.FreeStorageKB,
                DeviceGroupId: group.id,
                LastPing: Math.floor(Date.now()/ 1000)
            }) 
        }
    
        res.send(req.params.DeviceId)
        next()
    } catch (err) {
        console.error(err)
        if (typeof err === 'string') {
            return next(new errors.NotFoundError(err))
        } else {
            return next(new errors.NotFoundError(err.message))
        }
    }
}

initDatabase()

module.exports = router