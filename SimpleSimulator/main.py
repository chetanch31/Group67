import binary
import matplotlib.pyplot as plt

def get_type(reg, bin):
    for key, value in reg.items():
        if value == bin:
            return True
    return False

def checkTypeA(cmd, reg):
    

    r1 = binary.registers[cmd[7:10]]
    r2 = binary.registers[cmd[10:13]]
    r3 = binary.registers[cmd[13:16]]
    
    if binary.typeA['add'] == cmd[:5]:
        reg[r1] = reg[r2] + reg[r3]

    elif binary.typeA['sub'] == cmd[:5]:
        reg[r1] = reg[r2] - reg[r3]

    elif binary.typeA['mul'] == cmd[:5]:
        reg[r1] = reg[r2] * reg[r3]

    elif binary.typeA['xor'] == cmd[:5]:
        reg[r1] = reg[r2] ^ reg[r3]

    elif binary.typeA['or'] == cmd[:5]:
        reg[r1] = reg[r2] | reg[r3]

    elif binary.typeA['and'] == cmd[:5]:
        reg[r1] = reg[r2] & reg[r3]


    if reg[r1] >256 or reg[r1] < 0:
         reg['FLAGS'] = 8

def checkTypeB(cmd,reg):
    
    
    r1 = binary.registers[cmd[5:8]]
    n1 = cmd[8:16]

    if binary.typeB['mov'] == cmd[:5]:
        reg[r1] = int(n1,2)

    elif binary.typeB['ls'] == cmd[:5]:
        reg[r1] = (2**int(n1,2))*reg[r1]

    elif binary.typeB['rs'] == cmd[:5]:
        reg[r1] = reg[r1] / (2**int(n1,2))

def checkTypeC(cmd, reg):

    r1 = binary.registers[cmd[10:13]]
    r2 = binary.registers[cmd[13:16]]

    if cmd[:5] == binary.typeC['mov']:
        reg[r1] = reg[r2]


    elif cmd[:5] == binary.typeC['div']:
        reg['R0'] = reg[r1] // reg[r2] #stores quotient in R0
        reg['R1'] = reg[r1] % reg[r2] #stores remainder in R1
    
    else:
        reg[r1] = int(NOT(r2),2)


def checkTypeD(cmd, reg, mem_dmp):
 
    r1 = binary.registers[cmd[5:8]]

    if cmd[:5] == binary.typeD['ld']:
        reg[r1] =int(mem_dmp[int(cmd[8:16],2)],2)
    else:
        mem_dmp[int(cmd[8:16],2)] = format(reg[r1],'016b')
        
def checkTypeE(cmd, reg, mem_dmp):

    label_cmd = int(cmd[8:],2)

    if mem_dmp[label_cmd][:5] in binary.typeA:
        checkTypeA(mem_dmp[label_cmd], reg) 
    
    elif mem_dmp[label_cmd][:5] in binary.typeB:
        checkTypeB(mem_dmp[label_cmd], reg)
        
    
    elif mem_dmp[label_cmd][:5] in binary.typeC:
        checkTypeC(mem_dmp[label_cmd], reg)
        
    
    elif mem_dmp[label_cmd][:5] in binary.typeD:
       checkTypeD(mem_dmp[label_cmd], reg)

    else:
        pass    


def NOT(x):
    N=''
    for i in x :
        if i == '1' :
            N += '0'
        else :   
            N += '1'
    return N

def plotGraph(x, y):
    #X : program counter
    #Y : memory address
    
    plt.scatter(x, y)
    plt.xlabel("Cycle Number")
    plt.ylabel("Memory address")
    plt.savefig('bonus_question.png')
    

def main():
    usr_inp = []
    mem_dmp = ['0'*16 for i in range(256)]
    reg = {'R0':0,'R1': 0,'R2':0, 'R3':0, 'R4':0, 'R5':0, 'R6':0, 'FLAGS':0}

    x = []
    y = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        usr_inp.append(line)

    reset = True
    PC = -1 

    for indc, cmd in enumerate(usr_inp):
        
        mem_dmp[indc] = cmd

        if cmd[:5] == binary.typeC['cmp']:
        
            r1 = binary.registers[cmd[10:13]]
            r2 = binary.registers[cmd[13:16]]
                    
            if reg[r1] == reg[r2]:
                reg['FLAGS'] = 1
            elif reg[r1] > reg[r2]:
                reg['FLAGS'] = 2
            else:
                reg['FLAGS'] = 4

            reset = False

        elif get_type(binary.typeA, cmd[:5]):
            checkTypeA(cmd, reg)
            reset = True

        elif get_type(binary.typeB, cmd[:5]):
            checkTypeB(cmd, reg)
            reset = True
        
        elif get_type(binary.typeC, cmd[:5]):
            checkTypeC(cmd, reg)
            reset = True

        elif get_type(binary.typeD, cmd[:5]):
            checkTypeD(cmd, reg, mem_dmp)
            reset = True
        
        elif get_type(binary.typeE, cmd[:5]):
            checkTypeE(cmd, reg, mem_dmp)
            reset = True

        else:
            reset = True

        if reset == True:
            reg['FLAGS'] = 0

        PC += 1

        fin = ''
        fin += format(PC, '08b') + ' '
        for i in reg.keys():
            fin += format(reg[i], "016b") + " "

        print(fin)

        

        if get_type(binary.typeD, cmd[:5]) or get_type(binary.typeE, cmd[:5]):
            y.append(PC)
            y.append(int(cmd[8:],2))
            x.append(PC)
            x.append(PC)
        else:
            y.append(PC)
            x.append(PC)

    for mem in mem_dmp:
        print(mem)

   
    plotGraph(x, y)

if __name__ == '__main__':
    main()



