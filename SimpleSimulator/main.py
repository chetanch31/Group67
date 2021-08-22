import binary

FLAG='000000'

# 0001000100000101

def get_type(reg, bin):
    for key, value in reg.items():
        if value == bin:
            return True

    return False

def checkTypeA(cmd, reg):
    r1 = binary.registers(cmd[7:10])
    r2 = binary.registers(cmd[10:13])
    r3 = binary.registers(cmd[13:16])
    
    if binary.typeA['add'] == cmd[:5]:
        reg[r1] = reg[r2] + reg[r3]

    elif binary.typeA['sub']==cmd[:5]:
        reg[r1] = reg[r2] - reg[r3]

    elif binary.typeA['mul']==cmd[:5]:
        reg[r1] = reg[r2] * reg[r3]

    elif binary.typeA['xor']==cmd[:5]:
        reg[r1] = reg[r2] ^ reg[r3]

    elif binary.typeA['or']==cmd[:5]:
        reg[r1] = reg[r2] | reg[r3]

    elif binary.typeA['and']==cmd[:5]:
        reg[r1] = reg[r2] & reg[r3]

def checkTypeB(cmd,reg,bin_reg):
    
    r1 = binary.registers(cmd[5:8])
    r2 = binary.registers(cmd[8:16])

    if binary.typeB['mov'] == cmd[:5]:
        reg[r1] = int(cmd[8:16],2)

    elif binary.typeB['ls'] == cmd[:5]:
        reg[r1] = (2**int(cmd[8:16],2))*reg[r1]

    elif binary.typeB['rs'] == cmd[:5]:
        reg[r1] = reg[r1] / (2**int(cmd[8:16],2))


def checkTypeC(cmd,reg):

    r1 = binary.registers(cmd[10:13])
    r2 = binary.registers(cmd[13:16])

    if binary.typeC['mov']==cmd[:5]:
        reg[r1]=reg[r2]

    elif binary.typeC['div']==cmd[:5]:
        reg[r1]=reg[r1] / reg[r2]
        reg[r1]=reg[r1] % reg[r2]

    elif binary.typeC['cmp']==cmd[:5]:

        if reg[r1]==reg[r2]:
            FLAG ='000001'

        elif reg[r1]>reg[r2]:
            FLAG = '000010'

        elif reg[r1]<reg[r2]:
            FLAG = '000100'

        reset = False

   # elif binary.typeC['not']==cmd[:5]:

def main():
    usr_input=[]
    final_output = []
    mem_dump = ["0"*16 for i in range(256)]
    reg = {'R1' : 0 ,'R2' : 0 ,'R3' : 0 ,'R4' : 0,'R5' : 0,'R6' : 0}

    while True:
        try:
            line = input()
        except EOFError:
            break

        usr_input.append(line)

    for cmd in usr_input:
        
        if get_type(binary.typeA, cmd[:5]):
            checkTypeA(cmd, reg)

        elif get_type(binary.typeB, cmd[:5]):
            checkTypeB(cmd, reg)
        
        elif get_type(binary.typeC, cmd[:5]):
            checkTypeC(cmd, reg)
            
        else:
            print("Not Valid")


if __name__ == '__main__':
    main()

