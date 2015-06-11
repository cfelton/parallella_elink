
`timescale 1ps/1fs 

`ifndef VTRACE_LEVEL
 `define VTRACE_LEVEL 0
`endif

`ifndef VTRACE_MODULE
 `define VTRACE_MODULE tb_elink
`endif


module tb_elink;

    // manually added signals
    reg clock;
    reg reset;
    reg keep_alive;

    // auto-generated from extract ports (since been modified)
    reg          elink_reset;       
    reg 	 elink_sys_clk;
    reg 	 elink_tx_lclk;
    reg 	 elink_tx_lclk90;
    reg 	 elink_tx_lclk_div4;
    reg 	 elink_rx_lclk;
    reg 	 elink_rx_lclk_div4;
    reg 	 elink_rx_ref_clk;
    wire   	 elink_rx_lclk_pll;       
    wire 	 elink_en;
    wire [11:0]  elink_chipid;
    
    reg 	 elink_rxi_lclk_p;
    reg 	 elink_rxi_lclk_n;
    reg [7:0] 	 elink_rxi_data_p;
    reg [7:0] 	 elink_rxi_data_n;
    reg 	 elink_rxi_frame_p;
    reg 	 elink_rxi_frame_n;

    wire 	 elink_rxo_wr_wait_p;
    wire 	 elink_rxo_wr_wait_n;
    wire 	 elink_rxo_rd_wait_p;
    wire 	 elink_rxo_rd_wait_n;

    wire 	 elink_txo_lclk_p;
    wire 	 elink_txo_lclk_n;
    wire [7:0] 	 elink_txo_data_p;
    wire [7:0] 	 elink_txo_data_n;
    wire 	 elink_txo_frame_p;
    wire 	 elink_txo_frame_n;

    reg 	 elink_txi_wr_wait_p;
    reg 	 elink_txi_wr_wait_n;
    reg 	 elink_txi_rd_wait_p;
    reg 	 elink_txi_rd_wait_n;


    wire 	 elink_rxwr_access;
    wire [103:0] elink_rxwr_packet;
    reg 	 elink_rxwr_wait;

    wire 	 elink_rxrd_access;
    wire [103:0] elink_rxrd_packet;
    reg 	 elink_rxrd_wait;

    wire 	 elink_rxrr_access;
    wire [103:0] elink_rxrr_packet;
    reg 	 elink_rxrr_wait;

    reg 	 elink_txwr_access;
    reg [103:0]  elink_txwr_packet;
    wire 	 elink_txwr_wait;

    reg 	 elink_txrd_access;
    reg [103:0]  elink_txrd_packet;
    wire 	 elink_txrd_wait;

    reg 	 elink_txrr_access;
    reg [103:0]  elink_txrr_packet;
    wire 	 elink_txrr_wait;

    wire 	 elink_mailbox_full;
    wire 	 elink_mailbox_not_empty;
    wire         elink_timeout;


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

	   elink_reset,
	   elink_sys_clk,
	   elink_tx_lclk,
	   elink_tx_lclk90,
	   elink_tx_lclk_div4,
	   elink_rx_lclk,
	   elink_rx_lclk_div4,
	   elink_rx_ref_clk,

           elink_txwr_access,
           elink_txwr_packet,

           elink_txrd_access,
           elink_txrd_packet,

           elink_txrr_access,
	   elink_txrr_packet,
           elink_rxrr_wait,

           elink_rxrd_wait,

	   elink_rxwr_wait,

           elink_rxi_lclk_p,
           elink_rxi_lclk_n,
           elink_rxi_data_p,
           elink_rxi_data_n,
           elink_rxi_frame_p,
           elink_rxi_frame_n,

           elink_txi_wr_wait_p,
           elink_txi_wr_wait_n,
           elink_txi_rd_wait_p,
           elink_txi_rd_wait_n
	   );


	$to_myhdl
	  (
	   keep_alive,

	   elink_rx_lclk_pll,

	   elink_txo_lclk_p,
           elink_txo_lclk_n,
           elink_txo_data_p,
           elink_txo_data_n,
           elink_txo_frame_p,
           elink_txo_frame_n,

           elink_rxo_wr_wait_p,
           elink_rxo_wr_wait_n,
           elink_rxo_rd_wait_p,
           elink_rxo_rd_wait_n,

           elink_rxwr_access,
           elink_rxwr_packet,

           elink_rxrd_access,
           elink_rxrd_packet,

           elink_rxrr_access,
           elink_rxrr_packet,

           elink_txrd_wait,
           elink_txwr_wait,
           elink_txrr_wait,

           elink_mailbox_not_empty,
           elink_mailbox_full
	   );
    end


    reg toggle = 0;
    always @(posedge clock) begin
	toggle <= ~toggle;
    end

    initial begin
	forever begin
	    #100 keep_alive = ~keep_alive;
	end
    end
    
    // ELink design-under-test
    //defparam dut.ELINKID = 12'h800;
    defparam dut.ID = 12'h800;   // set to 810 as default
    elink 
      dut(
	  // man.o.man they are chaning this interface way too often
	  // why is it not set by now?
	  // clocks and resets
	  .reset             ( elink_reset            ),  // por reset
	  .sys_clk           ( elink_sys_clk          ),  // system clock for FIFOs only
	  .tx_lclk           ( elink_tx_lclk          ),  // fast tx clock for IO
	  .tx_lclk90         ( elink_tx_lclk90        ),  // fast 90deg shifted lclk
	  .tx_lclk_div4      ( elink_tx_lclk_div4     ),  // slow tx clock for core logic
	  .rx_lclk           ( elink_rx_lclk          ),  // rx input clock tweaked by pll for IO
	  .rx_lclk_div4      ( elink_rx_lclk_div4     ),  // slow rx clock for core logic
	  .rx_ref_clk        ( elink_rx_ref_clk       ),  // 200MHz ref clock for idelay
	  .rx_lclk_pll       ( elink_rx_lclk_pll      ),  // rx_lclk input for pll
      
	  // EPIPHANY interface I/O
	  .chipid            ( elink_chipid           ),  // chip id strap pins
	  .elink_en          ( elink_en               ),  // elink/ephiphany master enable 
      
	  // ELINK I/O pins
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

	  // System Interface
	  .rxwr_access       ( elink_rxwr_access      ) ,
          .rxwr_packet       ( elink_rxwr_packet      ) ,  
          .rxwr_wait         ( elink_rxwr_wait        ) ,

          .rxrd_access       ( elink_rxrd_access      ) ,
          .rxrd_packet       ( elink_rxrd_packet      ) ,
	  .rxrd_wait         ( elink_rxrd_wait        ) ,

	  .rxrr_access       ( elink_rxrr_access      ) ,
          .rxrr_packet       ( elink_rxrr_packet      ) ,     	  
          .rxrr_wait         ( elink_rxrr_wait        ) ,	  	   		     

          .txwr_access       ( elink_txwr_access      ) ,
          .txwr_packet       ( elink_txwr_packet      ) ,
          .txwr_wait         ( elink_txwr_wait        ) ,

          .txrd_access       ( elink_txrd_access      ) ,
          .txrd_packet       ( elink_txrd_packet      ) ,	  
	  .txrd_wait         ( elink_txrd_wait        ) ,

          .txrr_access       ( elink_txrr_access      ) ,	  		     
	  .txrr_packet       ( elink_txrr_packet      ) ,	 
          .txrr_wait         ( elink_txrr_wait        ) ,

	  .mailbox_full      ( elink_embox_full       ) ,
	  .mailbox_not_empty ( elink_embox_not_empty  ) ,
	  .timeout           ( )
	  );

endmodule
