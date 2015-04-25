
`timescale 1ps/1fs 

`ifndef VTRACE_LEVEL
 `define VTRACE_LEVEL 0
`endif

`ifndef VTRACE_MODULE
 `define VTRACE_MODULE tb_elink
`endif

module tb_elink;

    reg clock;
    reg reset;
    reg keep_alive;
    
    reg [103:0] elink_txrr_packet;
    wire 	elink_txo_lclk_p;
    wire 	elink_chip_resetb;
    reg 	elink_rxrr_wait;
    wire 	elink_txrd_wait;
    wire 	elink_rxwr_access;
    wire 	elink_cclk_p;
    reg 	elink_rxrd_wait;
    wire 	elink_cclk_n;
    wire 	elink_rxrr_access;
    reg 	elink_txwr_clk;
    wire [3:0] 	elink_rowid;
    reg 	elink_txwr_access;
    wire [3:0] 	elink_colid;
    wire 	elink_txo_lclk_n;
    reg 	elink_rxwr_clk;
    wire [103:0] elink_rxrr_packet;
    reg 	 elink_rxi_frame_n;
    reg [7:0] 	 elink_rxi_data_n;
    reg 	 elink_clkin;
    reg 	 elink_txrr_access;
    reg 	 elink_hard_reset;
    reg 	 elink_txi_rd_wait_p;
    reg 	 elink_rxrd_clk;
    wire 	 elink_txo_frame_n;
    reg [103:0]  elink_txrd_packet;
    reg 	 elink_txi_rd_wait_n;
    reg 	 elink_txi_wr_wait_p;
    reg 	 elink_txrd_clk;
    reg [7:0] 	 elink_rxi_data_p;
    reg 	 elink_rxi_frame_p;
    wire [7:0] 	 elink_txo_data_n;
    reg 	 elink_txrd_access;
    wire 	 elink_rxo_rd_wait_p;
    reg 	 elink_rxrr_clk;
    wire [103:0] elink_rxwr_packet;
    wire 	 elink_rxo_rd_wait_n;
    wire 	 elink_mailbox_not_empty;
    reg 	 elink_txi_wr_wait_n;
    wire 	 elink_mailbox_full;
    wire 	 elink_txwr_wait;
    wire [7:0] 	 elink_txo_data_p;
    wire 	 elink_txo_frame_p;
    reg 	 elink_rxwr_wait;
    wire [103:0] elink_rxrd_packet;
    reg 	 elink_rxi_lclk_p;
    wire 	 elink_rxo_wr_wait_p;
    wire 	 elink_txrr_wait;
    reg [2:0] 	 elink_clkbypass;
    wire 	 elink_rxrd_access;
    reg [103:0]  elink_txwr_packet;
    wire 	 elink_rxo_wr_wait_n;
    reg 	 elink_txrr_clk;
    reg 	 elink_rxi_lclk_n;


`ifdef VTRACE		
    initial begin
	$dumpfile("vcd/_tb_elink.vcd");
	$dumpvars(`VTRACE_LEVEL, `VTRACE_MODULE);
    end
`endif    

    
    initial begin
	$from_myhdl
	  (
	   clock,
	   reset,
	   elink_txrr_packet,
           elink_rxrr_wait,
           elink_rxrd_wait,
           elink_txwr_clk,
           elink_txwr_access,
           elink_rxwr_clk,
           elink_rxi_frame_n,
           elink_rxi_data_n,
           elink_clkin,
           elink_txrr_access,
           elink_hard_reset,
           elink_txi_rd_wait_p,
           elink_rxrd_clk,
           elink_txrd_packet,
           elink_txi_rd_wait_n,
           elink_txi_wr_wait_p,
           elink_txrd_clk,
           elink_rxi_data_p,
           elink_rxi_frame_p,
           elink_txrd_access,
           elink_rxrr_clk,
           elink_txi_wr_wait_n,
           elink_rxwr_wait,
           elink_rxi_lclk_p,
           elink_clkbypass,
           elink_txwr_packet,
           elink_txrr_clk,
           elink_rxi_lclk_n
	   );
	$to_myhdl
	  (
	   keep_alive,
	   elink_txo_lclk_p,
           elink_chip_resetb,
           elink_txrd_wait,
           elink_rxwr_access,
           elink_cclk_p,
           elink_cclk_n,
           elink_rxrr_access,
           elink_rowid,
           elink_colid,
           elink_txo_lclk_n,
           elink_rxrr_packet,
           elink_txo_frame_n,
           elink_txo_data_n,
           elink_rxo_rd_wait_p,
           elink_rxwr_packet,
           elink_rxo_rd_wait_n,
           elink_mailbox_not_empty,
           elink_mailbox_full,
           elink_txwr_wait,
           elink_txo_data_p,
           elink_txo_frame_p,
           elink_rxrd_packet,
           elink_rxo_wr_wait_p,
           elink_txrr_wait,
           elink_rxrd_access,
           elink_rxo_wr_wait_n
	   );
    end

    reg toggle = 0;
    always @(posedge clock) begin
	toggle <= ~toggle;
    end

    initial begin
	forever begin
	    #100 keep_alive <= ~keep_alive;
	end
    end
    
    // ELink design-under-test
    defparam dut.ELINKID = 12'h800;
    elink 
      dut(
	  .hard_reset        ( elink_hard_reset       ) ,	  
          .clkin             ( elink_clkin            ) ,
	  .clkbypass         ( elink_clkbypass        ) ,
      
	  .rowid             ( elink_rowid            ) ,
	  .colid             ( elink_colid            ) ,	  
	  .chip_resetb       ( elink_chip_resetb      ) ,
          .cclk_p            ( elink_cclk_p           ) ,
	  .cclk_n            ( elink_cclk_n           ) ,
      
	  .rxi_lclk_p        ( elink_rxi_lclk_p       ) ,	  
	  .rxi_lclk_n        ( elink_rxi_lclk_n       ) ,
	  .rxi_data_n        ( elink_rxi_data_n       ) ,
	  .rxi_data_p        ( elink_rxi_data_p       ) ,
	  .rxi_frame_p       ( elink_rxi_frame_p      ) ,
	  .rxi_frame_n       ( elink_rxi_frame_n      ) ,
	  .rxo_wr_wait_p     ( elink_rxo_wr_wait_p    ) ,
	  .rxo_wr_wait_n     ( elink_rxo_wr_wait_n    ) ,	  
	  .rxo_rd_wait_p     ( elink_rxo_rd_wait_p    ) ,
          .rxo_rd_wait_n     ( elink_rxo_rd_wait_n    ) ,
      
	  .txo_lclk_p        ( elink_txo_lclk_p       ) ,
	  .txo_lclk_n        ( elink_txo_lclk_n       ) ,
	  .txo_data_p        ( elink_txo_data_p       ) ,
	  .txo_data_n        ( elink_txo_data_n       ) ,
	  .txo_frame_n       ( elink_txo_frame_n      ) ,
	  .txo_frame_p       ( elink_txo_frame_p      ) ,
      
      
	  .txi_wr_wait_p     ( elink_txi_wr_wait_p    ) ,
	  .txi_wr_wait_n     ( elink_txi_wr_wait_n    ) ,
	  .txi_rd_wait_p     ( elink_txi_rd_wait_p    ) ,
	  .txi_rd_wait_n     ( elink_txi_rd_wait_n    ) ,

          .mailbox_full      ( elink_embox_full       ) ,
	  .mailbox_not_empty ( elink_embox_not_empty  ) ,	  

          .rxwr_clk          ( elink_rxwr_clk         ) ,	  
	  .rxwr_access       ( elink_rxwr_access      ) ,
          .rxwr_packet       ( elink_rxwr_packet      ) ,  
          .rxwr_wait         ( elink_rxwr_wait        ) ,

          .rxrd_clk          ( elink_rxrd_clk         ) ,	  
          .rxrd_access       ( elink_rxrd_access      ) ,
          .rxrd_packet       ( elink_rxrd_packet      ) ,
	  .rxrd_wait         ( elink_rxrd_wait        ) ,

          .rxrr_clk          ( elink_rxrr_clk         ) ,
	  .rxrr_access       ( elink_rxrr_access      ) ,
          .rxrr_packet       ( elink_rxrr_packet      ) ,     	  
          .rxrr_wait         ( elink_rxrr_wait        ) ,	  	   		     

	  .txwr_clk          ( elink_txwr_clk         ) ,	            
          .txwr_access       ( elink_txwr_access      ) ,
          .txwr_packet       ( elink_txwr_packet      ) ,
          .txwr_wait         ( elink_txwr_wait        ) ,


	  .txrd_clk          ( elink_txrd_clk         ) ,
          .txrd_access       ( elink_txrd_access      ) ,
          .txrd_packet       ( elink_txrd_packet      ) ,	  
	  .txrd_wait         ( elink_txrd_wait        ) ,

	  .txrr_clk          ( elink_txrr_clk         ) ,	  	  	  
          .txrr_access       ( elink_txrr_access      ) ,	  		     
	  .txrr_packet       ( elink_txrr_packet      ) ,	 
          .txrr_wait         ( elink_txrr_wait        ) 	  		               		     			  	            
	  );

endmodule
