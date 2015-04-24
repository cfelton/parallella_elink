module tb_m_elink_stub;

wire elink_s_axi_bvalid;
wire [31:0] elink_m_axi_awaddr;
reg [7:0] elink_s_axi_arlen;
reg elink_s_axi_wlast;
reg [3:0] elink_s_axi_arqos;
reg [3:0] elink_s_axi_wstrb;
reg elink_clkin;
reg elink_hard_reset;
reg elink_txi_rd_wait_p;
reg elink_txi_rd_wait_n;
wire elink_m_axi_wlast;
reg [2:0] elink_s_axi_arprot;
reg elink_s_axi_wvalid;
wire [1:0] elink_m_axi_wid;
wire elink_rxo_rd_wait_p;
reg [1:0] elink_s_axi_awlock;
wire elink_rxo_rd_wait_n;
wire elink_rxo_wr_wait_p;
reg [1:0] elink_m_axi_rresp;
reg [2:0] elink_clkbypass;
reg [1:0] elink_s_axi_wid;
reg [1:0] elink_s_axi_arburst;
wire [2:0] elink_m_axi_awprot;
wire elink_rxo_wr_wait_n;
wire [3:0] elink_m_axi_awcache;
reg elink_m_axi_rlast;
wire [31:0] elink_s_axi_rdata;
wire elink_chip_resetb;
wire elink_m_axi_awvalid;
wire elink_cclk_p;
wire elink_cclk_n;
reg elink_s_axi_bready;
wire [3:0] elink_rowid;
wire [7:0] elink_m_axi_arlen;
reg elink_m_axi_arready;
reg [2:0] elink_s_axi_awprot;
reg [7:0] elink_rxi_data_n;
reg [31:0] elink_s_axi_wdata;
reg [2:0] elink_s_axi_awsize;
reg [31:0] elink_s_axi_awaddr;
wire elink_s_axi_arready;
reg elink_s_axi_awvalid;
reg [7:0] elink_rxi_data_p;
reg elink_m_axi_rvalid;
reg [1:0] elink_s_axi_awburst;
reg [1:0] elink_s_axi_awid;
wire [7:0] elink_txo_data_n;
reg elink_m_axi_awready;
wire elink_m_axi_arvalid;
wire elink_s_axi_rvalid;
reg elink_s_axi_aresetn;
wire [7:0] elink_txo_data_p;
reg [63:0] elink_m_axi_rdata;
wire [2:0] elink_m_axi_arsize;
reg [1:0] elink_s_axi_arid;
wire [1:0] elink_s_axi_bresp;
reg [3:0] elink_s_axi_awqos;
wire [2:0] elink_m_axi_awsize;
wire elink_m_axi_rready;
reg [31:0] elink_s_axi_araddr;
wire [3:0] elink_m_axi_arqos;
wire [3:0] elink_m_axi_awqos;
reg elink_m_axi_bvalid;
reg elink_m_axi_wready;
reg [3:0] elink_s_axi_awcache;
reg elink_s_axi_arvalid;
wire [3:0] elink_m_axi_arcache;
wire [1:0] elink_m_axi_awid;
wire [1:0] elink_m_axi_awburst;
wire [1:0] elink_m_axi_arburst;
wire elink_txo_frame_n;
reg [1:0] elink_m_axi_bresp;
wire [7:0] elink_m_axi_awlen;
wire elink_txo_frame_p;
reg [1:0] elink_m_axi_rid;
wire elink_s_axi_awready;
reg elink_rxi_lclk_p;
wire [31:0] elink_m_axi_araddr;
wire [1:0] elink_m_axi_awlock;
reg elink_rxi_lclk_n;
wire elink_m_axi_wvalid;
wire [1:0] elink_m_axi_arid;
reg elink_s_axi_rready;
wire elink_txo_lclk_p;
reg [7:0] elink_s_axi_awlen;
wire [3:0] elink_colid;
wire elink_txo_lclk_n;
reg [1:0] elink_s_axi_arlock;
wire elink_embox_not_empty;
wire [2:0] elink_m_axi_arprot;
reg [3:0] elink_s_axi_arcache;
reg [1:0] elink_m_axi_bid;
wire [1:0] elink_s_axi_bid;
wire elink_m_axi_bready;
reg elink_m_axi_aclk;
reg elink_rxi_frame_p;
reg elink_m_axi_aresetn;
wire [1:0] elink_s_axi_rid;
reg elink_rxi_frame_n;
reg elink_s_axi_aclk;
reg elink_txi_wr_wait_p;
wire elink_s_axi_rlast;
reg [2:0] elink_s_axi_arsize;
wire [1:0] elink_m_axi_arlock;
wire elink_s_axi_wready;
reg elink_txi_wr_wait_n;
wire [1:0] elink_s_axi_rresp;
wire [63:0] elink_m_axi_wdata;
wire [7:0] elink_m_axi_wstrb;
wire elink_embox_full;

