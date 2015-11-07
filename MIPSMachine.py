"""
This class is used to simulate MIPS. It does several things:

1) Binds variable names to registers
2) Verification of variable bindings
3) simulate the stack in a MIPS processer. 



"""


class RegisterNotDefined(Exception):
    def __init__(self, register):
        self.value = register
    def __str_(self):
        return repr(self.value)

class StackPointerOutOfBoundsError(Exception):
    def __init__(self, amount):
        self.value = amount
    def __str__(self):
        return 'Placement of element: ' + str(self.value)

class StackElementNotBoundedError(Exception):
    def __init__(self, stackLocation):
        self.value = stackLocation
        
class MIPSRegisters:
    def __init__(self):
        self.register_names = ['$v0', '$v1', '$zero', '$a0', '$a1', '$a2', '$a3', '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7', '$t8', '$t9', '$ra']
        self.registers = {register_name:'' for register_name in register_names}

    def bindRegister(self, register, variableName):
        if register in self.register_names:
            self.registers[register] = variableName
        else:
            raise RegisterNotDefined(register)
    def unbindRegister(self, register):
        if register in self.registers_names:
            self.registers[register] = ''
        else:
            raise RegisterNotDefined(register)
    def verifyRegisterBinding(self, register, variableName):
        if register not in self.register_names:
            raise RegisterNotDefined(register)
        else:
            if self.registers[register] == variableName:
                return True
            else:
                return False




"""
This holds the stack, as well as what the stack pointer is pointing to
"""
class MIPStack:
    #stacksize is the size of the stack in bytes
    def __init__(self, stackSize):
        self.stack = dict()
        self.stackPointer = 0
        #stack size is in bytes, but let's convert it to elements
        self.stackSize = stackSize/4
        
    def addToStackPointer(self, amount):
        """
        You use this method to change where the stack pointer is. For example, if we were at an instruction like:

               addi $sp, $sp, -8 

        This call would usually be used to push two items to the stack. You would call addToStackPointer(-8)

        Args:
            amount: The number of bytes to move the stack by.
        Raises:
            StackPointerOutOfBoundsError: If the movement of the stack pointer would place it before or after the bounds of the stack. 
            
        """
        
        #Divide by -4.
        numElements = amount/-4
        stackLocation = self.stackPointer + numElements
        if stackLocation  < 0 or stackLocation >= stackSize:
            raise StackPointerOutOfBoundsError(stackLocation)
        else:
            self.stackPointer = stackLocation


    def bindStackElement(self, stackPointerOffset, varName):
        """ Binds an element of the MIPS stack to a variable name.

        Args:
            stackPointerOffset: The offset of the stack pointer (the same value as if you were placing a value into that part of the stack)
            varName: The name to bind the element to.

        Raises:
            StackPointerOutOfBoundsError: If the stack element is out of the bounds of the stack.
        """
        numElements = stackPointerOffset/-4
        elementLocation = self.stackPointer + numElements
        if elementLocation < 0 or elementLocation >= self.stackSize:
            raise StackPointerOutOfBoundsError(elementLocation)
        else:
            self.stack[elementLocation] = varName

    def unbindStackElement(self, stackPointerOffset):
        """ Unbinds an element of the MIPS stack from a variable name.

            Args:
               stackPointerOffset: The offset of the stack pointer (the same value as if you were placing a value into that part of the stack)
       
            Raises:
               StackPointerOutOfBoundsError: If the stack element is out of the bounds of the stack
             
               StackElementNotBoundedError: If the stack element isn't bound to a variable name
        """
        numElements = stackPointerOffset/-4
        elementLocation = self.stackPointer + numElements
        if elementLocation < 0 or elementLocation >= self.stackSize:
            raise StackPointerOutOfBoundsError(elementLocation)
        else:
            try:
                self.stack.pop(elementLocation)
            except KeyError:
                raise StackElementNotBoundedError(self.stackPointerOffset)

    def verifyStackElementBinding(self, stackPointerOffset, variableName):
        """ Use this method to verify that a stack element is bound to a given variable.

        Args:
            stackPointerOffset: The offset of the stack pointer

            variableName: Check that the stack element is bound to the given variable

        Returns:
            True if the stack element is bounded to the given variable, false if it is bound to a different variable, and 

        
        Raises:
            StackPointerOutOfBoundsError: If the stack element is out of the bounds of the stack
             
            StackElementNotBoundedError: If the stack element isn't bound to a variable name
        """
        numElements = stackPointerOffset/-4
        elementLocation = self.stackPointer + numElements
        if elementLocation < 0 or elementLocation >= self.stackSize:
            raise StackPointerOutOfBoundsError(elementLocation)
        else:
            try:
                varName = self.stack[elementLocation]
                return (varName == variableName) 
            except KeyError:
                raise StackElementNotBoundedError(self.stackPointerOffset)

    def getStackElementBinding(self, stackPointerOffset):
        """ Use this method to get the variable name that stack element is bound to.

        Args:
            stackPointerOffset: The offset of the stack pointer

        

        Returns:
            Returns the binding if the stack element is bound to something. Raises a StackElementNotBoundedError if the element is not bound to anything.

        
        Raises:
            StackPointerOutOfBoundsError: If the stack element is out of the bounds of the stack
             
            StackElementNotBoundedError: If the stack element isn't bound to a variable name
        """
        numElements = stackPointerOffset/-4
        elementLocation = self.stackPointer + numElements
        if elementLocation < 0 or elementLocation >= self.stackSize:
            raise StackPointerOutOfBoundsError(elementLocation)
        else:
            try:
                varName = self.stack[elementLocation]
                return varName 
            except KeyError:
                raise StackElementNotBoundedError(self.stackPointerOffset)


class MIPSMachine:


