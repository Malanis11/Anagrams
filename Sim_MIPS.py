import math

def process2Comp(string):
    imm = int(string,2)
    return imm


def simulate(I):
    PC = 0                                # Program counter
    Memory = [0 for i in range(80)]       # Initialize memory array
    Register = [ 0 for i in range(8)]    # Initialize register 8-23
    finished = False
    print("***Simulation started***")
    while(not(finished)):
        Register[0] = 0     # Let's enforce $0 here
        fetch = I[PC]
        if (fetch == "00010000000000001111111111111111"):   # END instruction
            finished = True
            print("***Simulation finished***")
        elif(fetch[0:4] == "001101]]"):   # ORI instruction
            imm = int(fetch[16:32],2)
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  ori $" + str(Rt) + ",$" + str(Rs) + "," + str(imm))
            Register[Rt] = Register[Rs] | imm
            PC += 4
            print("  result: $" + str(Rt) + "=" + str(Register[Rt]))

        elif(fetch[0:3] == "010"):   #ADDI 
            imm = process2Comp(fetch[6:8])
            Rx = int(fetch[3:6],2)
            print("PC " + str(PC) + ":  addi $" + str(Rx) + ", " +  str(imm))
            if(imm == 0):
                Register[Rx] = 0
            else:
                Register[Rx] = Register[Rx] + imm
            PC += 1
            print("  result: $" + str(Rt) + "=" + str(Register[Rt]))

        elif(fetch[0:4] == "0111"):  #SUB 
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print("PC " + str(PC) + ":  sub $" + str(Rx) + ",$" + str(Rx) + ",$" + str(Ry))
            Register[Rx] = Register[Rx] - Register[Ry]
            PC += 1
            print("  result: $" + str(Rx) + "=" + str(Register[Rx]))

        elif(fetch[0:6] == "000100"):   #BEQ 
            offset = process2Comp(fetch[16:32])
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  beq $" + str(Rs) + ",$" + str(Rt) + "," + str(offset))
            if (Register[Rs] == Register[Rt]):
                PC = PC + 4 + (4*offset)
                print("  result: branch Taken")
            else:
                PC = PC + 4
                print("  result: branch Not Taken")

#this is where we do it
        elif(fetch[0:6] == "000000" and fetch[26:32] == "100001"):    #ADDU instruction
            Rd = int(fetch[16:21],2)
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  addu $" + str(Rd) + ",$" + str(Rs) + ",$" + str(Rt))
            Register[Rd] = Register[Rs] + Register[Rt]
            PC += 4
            print("  result: $" + str(Rd) + "=" + str(Register[Rd]))

        elif(fetch[0:3] == "011"):   #SLT
            Rx = int(fetch[16:21],2)
            Ry = int(fetch[6:11],2)
            Rz = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  slt $" + str(Rz) + ",$" + str(Rx) + ",$" + str(Ry))
            if (Register[Rx] < Register[Ry]):
                Register[Rz] = 1
                PC += 1
                print("  result: $" + str(Rz) + "=" + str(Register[Rz]))
            else:
                Register[Rz] = 0
                PC += 1
                print("  result: $" + str(Rz) + "=" + str(Register[Rz]))

        elif(fetch[0:4] == "1010"):   #AND
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)

            print("PC " + str(PC) + ":  and $" + str(Rx) + ",$" + str(Rx) + ",$" + str(Ry))
            Register[Rx] = Register[Rx] & Register[Ry]
            PC += 1
            print("  result: $" + str(Rx) + "=" + str(Register[Rx]))

        elif(fetch[0:6] == "000101"):  #BNE
            offset = process2Comp(fetch[16:32])
            Rs = int(fetch[6:11], 2)
            Rt = int(fetch[11:16], 2)

            if(Register[Rs] != Register[Rt]):
                PC+= offset * 4

            else:
                PC+= 4
                print("  result: $" + str(Rd) + "=" + str(Register[Rd]))

        elif(fetch[0:4] == "1001"):  #SW 
           Rx = int(fetch[4:6], 2)
           Ry = int(fetch[6:8], 2)
           PC += 1
           print("SW $" + str(Rx) + ", " + "($" + str(Ry) + ")")
           Index = ((offset + Register[Rs]) - 8192)
           Register[Rt] = Memory[Index]


        elif(fetch[0:4] == "0111"):  #LW 
           offset = process2Comp(fetch[16:32])
           Rx = int(fetch[4:6], 2)
           Ry = int(fetch[6:8], 2)
        
           print("PC " + str(PC) + ":  lw $" + str(Rx) + ", " + "($" + str(Ry) + ")")
           Index = ((offset + Register[Rx]) - 8192)
           Register[Rx] = Memory[Index]
           PC += 1
          
        elif(fetch[0:3] == "110"):  #SLL 
           Rx = int(fetch[3:5], 2)
           shift = int(fetch[5:8], 2)
           print("PC " + str(PC) + ":  sll $" + str(Rx) + ", $" + str(Rx) + ", " + str(shift))
           Register[Rx] = int(math.floor(Register[Rx] * (pow(2,shift))))
           PC += 1
           print("  result: $" + str(Rx) + "=" + str(Register[Rx]))

        elif(fetch[0:3] == "111"):  #SRL 
           Rx = int(fetch[3:5], 2)
           shift = int(fetch[5:8], 2)
           print("PC " + str(PC) + ":  srl $" + str(Rd) + ", $" + str(Rt) + ", " + str(shift))
           Register[Rd] = Register[Rt] >> shift
           PC += 1
           print("  result: $" + str(Rd) + "=" + str(Register[Rd]))

        elif(fetch[0:6] == "000010"):   #J 
           imm = int(fetch[6:32], 2)
           print(imm)
           print("PC " + str(PC) + ":  j " + str(imm))
           PC = ((PC & 0xF0000000) | (imm << 2))

        elif(fetch[0:6] == "001100"):   #ANDI 
           imm = process2Comp(fetch[16:32])
           Rs = int(fetch[6:11],2)
           Rt = int(fetch[11:16],2)
           print("PC " + str(PC) + ":  andi $" + str(Rt) + ",$" + str(Rs) + ", " + str(imm))
           Register[Rt] = Register[Rs] and imm
           PC += 4
           print("  result: $" + str(Rt) + "=" + str(Register[Rt]))

        elif(fetch[0:4] == "1011"):   #ADD
           Rd = int(fetch[16:21],2)
           Rs = int(fetch[6:11],2)
           Rt = int(fetch[11:16],2)
           print("PC " + str(PC) + ":  and $" + str(Rt) + ",$" + str(Rs) + ", " + str(imm))
           Register[Rd] = Register[Rs] + Register[Rt]
           PC += 4
           print("  result: $" + str(Rd) + "=" + str(Register[Rd]))

        else:
            print("Instruction not supported. Exiting")
            exit()

    print("\nRegister contents: ")
    for i in range(24):
        print("$" + str(i) + ": " + str(Register[i]))
    print("Memory contents: ", Memory)


def main():
    filename = "myfile.txt"
    print("Reading in machine code from " + filename)
    file = open(filename,"r")
    I = []                                  # Instructions to execute
    for line in file:
        if (line == "\n" or line[0] == "#" ):
            continue    # Skip empty lines and comments
        instr = bin(int(line[2:10],16))[2:].zfill(32)
        #  'zfill' pads the string with 0's to normalize instruction's length of 32
        I.append(instr)
        I.append(0)     # Since PC increments by 4,  let's fill
        I.append(0)     # null spaces with 0's to align correct
        I.append(0)     # address

    simulate(I)

if __name__ == "__main__":
    main()