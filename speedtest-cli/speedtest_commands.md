# 🧪 Speedtest Trigger CLI - Test Commands

This file contains all commands to test the functionality of `speedtest.py`.

---

## ✅ BASIC CHECKS

### 1. Checker mode (no data)
```bash
python speedtest.py --no-download --no-upload
```

### 2. Trigger only (light mode)
```bash
python speedtest.py --no-download
```

### 3. Download only (main use case)
```bash
python speedtest.py --no-upload
```

### 4. Full test (default)
```bash
python speedtest.py
```

---

## ⚙️ PARAMETER TESTS

### 5. Short test (low data)
```bash
python speedtest.py --no-upload --seconds 5 --threads 2 --download-max-mb 10
```

### 6. Ultra low data test
```bash
python speedtest.py --no-upload --seconds 3 --threads 1 --download-max-mb 5
```

### 7. High load test (stress)
```bash
python speedtest.py --threads 6 --seconds 10 --download-max-mb 50
```

### 8. Upload only test
```bash
python speedtest.py --no-download --upload-max-mb 5
```

---

## ⏱️ DELAY TESTS

### 9. No delay
```bash
python speedtest.py --delay 0
```

### 10. Longer delay
```bash
python speedtest.py --delay 5
```

---

## 🧠 EDGE CASE TESTS

### 11. Checker mode with delay (should NOT wait)
```bash
python speedtest.py --no-download --no-upload --delay 5
```

### 12. High threads (robustness test)
```bash
python speedtest.py --threads 50 --seconds 1
```

---

## 🔥 REAL USE CASE

### 13. Recommended (efficient + effective)
```bash
python speedtest.py --no-upload --seconds 5 --download-max-mb 10
```

---

## 🔁 LOOP TESTING

### Git Bash / Linux
```bash
for i in {1..3}; do python speedtest.py --no-upload --seconds 5; sleep 5; done
```

### Windows PowerShell
```powershell
for ($i=0; $i -lt 3; $i++) { python speedtest.py --no-upload --seconds 5; Start-Sleep 5 }
```

---

## ✅ What You're Testing

| Test Type        | Purpose                          |
|-----------------|----------------------------------|
| Checker Mode    | No data usage, server + ping only |
| Trigger Mode    | Light ISP trigger                |
| Download Test   | Main boost trigger               |
| Upload Test     | Optional traffic simulation      |
| Parameters      | Stability and limits             |
| Delay           | Timing behavior                  |
| Stress Test     | Thread handling                  |

---

## 🚀 Notes

- Use `--no-download --no-upload` for **pure checker mode**
- Use `--no-upload` for **best balance (low data + effective trigger)**
- Default mode runs **full test (download + upload)**
