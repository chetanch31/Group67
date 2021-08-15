import binary

FLAGS='0'
reset = False

def checkTypeA(cmd, lst, reg_values):

    bin = ""

    if len(cmd) != 4:
        print("SyntaxError: Not all required paramters provided for Type A command")
        quit()

    
    for reg in cmd[1:]:
        if reg not in binary.registers:
            print("Invalid register used")
            quit()

    #updates register values
    if cmd[0] == "add":
        reg_values[cmd[1]] = reg_values[cmd[2]] + reg_values[cmd[3]]
    elif cmd[0] == "sub":
        reg_values[cmd[1]] = reg_values[cmd[2]] - reg_values[cmd[3]]
    elif cmd[0] == "mul":
        reg_values[cmd[1]] = reg_values[cmd[2]] * reg_values[cmd[3]]
    elif cmd[0] == "xor":
        reg_values[cmd[1]] = reg_values[cmd[2]] ^ reg_values[cmd[3]]
    elif cmd[0] == "or":
        reg_values[cmd[1]] = reg_values[cmd[2]] | reg_values[cmd[3]]
    else:
        reg_values[cmd[1]] = reg_values[cmd[2]] & reg_values[cmd[3]]
        
    #generates and prints the binary value of the given command
    bin += binary.typeA[cmd[0]]
    bin += "00" 
    bin += binary.registers[cmd[1]] + binary.registers[cmd[2]] + binary.registers[cmd[3]]

    lst.append(bin)

def checkTypeB(cmd, lst, reg_values):

    bin = ""
    
    if len(cmd) != 3:
        print("SyntaxError: Not all required paramters provided for Type B command")
        quit()


    if cmd[2][0] != "$" and cmd[1][0] == "R":
        checkTypeC(cmd, lst, reg_values)
    elif cmd[1][0] != "R":
        print("Syntax Error")
        quit()
    else:
        x=int(cmd[-1][1:])
        if x<0 or x>255:
            print('Syntax error: Illegal Immediate values')
            quit()
        
        if cmd[1] not in binary.registers:
            print("Invalid register used")
            quit()

        reg_values[cmd[1]] = x

        bin += binary.typeB[cmd[0]]
        bin += binary.registers[cmd[1]]
        bin += str(format(x, '08b'))

        lst.append(bin)


def checkTypeC(cmd, lst,reg_values):
    
    bin = ''

    if len(cmd) != 3:
        print("SyntaxError: Not all required paramters provided for Type C command")
        quit()


    if cmd[2] == "FLAGS":
        bin += binary.typeC[cmd[0]]
        bin += '00000'
        bin += binary.registers[cmd[1]] + binary.flag[cmd[2]]
    
    else:
        for i in (1,len(cmd)-1):
            if cmd[i] not in binary.registers:
                print("Invalid registers used")
                quit()

        if cmd[0]=='mov':
            reg_values[cmd[1]]=reg_values[cmd[2]]

        bin += binary.typeC[cmd[0]]
        bin += '00000'
        bin += binary.registers[cmd[1]] + binary.registers[cmd[2]]

    lst.append(bin)

def checkTypeD(cmd, lst, labels, reg_values, variables):


    bin = ""

    if len(cmd)!=3:
        print("SyntaxError: Not all required parametrs provided for Type D command")
    
        quit()
    
    if cmd[1] not in binary.registers:
        print("Invalid register used")
        quit()    

    if cmd[-1] not in variables.keys():
        print('SytaxError: Misuse of variables')
        quit()
        
    if cmd[0]=='ld':
        reg_values[cmd[1]]=variables[cmd[-1]]
    

    bin += binary.typeD[cmd[0]]
    bin += binary.registers[cmd[1]]
    bin += format(variables[cmd[-1]], "08b")

    lst.append(bin)

def checkTypeE(cmd, lst, labels):

    bin=''
    if len(cmd)!=2:
        print("SyntaxError : Wrong syntax used for instructions")
        quit()

    if cmd[1] not in labels:
        print("SytaxError: Label not defined")
        quit()
    
    bin+=binary.typeE[cmd[0]]
    bin+='000'
    bin+=labels[cmd[1]]

    lst.append(bin)

