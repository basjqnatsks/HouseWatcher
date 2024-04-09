class read(object):
    def __new__(cls, filename: str, delim: str = None, Encoding : str ="ISO-8859-1", Remove: list = ['\r', '\t']) -> open:
        cls.Encoding = Encoding
        cls.Remove = Remove
        if delim != None:
            return cls.fileread(cls, filename).split(delim)
        return cls.fileread(cls, filename)
    def fileread(self, filename: str) -> open:
        with open(filename, "rb") as f:
            var = f.read().decode(self.Encoding)
            if self.Remove:
                for x in self.Remove:
                    var = var.replace(x, "")
        return var
class FileLength(object):
    def __new__(cls, FileString=None):
        cls.__init__(cls, FileString)
        return cls.main(cls)
    def __init__(self, FileString=None):
        if FileString == None:
            self.Input = self.getandcheck(self)
        else:
            self.Input = FileString
    def getandcheck(self):
        name = input("File Name: ")
        try:
            name = str(name)
            open(name, "rb")
        except:
            raise FileExistsError("No File")
        return name
    def main(self):
        with open(self.Input, 'rb') as f:
            for i, r in enumerate(f):
                pass
        return i