#  TikTok Shop Bot – Scale Your Partnerships

<p align="center"> <a href="https://github.com/yourusername/facebook-bot"> <img src="https://img.shields.io/badge/Try%20It%20Free-1E90FF?style=for-the-badge&logo=fire&logoColor=white" alt="Try it Free" width="30%"> </a> </p>

<p align="center">
  <a href="https://discord.gg/vBu9huKBvy">
    <img src="https://img.shields.io/badge/Join-Discord-5865F2?logo=discord" alt="Join Discord">
  </a>
  <a href="https://t.me/devpilot1">
    <img src="https://img.shields.io/badge/Contact-Telegram-2CA5E0?logo=telegram" alt="Contact on Telegram">
  </a>
</p>

---

##  About

**TikTok Shop Affiliate Outreach Bot** is a workflow assistant that helps sellers, brands, and agencies **scale affiliate recruitment** on TikTok Shop.  
It centralizes affiliate databases, automates personalized messaging, prevents duplication, and tracks replies—so you can grow faster without drowning in spreadsheets.

This bot helps you:  
- Import leads from affiliate databases or CSV files  
- Generate and personalize outreach messages  
- Automate follow-up sequences  
- Track statuses with a CRM-style pipeline  
- Manage multiple shops and campaigns from one place  

---

##  Features

| Feature                     | Description |
|------------------------------|-------------|
| **Cross-Platform Compatibility** | Works on Windows, Mac, and VPS for easy installation and use |
| **Up-To-Date Affiliate Database** | Access 900k+ TikTok Shop affiliate profiles |
| **100k Email List**         | Access a comprehensive list of 100k emails for outreach |
| **Automate Open Collaboration** | Seamlessly automate open collaboration initiatives |
| **Automate Target Collaboration** | Effortlessly automate targeted collaboration efforts |
| **Dashboard Overview**      | Unified dashboard to track outreach efforts |
| **AI Smart Bot**            | Personalized messages, duplication detection, and smart filtering |
| **5X Your Product Sale**    | Boost sales by 500% and sample requests by 400% |
| **Multiple Shops Automation** | Manage multiple brands from one place |
| **Advanced Database Search** | Efficient and precise affiliate data retrieval |
| **Personalized Messaging Automation** | Craft unique messages while maintaining brand voice |
| **Smart Duplication Prevention** | Intelligent detection to eliminate duplicate affiliates |
| **Premium Support**         | VIP support via WhatsApp, meetings, email, and Discord |
| **Mimicking Your VA**       | Human-like typing with varying speed for natural interaction |
| **Product Cards**           | Include product cards in messages |
| **Follow-up Messages**      | Prevent duplicates but ensure consistent follow-ups |
| **Proven Results**          | 30% increase in sample requests and 40% increase in sales |
| **Stats**                   | 150+ brands using TTinit, 2.5M+ messages sent, 40K sample requests received, 1.2M follow-ups sent |

---

##  Use Cases

- **Sellers** → Recruit affiliates faster, boost shop exposure, and increase product sales  
- **Agencies** → Manage outreach for multiple client shops with one tool  
- **Affiliate Managers** → Track campaigns, prevent duplicates, and measure responses  
- **Growth Teams** → Automate messaging while keeping personalization and compliance  

---

##  Installation

### 1. Clone & Install
```bash
# 1) Install deps
pip install -r requirements.txt

# 2) Configure environment
cp .env.example .env  # fill SMTP vars if you want email sending

# 3) Validate & dedupe leads
python -m src.cli validate --in data/leads.csv --out data/leads.valid.csv

# 4) Render outreach messages from template
python -m src.cli render --in data/leads.valid.csv --template templates/intro_email.md --out out/intro.batch.csv

# 5a) Send via email (dry-run first)
python -m src.cli send --batch out/intro.batch.csv --channel email --dry-run
# remove --dry-run to actually send after you’ve configured SMTP

# 5b) OR produce manual DM checklist (you send messages yourself on TikTok)
python -m src.cli send --batch out/intro.batch.csv --channel manual_dm --out out/dm_checklist.csv

# 6) Prepare a follow-up batch from the sent log
python -m src.cli followup --log reports/sent.log.csv --days-since 3 --template templates/followup_email.md --out out/followup.batch.csv

# 7) Update a lead status when someone replies
python -m src.cli update --in data/leads.valid.csv --id "@coolcreator" --status replied --notes "Wants product sample"

# 8) Generate a weekly summary report
python -m src.cli report --log reports/sent.log.csv --out reports/weekly_summary.csv

