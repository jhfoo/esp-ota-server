let DefaultDb = null

class DeviceGroupMgr {
    constructor() {

    }

    createTable() {
        return new Promise((resolve, reject) => {
            DefaultDb.run('create table if not exists devicegroups ('
            + 'id string primary key,'
            + 'GroupToken string,'
            + 'name string'
            + ')', (err) => {
                if (err) {
                    reject(err)
                } else {
                    resolve()
                }
            })
        })
    }

    getGroups(filter) {
        return new Promise((resolve, reject) => {
            DefaultDb.all('select * from devicegroups', (err, result) => {
                if (err) {
                    reject(err)
                }

                if (err)
                    console.log('WARNING: this should not be run but it is!!!')
                if (result === null) {
                    result = []
                }
                resolve(result)
            })
        })
    }

    getById(GroupId) {
        return new Promise((resolve, reject) => {
            DefaultDb.get('select * from devicegroups where id = ?',
                GroupId, (err, record) => {
                if (err) {
                    console.error(err)
                    reject(err)
                } else {
                    resolve(record)
                }
            })
        })
    }

    clearTable() { 
        return new Promise((resolve, reject) => {
            DefaultDb.run('drop table devicegroups',async (err) => {
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
            DefaultDb.run('delete from devicegroups where id is null', (err) => {
                if (err) {
                    console.error(err)
                    reject(err)
                } else {
                    resolve()
                }
            })
        })
    }

    isGroupIdExist(DeviceId) {
        console.log('isGroupIdExist()')
        return new Promise((resolve, reject) => {
            DefaultDb.get('select * from devicegroups where id = ?', DeviceId, (err, row) => {
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
    
    create(record) {
        if (!record.id) {
            return reject('[DeviceGroupMgr] Missing id in create()')
        }

        return new Promise((resolve, reject) => {
            DefaultDb.run('insert into devicegroups (id, name, GroupToken) values (?,?,?)',
            record.id, record.name, 
            record.GroupToken, (err) => {
                if (err) {
                    reject(err)
                } else {
                    resolve()
                }
            })
        })
    }
    
}

const singleton = new DeviceGroupMgr()

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
