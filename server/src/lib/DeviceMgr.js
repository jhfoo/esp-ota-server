let DefaultDb = null

class DeviceMgr {
    constructor() {

    }

    getDevices(filter) {
        return new Promise((resolve, reject) => {
            DefaultDb.all('select * from devices', (err, result) => {
                if (err) {
                    reject(err)
                }

                console.log('this is run')
                if (result === null) {
                    result = []
                }
                resolve(result)
            })
        })
    }

    isDeviceIdExist(DeviceId) {
        console.log('isDeviceIdExist()')
        return new Promise((resolve, reject) => {
            DefaultDb.get('select * from devices where id = ?', DeviceId, (err, row) => {
                console.log('err, row')
                console.log(err)
                console.log(row)
                if (!row) {
                    // no matching DeviceId
                    resolve(false)
                } else {
                    resolve(true)
                }
            })
        })
    }
    
    registerDevice(DeviceId) {
        console.log(DeviceId)
        console.log(DefaultDb)
        return new Promise((resolve, reject) => {
            DefaultDb.run('insert into devices (id, LastKnownIp) values (?,?)',
            DeviceId, '', (err) => {
                if (err) {
                    reject(err)
                } else {
                    resolve()
                }
            })
        })
    }
    
}

const singleton = new DeviceMgr()

function setDefaultDatabase(db) {
    DefaultDb = db
}
function getDefaultDatabase() {
    return DefaultDb
}

module.exports = {
    singleton: singleton,
    setDefaultDatabase,
    getDefaultDatabase
}