initial begin
    $from_myhdl(
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
        elink_s_axi_awsize,
        elink_s_axi_awaddr,
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
        elink_s_axi_aclk,
        elink_txi_wr_wait_p,
        elink_s_axi_arsize,
        elink_txi_wr_wait_n
    );
    $to_myhdl(
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
        elink_m_axi_arlen,
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
        elink_colid,
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

m_elink_stub dut(
    elink_s_axi_bvalid,
    elink_m_axi_awaddr,
    elink_s_axi_arlen,
    elink_s_axi_wlast,
    elink_s_axi_arqos,
    elink_s_axi_wstrb,
    elink_clkin,
    elink_hard_reset,
    elink_txi_rd_wait_p,
    elink_txi_rd_wait_n,
    elink_m_axi_wlast,
    elink_s_axi_arprot,
    elink_s_axi_wvalid,
    elink_m_axi_wid,
    elink_rxo_rd_wait_p,
    elink_s_axi_awlock,
    elink_rxo_rd_wait_n,
    elink_rxo_wr_wait_p,
    elink_m_axi_rresp,
    elink_clkbypass,
    elink_s_axi_wid,
    elink_s_axi_arburst,
    elink_m_axi_awprot,
    elink_rxo_wr_wait_n,
    elink_m_axi_awcache,
    elink_m_axi_rlast,
    elink_s_axi_rdata,
    elink_chip_resetb,
    elink_m_axi_awvalid,
    elink_cclk_p,
    elink_cclk_n,
    elink_s_axi_bready,
    elink_rowid,
    elink_m_axi_arlen,
    elink_m_axi_arready,
    elink_s_axi_awprot,
    elink_rxi_data_n,
    elink_s_axi_wdata,
    elink_s_axi_awsize,
    elink_s_axi_awaddr,
    elink_s_axi_arready,
    elink_s_axi_awvalid,
    elink_rxi_data_p,
    elink_m_axi_rvalid,
    elink_s_axi_awburst,
    elink_s_axi_awid,
    elink_txo_data_n,
    elink_m_axi_awready,
    elink_m_axi_arvalid,
    elink_s_axi_rvalid,
    elink_s_axi_aresetn,
    elink_txo_data_p,
    elink_m_axi_rdata,
    elink_m_axi_arsize,
    elink_s_axi_arid,
    elink_s_axi_bresp,
    elink_s_axi_awqos,
    elink_m_axi_awsize,
    elink_m_axi_rready,
    elink_s_axi_araddr,
    elink_m_axi_arqos,
    elink_m_axi_awqos,
    elink_m_axi_bvalid,
    elink_m_axi_wready,
    elink_s_axi_awcache,
    elink_s_axi_arvalid,
    elink_m_axi_arcache,
    elink_m_axi_awid,
    elink_m_axi_awburst,
    elink_m_axi_arburst,
    elink_txo_frame_n,
    elink_m_axi_bresp,
    elink_m_axi_awlen,
    elink_txo_frame_p,
    elink_m_axi_rid,
    elink_s_axi_awready,
    elink_rxi_lclk_p,
    elink_m_axi_araddr,
    elink_m_axi_awlock,
    elink_rxi_lclk_n,
    elink_m_axi_wvalid,
    elink_m_axi_arid,
    elink_s_axi_rready,
    elink_txo_lclk_p,
    elink_s_axi_awlen,
    elink_colid,
    elink_txo_lclk_n,
    elink_s_axi_arlock,
    elink_embox_not_empty,
    elink_m_axi_arprot,
    elink_s_axi_arcache,
    elink_m_axi_bid,
    elink_s_axi_bid,
    elink_m_axi_bready,
    elink_m_axi_aclk,
    elink_rxi_frame_p,
    elink_m_axi_aresetn,
    elink_s_axi_rid,
    elink_rxi_frame_n,
    elink_s_axi_aclk,
    elink_txi_wr_wait_p,
    elink_s_axi_rlast,
    elink_s_axi_arsize,
    elink_m_axi_arlock,
    elink_s_axi_wready,
    elink_txi_wr_wait_n,
    elink_s_axi_rresp,
    elink_m_axi_wdata,
    elink_m_axi_wstrb,
    elink_embox_full
);

endmodule
