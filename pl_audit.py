import pandas as pd

# Mapped financial data structured entirely in English with accurate metrics
financial_data = {
    "Year": [1, 2, 3, 4, 5],
    "Gross_Revenue": [216000.0, 720000.0, 1000000.0, 1440000.0, 1800000.0],
    "Commissions": [-21600.0, -72000.0, -100000.0, -144000.0, -180000.0],
    "Sales_Tax": [-12960.0, -43200.0, -60000.0, -86400.0, -108000.0],
    "Net_Revenue": [181440.0, 604800.0, 840000.0, 1209600.0, 1512000.0],
    "Variable_Costs": [-56508.0, -170142.0, -202323.0, -340494.0, -475272.0],
    "Fixed_Costs": [-9000.0, -20400.0, -22800.0, -48000.0, -55200.0],
    "Total_Costs": [-65508.0, -190542.0, -225123.0, -388494.0, -530272.0],
    "Corporate_Expenses": [-22980.0, -22980.0, -22980.0, -22980.0, -22980.0],
    "Marketing_Sales": [-3794.0, -72000.0, -108000.0, -144000.0, -180000.0],
    "EBIT": [89158.0, 336258.0, 523677.0, 667106.0, 796748.0],
    "Initial_CapEx": [-166991.0, 0.0, 0.0, 0.0, 0.0],
    "Working_Capital_NCG": [0.0, 0.0, 0.0, 0.0, 0.0],
    "Operational_Savings": [18000.0, 18000.0, 18000.0, 18000.0, 18000.0],
    "Free_Cash_Flow": [-59833.0, 354258.0, 541677.0, 685106.0, 814748.0]
}

df = pd.DataFrame(financial_data)

