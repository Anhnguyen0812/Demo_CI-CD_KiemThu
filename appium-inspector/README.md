# Appium Inspector Profiles

## Files

- `device-installed-app.json`: dung khi app da cai san tren dien thoai.
- `local-apk.json`: dung khi muon mo app tu file APK local.

## Appium Server

Trong Appium Inspector, su dung remote host:

- Host: `127.0.0.1`
- Port: `4723`
- Path: `/`

Neu ban chay Appium theo kieu cu thi co the dung path `/wd/hub`, nhung workflow hybrid hien tai dang start voi `--base-path /`.

## Luu y

- Neu thay doi dien thoai, sua lai `appium:udid` va `appium:deviceName`.
- Neu APK duoc build o duong dan khac, sua lai truong `appium:app` trong `local-apk.json`.
- Neu app chua cai san, uu tien `local-apk.json`.