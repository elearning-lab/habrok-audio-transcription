# SSH Key Setup for Habrok

Passwordless SSH access to Habrok for faster workflow. One-time setup takes ~5 minutes.

---

## Why Set This Up?

- **No more password typing** for every SSH connection
- **Enable automation** - scripts can connect without user input
- **Faster workflow** - instant connection to Habrok

---

## Prerequisites

- Habrok account (p-number)
- Terminal access (Mac/Linux) or PowerShell (Windows)
- Access to Habrok web portal: https://portal.hb.hpc.rug.nl

---

## Step 1: Generate SSH Key (On Your Computer)

### Mac/Linux:
```bash
ssh-keygen -t ed25519 -C "habrok-access"
```

### Windows (PowerShell):
```powershell
ssh-keygen -t ed25519 -C "habrok-access"
```

**When prompted:**
- `Enter file...` → Press **Enter** (use default location)
- `Enter passphrase...` → Press **Enter** (no passphrase for automation)
- `Enter same passphrase again...` → Press **Enter**

**Output shows:**
```
Your public key has been saved in /Users/username/.ssh/id_ed25519.pub
```

---

## Step 2: Copy Your Public Key
```bash
cat ~/.ssh/id_ed25519.pub
```

**Copy the entire output** (starts with `ssh-ed25519 ...` and ends with your comment)

Example:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJl3dIeudNqd1... habrok-access
```

---

## Step 3: Add Key to Habrok (Via Web Portal)

1. Go to: **https://portal.hb.hpc.rug.nl**
2. Log in with p-number + password (+ MFA if required)
3. Click **Files** → **Home Directory**
4. Click **Show Dotfiles** (button at top)
5. Look for `.ssh` folder:
   - **If exists:** Click into it
   - **If doesn't exist:** Click **New Directory** → name it `.ssh`

6. Inside `.ssh/`, handle `authorized_keys` file:
   - **If file exists:** Click it → **Edit** → Paste your public key on a **new line** at the end
   - **If doesn't exist:** Click **New File** → name it `authorized_keys` → Paste your public key

7. Click **Save**

---

## Step 4: Set Correct Permissions

1. In web portal: **Jobs** → **Shell Access** → Click **Launch**
2. In the terminal that opens, type:
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

3. Verify permissions:
```bash
ls -la ~/.ssh/
```

**Should show:**
```
drwx------  .ssh/
-rw-------  authorized_keys
```

4. Close web terminal

---

## Step 5: Test Connection

### From Your Computer:
```bash
ssh YOUR_P_NUMBER@login1.hb.hpc.rug.nl
```

**Expected result:** You connect immediately without password prompt! 🎉

---

## Troubleshooting

### "Connection refused"

**Problem:** Network/firewall blocking connection

**Solutions:**
- Connect to RUG VPN if off-campus
- Try alternate login node: `ssh YOUR_P_NUMBER@login2.hb.hpc.rug.nl`
- Check Habrok status: https://status.hpc.rug.nl
- Use web portal as alternative: https://portal.hb.hpc.rug.nl

### "Permission denied (publickey)"

**Problem:** Key not properly configured

**Check:**
1. Did you paste the **public** key (ends in `.pub`)?
2. Is the key on a single line in `authorized_keys`?
3. Are permissions correct? (`chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`)

### Still asks for password

**Problem:** Habrok not recognizing your key

**Solutions:**
1. Verify public key is in `~/.ssh/authorized_keys` on Habrok
2. Check permissions (Step 4)
3. Try regenerating key and starting over

---

## Network Access Requirements

### On-Campus:
- Direct SSH works from university network

### Off-Campus (Home/Elsewhere):
- **Requires RUG VPN** for SSH access
- Web portal (https://portal.hb.hpc.rug.nl) works without VPN
- VPN setup: https://myuniversity.rug.nl → Search "VPN"

---

## Advanced: Multiple Keys

If you already have SSH keys for other services (GitHub, etc.), you can have multiple keys:

### Create Habrok-specific key:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_habrok -C "habrok-only"
```

### Configure SSH to use it:

Create/edit `~/.ssh/config`:
```
Host habrok
    HostName login1.hb.hpc.rug.nl
    User YOUR_P_NUMBER
    IdentityFile ~/.ssh/id_ed25519_habrok
```

**Then connect with:**
```bash
ssh habrok
```

---

## Security Notes

- **Never share your private key** (`id_ed25519` without `.pub`)
- **Only share the public key** (`id_ed25519.pub`)
- Private key stays on your computer only
- If compromised, remove the public key from Habrok's `authorized_keys` and generate new keys

---

## See Also

- [SETUP.md](SETUP.md) - Main Habrok setup guide
- [QUICK_START.md](QUICK_START.md) - Daily workflow
- Habrok SSH docs: https://wiki.hpc.rug.nl/habrok/connecting_to_the_system/connecting

---

## Support

- **Habrok issues:** https://wiki.hpc.rug.nl/habrok/
- **This workflow:** Open an issue on this repository
