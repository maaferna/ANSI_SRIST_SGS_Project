
# 🚀 Development Environment Setup (Ubuntu ECS + GitHub + Python)

This guide explains how to configure a **secure, isolated development environment**
on a Huawei Cloud ECS (Ubuntu) using:

- Non-root user (`mparraf_dev`)
- Git + GitHub SSH
- Python virtual environments (venv / Conda)
- Safe collaboration workflow
- Corporate GitHub migration readiness

---

## 1️⃣ Use a Non-Root Development User

### 1.1 Verify Current User

```bash
whoami
pwd
````

Expected:

```
mparraf_dev
/home/mparraf_dev
```

### 1.2 Ensure Sudo Access

```bash
sudo whoami
```

If not authorized, as root:

```bash
usermod -aG sudo mparraf_dev
```

Then log out/in.

---

## 2️⃣ Recommended Project Layout

Never work inside `/root`.

```bash
mkdir -p ~/dev ~/dev/_repos ~/dev/_data ~/dev/_models
```

Structure:

```
~/dev/
 ├── _repos/     → Git repositories
 ├── _data/      → Datasets
 └── _models/    → Trained models
```

---

## 3️⃣ Install System Dependencies

```bash
sudo apt update
sudo apt install -y git curl wget ca-certificates build-essential
git --version
```

---

## 4️⃣ Configure Git Identity (User Only)

```bash
git config --global user.name "Marco Parra"
git config --global user.email "maaferna@gmail.com"
git config --global init.defaultBranch main
git config --global pull.rebase false

git config --global --list
```

---

## 5️⃣ Configure GitHub SSH (Personal Account)

### 5.1 Create SSH Directory

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

---

### 5.2 Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "maaferna@github.com" \
-f ~/.ssh/id_ed25519_github_personal
```

Permissions:

```bash
chmod 600 ~/.ssh/id_ed25519_github_personal
chmod 644 ~/.ssh/id_ed25519_github_personal.pub
```

---

### 5.3 Start SSH Agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github_personal
ssh-add -l
```

---

### 5.4 Configure SSH (Cloud Safe / Port 443)

Many cloud networks block port 22.

```bash
cat > ~/.ssh/config <<'EOF'
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/id_ed25519_github_personal
  IdentitiesOnly yes
EOF

chmod 600 ~/.ssh/config
```

---

### 5.5 Register Key on GitHub

```bash
cat ~/.ssh/id_ed25519_github_personal.pub
```

Copy → GitHub → Settings → SSH Keys → New Key.

---

### 5.6 Test Connection

```bash
ssh -T git@github.com
```

Expected:

```
Hi username! You've successfully authenticated
```

---

## 6️⃣ Clone vs Init

### Clone Existing Repository

```bash
cd ~/dev/_repos
git clone git@github.com:USER/REPO.git
cd REPO
```

---

### Create New Repository

```bash
cd ~/dev/_repos
mkdir my_project
cd my_project

git init
echo "# my_project" > README.md

git add .
git commit -m "Initial commit"

git remote add origin git@github.com:USER/my_project.git
git branch -M main
git push -u origin main
```

---

---

## 9️⃣ Corporate GitHub Migration (Future-Proof)

### Option 1 — Organization Access (Best)

Later:

```bash
git remote set-url origin git@github.com:ORG/REPO.git
```

---

### Option 2 — Multiple SSH Accounts

Generate corporate key:

```bash
ssh-keygen -t ed25519 -C "user@company.com" \
-f ~/.ssh/id_ed25519_github_corp
```

Update SSH config:

```bash
Host github-personal
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/id_ed25519_github_personal

Host github-corp
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/id_ed25519_github_corp
```

Set remote:

```bash
git remote set-url origin git@github-corp:ORG/REPO.git
```

---

## 🔍 10️⃣ Verification Checklist

```bash
git status
git remote -v
git log -1

ssh -T git@github.com
python --version
which python
```

Venv:

```bash
echo $VIRTUAL_ENV
```

Conda:

```bash
conda info --envs
```

---

## 🛠️ 11️⃣ Troubleshooting

### Not a Git Repository

```bash
cd project_folder
# or
git init
```

---

### Permission Denied (SSH)

```bash
ssh-add -l
ssh -vT git@github.com
```

---

### Port 22 Blocked

Use:

```
ssh.github.com:443
```

---

### Docker Permission Issues

```bash
sudo chown -R mparraf_dev:mparraf_dev PROJECT_DIR
```

---

## ✅ Best Practices

* Never develop as root
* One SSH key per account
* One venv per project
* Always use .gitignore
* Use branches for features
* Freeze dependencies

---

## 📌 Recommended Workflow

```bash
cd ~/dev/_repos/project
source .venv/bin/activate

git checkout -b feature-x
git commit -am "Feature work"
git push origin feature-x
```

Create Pull Request → Merge → Delete branch.

---
