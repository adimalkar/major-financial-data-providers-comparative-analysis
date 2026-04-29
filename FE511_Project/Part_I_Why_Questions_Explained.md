# Part I: Why Questions - Data Provider Feature Differences Explained

## Overview

This document explains why different data providers have different features, based on their target audience, business model, and core purpose.

---

## Q1: Why doesn't CRSP provide intraday data?

### Answer

CRSP (Center for Research in Security Prices) is designed specifically for **academic research**, not day trading or real-time market analysis.

**Key Reasons:**

1. **Academic Research Focus**
   - Academic studies focus on end-of-day (EOD) pricing for statistical validity
   - Daily returns calculated consistently at market close eliminate intraday noise
   - Long-term research (months/years) does not require minute-by-minute data

2. **Statistical Validity**
   - EOD prices represent final consensus value for the day
   - Intraday data contains microstructure noise (bid-ask bounce, temporary imbalances)
   - Research on returns, volatility, correlations uses daily or monthly data

3. **Data Management**
   - Storing more than 100 years of intraday data would be massive
   - CRSP maintains data since 1926; intraday would be terabytes
   - Processing and adjustment complexity would increase substantially

4. **Not the Mission**
   - CRSP's mission is to provide accurate, adjusted historical prices for research
   - Real-time trading data is covered by databases such as TAQ (Trade and Quote)
   - CRSP focuses on historical accuracy, not trading infrastructure

**Bottom Line:** If intraday data is needed, use TAQ or similar databases. CRSP serves a different purpose.

---

## Q2: Why does Yahoo Finance have analyst recommendations and institutional holdings?

### Answer

Yahoo Finance targets **retail investors** making current investment decisions, not academic researchers studying historical patterns.

**Key Reasons:**

1. **Retail Investor Audience**
   - Retail investors ask: "What should I buy now?"
   - Academic researchers ask: "What patterns existed historically?"
   - These are fundamentally different use cases

2. **Investment Decision Support**
   - Analyst ratings (Buy/Sell/Hold) help non-professionals make decisions
   - Institutional holdings show large investor positions
   - Earnings estimates provide forward-looking guidance
   - These features have little or no value for historical backtesting

3. **Business Model**
   - Yahoo Finance is **free** and **ad-supported**
   - It needs daily users to generate advertising revenue
   - Features that drive engagement include recommendations, real-time quotes, and news
   - Historical research data does not drive traffic

4. **User Engagement**
   - Retail investors check Yahoo daily or weekly
   - Academic researchers run large queries infrequently
   - Recommendations and holdings change frequently, bringing users back
   - This repeat traffic is valuable for advertising

**Bottom Line:** Yahoo optimizes for user engagement and current trading, not historical research accuracy.

---

## Q3: Why does Yahoo Finance not have PERMNO or delisting returns?

### Answer

Yahoo Finance serves **current market participants**, not historical researchers conducting backtests.

**Key Reasons:**

1. **No Academic Research Use Case**
   - PERMNO is an academic construct created by CRSP
   - Retail traders do not need permanent identifiers; they trade current tickers
   - "What is AAPL worth today?" does not require PERMNO
   - "How did this portfolio perform from 1990 to 2020?" does require a permanent identifier

2. **Current Trading Focus**
   - Yahoo users want: "What is META trading at right now?"
   - They do not ask: "What was Facebook's PERMNO in 2015?"
   - The current ticker is sufficient for current trading

3. **Delisting Returns and Revenue**
   - Delisting returns matter for backtest accuracy
   - Most Yahoo users are not running academic backtests
   - Retail investors typically do not hold stocks through bankruptcy
   - Maintaining data on failed companies costs money and generates little traffic

4. **Data Retention Costs**
   - Storing Lehman Brothers data generates almost no revenue
   - Few users search for prices of completely delisted tickers
   - Free services reduce costs by removing unused data
   - CRSP charges universities because it maintains this long history

**Bottom Line:** Free sources optimize for current data. Historical research data typically requires paid academic databases.

---

## Q4: Why does Compustat not have detailed daily price data like CRSP?

### Answer

Compustat's core mission is **fundamental analysis** (financial statements), not price and return research.

**Key Reasons:**

1. **Different Core Purpose**
   - **Compustat:** balance sheets, income statements, cash flows, and ratios
   - **CRSP:** prices, returns, trading volume, and corporate actions
   - These support different research questions

2. **Historical Origins**
   - Compustat began as a fundamental data provider in 1962
   - Initially focused on quarterly and annual financials
   - Daily prices (comp.secd) were added later as supplementary data
   - CRSP was designed for price and return research from the beginning

3. **Market Segmentation**
   - CRSP dominates academic price and return research
   - Compustat dominates fundamental analysis research
   - They are complements, not direct competitors
   - Most academic papers use both: CRSP prices plus Compustat fundamentals

4. **Missing Fields Explained**
   - **OPENPRC** (open price): not necessary for fundamental analysis
   - **DLRET** (delisting return): not calculated by Compustat
   - **RET** (daily return): can be calculated from prccd if needed
   - Compustat provides what fundamental researchers need, not full market microstructure

5. **Research Workflow**
   - Typical academic study:
     - Obtain prices and returns from **CRSP**
     - Obtain financial ratios and statements from **Compustat**
     - Merge using a PERMNO-GVKEY link table
   - Researchers do not expect Compustat to duplicate CRSP

**Bottom Line:** Compustat and CRSP divide the market: fundamentals versus prices. Researchers use both together.

---

## Summary Table

| Feature | CRSP | Yahoo Finance | Compustat | Why the Difference? |
|---------|------|---------------|-----------|---------------------|
| Intraday prices | No | Yes (delayed) | No | Yahoo: retail traders; CRSP/Compustat: academic focus |
| Analyst recommendations | No | Yes | No | Yahoo: user engagement; others: not research relevant |
| Institutional holdings | No | Yes | No | Yahoo: retail interest; others: not historical research data |
| PERMNO (permanent ID) | Yes | No | No | CRSP invention for research; retail traders do not need it |
| GVKEY (permanent ID) | No | No | Yes | Compustat invention for fundamentals linking |
| Delisting returns (DLRET) | Yes | No | No | CRSP: research accuracy; others: no use case |
| Daily OHLC prices | Yes | Yes | Partial | CRSP: complete; Yahoo: current only; Compustat: supplementary |
| Fundamental data | No | Yes (via API) | Yes | Compustat core; CRSP not their mission |
| Historical data for delisted | Yes | No | Partial | CRSP: academic requirement; Yahoo: cost with no benefit |
| Data back to 1926 | Yes | No | No | CRSP: research database; others: modern focus |

---

## Key Takeaways

1. **Business Model Drives Features**
   - Free (Yahoo): Features that drive ad revenue (current data, recommendations)
   - Paid academic (CRSP/Compustat): Features that enable research (PERMNO, DLRET)

2. **Target Audience Matters**
   - Retail investors: Need current info, not historical rigor
   - Academic researchers: Need historical accuracy, not trading features

3. **Core Competency Focus**
   - CRSP: Price and return research
   - Compustat: Fundamental analysis
   - Yahoo: Current market information for retail

4. **They Are Complementary, Not Competing**
   - Researchers use CRSP and Compustat together
   - Retail investors use Yahoo for free current data
   - Each serves its purpose well

---

**Document Created:** December 2025  
**Purpose:** FE511 Project Part I - Data Provider Comparison
