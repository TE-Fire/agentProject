class Test(object):
    def __init__(self, name):
        self.name = name
    
    def __or__(self, other):
        return MySquence(self, other)

    def __str__(self):
        return self.name
    
class MySquence(object):
    def __init__(self, *args):
        self.squence = []
        for arg in args:
            self.squence.append(arg)
    
    def __or__(self, other):
        self.squence.append(other)
        return self
    
    def run(self):
        for str in self.squence:
            print(str)
    
        
if __name__ == '__main__':
    a = Test('a')
    b = Test('b')
    c = Test('c')

    d = a | b | c
    d.run()
    print(type(d))