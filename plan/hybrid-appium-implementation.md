# Hybrid Appium CI/CD Implementation

Tai lieu nay mo ta phien ban CI/CD phuc vu demo cuoi ky theo mo hinh hybrid:

- Build APK tren GitHub-hosted runner
- Truyen APK qua GitHub artifact
- Chay Appium Python tests tren Windows self-hosted runner
- Upload report, screenshot va log ve GitHub Actions

## File da duoc them vao repo

- `.github/workflows/appium-hybrid-ci.yml`
- `requirements.txt`
- `tests/`
- `pages/`
- `apps/.gitkeep`
- `reports/.gitkeep`
- `screenshots/.gitkeep`
- `logs/.gitkeep`

## Luong chay

1. Pull request vao `main` kich hoat workflow `Appium Hybrid CI`
2. Job `build-apk` build `app-debug.apk` tren `ubuntu-latest`
3. APK duoc upload thanh artifact `android-debug-apk`
4. Job `appium-test` chay tren Windows self-hosted runner
5. Job tai APK ve thu muc `apps/`
6. Workflow start Appium Server va doi endpoint `/status` san sang
7. `pytest` chay smoke tests trong `tests/`
8. `report.html`, `junit.xml`, screenshot va `appium.log` duoc upload lai len GitHub

## Viec can lam tren may self-hosted runner

1. Cai JDK 17
2. Cai Android SDK va dam bao `adb devices` thay thiet bi/emulator
3. Cai Node.js 20
4. Cai Appium 2 va `uiautomator2`
5. Cai Python va kiem tra `pip install -r requirements.txt`
6. Dang ky runner voi label `self-hosted`, `Windows`

## Lenh kiem tra nhanh

```powershell
java -version
adb devices
node -v
appium -v
appium driver list --installed
python --version
pytest --version
```

## Smoke tests hien co

- `test_open_catalog`
- `test_login_success`
- `test_login_empty_credentials`

## Quality gate

- Neu `pytest` fail thi job `Appium Test` fail
- Artifact van duoc upload nho `if: always()`
- Co the bat branch protection tren `main` de khong merge khi `Appium Test` fail