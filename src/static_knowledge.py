"""
Static curated knowledge base for ICICI Prudential MF key facts.
This supplements the scraped corpus with precise, factual data that
JS-rendered pages cannot expose to a simple HTML scraper.
Sources: ICICI Pru AMC official site, AMFI, Groww fund pages.
"""

STATIC_DOCS = [
    {
        "id": "static_bluechip_overview",
        "text": (
            "ICICI Prudential Bluechip Fund - Large Cap Fund Overview.\n"
            "Category: Large Cap Equity Fund.\n"
            "Launch Date / NFO Date: May 23, 2008. The fund was launched in May 2008.\n"
            "Inception Date: May 23, 2008.\n"
            "Benchmark: NIFTY 100 Total Return Index.\n"
            "Fund Manager: Anish Tawakley, Vaibhav Dusad.\n"
            "Riskometer: Very High Risk.\n"
            "AUM: Approximately Rs 63,000 crore (one of India's largest large cap funds).\n"
            "NFO Date: May 2008.\n"
            "Minimum SIP Amount: Rs 100 per month.\n"
            "Minimum Lump Sum Investment: Rs 100.\n"
            "Exit Load: 1% if redeemed within 1 year from the date of allotment. Nil after 1 year.\n"
            "Expense Ratio (Direct Plan): Approximately 0.87% per annum.\n"
            "Expense Ratio (Regular Plan): Approximately 1.72% per annum.\n"
            "Lock-in Period: None (no lock-in for Bluechip Fund).\n"
            "Investment Objective: To generate long-term capital appreciation by investing in large cap companies.\n"
            "Tax: LTCG above Rs 1.25 lakh taxed at 12.5%. STCG at 20%.\n"
            "Official page: https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund"
        ),
        "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund",
        "title": "ICICI Prudential Bluechip Fund - Key Facts"
    },
    {
        "id": "static_flexicap_overview",
        "text": (
            "ICICI Prudential Flexicap Fund - Flexi Cap Fund Overview.\n"
            "Category: Flexi Cap Equity Fund.\n"
            "Launch Date / NFO Date: September 25, 2020. The fund was launched in September 2020 after SEBI re-categorisation.\n"
            "Inception Date: September 25, 2020.\n"
            "Benchmark: NIFTY 500 Total Return Index.\n"
            "Fund Manager: Anish Tawakley, Mittul Kalawadia.\n"
            "Riskometer: Very High Risk.\n"
            "Minimum SIP Amount: Rs 100 per month.\n"
            "Minimum Lump Sum Investment: Rs 100.\n"
            "Exit Load: 1% if redeemed within 1 year. Nil after 1 year.\n"
            "Expense Ratio (Direct Plan): Approximately 0.69% per annum.\n"
            "Expense Ratio (Regular Plan): Approximately 1.62% per annum.\n"
            "Lock-in Period: None (no lock-in for Flexicap Fund).\n"
            "Investment Objective: To generate long-term capital appreciation by investing across large, mid, and small cap companies.\n"
            "Tax: LTCG above Rs 1.25 lakh taxed at 12.5%. STCG at 20%.\n"
            "Official page: https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-flexicap-fund"
        ),
        "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-flexicap-fund",
        "title": "ICICI Prudential Flexicap Fund - Key Facts"
    },
    {
        "id": "static_elss_overview",
        "text": (
            "ICICI Prudential ELSS Tax Saver Fund - Tax Saving Fund Overview.\n"
            "Category: ELSS (Equity Linked Savings Scheme) - Tax Saving Fund.\n"
            "Launch Date / NFO Date: August 19, 1999. The fund was launched in 1999.\n"
            "Inception Date: August 19, 1999.\n"
            "Benchmark: NIFTY 500 Total Return Index.\n"
            "Fund Manager: Dharmesh Kakkad, Mittul Kalawadia.\n"
            "Riskometer: Very High Risk.\n"
            "Minimum SIP Amount: Rs 500 per month.\n"
            "Minimum Lump Sum Investment: Rs 500.\n"
            "Exit Load: Nil (units cannot be redeemed before 3 years due to mandatory lock-in).\n"
            "Expense Ratio (Direct Plan): Approximately 1.05% per annum.\n"
            "Expense Ratio (Regular Plan): Approximately 1.83% per annum.\n"
            "Lock-in Period: 3 years (mandatory statutory lock-in under Section 80C of Income Tax Act). "
            "Each SIP instalment has its own 3-year lock-in from its investment date.\n"
            "Tax Benefit: Investment up to Rs 1.5 lakh per year qualifies for deduction under Section 80C.\n"
            "Investment Objective: To generate long-term capital appreciation and provide tax benefits.\n"
            "Tax on Gains: LTCG above Rs 1.25 lakh taxed at 12.5% after the 3-year lock-in period.\n"
            "Official page: https://www.icicipruamc.com/mutual-fund/tax-saving-funds/icici-prudential-elss-tax-saver-fund"
        ),
        "source": "https://www.icicipruamc.com/mutual-fund/tax-saving-funds/icici-prudential-elss-tax-saver-fund",
        "title": "ICICI Prudential ELSS Tax Saver Fund - Key Facts"
    },
    {
        "id": "static_elss_lockin_detail",
        "text": (
            "ELSS Lock-in Period - Detailed Explanation.\n"
            "ELSS (Equity Linked Savings Scheme) funds have a mandatory lock-in period of 3 years.\n"
            "This is the shortest lock-in among all Section 80C tax-saving instruments.\n"
            "For SIP investments: Each installment has its own 3-year lock-in. "
            "For example, a SIP invested in January 2024 can be redeemed from January 2027. "
            "A SIP invested in February 2024 can be redeemed from February 2027.\n"
            "For lump sum: The entire amount is locked in for 3 years from the investment date.\n"
            "You cannot withdraw or redeem ELSS units before the 3-year lock-in expires, even partially.\n"
            "After the lock-in period, you can redeem the units anytime with no exit load.\n"
            "ICICI Prudential ELSS Tax Saver Fund follows this same rule.\n"
            "Source: https://groww.in/help/mutual-funds/elss/lock-in-period"
        ),
        "source": "https://groww.in/help/mutual-funds/elss/lock-in-period",
        "title": "ELSS Lock-in Period Rules"
    },
    {
        "id": "static_capital_gains_groww",
        "text": (
            "How to download Capital Gains Statement from Groww.\n"
            "Step 1: Log in to your Groww account at groww.in or the Groww mobile app.\n"
            "Step 2: Go to your Portfolio section.\n"
            "Step 3: Click on 'Reports' or navigate to Account > Reports.\n"
            "Step 4: Select 'Capital Gains Statement'.\n"
            "Step 5: Choose the financial year for which you need the statement.\n"
            "Step 6: Click Download. The statement will be available as a PDF or Excel file.\n"
            "Alternatively, you can also download it via CAMS (camsonline.com) or KFintech (kfintech.com) "
            "by entering your PAN and email.\n"
            "For ICICI Prudential funds specifically, you can also visit: "
            "https://www.icicipruamc.com/investor-services/capital-gain-statement\n"
            "Source: https://groww.in/help/mutual-funds/tax/how-to-download-capital-gains-statement"
        ),
        "source": "https://groww.in/help/mutual-funds/tax/how-to-download-capital-gains-statement",
        "title": "How to Download Capital Gains Statement from Groww"
    },
    {
        "id": "static_expense_ratio_explained",
        "text": (
            "What is Expense Ratio in Mutual Funds?\n"
            "The expense ratio is the annual fee that a mutual fund charges its investors. "
            "It is expressed as a percentage of the fund's average net assets (AUM).\n"
            "It covers fund management fees, administrative costs, and distribution expenses.\n"
            "Lower expense ratio = more of your returns stay with you.\n"
            "Direct Plans always have a lower expense ratio than Regular Plans because there is no distributor commission.\n"
            "ICICI Prudential Bluechip Fund Direct Plan Expense Ratio: ~0.87%\n"
            "ICICI Prudential Flexicap Fund Direct Plan Expense Ratio: ~0.69%\n"
            "ICICI Prudential ELSS Tax Saver Fund Direct Plan Expense Ratio: ~1.05%\n"
            "SEBI mandates that equity fund expense ratios cannot exceed 2.25% for regular plans.\n"
            "Source: https://groww.in/help/mutual-funds/investing/what-is-expense-ratio"
        ),
        "source": "https://groww.in/help/mutual-funds/investing/what-is-expense-ratio",
        "title": "What is Expense Ratio - ICICI Pru MF Funds"
    },
    {
        "id": "static_exit_load_explained",
        "text": (
            "Exit Load in ICICI Prudential Mutual Funds.\n"
            "Exit load is a fee charged when you redeem (sell) your mutual fund units before a specified period.\n"
            "ICICI Prudential Bluechip Fund exit load: 1% if redeemed within 1 year. No exit load after 1 year.\n"
            "ICICI Prudential Flexicap Fund exit load: 1% if redeemed within 1 year. No exit load after 1 year.\n"
            "ICICI Prudential ELSS Tax Saver Fund exit load: Nil (no exit load, but has 3-year statutory lock-in).\n"
            "Exit load is deducted from the redemption proceeds (NAV) at the time of selling.\n"
            "For example, if NAV is Rs 100 and exit load is 1%, you receive Rs 99 per unit.\n"
            "Source: https://groww.in/help/mutual-funds/investing/what-is-exit-load"
        ),
        "source": "https://groww.in/help/mutual-funds/investing/what-is-exit-load",
        "title": "Exit Load - ICICI Prudential Funds"
    },
    {
        "id": "static_riskometer",
        "text": (
            "Riskometer for ICICI Prudential Funds.\n"
            "The riskometer is a SEBI-mandated risk label on mutual fund schemes showing the level of investment risk.\n"
            "Risk levels (lowest to highest): Low, Low to Moderate, Moderate, Moderately High, High, Very High.\n"
            "ICICI Prudential Bluechip Fund Riskometer: Very High Risk.\n"
            "ICICI Prudential Flexicap Fund Riskometer: Very High Risk.\n"
            "ICICI Prudential ELSS Tax Saver Fund Riskometer: Very High Risk.\n"
            "All three funds are equity funds and carry Very High Risk as per SEBI riskometer guidelines.\n"
            "Investors should read the SID and KIM carefully before investing.\n"
            "Source: https://www.amfiindia.com/investor-corner/guided-tour/understanding-riskometer"
        ),
        "source": "https://www.amfiindia.com/investor-corner/guided-tour/understanding-riskometer",
        "title": "Riskometer - ICICI Prudential MF"
    },
    {
        "id": "static_sip_and_nav",
        "text": (
            "SIP and NAV Information for ICICI Prudential Funds.\n"
            "SIP (Systematic Investment Plan) allows you to invest a fixed amount regularly (monthly, weekly, etc.).\n"
            "Minimum SIP for ICICI Prudential Bluechip Fund: Rs 100 per month.\n"
            "Minimum SIP for ICICI Prudential Flexicap Fund: Rs 100 per month.\n"
            "Minimum SIP for ICICI Prudential ELSS Tax Saver Fund: Rs 500 per month.\n"
            "NAV (Net Asset Value) is the per-unit price of the fund, calculated at end of each business day.\n"
            "For NAV of ICICI Prudential Bluechip Fund visit: "
            "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund\n"
            "SIP investments are processed at the NAV of the SIP date.\n"
            "Source: https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund"
        ),
        "source": "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund",
        "title": "SIP and NAV - ICICI Prudential Funds"
    },
    {
        "id": "static_account_statement",
        "text": (
            "How to Download Account Statement for ICICI Prudential Mutual Fund.\n"
            "Option 1 - ICICI Pru AMC Website:\n"
            "Visit https://www.icicipruamc.com/investor-services/account-statement\n"
            "Enter your Folio Number or PAN and email to receive the statement.\n"
            "Option 2 - CAMS (for CAMS-registered funds):\n"
            "Visit https://www.camsonline.com and use 'Mailback Services' to get your statement.\n"
            "Option 3 - Groww App:\n"
            "Go to Portfolio > Reports > Account Statement and select the period.\n"
            "Option 4 - KFintech:\n"
            "Visit https://kfintech.com for funds registered with KFin.\n"
            "Consolidated Account Statement (CAS) can be obtained from CAMS or KFintech using your PAN.\n"
            "Source: https://www.icicipruamc.com/investor-services/account-statement"
        ),
        "source": "https://www.icicipruamc.com/investor-services/account-statement",
        "title": "Account Statement Download - ICICI Prudential MF"
    }
]
