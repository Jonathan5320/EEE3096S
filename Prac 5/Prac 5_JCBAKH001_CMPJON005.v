//Define the module
module ALU(
  input clk,
  input [7:0] A,B,
  input [3:0] ALU_Sel,
  output reg [7:0] ALU_Out
);

reg [7:0] ALU_result;

always@(posedge clk) //Triggered on rising edge clock
    begin
		ALU_result = 8'b00000101;// sets initial value 0b00000101
        case(ALU_Sel)
            4'b0000:  //ADD 0000 Acc = A + B
                ALU_result = A + B;
            
            4'b0001:  //SUB 0001 Acc = A - B
                ALU_result = A - B;

            4'b0010:  //MUL 0010 Acc = A * B
                ALU_result = B * A;
            
            4'b0011:  //DIV 0011 Acc = A / B
                ALU_result = A / B;
            
            4'b0100:  //ADDA 0100 Acc = Acc + A
                ALU_result += A;
          
            4'b0101:  //MULA 0101 Acc = Acc * A
                ALU_result *= A;
          
            4'b0110:  //MAC 0110 Acc = Acc + (A * B)
			    //ALU_result = 8'b00000101;
                ALU_result += (A * B);
          
            4'b0111:  //ROL 0111 Acc = A rotated left by 1
                ALU_result = {A[6:0],A[7]};
          
            4'b1000:  //ROR 1000 Acc = A rotated right by 1
                ALU_result = {A[0],A[7:1]};

            4'b1001:  //AND 1001 Acc = A and B
                ALU_result = A & B;

            4'b1010:  //OR 1010 Acc = A or B
                ALU_result = A | B;

            4'b1011:  //XOR 1011 Acc = A xor B
                ALU_result = A ^ B;

            4'b1100:  //NAND 1100 Acc = A nand B
                ALU_result = ~(A & B);

            4'b1101:  //ETH 1101 Acc = 0xFF is A=B else 0
                ALU_result = (A==B)?8'b11111111:8'b00000000;
			
            4'b1110:  //GTH 1110 Acc = 0xFF if A>B else 0
              //ALU_result = (A<B)?8'b11111111:8'b00000000;
              if (A>B)
                  ALU_result =8'b11111111;
                else 
                  ALU_result =8'b00000000;
          
            4'b1111:  //LTH 1111 Acc = 0xFF if A<B else 0
              //ALU_result = (B<A)?8'b11111111:8'b00000000;
              if (A<B)
                  ALU_result =8'b11111111;
                else 
                  ALU_result =8'b00000000;
          
          default: ALU_result = A;
        endcase
      ALU_Out <= ALU_result;
    end    
endmodule