def checkTypeF(cmd, lst):
    print("SyntaxError: hlt statement encountered between code")
    quit()


def check_cmp(cmd, val):

    global reset
    
    if val[cmd[1]] == val[cmd[2]]:
        FLAGS = '000001'
    elif val[cmd[1]]>val[cmd[2]]:
        FLAGS='000010'
    elif val[cmd[1]]<val[cmd[2]]:
        FLAGS='000100'
    else:
        FLAGS='001000'
        
    reset = True

    
def main():

    global reset, FLAGS 

    usr_inp = [] #Holds the input values
    instructions = [] #Holds the instructions to be expected
    labels = {} #holds label address
    reg_values = {"R1" : 0, "R2" : 0, "R3" : 0, "R4" : 0, "R5" :0, "R6" : 0}
    variables = {} #store the values of variables
    cmd_enc = False #Pointer to check if var anywhere other than top

    final_out = []

    '''while True:
        line = input()
        if line == '':
            break
        usr_inp.append(line)'''

    while True:
        try:
            line = input()
        except EOFError:
            break
        usr_inp.append(line)

    if usr_inp[-1]=='hlt' or usr_inp[-1][-3:]=='hlt':
        pass
    else:
        print('SyntaxError : No hlt statement')
        return

    for i in range(len(usr_inp)-1):
        instructions.append(usr_inp[i].split(" "))

        temp = usr_inp[i].split(" ")[0]
        if temp[-1] == ":":
            labels[usr_inp[i].split(" ")[0][:-1]] = 0

    level= -1 #to track where the label occurs

    for i in usr_inp:
        cmd = i.split(" ") 
         
        if cmd[0] != 'var':
            level = level + 1

        if cmd[0][-1]==':':
            labels[cmd[0][:-1]] = format(level,'08b')

    line=0
    for i in instructions:
        if i[0]!='var':
            line=line+ 1

    for i in instructions:
        if i[0]=='var':
            if len(i)==2:
                variables[i[1]]=0
  
    for i in variables.keys():
        line=line+1
        variables[i]=line

            

    for cmd in instructions:
        
        if reset == False:
            FLAGS='000000'

        if cmd[0] == "var":
            if cmd_enc!=False:
                print("SyntaxError: Variable not declared on top")
                quit()

        elif cmd[0] == "cmp":
            cmd_enc = True
            check_cmp(cmd, reg_values)
            checkTypeC(cmd, final_out, reg_values)
            
        elif cmd[0] in binary.typeA:
            cmd_enc = True
            checkTypeA(cmd, final_out, reg_values)
            reset=False

        elif cmd[0] in binary.typeB: 
            cmd_enc = True
            checkTypeB(cmd, final_out, reg_values)
            reset = False

        elif cmd[0] in binary.typeC: 
            cmd_enc = True
            checkTypeC(cmd, final_out, reg_values)
            reset = False

        elif cmd[0] in binary.typeD: 
            cmd_enc = True
            checkTypeD(cmd, final_out, labels, reg_values, variables)
            reset = False

        elif cmd[0] in binary.typeE: 
            cmd_enc = True
            checkTypeE(cmd, final_out, labels)
            reset= False

        elif cmd[0] in binary.typeF: 
            cmd_enc = True
            checkTypeF(cmd, final_out)
            reset=False
        
        elif cmd[0][:-1] in labels:
            emd_enc = True
            if cmd[1] == "hlt":
                pass
            elif cmd[1] in binary.typeA:
                checkTypeA(cmd[1:], final_out, reg_values)
            elif cmd[1] in binary.typeB:
                checkTypeB(cmd[1:], final_out, reg_values)
            elif cmd[1] in binary.typeC:
                checkTypeC(cmd[1:], final_out, reg_values)
            elif cmd[1] in binary.typeD:
                checkTypeD(cmd[1:], final_out, labels, reg_values)
            elif cmd[1] in binary.typeE:
                checkTypeE(cmd[1:],final_out)
            else:
                print("Syntax Error: undefined label")
                return

        else:
            print(f"Invalid Sytnax: Unexpected instruction type: {cmd[0]}")
            return

    final_out.append("1001100000000000")
    
    for out in final_out:
        print(out)

if __name__ == '__main__':
    main()
