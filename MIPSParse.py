import networkx as nx
import matplotlib.pyplot as plt
import re
"""
Major issue to deal with (that's really difficult!): What about 'jr $ra', which is typically used to return to the instruction after the last jal or jalr instruction?
"""
class ProgramSection:
    def __init__(self, label):
        self.label = label
        self.code_lines = []

    def add_code_line(self, line):
        self.code_lines.append(line)

    def __hash__(self):
        return self.label.__hash__()

    def __repr__(self):
        return self.label
    
"""
Three methods:
    add_label('label')
    place_pointer('label')
    split_node_connect('label') -> Splits node that pointer is at into nodes A and B, and creates edge from A to B. A is original node; then it adds a connection from A to 'label' and moves the pointer to B. 
    add_edge('label') adds an edge from the node that pointer is currently at to label
    add_code_line(line) adds a line of code to the node that the pointer points to.
"""

class ProgramSectionGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.pointer = None
        #maps label to ProgramSection instance
        self.sectionMap = dict()
    def place_pointer(self, label):
        self.pointer = label

    #takes instance of ProgramSection
    def add_section(self, label):
        section = ProgramSection(label)
        self.sectionMap[label] = section
        self.graph.add_node(section)

    def split_node_connect(self, label):
        #this is B, the result of spliting the node.
        #this is usually in the context of branches.
        child_section = ProgramSection(self.pointer + '*')
        self.sectionMap[self.pointer + '*'] = child_section
        self.graph.add_node(child_section)
        self.graph.add_edge(self.sectionMap[self.pointer], child_section)
        self.graph.add_edge(self.sectionMap[self.pointer], self.sectionMap[label])
        self.pointer = self.pointer + '*'

    def add_edge(self, label):
        print('label: ' + label)
        self.graph.add_edge(self.sectionMap[self.pointer], self.sectionMap[label])

    def add_code_line(self, line):
        self.sectionMap[self.pointer].add_code_line(line)
    #return networkx object
    def getNetworkXGraph(self):
        return self.graph
#takes in a list of re.compile objects, and a text to match against the re's
def matchAgainstRegexList(reList, text):
    for regex in reList:
        match = regex.match(text)
        if match != None:
            return match

    return False
#pass in text of assembly
#returns an instance of the ProgramSectionGraph class.
def getGraph(mipsCode):
    
    #first, remove all whitespace from the start and end of the lines
    mipsLines = map(lambda x: x.strip(), mipsCode.split('\n'))

    #for each line, remove any section that comes after a '#'. DON'T DO THIS!
    comment = re.compile('#')
    #mipsLines = map(lambda x: comment.split(x)[0], mipsLines)
    #remove the lines that are empty
    mipsLines = filter(lambda x: len(x) > 0, mipsLines)
    #for each line, remove 
    #now we want to go through the lines, and group them by labels
    labeledCode = []
    currentLabel = None
    currentCode = []
    #assume only one label per line -- I'm not sure if this is in the MIPS specs, but if it becomes a problem, I will deal with it later.
    for line in mipsLines:
        #Remove any part of the line that is a comment before the 'if' statement
        rawLine = line
        line = comment.split(line)[0]
        if ':' in line:
            if currentLabel != None:
                labeledCode.append((currentLabel, currentCode))
                
            splitLine = line.split(':')
            currentLabel = splitLine[0]
            currentCode = []
            if len(splitLine) > 1:
                cSplit = comment.split(line)
                
                if len(cSplit) > 1:
                    #then there was a comment in the line -- add to splitLine[1]
                    currentCode.append(splitLine[1] + '#' + '#'.join(cSplit[1::]))
                else:
                    currentCode.append(splitLine[1])
                
        else:
            if currentLabel != None:
                currentCode.append(rawLine)
    if currentLabel != None:
        labeledCode.append((currentLabel, currentCode))
    
    #add the labels as nodes to the graph
    graph = ProgramSectionGraph()
    for (label, code) in labeledCode:
        graph.add_section(label)

    #now that we have a labels, we need to go through, and detect branches and jumps
    #start from the main label.

    threeArgBranchRegex = re.compile('(?:beq|bne)\s+[^,-]*,[^,-]*,\s+(.*)')
    twoArgBranchRegex = re.compile('(?:bgez|bgtz|blez|bltz)\s+[^,-]*,\s+(.*)')
    jumpRegex = re.compile('(?:j|jal|jr|jalr)\s+(.*)')
    jumpNoReturnRegex = re.compile('(?:j|jr)\s+(.*)')
    regexList = [threeArgBranchRegex, twoArgBranchRegex, jumpRegex]
    #If we can go from a label to the label immediately after it in the code, then set this to true
    connectToLastLabel = False
    for (label, code) in labeledCode:
        if connectToLastLabel:
            graph.add_edge(label)
        graph.place_pointer(label)
    

        for i in range(0, len(code)):
            rawLine = code[i]
            #we may have a comment in this line -- If that's the case, then remove the comment.
            line = comment.split(rawLine)[0]
            
            match = matchAgainstRegexList(regexList, line)
            if match == False:
                #then not a jump or branch
                graph.add_code_line(rawLine)
            else:
                #so if it's a branch, then do the split_node_connect
                if line.startswith('b'):
                    #if we are the last line of the function, then don't do the splitting
                    #instead, add the edge from the current node to the branch target. 
                    if i < len(code) - 1:
                        graph.split_node_connect(match.group(1))
                    else:
                        graph.add_edge(match.group(1))

                elif line.startswith('j'):
                    print('jumping')
                    print(line)
                    target = match.group(1)
                    print(target)
                    graph.add_edge(target)
        #if the last line was not a jump, then we will need to connect this label to the next label.
        if jumpNoReturnRegex.match(code[-1]) == None:
            connectToLastLabel = True
            
    
    return graph
        




with open('simple.asm', 'r') as asmFile:
    asmText = asmFile.read()
    
    graph = getGraph(asmText).getNetworkXGraph()
    nx.draw_networkx(graph)
    
    plt.savefig('simple.png')
    print('graph')
    
