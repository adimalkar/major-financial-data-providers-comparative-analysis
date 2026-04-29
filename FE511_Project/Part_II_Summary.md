# Part II: Historical Data Integrity & Survivorship Bias - Summary

## Section 1: Corporate Name/Ticker Changes

### Case Study: Facebook (FB) to Meta (META) - December 2021

#### Yahoo Finance
- **Old ticker (FB):** Still works, provides historical data
- **New ticker (META):** Works, includes pre-2021 data
- **Method:** Automatic ticker linking
- **Reliability:** Good for continuous price history
- **Limitation:** Ticker-based only, no permanent ID

#### CRSP
- **Unique Identifier:** PERMNO (never changes)
- **Method:** Join dsf (prices) with dsenames (ticker/dates)
- **Query approach:** Filter by PERMNO, not ticker
- **Benefit:** Can retrieve data using either old or new ticker
- **Key advantage:** PERMNO provides bulletproof linking across any corporate change

#### Compustat
- **Unique Identifier:** GVKEY (permanent company ID)
- **Method:** Similar to CRSP, use GVKEY for linking
- **Benefit:** Tracks company across ticker changes
- **Advantage:** Links price and fundamental data consistently

#### Key Findings
1. All three sources can provide continuous price history across ticker changes
2. CRSP (PERMNO) and Compustat (GVKEY) use permanent identifiers - more reliable
3. Yahoo Finance relies on automatic ticker linking - works but less transparent
4. For research: Always use PERMNO or GVKEY, not tickers

---

## Section 2: Delistings & Bankruptcies

### Case Study: Lehman Brothers (LEH) - Bankruptcy September 2008

#### Yahoo Finance
- **Historical data:** May or may not be available
- **Data through delisting:** Sometimes yes, sometimes no
- **Delisting return:** NOT provided
- **Final outcome:** Unpredictable availability
- **Risk:** Cannot reliably include failed companies in analysis

#### CRSP
- **Historical data:** ALWAYS available
- **Data through delisting:** YES, complete through final day
- **Delisting return (DLRET):** YES - CRITICAL FEATURE
- **Delisting code (DLSTCD):** Indicates reason (bankruptcy = 500-599)
- **Delisting date (DLSTDT):** Exact date recorded
- **Example:** Lehman DLRET ~ -100% (total loss)
- **Benefit:** Can accurately calculate investor returns including failure

#### Compustat
- **Historical data:** Sometimes available, sometimes removed
- **Delisting return:** NOT provided
- **Limitation:** Data may stop abruptly at delisting
- **Risk:** Incomplete picture of company failure

#### Critical Insight: CRSP's Delisting Return (DLRET)

The DLRET field captures the final return when a company:
- Goes bankrupt (typically -90% to -100%)
- Is liquidated
- Stops trading

**Why this matters:**
- Lehman's last trading price: ~$0.21
- Delisting return: -100%
- **Without DLRET:** You miss the final 100% loss
- **With DLRET:** You capture complete investor experience

This is the SINGLE MOST IMPORTANT feature for avoiding survivorship bias.

---

## Section 3: Survivorship Bias Implications

### What is Survivorship Bias?

Survivorship bias occurs when analysis includes only companies that "survived" to the present,
excluding those that failed, were acquired, or delisted. This creates an upward bias because
losers are systematically excluded.

### The Classic Error

**Scenario:** Backtest a strategy on S&P 500 from 2005-2025

**Wrong approach (survivorship bias):**
1. Download 2025 S&P 500 constituent list (500 companies)
2. Get 20 years of price data for these companies
3. Run backtest

**What's wrong:**
- These are the WINNERS - they survived 20 years
- Missing companies that were in S&P 500 in 2005 but:
  - Went bankrupt (Lehman, Bear Stearns, Washington Mutual)
  - Were acquired (Countrywide, Merrill Lynch)
  - Were removed from index for poor performance

**Result:** Strategy appears more profitable than it would have been in real-time

### Magnitude of the Problem

Academic research shows survivorship bias inflates returns by:
- **Large-cap stocks:** 1-3% annually
- **Small-cap stocks:** 3-5% annually  
- **Emerging markets:** 5-10% annually
- **Corporate bonds:** Can be even higher

Over 20 years, a 2% annual bias compounds to 48% cumulative error!

### Which Database Avoids Survivorship Bias?

| Feature | Yahoo Finance | CRSP | Compustat |
|---------|--------------|------|-----------|
| Complete delisting data | No | **YES** | Partial |
| Delisting returns (DLRET) | No | **YES** | No |
| Historical index constituents | No | **YES** | Limited |
| Permanent identifiers | No | **YES (PERMNO)** | **YES (GVKEY)** |
| Risk of survivorship bias | **HIGH** | **LOW** | Medium |

**Answer: CRSP is uniquely equipped to avoid survivorship bias**

### Why CRSP Solves This

1. **Never deletes data:** All companies remain in database forever
2. **PERMNO is permanent:** Tracks company even after delisting
3. **Delisting returns:** Captures final investor loss/gain
4. **Delisting codes:** Identifies reason for delisting
5. **Historical constituents:** Can reconstruct indices as they existed in the past

### Practical Example

**Portfolio backtest 2005-2025 without survivorship bias correction:**

Hypothetical results:
- Strategy return: 12% annually
- S&P 500 return: 10% annually
- **Conclusion:** Strategy beats market!

**Same backtest with CRSP delisting returns included:**
- Strategy return: 9% annually (includes Lehman, etc. losses)
- S&P 500 return: 8% annually (also corrected)
- **Conclusion:** Strategy beats market by less, may not be significant

The difference? Including companies that FAILED.

### Best Practices

1. **Always use CRSP for backtesting** if survivorship bias is a concern
2. **Never use current index constituents** for historical analysis
3. **Always include delisting returns** in return calculations
4. **Use PERMNO, not tickers** for historical studies
5. **Document your survivorship bias treatment** in research

---

## Conclusion

### Summary of Findings

**Ticker Changes:**
- All sources handle ticker changes, but CRSP (PERMNO) and Compustat (GVKEY) are most reliable
- Permanent identifiers are essential for robust research

**Delistings:**
- Only CRSP provides complete delisting data and returns
- DLRET field is unique and critical
- Yahoo Finance and Compustat have incomplete delisting coverage

**Survivorship Bias:**
- CRSP is the gold standard for avoiding survivorship bias
- Delisting returns (DLRET) are the key differentiator
- Survivorship bias can inflate returns by 1-5% annually

### Data Source Selection Guide

- **Academic research:** Use CRSP (mandatory for published research)
- **Professional backtesting:** Use CRSP to avoid survivorship bias
- **Fundamental analysis:** Compustat (but be aware of delisting limitations)
- **Quick prototypes:** Yahoo Finance (acceptable if survivorship bias is not critical)
- **Real money trading:** Combine CRSP (prices) + Compustat (fundamentals)

### Key Takeaway

The difference between data sources is not just convenience or cost—it's about
**research validity**. Using the wrong source can lead to completely invalid conclusions,
especially in backtesting and performance analysis.

CRSP's delisting returns are not a "nice to have" feature—they are essential for
accurate financial research.

---

**Analysis Date:** December 2025  
**Case Studies:** Meta (ticker change), Lehman Brothers (delisting)  
**Key Finding:** Only CRSP provides complete protection against survivorship bias
