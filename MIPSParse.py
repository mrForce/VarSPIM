import networkx as nx
import re

#pass in text of assembly
#returns a graph representing the code. Edges are jumps or branches.
def getGraph(mipsCode):
    #first, remove all whitespace from the start and end of the lines
    mipsLines = map(lambda x: x.strip(), mipsCode.split('\n'))

    #for each line, remove any section that comes after a '#'.
    comment = re.compile('#')
    mipsLines = map(lambda x: comment.split(x)[0], mipsLines)
    #remove the lines that are empty
    mipsLines = filter(lambda x: len(x) > 0, mipsLines)
    #for each line, remove 
    #now we want to go through the lines, and group them by labels
    labeledCode = []
    currentLabel = None
    currentCode = []
    #assume only one label per line -- I'm not sure if this is in the MIPS specs, but if it becomes a problem, I will deal with it later.
    for line in mipsLines:
        if ':' in labels:
            if currentLabel != None:
                labeledCode.append((currentLabel, currentCode))
                
            splitLine = line.split(':')
            currentLabel = splitLine[0]
            currentCode = []
            if len(splitLine) > 1:
                currentCode.append(splitLine[1])
                
        else:
            if currentLabel != None:
                currentCode.append(line)

    #now that we have a labels, we need to go through, and detect branches.
                
        
        
        




        
