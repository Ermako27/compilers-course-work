class ParseTreeProperty:
    def __init__(self):
        self.annotations = dict();
    
    def put(self, node, value):
        uid = node.uid
        self.annotations[uid] = value
    
    def get(self, node):
        uid = node.uid
        value = self.annotations[uid]
        return value