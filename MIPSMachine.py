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
    def verifyRegister(self, register, variableName):
        if register not in self.register_names:
            raise RegisterNotDefined(register)
        else:
            if self.registers[register] == variableName:
                return True
            else:
                return False

class MIPStack:
    

class MIPSMachine:
    
