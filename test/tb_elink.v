
`timescale 1ps/1fs 

`ifndef VTRACE_LEVEL
 `define VTRACE_LEVEL 0
`endif

`ifndef VTRACE_MODULE
 `define VTRACE_MODULE tb_elink
`endif

module tb_elink;

    reg clock      = 1'b0 ;
    reg reset      = 1'b0 ;
    reg keep_alive = 1'b0 ;
    
    wire elink_s_axi_bvalid;
    wire [31:0] elink_m_axi_awaddr;
    reg [7:0] 	elink_s_axi_arlen;
    reg 	elink_s_axi_wlast;
    reg [3:0] 	elink_s_axi_arqos;
    reg [3:0] 	elink_s_axi_wstrb;
    reg 	elink_clkin;
    reg 	elink_hard_reset;
    reg 	elink_txi_rd_wait_p;
    reg 	elink_txi_rd_wait_n;
    wire 	elink_m_axi_wlast;
    reg [2:0] 	elink_s_axi_arprot;
    reg 	elink_s_axi_wvalid;
    wire [11:0] elink_m_axi_wid;
    wire 	elink_rxo_rd_wait_p;
    reg [1:0] elink_s_axi_awlock;
    wire 	elink_rxo_rd_wait_n;
    wire 	elink_rxo_wr_wait_p;
    reg [1:0] 	elink_m_axi_rresp;
    reg [2:0]   elink_clkbypass;
    reg [11:0] elink_s_axi_wid;
    reg [1:0] 	elink_s_axi_arburst;
    wire [2:0] 	elink_m_axi_awprot;
    wire 	elink_rxo_wr_wait_n;
    wire [3:0] 	elink_m_axi_awcache;
    reg 	elink_m_axi_rlast;
    wire [31:0] elink_s_axi_rdata;
    wire 	elink_chip_resetb;
    wire 	elink_m_axi_awvalid;
    wire 	elink_cclk_p;
    wire 	elink_cclk_n;
    reg 	elink_s_axi_bready;
    wire [3:0] 	elink_rowid;
    wire [7:0] 	elink_m_axi_arlen;
    reg 	elink_m_axi_arready;
    reg [2:0] 	elink_s_axi_awprot;
    reg [7:0] 	elink_rxi_data_n;
    reg [31:0] 	elink_s_axi_wdata;
    reg [2:0] 	elink_s_axi_awsize;
    reg [31:0] 	elink_s_axi_awaddr;
    wire 	elink_s_axi_arready;
    reg 	elink_s_axi_awvalid;
    reg [7:0] 	elink_rxi_data_p;
    reg 	elink_m_axi_rvalid;
    reg [1:0] 	elink_s_axi_awburst;
    reg [11:0] elink_s_axi_awid;
    wire [7:0] 	elink_txo_data_n;
    reg 	elink_m_axi_awready;
    wire 	elink_m_axi_arvalid;
    wire 	elink_s_axi_rvalid;
    reg 	elink_s_axi_aresetn;
    wire [7:0] 	elink_txo_data_p;
    reg [63:0] 	elink_m_axi_rdata;
    wire [2:0] 	elink_m_axi_arsize;
    reg [11:0] elink_s_axi_arid;
    wire [1:0] 	elink_s_axi_bresp;
    reg [3:0] 	elink_s_axi_awqos;
    wire [2:0] 	elink_m_axi_awsize;
    wire 	elink_m_axi_rready;
    reg [31:0] 	elink_s_axi_araddr;
    wire [3:0] 	elink_m_axi_arqos;
    wire [3:0] 	elink_m_axi_awqos;
    reg 	elink_m_axi_bvalid;
    reg 	elink_m_axi_wready;
    reg [3:0] 	elink_s_axi_awcache;
    reg 	elink_s_axi_arvalid;
    wire [3:0] 	elink_m_axi_arcache;
    wire [11:0] elink_m_axi_awid;
    wire [1:0] 	elink_m_axi_awburst;
    wire [1:0] 	elink_m_axi_arburst;
    wire 	elink_txo_frame_n;
    reg [1:0] 	elink_m_axi_bresp;
    wire [7:0] 	elink_m_axi_awlen;
    wire 	elink_txo_frame_p;
    reg [11:0] elink_m_axi_rid;
    wire 	elink_s_axi_awready;
    reg 	elink_rxi_lclk_p;
    wire [31:0] elink_m_axi_araddr;
    wire [1:0] elink_m_axi_awlock;
    reg 	elink_rxi_lclk_n;
    wire 	elink_m_axi_wvalid;
    wire [11:0] elink_m_axi_arid;
    reg 	elink_s_axi_rready;
    wire 	elink_txo_lclk_p;
    reg [7:0] 	elink_s_axi_awlen;
    wire [3:0] 	elink_colid;
    wire 	elink_txo_lclk_n;
    reg [1:0] elink_s_axi_arlock;
    wire 	elink_embox_not_empty;
    wire [2:0] 	elink_m_axi_arprot;
    reg [3:0] 	elink_s_axi_arcache;
    reg [11:0]   elink_m_axi_bid;
    wire [11:0]  elink_s_axi_bid;
    wire 	elink_m_axi_bready;
    reg 	elink_m_axi_aclk;
    reg 	elink_rxi_frame_p;
    reg 	elink_m_axi_aresetn;
    wire [11:0] elink_s_axi_rid;
    reg 	elink_rxi_frame_n;
    reg 	elink_s_axi_aclk;
    reg 	elink_txi_wr_wait_p;
    wire 	elink_s_axi_rlast;
    reg [2:0] 	elink_s_axi_arsize;
    wire [1:0]  elink_m_axi_arlock;
    wire 	elink_s_axi_wready;
    reg 	elink_txi_wr_wait_n;
    wire [1:0] 	elink_s_axi_rresp;
    wire [63:0] elink_m_axi_wdata;
    wire [7:0] 	elink_m_axi_wstrb;
    wire 	elink_embox_full;


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
	   elink_s_axi_arlen,
	   elink_s_axi_wlast,
	   elink_s_axi_arqos,
	   elink_s_axi_wstrb,
	   elink_clkin,
	   elink_hard_reset,
	   elink_txi_rd_wait_p,
	   elink_txi_rd_wait_n,
	   elink_s_axi_arprot,
	   elink_s_axi_wvalid,
	   elink_s_axi_awlock,
	   elink_m_axi_rresp,
           elink_clkbypass,
           elink_s_axi_wid,
	   elink_s_axi_arburst,
	   elink_m_axi_rlast,
	   elink_s_axi_bready,
	   elink_m_axi_arready,
	   elink_s_axi_awprot,
	   elink_rxi_data_n,
	   elink_s_axi_wdata,
	   elink_s_axi_aclk,
	   elink_s_axi_awsize,
	   elink_s_axi_awvalid,
	   elink_rxi_data_p,
	   elink_m_axi_rvalid,
	   elink_s_axi_awburst,
           elink_s_axi_awid,
	   elink_m_axi_awready,
	   elink_s_axi_aresetn,
	   elink_m_axi_rdata,
           elink_s_axi_arid,
	   elink_s_axi_awqos,
	   elink_s_axi_araddr,
	   elink_m_axi_bvalid,
	   elink_m_axi_wready,
	   elink_s_axi_awcache,
	   elink_s_axi_arvalid,
	   elink_m_axi_bresp,
           elink_m_axi_rid,
	   elink_rxi_lclk_p,
	   elink_rxi_lclk_n,
	   elink_s_axi_rready,
	   elink_s_axi_awlen,
           elink_s_axi_arlock,
	   elink_s_axi_arcache,
           elink_m_axi_bid,
	   elink_m_axi_aclk,
	   elink_rxi_frame_p,
	   elink_m_axi_aresetn,
	   elink_rxi_frame_n,
	   elink_s_axi_awaddr,
	   elink_txi_wr_wait_p,
	   elink_s_axi_arsize,
	   elink_txi_wr_wait_n
	   );
	$to_myhdl
	  (
	   keep_alive,
	   elink_s_axi_bvalid,
	   elink_m_axi_awaddr,
	   elink_m_axi_wlast,
           elink_m_axi_wid,
	   elink_rxo_rd_wait_p,
	   elink_rxo_rd_wait_n,
	   elink_rxo_wr_wait_p,
	   elink_m_axi_awprot,
	   elink_rxo_wr_wait_n,
	   elink_m_axi_awcache,
	   elink_s_axi_rdata,
	   elink_chip_resetb,
	   elink_m_axi_awvalid,
	   elink_cclk_p,
	   elink_cclk_n,
	   elink_rowid,
	   elink_colid,
	   elink_s_axi_arready,
	   elink_txo_data_n,
	   elink_m_axi_arvalid,
	   elink_s_axi_rvalid,
	   elink_txo_data_p,
	   elink_m_axi_arsize,
	   elink_s_axi_bresp,
	   elink_m_axi_awsize,
	   elink_m_axi_rready,
	   elink_m_axi_arqos,
	   elink_m_axi_awqos,
	   elink_m_axi_arcache,
           elink_m_axi_awid,
	   elink_m_axi_awburst,
	   elink_m_axi_arburst,
	   elink_txo_frame_n,
	   elink_m_axi_awlen,
	   elink_txo_frame_p,
	   elink_s_axi_awready,
	   elink_m_axi_araddr,
           elink_m_axi_awlock,
	   elink_m_axi_wvalid,
           elink_m_axi_arid,
	   elink_txo_lclk_p,
	   elink_m_axi_arlen,
	   elink_txo_lclk_n,
	   elink_embox_not_empty,
	   elink_m_axi_arprot,
           elink_s_axi_bid,
	   elink_m_axi_bready,
           elink_s_axi_rid,
	   elink_s_axi_rlast,
           elink_m_axi_arlock,
	   elink_s_axi_wready,
	   elink_s_axi_rresp,
	   elink_m_axi_wdata,
	   elink_m_axi_wstrb,
	   elink_embox_full
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
    elink 
      dut(
	  .s_axi_bvalid    ( elink_s_axi_bvalid     ) ,
	  .m_axi_awaddr    ( elink_m_axi_awaddr     ) ,
	  .s_axi_arlen     ( elink_s_axi_arlen      ) ,
	  .s_axi_wlast     ( elink_s_axi_wlast      ) ,
	  .s_axi_arqos     ( elink_s_axi_arqos      ) ,
	  .s_axi_wstrb     ( elink_s_axi_wstrb      ) ,
	  .clkin           ( elink_clkin            ) ,
	  .hard_reset      ( elink_hard_reset       ) ,
	  .txi_rd_wait_p   ( elink_txi_rd_wait_p    ) ,
	  .txi_rd_wait_n   ( elink_txi_rd_wait_n    ) ,
	  .m_axi_wlast     ( elink_m_axi_wlast      ) ,
	  .s_axi_arprot    ( elink_s_axi_arprot     ) ,           
	  .s_axi_wvalid    ( elink_s_axi_wvalid     ) ,
	  .m_axi_wid       ( elink_m_axi_wid        ),
	  .rxo_rd_wait_p   ( elink_rxo_rd_wait_p    ) ,
          .s_axi_awlock    ( elink_s_axi_awlock     ), 
	  .rxo_rd_wait_n   ( elink_rxo_rd_wait_n    ) ,
	  .rxo_wr_wait_p   ( elink_rxo_wr_wait_p    ) ,
	  .m_axi_rresp     ( elink_m_axi_rresp      ) ,
          .clkbypass       ( elink_clkbypass        ),
          .s_axi_wid       ( elink_s_axi_wid        ),
	  .s_axi_arburst   ( elink_s_axi_arburst    ) ,
	  .m_axi_awprot    ( elink_m_axi_awprot     ) ,
	  .rxo_wr_wait_n   ( elink_rxo_wr_wait_n    ) ,
	  .m_axi_awcache   ( elink_m_axi_awcache    ) ,
	  .m_axi_rlast     ( elink_m_axi_rlast      ) ,
	  .s_axi_rdata     ( elink_s_axi_rdata      ) ,
	  .chip_resetb     ( elink_chip_resetb      ) ,
	  .m_axi_awvalid   ( elink_m_axi_awvalid    ) ,
	  .cclk_p          ( elink_cclk_p           ) ,
	  .cclk_n          ( elink_cclk_n           ) ,
	  .s_axi_bready    ( elink_s_axi_bready     ) ,
	  .rowid           ( elink_rowid            ) ,
	  .colid           ( elink_colid            ) ,
	  .m_axi_arready   ( elink_m_axi_arready    ) ,
	  .s_axi_awprot    ( elink_s_axi_awprot     ) ,
	  .rxi_data_n      ( elink_rxi_data_n       ) ,
	  .s_axi_wdata     ( elink_s_axi_wdata      ) ,
	  .s_axi_awsize    ( elink_s_axi_awsize     ) , 
	  .s_axi_aclk      ( elink_s_axi_aclk       ) ,
	  .s_axi_arready   ( elink_s_axi_arready    ) ,
	  .s_axi_awvalid   ( elink_s_axi_awvalid    ) ,
	  .rxi_data_p      ( elink_rxi_data_p       ) ,
	  .m_axi_rvalid    ( elink_m_axi_rvalid     ) ,
	  .s_axi_awburst   ( elink_s_axi_awburst    ) ,
          .s_axi_awid      ( elink_s_axi_awid       ),
	  .txo_data_n      ( elink_txo_data_n       ) ,
	  .m_axi_awready   ( elink_m_axi_awready    ) ,
	  .m_axi_arvalid   ( elink_m_axi_arvalid    ) ,
	  .s_axi_rvalid    ( elink_s_axi_rvalid     ) ,
	  .s_axi_aresetn   ( elink_s_axi_aresetn    ) ,
	  .txo_data_p      ( elink_txo_data_p       ) ,
	  .m_axi_rdata     ( elink_m_axi_rdata      ) ,
	  .m_axi_arsize    ( elink_m_axi_arsize     ) ,
          .s_axi_arid      ( elink_s_axi_arid       ) ,
	  .s_axi_bresp     ( elink_s_axi_bresp      ) ,
	  .s_axi_awqos     ( elink_s_axi_awqos      ) ,
	  .m_axi_awsize    ( elink_m_axi_awsize     ) ,
	  .m_axi_rready    ( elink_m_axi_rready     ) ,
	  .s_axi_araddr    ( elink_s_axi_araddr     ) ,
	  .m_axi_arqos     ( elink_m_axi_arqos      ) ,
	  .m_axi_awqos     ( elink_m_axi_awqos      ) ,
	  .m_axi_bvalid    ( elink_m_axi_bvalid     ) ,
	  .m_axi_wready    ( elink_m_axi_wready     ) ,
	  .s_axi_awcache   ( elink_s_axi_awcache    ) ,
	  .s_axi_arvalid   ( elink_s_axi_arvalid    ) ,
	  .m_axi_arcache   ( elink_m_axi_arcache    ) ,
          .m_axi_awid      ( elink_m_axi_awid       ) ,
	  .m_axi_awburst   ( elink_m_axi_awburst    ) ,
	  .m_axi_arburst   ( elink_m_axi_arburst    ) ,
	  .txo_frame_n     ( elink_txo_frame_n      ) ,
	  .m_axi_bresp     ( elink_m_axi_bresp      ) ,
	  .m_axi_awlen     ( elink_m_axi_awlen      ) ,
	  .txo_frame_p     ( elink_txo_frame_p      ) ,
          .m_axi_rid       ( elink_m_axi_rid        ) ,
	  .s_axi_awready   ( elink_s_axi_awready    ) ,
	  .rxi_lclk_p      ( elink_rxi_lclk_p       ) ,
	  .m_axi_araddr    ( elink_m_axi_araddr     ) ,
          .m_axi_awlock    ( elink_m_axi_awlock     ) ,
	  .rxi_lclk_n      ( elink_rxi_lclk_n       ) ,
	  .m_axi_wvalid    ( elink_m_axi_wvalid     ) ,
          .m_axi_arid      ( elink_m_axi_arid       ) ,
	  .s_axi_rready    ( elink_s_axi_rready     ) ,
	  .txo_lclk_p      ( elink_txo_lclk_p       ) ,
	  .s_axi_awlen     ( elink_s_axi_awlen      ) ,
	  .m_axi_arlen     ( elink_m_axi_arlen      ) ,
	  .txo_lclk_n      ( elink_txo_lclk_n       ) ,
          .s_axi_arlock    ( elink_s_axi_arlock     ) ,
	  .embox_not_empty ( elink_embox_not_empty  ) ,
	  .m_axi_arprot    ( elink_m_axi_arprot     ) ,
	  .s_axi_arcache   ( elink_s_axi_arcache    ) ,
          .m_axi_bid       ( elink_m_axi_bid        ) ,
          .s_axi_bid       ( elink_s_axi_bid        ) ,
	  .m_axi_bready    ( elink_m_axi_bready     ) ,
	  .m_axi_aclk      ( elink_m_axi_aclk       ) ,
	  .rxi_frame_p     ( elink_rxi_frame_p      ) ,
	  .m_axi_aresetn   ( elink_m_axi_aresetn    ) ,
          .s_axi_rid       ( elink_s_axi_rid        ) ,    
	  .rxi_frame_n     ( elink_rxi_frame_n      ) ,
	  .s_axi_awaddr    ( elink_s_axi_awaddr     ) ,
	  .txi_wr_wait_p   ( elink_txi_wr_wait_p    ) ,
	  .s_axi_rlast     ( elink_s_axi_rlast      ) ,
	  .s_axi_arsize    ( elink_s_axi_arsize     ) ,
          .m_axi_arlock    ( elink_m_axi_arlock     ) ,
	  .s_axi_wready    ( elink_s_axi_wready     ) ,
	  .txi_wr_wait_n   ( elink_txi_wr_wait_n    ) ,
	  .s_axi_rresp     ( elink_s_axi_rresp      ) ,
	  .m_axi_wdata     ( elink_m_axi_wdata      ) ,
	  .m_axi_wstrb     ( elink_m_axi_wstrb      ) ,
	  .embox_full      ( elink_embox_full       ) 
	  );

endmodule
