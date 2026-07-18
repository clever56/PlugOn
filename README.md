# Bug Bounty Dorks - Security Research Tool

## 🎯 Overview

A comprehensive collection of Google search queries ("dorks") designed to help security researchers and bug bounty hunters discover bug bounty programs, vulnerability disclosure policies, and security reward programs worldwide.

This project contains **100+ carefully curated search queries** to find:
- Active bug bounty programs
- Vulnerability disclosure policies
- Security reward programs
- Organizations with security.txt files
- Responsible disclosure policies
- Companies offering bug bounties in different regions and currencies

## 📚 What Are Google Dorks?

Google dorks are specialized search queries using advanced Google search operators to find specific information on the internet. Common operators include:

- `inurl:` - Find pages with specific words in the URL
- `intext:` - Find pages containing specific text
- `site:` - Limit search to a specific domain or TLD
- `filetype:` - Find specific file types
- `intitle:` - Find pages with specific words in the title
- `-` - Exclude results containing this term
- `""` - Search for exact phrase

## 🚀 How to Use

### Method 1: Manual Search (Quick & Simple)

1. Open [Google](https://www.google.com)
2. Copy a dork from `dorks.txt`
3. Paste it into the Google search bar
4. Press Enter
5. Review results for bug bounty programs

### Method 2: Automated Script (Recommended)

See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed instructions on running the automated Python script.

## 📂 Files Included

- **dorks.txt** - Raw list of all Google dorks (one per line)
- **README.md** - This file, project overview
- **USAGE_GUIDE.md** - Detailed step-by-step guide
- **dork_search.py** - Python script for automated searching
- **requirements.txt** - Python dependencies

## 🎓 Understanding the Dorks

### By Category

#### General Bug Bounty Programs
```
inurl /bug bounty
inurl:security "reward"
"powered by bugcrowd" -site:bugcrowd.com
```

#### Vulnerability Disclosure Policies
```
inurl:responsible-disclosure-policy
inurl:/.well-known/security.txt
"If you believe you've found a security vulnerability"
```

#### Government & Education
```
site:*.gov* "vulnerability disclosure program"
site:*.edu "responsible disclosure" AND (reward OR swag OR bounty)
```

#### Regional Searches
```
site:*.nl responsible disclosure          # Netherlands
site:*.uk intext:security report reward   # United Kingdom
site:*.de inurl:bug inurl:bounty          # Germany
site:*.fr intext:"bug bounty"             # France
```

#### Currency-Specific
```
inurl:"bug bounty" and intext:"$"       # USD rewards
inurl:bug bounty intext:"€"              # EUR rewards
inurl:bug bounty intext:"₹"              # INR rewards
```

## ⚠️ Legal & Ethical Considerations

**IMPORTANT**: Always follow these rules:

1. **Authorized Access Only** - Only test systems you own or have explicit written permission to test
2. **Follow Responsible Disclosure** - If you find a vulnerability, follow the program's disclosure policy
3. **Respect Rate Limits** - Don't hammer servers with automated requests
4. **Read Terms & Conditions** - Always review the program's rules before participation
5. **Stay Legal** - Ensure your testing complies with local laws and regulations
6. **Document Everything** - Keep records of your findings and communications

## 🔧 Quick Start

### For Manual Users:
```bash
1. Open dorks.txt
2. Copy a dork query
3. Paste in Google
4. Review results
5. Visit promising targets and check their security pages
```

### For Python Users:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the search script
python dork_search.py
```

## 💡 Tips for Success

1. **Be Specific** - Start with regional or niche dorks before broader searches
2. **Verify Programs** - Always verify that programs are legitimate before reporting
3. **Check Scope** - Confirm the vulnerability is within the program's scope
4. **Follow Policies** - Each program has different rules and reward structures
5. **Keep Records** - Document your findings with timestamps and details
6. **Be Professional** - Communicate respectfully with program managers

## 📊 Expected Results

You should find:
- Bug bounty platform links (HackerOne, Bugcrowd, Intigriti, etc.)
- Direct corporate bug bounty programs
- Vulnerability disclosure policies
- Security contact information
- Hall of fame pages
- Security reward structures

## 🌐 Supported Regions

Dorks included for:
- 🇺🇸 United States (com, gov)
- 🇬🇧 United Kingdom (uk)
- 🇳🇱 Netherlands (nl)
- 🇩🇪 Germany (de)
- 🇫🇷 France (fr)
- 🇪🇸 Spain (es)
- 🇮🇹 Italy (it)
- 🇦🇺 Australia (au)
- 🇧🇷 Brazil (br)
- 🇯🇵 Japan (jp)
- 🇸🇪 Sweden (se)
- 🇩🇰 Denmark (dk)
- 🇳🇴 Norway (no)
- 🇨🇭 Switzerland (ch)
- And many more!

## 📝 Contributing

Found a new effective dork? Want to improve the list?

1. Fork this repository
2. Add your dorks to `dorks.txt`
3. Submit a pull request with a description

## ⚖️ Disclaimer

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring their use complies with all applicable laws and regulations. Unauthorized access to computer systems is illegal. Always obtain written permission before testing any system you do not own.

## 📞 Support

For questions or issues:
- Open an Issue on GitHub
- Check USAGE_GUIDE.md for detailed help
- Review the dork explanations in this README

## 📜 License

This project is provided as-is for educational purposes.

---

**Happy Hunting! 🔍🛡️**
