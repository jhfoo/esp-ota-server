const md5 = require('md5'),
    Router = require('restify-router').Router,
    router = new Router(),
    // requestIp = require('request-ip'),
    errors = require('restify-errors'),
    sqlite3 = require('sqlite3').verbose(),
    db = new sqlite3.Database('db/main.db', sqlite3.OPEN_CREATE | sqlite3.OPEN_READWRITE),
    DeviceGroupMgrClass = require('../lib/DeviceGroupMgr'),
    DeviceGroupMgr = DeviceGroupMgrClass.singleton

DeviceGroupMgrClass.setDefaultDatabase(db)
console.log(DeviceGroupMgrClass.getDefaultDatabase())

async function initDatabase() {
    const tables = ['devicegroups']

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
        case 'devicegroups':
            DeviceGroupMgr.createTable()
            break
    }
}

router.get('/clear', clearDevices)
function clearDevices(req, res, next) {
    try {
        DeviceGroupMgr.clearTable()
        res.send('OK')
        next()
    } catch (err) {
        next(new errors.NotFoundError(err.message))
    }
}

router.get('/clean', cleanDevices)
function cleanDevices(req, res, next) {
    try {
        DeviceGroupMgr.cleanTable()
        res.send('OK')
        next()
    } catch (err) {
        next(new errors.NotFoundError(err.message))
    }
}

router.get('/list', listDevices)
async function listDevices(req, res, next) {
    try {
        res.send(await DeviceGroupMgr.getGroups())
        next()
    } catch (err) {
        console.error(err)
        next(new errors.NotFoundError(err.message))
    }

}

router.post('/create', createGroup)
async function createGroup(req, res, next) {
    console.log(req.body)
    if (req.body.ApiToken !== 'def') {
        return next(new errors.NotFoundError('Invalid API token'))
    } 

    if (await DeviceGroupMgr.isGroupIdExist(req.body.id)) {
        return next(new errors.NotFoundError('GroupId already registered'))
    }

    try {
        await DeviceGroupMgr.create({
            id: req.body.id,
            name: req.body.name,
            GroupToken: md5((new Date()).getTime())
        }) 
        res.send(req.body.id)
        next()
    } catch (err) {
        console.error(err)
        return next(new errors.NotFoundError(err.message))
    }
}

initDatabase()

module.exports = router