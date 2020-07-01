let DefaultDb = null

class DeviceMgr {
    constructor() {

    }

    createTable() {
        return new Promise((resolve, reject) => {
            DefaultDb.run('create table if not exists devices ('
            + 'id string primary key,'
            + 'LastKnownIp string,'
            + 'FreeStorageKB integer,'
            + 'DeviceGroupId string,'
            + 'LastPing datetime'
            + ')', (err) => {
                if (err) {
                    reject(err)
                } else {
                    resolve()
                }
            })
        })
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

    clearTable() { 
        return new Promise((resolve, reject) => {
            DefaultDb.run('drop table devices',async (err) => {
                if (err) {
                    console.error(err)
                    reject(err)
                } else {
                    await this.createTable()
                    resolve()
                }
            })
        })
    }

    cleanTable() { 
        return new Promise((resolve, reject) => {
            DefaultDb.run('delete from devices where id is null', (err) => {
                if (err) {
                    console.error(err)
                    reject(err)
                } else {
                    resolve()
                }
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
    
    registerDevice(DeviceRec) {
        if (!DeviceRec.id) {
            return reject('[registerDevice] Missing id in param')
        }

        return new Promise((resolve, reject) => {
            DefaultDb.run('insert into devices (id, LastKnownIp'
            + ', LastPing, FreeStorageKB'
            + ', DeviceGroupId'
            + ') values (?,?,?,?,?)',
            DeviceRec.id, DeviceRec.LastKnownIp, 
            DeviceRec.LastPing, DeviceRec.FreeStorageKB,
            DeviceRec.DeviceGroupId, (err) => {
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
