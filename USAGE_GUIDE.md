# Bug Bounty Dorks - Complete Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Understanding Google Dorks](#understanding-google-dorks)
3. [Manual Search Method](#manual-search-method)
4. [Automated Python Script](#automated-python-script)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Fastest Way to Get Started (5 minutes)

1. **Open Google** - Go to www.google.com
2. **Copy a dork** - From `dorks.txt`, copy this one:
   ```
   "powered by bugcrowd" -site:bugcrowd.com
   ```
3. **Paste & Search** - Paste in Google search bar and press Enter
4. **Review Results** - Look for company websites with bug bounty programs
5. **Repeat** - Try different dorks to find more programs

---

## Understanding Google Dorks

### Core Operators

| Operator | Example | Meaning |
|----------|---------|----------|
| `inurl:` | `inurl:bug-bounty` | Find pages with "bug-bounty" in the URL |
| `intext:` | `intext:reward` | Find pages containing the word "reward" |
| `site:` | `site:*.edu` | Search only .edu domains |
| `filetype:` | `filetype:txt` | Find specific file types |
| `intitle:` | `intitle:"Bug Bounty"` | Find pages with title containing this |
| `-` | `-site:hackerone.com` | Exclude results from this site |
| `""` | `"exact phrase"` | Search for exact phrase |
| `AND` | `term1 AND term2` | Both terms must appear |
| `OR` | `term1 OR term2` | Either term can appear |

### Real-World Examples

#### Example 1: Find corporate bug bounty programs
```
"responsible disclosure" AND (reward OR bounty)
```
**What it does:**
- Finds pages mentioning "responsible disclosure"
- AND also mention either "reward" or "bounty"
- Great for finding formal programs

#### Example 2: Find security.txt files
```
inurl:/.well-known/security.txt
```
**What it does:**
- Searches for the standard security.txt file location
- These files usually contain security contact info and program details
- Highly reliable for finding legitimate programs

#### Example 3: Find government programs
```
site:*.gov* "vulnerability disclosure program" OR "bug bounty"
```
**What it does:**
- Limits search to government domains (*.gov)
- Looks for pages mentioning either vulnerability disclosure or bug bounty
- Good for government agencies and contractors

#### Example 4: Regional search (Netherlands)
```
site:*.nl intext:responsible disclosure intext:reward
```
**What it does:**
- Limits search to .nl (Dutch) domains
- Looks for pages with both "responsible disclosure" and "reward"
- Useful for country-specific hunting

---

## Manual Search Method

### Step-by-Step Instructions

#### Step 1: Open Google Search
- Go to [Google.com](https://www.google.com)
- Make sure you're logged out or use Incognito mode for consistent results

#### Step 2: Copy a Dork
- Open `dorks.txt` file
- Select a search query
- Copy it (Ctrl+C or Cmd+C)

#### Step 3: Paste into Google
- Click the search box
- Paste the query (Ctrl+V or Cmd+V)
- Press Enter

#### Step 4: Review Results
Evaluate each result:
- **Check the URL** - Does it look like a real company?
- **Read the snippet** - Does it mention bug bounty or rewards?
- **Click the link** - Visit the website and look for:
  - Security page
  - Bug bounty program details
  - Reward amounts
  - Contact information
  - Submission guidelines

#### Step 5: Create a List
Keep track of promising targets:

```
Company: Acme Corp
URL: https://www.acmecorp.com/security
Program: Yes - Bug Bounty
Rewards: $100-$5000
Scope: Web app + API
Status: Active
Notes: Uses HackerOne platform
```

### Organizing Your Findings

Create a spreadsheet:

| Company | URL | Program | Min Reward | Max Reward | Platform | Status | Date Found |
|---------|-----|---------|-----------|-----------|----------|--------|------------|
| Acme Corp | https://acmecorp.com/security | Yes | $100 | $5000 | HackerOne | Active | 2026-07-18 |
| Tech Inc | https://techinc.com/report | Yes | €250 | €10000 | Direct | Active | 2026-07-18 |

---

## Automated Python Script

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection

### Installation

#### Step 1: Install Python

**Windows/Mac/Linux:**
- Download from [python.org](https://www.python.org/downloads/)
- Install with default settings

**Verify installation:**
```bash
python --version
pip --version
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - For web requests
- `beautifulsoup4` - For parsing HTML
- `google-search-results` - For programmatic Google searches
- `tqdm` - For progress bars

### Running the Script

#### Basic Usage

```bash
python dork_search.py
```

#### With Options

```bash
# Search specific number of dorks
python dork_search.py --limit 10

# Save results to file
python dork_search.py --output results.csv

# Add delay between searches (in seconds)
python dork_search.py --delay 5

# Verbose output
python dork_search.py --verbose
```

#### Full Command Example

```bash
python dork_search.py --limit 20 --delay 3 --output findings.csv --verbose
```

### Understanding the Output

#### Console Output
```
[1/100] Searching: inurl /bug bounty
  ├─ Found 5 results
  ├─ Valid: 4
  └─ Added to report

[2/100] Searching: inurl:/security "reward"
  ├─ Found 8 results
  ├─ Valid: 6
  └─ Added to report
```

#### CSV Output (results.csv)
```csv
Dork,URL,Title,Description,Found_Date
"inurl /bug bounty",https://company.com/security,Security Rewards,Our bug bounty program...,2026-07-18
"inurl:/security reward",https://tech.co/report-bug,Bug Bounty,Report vulnerabilities and earn...,2026-07-18
```

---

## Best Practices

### 1. Research Strategy

**Start Broad, Get Specific:**
```
1st Search: "bug bounty"                    # Most results
2nd Search: "bug bounty" site:*.com         # Narrow to commercial
3rd Search: "bug bounty" "$10,000"          # Find high-reward programs
```

**Geographic Focus:**
```
# For Netherlands
site:*.nl responsible disclosure

# For EMEA region
site:*.eu bug bounty

# For North America
site:*.com OR site:*.ca bug bounty
```

### 2. Verification Checklist

Before reporting to a program:

- [ ] Is the program officially listed on a known platform (HackerOne, Bugcrowd)?
- [ ] Does the website have HTTPS/SSL certificate?
- [ ] Is there an official security/vulnerability policy?
- [ ] Are there published reports from other researchers?
- [ ] Is there a legitimate company behind this?
- [ ] Do they mention specific rewards/ranges?

### 3. Safety First

**Always:**
- [ ] Read the program rules before testing
- [ ] Only test within declared scope
- [ ] Don't access other users' data
- [ ] Don't modify or delete anything
- [ ] Report through proper channels
- [ ] Keep findings confidential until resolved

### 4. Documentation

**Record everything:**
- Date and time of discovery
- Exact steps to reproduce
- Screenshots if applicable
- Affected URLs/endpoints
- Potential impact
- Your contact information

### 5. Communication

**When reporting:**
- Be clear and concise
- Provide proof of concept
- Be respectful and professional
- Give reasonable deadline for fix
- Follow their disclosure timeline
- Don't publicly disclose until resolved

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "Google detected automated traffic"
**Solution:**
```bash
# Add larger delays between requests
python dork_search.py --delay 10

# Use smaller batches
python dork_search.py --limit 5

# Try manual searches instead (no risk of blocking)
```

#### Issue: "Results look like spam/irrelevant"
**Solution:**
- Try more specific dorks first
- Use more restrictive operators (site:, filetype:)
- Check if the dork is outdated
- Look for newest dorks that reference specific platforms

#### Issue: "Can't find legitimate programs"
**Solution:**
- Check established platforms first:
  - HackerOne.com
  - Bugcrowd.com
  - Intigriti.io
  - YesWeHack.com
- Use dorks that reference these platforms
- Try government and educational institution dorks

#### Issue: "Script crashes or errors"
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version

# Run with verbose output
python dork_search.py --verbose
```

#### Issue: "No results for a dork"
**Solutions:**
- The dork might be outdated
- Sites may have changed URL structure
- The operator syntax might be wrong
- Google might have indexed less of that content
- Try a similar/alternative dork

### Getting Help

**If stuck:**
1. Check this guide again
2. Read the README.md
3. Try manual Google search first
4. Review the dork syntax
5. Open an Issue on GitHub

---

## Advanced Tips

### Creating Custom Dorks

**Formula:**
```
[Scope Operator] [Required Keywords] [Exclusions]
```

**Examples:**
```
site:*.us AND intext:"bug bounty" AND intext:"hall of fame"
site:linkedin.com/company intext:"responsible disclosure" -denied
inurl:security.txt AND intext:hackerone -site:hackerone.com
```

### Monitoring

For continuous discovery:
- Set up Google Alerts for bug bounty terms
- Use RSS feeds from disclosure aggregators
- Follow security researcher communities
- Check Twitter/X hashtags: #bugbounty #infosec

### Optimization

**For maximum efficiency:**
1. Use most effective dorks first
2. Focus on high-reward programs
3. Target industries aligned with your skills
4. Join researcher communities for tips
5. Track which dorks work best

---

## Success Stories - What to Look For

Good indicators of legitimate programs:
- ✅ Mentions specific rewards ($, €, etc.)
- ✅ References well-known platforms
- ✅ Published hall of fame
- ✅ Clear vulnerability categories
- ✅ Defined response times
- ✅ SSL/HTTPS certificate
- ✅ Official company domain

Red flags to avoid:
- ❌ No reward mentioned
- ❌ Suspicious domain name
- ❌ No contact information
- ❌ Poor English/grammar
- ❌ Demands payment upfront
- ❌ No clear submission process
- ❌ Requests personal info before disclosure

---

## Next Steps

1. **Start Small** - Try 5-10 manual searches this week
2. **Build List** - Collect 20+ potential targets
3. **Verify Programs** - Check if they're legitimate and active
4. **Plan Testing** - Decide which to target first
5. **Start Hunting** - Follow their rules and report responsibly
6. **Track Results** - Keep detailed records
7. **Improve** - Use what you learn to refine your approach

---

**Happy hunting! 🔍🛡️**