def run_comprehensive_financial_suite(dataframe):
    print("==========================================================================================")
    print("                    STANDARD FINANCIAL REPORTING & PERFORMANCE DASHBOARD                  ")
    print("==========================================================================================\n")

    fixed_initial_base = abs(dataframe["Initial_CapEx"].iloc[0]) # Absolute asset anchor $166,991.00
    cumulative_fcf = 0.0

    variance_metrics = [
        "Gross_Revenue", "Commissions", "Sales_Tax", "Net_Revenue",
        "Variable_Costs", "Fixed_Costs", "Total_Costs",
        "Corporate_Expenses", "Marketing_Sales", "EBIT", "Free_Cash_Flow"
    ]

    yoy_df = dataframe[variance_metrics].pct_change()

    for i in range(len(dataframe)):
        year = int(dataframe["Year"].iloc[i])
        rev = dataframe["Gross_Revenue"].iloc[i]
        comm = dataframe["Commissions"].iloc[i]
        tax = dataframe["Sales_Tax"].iloc[i]
        net_rev = dataframe["Net_Revenue"].iloc[i]
        v_cost = dataframe["Variable_Costs"].iloc[i]
        f_cost = dataframe["Fixed_Costs"].iloc[i]
        t_cost = dataframe["Total_Costs"].iloc[i]
        corp = dataframe["Corporate_Expenses"].iloc[i]
        mkt = dataframe["Marketing_Sales"].iloc[i]
        ebit = dataframe["EBIT"].iloc[i]
        capex = dataframe["Initial_CapEx"].iloc[i]
        ncg = dataframe["Working_Capital_NCG"].iloc[i]
        sav = dataframe["Operational_Savings"].iloc[i]
        fcf = dataframe["Free_Cash_Flow"].iloc[i]

        # Accumulate absolute baseline cash flow changes
        cumulative_fcf += fcf

        # Core accounting calculation fix: Unrecovered Capital = (-Initial CapEx) + Cumulative FCF
        net_unrecovered_position = (-fixed_initial_base) + cumulative_fcf

        print(f"===================== YEAR {year} FINANCIAL P&L / CASH FLOW STATEMENT =====================")

        def format_row(label, val, is_pct_of_gross=True, metric_name=None, strip_va=False):
            if strip_va:
                va_str = "      "
            else:
                va_str = f"({abs(val)/rev:.1%} VA)" if is_pct_of_gross else "(--)   "

            yoy_str = "(-- YoY)"
            if year >= 2 and metric_name in variance_metrics:
                prev_val = dataframe[metric_name].iloc[i-1]
                if prev_val < 0 and val < 0:
                    yoy_val = (abs(val) - abs(prev_val)) / abs(prev_val)
                else:
                    yoy_val = yoy_df.loc[i, metric_name]
                yoy_str = f"({yoy_val:+.1%} YoY)"
            return f"  {label:<38} ${val:>12,.2f}   {va_str:<10} {yoy_str}"

        print(format_row("[+] Gross Revenue:", rev, False, "Gross_Revenue", strip_va=True))
        print(format_row("  [-] Commissions:", comm, True, "Commissions"))
        print(format_row("  [-] Sales Tax:", tax, True, "Sales_Tax"))
        print(format_row("[=] Net Revenue:", net_rev, True, "Net_Revenue"))
        print(format_row("  [-] Variable Costs:", v_cost, True, "Variable_Costs"))
        print(format_row("  [-] Fixed Costs:", f_cost, True, "Fixed_Costs"))
        print(format_row("[=] Total Costs:", t_cost, True, "Total_Costs"))
        print(format_row("  [-] Corporate Expenses (G&A):", corp, True, "Corporate_Expenses"))
        print(format_row("  [-] Marketing & Sales:", mkt, True, "Marketing_Sales"))
        print(format_row("[=] Operating Profit (EBIT):", ebit, True, "EBIT"))
        print(format_row("  [-] Capital Expenditure (CapEx):", capex, False))
        print(format_row("  [+/-] Net Working Capital (NCG):", ncg, True, "Working_Capital_NCG"))
        print(format_row("  [+] Operational Savings:", sav, True, "Operational_Savings"))
        print(format_row("[=] Free Cash Flow (FCF):", fcf, True, "Free_Cash_Flow"))

        print("\n  [i] CAPITAL DEPLOYMENT & DILUTION TRACKING:")
        print(f"      -> Initial Unrecovered Base:        ${fixed_initial_base:,.2f}")

        if fcf < 0:
            print(f"      -> Current Year FCF:                $({abs(fcf):,.2f})")
        else:
            print(f"      -> Current Year FCF:                ${fcf:,.2f}")

        # Format output to perfectly separate capital surplus vs remaining deficit
        if net_unrecovered_position < 0:
            print(f"      -> Unrecovered Capital:             $({abs(net_unrecovered_position):,.2f})")
        else:
            print(f"      -> Unrecovered Capital:             ${net_unrecovered_position:,.2f}  [Net Positive Capital Surplus]")

        print("-" * 88)

    print("\n==========================================================================================")
    print("                                EXECUTIVE REVIEW & RECOMMENDATIONS                        ")
    print("==========================================================================================")
    print("* TOP-LINE SCALE & DEDUCTIONS: Gross Revenue showcases an aggressive but achievable scale")
    print("  trajectory, expanding from $216K in Year 1 to a mature $1.8M in Year 5. Deductions are perfectly")
    print("  standardized—with Commissions and Sales Taxes locked at 10.0% and 6.0% respectively—yielding")
    print("  a predictable Net Revenue conversion rate of exactly 84.0% across the entire horizon.")
    print("")
    print("* OPERATING EFFICIENCY & CORE MARGINS: Total Costs (Variable + Fixed) drop from 30.3% of Gross")
    print("  Revenue in Year 1 to a lean 29.5% by Year 5. This optimization, combined with a targeted, heavy")
    print("  front-loaded Marketing investment in Year 2 (10.0% VA) to capture market share, successfully")
    print("  stabilizes long-term Customer Acquisition Cost (CAC) and drives robust mid-stage margins.")
    print("")
    print("* OPERATING LEVERAGE (EBIT) & RISK TRANSPARENCY: Operating Profit (EBIT) surges from a modest")
    print("  $89,158 (41.3% margin) in Year 1 to $796,748 (44.3% margin) in Year 5. To remain realistic for")
    print("  investors, this extreme operating leverage assumes Corporate G&A overhead remains flat at")
    print("  $22,980. In a live deployment, we anticipate a structural step-up will be required to absorb")
    print("  administrative strain once enterprise revenue scales past the $1.0M threshold.")
    print("")
    print("* CAPITAL VELOCITY & INVESTMENT PAYBACK: Year 1 requires an aggressive upfront CapEx deploy-")
    print("  ment of $166,991.00. Combined with a Year 1 operational cash burn of $(59,833.00), investors face")
    print("  a peak exposure threshold of $(226,824.00). However, due to high-velocity operational efficiency")
    print("  and an ongoing $18,000 annual Operational Savings tailwind, this initial capital drag is com-")
    print("  pletely erased in Year 2, generating an immediate positive net surplus of $127,434.00.")
    print("")
    print("* FREE CASH FLOW & SURPLUS REALIZATION: By Year 5, Free Cash Flow reaches an elite $814,748")
    print("  (45.3% of Gross Revenue), driving the cumulative Unrecovered Capital into a massive, net-positive")
    print("  surplus of $2,168,965.00. While this FCF yield is highly attractive, sophisticated investors")
    print("  should note that Net Working Capital (NCG) is currently modeled at flat zero. Transitioning to a")
    print("  realistic trade receivables aging schedule will slightly alter intra-year cash collection timing")
    print("  but will not dilute the overwhelming structural profitability of the venture.")
    print("==========================================================================================\n")

if __name__ == "__main__":
    run_comprehensive_financial_suite(df)
