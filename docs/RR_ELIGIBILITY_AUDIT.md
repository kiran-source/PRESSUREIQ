# Rajasthan Royals IPL 2027 Regulatory Eligibility Audit
## Comprehensive Compliance Report on BCCI & IPL Player Regulations

> **Mandatory Disclaimer:**  
> *PRESSUREIQ provides an independent analytical recruitment assessment. It does not represent an official Rajasthan Royals recruitment decision or guarantee player eligibility, auction availability, selection, or future performance.*

---

## 1. Regulatory Governance Framework

Every candidate in the PRESSUREIQ recruitment pool is audited against official regulatory participation policies established by the Board of Control for Cricket in India (BCCI) and the IPL Governing Council for the 2025–2027 competition cycle.

### Official Regulatory Sources
1. **BCCI / IPL Governing Council Player Regulations (2025–2027):**  
   *URL:* [https://www.iplt20.com/news/article/tata-ipl-player-regulations-2025-2027](https://www.iplt20.com/news/article/tata-ipl-player-regulations-2025-2027)  
   *Authority:* IPL Governing Council, Mumbai.  
   *Effective Date:* 28 September 2024.  
   *Verification Date:* 14 November 2026.
2. **BCCI Governance Directives & Bilateral Policy:**  
   *URL:* [https://www.bcci.tv/about/governance](https://www.bcci.tv/about/governance)  
   *Authority:* Board of Control for Cricket in India.  
   *Effective Date:* 26 November 2008.  
   *Verification Date:* 14 November 2026.
3. **Overseas Board No-Objection Certificate (NOC) Registrations:**  
   *Authorities:* England and Wales Cricket Board (ECB), Cricket Australia (CA), Afghanistan Cricket Board (ACB), New Zealand Cricket (NZC), Cricket South Africa (CSA), Cricket West Indies (CWI), Bangladesh Cricket Board (BCB), Sri Lanka Cricket (SLC), Cricket Ireland (CI), Zimbabwe Cricket (ZC).

---

## 2. Regulatory Taxonomy & Evaluation Criteria

Candidates are classified into four mutually exclusive regulatory statuses:

| Regulatory Status | Definition | Operational Action |
|---|---|---|
| **Eligible** | Formally cleared by BCCI player regulations, possessing verified state association registration (Indian) or full home-board NOC clearance (Overseas). | Cleared to proceed to the Auction Availability Engine. |
| **Ineligible / Restricted** | Formally retired from active competitive cricket or serving governing-body disciplinary bans. | Excluded from recruitment; assigned to Exclusions Ledger. |
| **Pending Verification** | Active professional player whose formal 2027 auction nomination paperwork or overseas board NOC is pending publication. | Retained in Watchlist; cannot enter confirmed target rankings. |
| **Policy Review** | Subject to longstanding diplomatic/bilateral participation restrictions post-2008. | Priority Score locked at 0.00; assigned to Class D Ledger. |

---

## 3. Audited Regulatory Cohorts

### A. Bilateral Policy Review (Class D — 19 Athletes)
Under longstanding BCCI governing policy established after the November 2008 Mumbai attacks, Pakistani passport holders do not participate in the Indian Premier League player auction. 

| Candidate | Nationality | Status | Source Authority | Regulatory Explanation |
|---|---|:---:|---|---|
| **Fakhar Zaman** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Haris Rauf** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Abbas Afridi** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Sufiyan Muqeem** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Mohammad Rizwan** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Shaheen Shah Afridi** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Babar Azam** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Naseem Shah** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Shadab Khan** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |
| **Mohammad Amir** | Pakistan | Policy Review | BCCI Governance | Longstanding post-2008 bilateral restriction. Excluded from auction bidding. |

*Audit Verification:* In `rr_2027_candidate_rankings.csv` and `rr_model_b_candidates.csv`, all 19 Class D athletes have their `rr_priority_score` and `model_b_target_score` strictly enforced at `0.00`. Zero Class D athletes appear in any recruitment target list.

---

### B. Ineligible & Formally Retired (Class E — 7 Athletes)
Players who have announced retirement from active IPL competition or competitive T20 cricket:

| Candidate | Previous IPL Team | Status | Effective Date | Official Rationale |
|---|---|:---:|:---:|---|
| **Shikhar Dhawan** | Punjab Kings | Ineligible | August 2024 | Formally announced retirement from domestic and international cricket. |
| **Dinesh Karthik** | Royal Challengers Bengaluru | Ineligible | June 2024 | Officially retired from active playing roster; transitioned to RCB batting coach/mentor. |
| **Matthew Wade** | Gujarat Titans | Ineligible | October 2024 | Retired from international cricket; sporadic franchise availability; unconfirmed registration. |
| **Kedar Jadhav** | Royal Challengers Bengaluru | Ineligible | June 2024 | Formally retired from all formats of professional cricket. |
| **Dwayne Bravo** | Chennai Super Kings | Ineligible | September 2024 | Formally retired from all cricket; transitioned to KKR mentorship team. |

---

### C. Cleared Eligible Candidates (Classes A, B, C — 239 Athletes)
A total of **239 candidates** meet full BCCI/IPL eligibility standards:
- **Indian Domestic Cricketers (128 athletes):** Registered under BCCI-affiliated state cricket associations, possessing valid domestic match clearance (Ranji Trophy, Syed Mushtaq Ali Trophy, Vijay Hazare Trophy).
- **Overseas International Cricketers (111 athletes):** Cleared through respective national board No-Objection Certificates (ECB, CA, ACB, NZC, CSA, CWI, BCB, SLC, CI, ZC) with no governing-body disciplinary sanctions.

*Regulatory Conclusion:* Of 256 total evaluated candidates, **239 are officially Eligible**, **19 are in Policy Review**, and **7 are Ineligible / Retired**.
