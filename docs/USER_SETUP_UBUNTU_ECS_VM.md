# 🚀 Ubuntu VM Development User Setup (Cloud / ECS / Enterprise)

This document describes the **recommended procedure to create and configure a non-root development user** on an Ubuntu Virtual Machine in a cloud environment.

The objective is to ensure:

- Security
- Access control
- Auditability
- Safe collaboration
- Long-term scalability
- Separation between system administration and development

---

## 📌 Objectives

This setup prevents:

- Development as `root`
- Accidental system damage
- Security risks
- Credential sharing
- Configuration conflicts

And enables:

- Per-user GitHub access
- Corporate account migration
- Controlled sudo usage
- Isolated environments

---

## 1️⃣ Initial Access as Root

Most cloud instances provide initial access as `root`.

Verify:

```bash
whoami
````

Expected:

```
root
```

If not:

```bash
sudo -i
```

---

## 2️⃣ Create Development User

Create a dedicated development user.

Example:

```bash
adduser mparraf_dev
```

Follow the interactive prompts.

You may leave optional fields blank.

---

## 3️⃣ Grant Sudo Privileges

Allow the user to install packages and manage services.

```bash
usermod -aG sudo mparraf_dev
```

Verify:

```bash
groups mparraf_dev
```

Must include:

```
sudo
```

---

## 4️⃣ Configure SSH Access

Never reuse root SSH keys.

Each user must have independent credentials.

---

### 4.1 Create SSH Directory

Switch to user:

```bash
su - mparraf_dev
```

Create SSH directory:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

---

### 4.2 Copy Existing Key (Optional)

If root already has SSH access:

```bash
sudo cp /root/.ssh/authorized_keys /home/mparraf_dev/.ssh/
sudo chown -R mparraf_dev:mparraf_dev /home/mparraf_dev/.ssh
sudo chmod 600 /home/mparraf_dev/.ssh/authorized_keys
```

Recommended only for temporary use.

---

### 4.3 Recommended: Generate New Key

From your local machine:

```bash
ssh-keygen -t ed25519 -C "mparraf_dev@ecs"
ssh-copy-id mparraf_dev@VM_IP
```

---

## 5️⃣ Disable Root SSH Login (Recommended)

⚠️ Perform only after confirming user access.

Edit SSH config:

```bash
sudo nano /etc/ssh/sshd_config
```

Find:

```
PermitRootLogin yes
```

Change to:

```
PermitRootLogin no
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

---

## 6️⃣ Prepare Development Workspace

Login as user:

```bash
su - mparraf_dev
```

Create structure:

```bash
mkdir -p ~/dev/{repos,data,models,logs}
```

Result:

```
/home/mparraf_dev/dev/
 ├── repos
 ├── data
 ├── models
 └── logs
```

---

## 7️⃣ Shared Team Access (Optional)

For multi-user environments.

Create group:

```bash
sudo groupadd devteam
sudo usermod -aG devteam mparraf_dev
```

Shared directory:

```bash
sudo mkdir -p /srv/projects
sudo chgrp -R devteam /srv/projects
sudo chmod -R 2775 /srv/projects
```

---

## 8️⃣ Install Base Development Packages

As user:

```bash
sudo apt update
sudo apt install -y \
git \
curl \
wget \
vim \
htop \
tmux \
build-essential \
python3-pip \
python3-venv
```

---

## 9️⃣ Configure Git Identity (Per User)

```bash
git config --global user.name "Marco Parra"
git config --global user.email "user@company.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

Verify:

```bash
git config --global --list
```

---

## 🔟 Configure GitHub SSH Access (Per User)

Generate key:

```bash
ssh-keygen -t ed25519 -C "github@company.com"
```

Start agent:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Upload `.pub` key to GitHub.

Test:

```bash
ssh -T git@github.com
```

---

## 1️⃣1️⃣ Clone or Initialize Projects

### Clone Existing Repository

```bash
cd ~/dev/repos
git clone git@github.com:ORG/REPO.git
```

---

### Create New Repository

```bash
cd ~/dev/repos
mkdir project
cd project

git init
echo "# Project" > README.md

git add .
git commit -m "Initial commit"

git remote add origin git@github.com:ORG/project.git
git push -u origin main
```

---

## 1️⃣2️⃣ Python Virtual Environments

### Using venv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Freeze:

```bash
pip freeze > requirements.lock.txt
```

---

### Using Conda/Mamba

```bash
mamba create -n project python=3.11
mamba activate project
mamba env export --no-builds > environment.yml
```

---

## 1️⃣3️⃣ Corporate GitHub Migration

When organization account is created:

```bash
git remote set-url origin git@github.com:ORG/REPO.git
```

No local changes required.

---

## 1️⃣4️⃣ Verification Checklist

```bash
whoami
groups
pwd
sudo whoami

git status
git remote -v

ssh -T git@github.com
python --version
```

---

## 1️⃣5️⃣ Troubleshooting

### Not a Git Repository

```bash
git init
```

Or clone.

---

### SSH Permission Denied

```bash
ssh-add -l
ssh -vT git@github.com
```

---

### File Permission Errors

```bash
sudo chown -R mparraf_dev:mparraf_dev ~/dev
```

---

## ✅ Best Practices

| Rule                           | Status |
| ------------------------------ | ------ |
| Never use root for development | ✅      |
| One SSH key per user           | ✅      |
| One virtual env per project    | ✅      |
| Use .gitignore                 | ✅      |
| Use feature branches           | ✅      |
| Regular backups                | ✅      |

---

## 📌 Recommended Daily Workflow

```bash
ssh mparraf_dev@vm
cd ~/dev/repos/project
source .venv/bin/activate

git pull
git checkout -b feature-x
git commit -am "Feature work"
git push origin feature-x
```

Create Pull Request → Merge → Delete branch.

---

## 🏁 Summary

This approach ensures:

✔ Secure access
✔ Individual accountability
✔ Corporate readiness
✔ Minimal operational risk
✔ Professional workflow

---
