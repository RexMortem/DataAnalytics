import sys

outputFolder = "Outputs/"

class Output():
    def __init__(self, type=None):
        self.output = ""

        self.type = type
    
    # may be useful when adding methods to output to LaTeX
    def write(self, filePath:str = "1.out"):
        if self.type == None:
            sys.stdout.write(self.output)
        elif self.type == "File":
            with open(outputFolder + filePath, "w") as outFile:
                outFile.write(self.output)