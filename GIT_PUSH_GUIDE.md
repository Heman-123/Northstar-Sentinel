# Step-by-Step Guide: Pushing Northstar Sentinel to GitHub
**Repository URL:** `https://github.com/Heman-123/Northstar-Sentinel.git`  
**Local Project Directory:** `C:\Users\DELL\.gemini\antigravity\scratch\Northstar-Sentinel`

---

### Step 1: Open PowerShell or Command Prompt
Open your terminal (PowerShell, CMD, or Git Bash) and navigate to the project directory:

```bash
cd C:\Users\DELL\.gemini\antigravity\scratch\Northstar-Sentinel
```

---

### Step 2: Initialize Git & Check Status
If the repository is not already initialized, run:

```bash
git init
git status
```

---

### Step 3: Add the Remote Origin
Link your local project to your GitHub repository:

```bash
git remote remove origin 2>nul || true
git remote add origin https://github.com/Heman-123/Northstar-Sentinel.git
git branch -M main
```

---

### Step 4: Stage All Files
Add all the forensic scripts, tests, evidence, deliverables, and React application:

```bash
git add .
```

Verify that all files are staged:

```bash
git status
```

---

### Step 5: Commit the Changes with a Professional Forensic Message
```bash
git commit -m "feat: complete Northstar Sentinel platform for CRIMEATHON 26 (DEFENSE Track)

- Implemented 6-stage evidence processing and DFIR pipeline
- Created 10 behavioral & policy detection rules (DET-001 to DET-010)
- Engineered Zero-Trust Policy Enforcement Point (PEP) with IP pinning & scope gates
- Built dark-mode React + Tailwind CSS SOC Command Center
- Added 10 automated test cases with 100% pass rate
- Completed Deliverables 1 (Problem Statement), 2 (PPT Deck), and 4 (Video Script)"
```

---

### Step 6: Push to GitHub
Push the branch to GitHub:

```bash
git push -u origin main --force
```

*(If prompted, log in with your GitHub credentials or Personal Access Token).*

---

### Step 7: Verify on GitHub
Visit [https://github.com/Heman-123/Northstar-Sentinel](https://github.com/Heman-123/Northstar-Sentinel) to confirm all files, directories, deliverables, and the README are live!
