class RealmFullException(Exception):
    def __init__(self, msg):
        super(RealmFullException, self).__init__(msg)
