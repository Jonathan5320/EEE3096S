//Define the ALU testbench module
module ALU_tb();
  //inputs
  reg clk;
  reg [7:0] A,B;
  reg [3:0] ALU_Sel;
  // output
  wire [7:0] ALU_Out; 
  integer i;
//Instantiate the design under test
ALU dut(
    .clk(clk),
    .A(A),
    .B(B),
    .ALU_Sel(ALU_Sel),
  .ALU_Out(ALU_Out));

initial begin //Initial means this only happens once
  $display("A         B         ALU_Sel  ALU_Out");
  $monitor("%b  %b  %b     %b",A,B,ALU_Sel, ALU_Out);
  $dumpfile("dump.vcd");
  $dumpvars;
    clk = 1'b1;
    A = 8'b10110001;
    B = 8'b00100000;
    ALU_Sel = 4'b0000;
    #5
    clk = !clk;
  for(i=0; i<15; i++)
    begin
      ALU_Sel = ALU_Sel + 4'b0001;
      clk = !clk;
      #5
      clk = !clk;
    end
  end
endmodule