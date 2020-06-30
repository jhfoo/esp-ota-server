const Router = require('restify-router').Router,
    router = new Router(),
    errors = require('restify-errors'),
    sqlite3 = require('sqlite3').verbose(),
    db = new sqlite3.Database('db/main.db', sqlite3.OPEN_CREATE | sqlite3.OPEN_READWRITE),
    DeviceMgrClass = require('../lib/DeviceMgr'),
    DeviceMgr = DeviceMgrClass.singleton

DeviceMgrClass.setDefaultDatabase(db)
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
            db.run('create table if not exists devices ('
                + 'id string primary key,'
                + 'LastKnownIp string'
                + ')')
            break
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

router.get('/register/:DeviceId/:DeviceToken', registerDevice)
async function registerDevice(req, res, next) {
    if (req.params.DeviceToken !== 'def') {
        return next(new errors.NotFoundError('Invalid device token'))
    } 

    if (await DeviceMgr.isDeviceIdExist(req.params.DeviceId)) {
        return next(new errors.NotFoundError('DeviceId already registered'))
    }

    try {
        await DeviceMgr.registerDevice(req.params.DeviceId) 
        res.send(req.params.DeviceId)
        next()
    } catch (err) {
        console.error(err)
        return next(new errors.NotFoundError(err.message))
    }
}

initDatabase()

module.exports = router