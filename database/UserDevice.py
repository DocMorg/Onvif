from . import db


class UserDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship("Device", backref="userdevices")
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship("Group", backref="devices")



    def __repr__(self):
        pass