# my-demo-app-android

*My Demo App* is a... demo app! 
It was built by the Sauce Labs team to showcase product capabilities of the Sauce Labs mobile devices cloud, The Sauce Labs mobile beta testing platform, TestFairy, and more products and technologies that will be added to this project soon.

This app is part of a set of demo apps.

[My Demo App - Android](https://github.com/saucelabs/my-demo-app-android)

[My Demo App - iOS](https://github.com/saucelabs/my-demo-app-ios)

### QR code scanner

This app has a QR code scanner.
You can find it in the menu under the option "QR CODE SCANNER".
This page opens the camera (you first need to allow the app to use the camera) which can be used to scan a QR Code.
If the QR code holds an URL it will automatically open it in a browser. The [following image](./docs/assets/qr-code.png)
can be used to demo this option.

![QR Code](./docs/assets/qr-code.png)

## Publish

To publish a new version, create a release with a valid semver tag name. A CI workflow will handle setting the app version name/code and upload the APK into the release. 

## CI/CD

This repository now supports a split mobile CI flow on GitHub Actions:

- `Android CI`: required checks for pull requests and pushes to `main`/`master`
- `Appium Smoke`: Appium-based login smoke test on a GitHub-hosted Android emulator
- `Appium Hybrid CI`: build APK on a GitHub-hosted runner and run Appium Python tests on a Windows self-hosted runner
- `Publish APK`: release build on tag push

### Mandatory checks

The required merge gate should be the `Android CI` workflow:

- `build-and-unit`: `lintDebug`, `testDebugUnitTest`, `assembleDebug`, `assembleDebugAndroidTest`
- `mandatory-espresso`: runs instrumentation tests tagged with:
  - `com.saucelabs.mydemoapp.android.HappyFlow`
  - `com.saucelabs.mydemoapp.android.ErrorFlow`

This keeps the PR gate focused on business-critical happy/error flows and avoids running every long-running UI test on every commit.

### Appium on GitHub Actions

The `Appium Smoke` workflow:

- builds the debug APK
- boots an Android emulator
- installs Appium 2 with the `uiautomator2` driver
- runs `AppiumLoginTest`

`AppiumLoginTest` reads these environment variables:

- `APPIUM_SERVER_URL`
- `APPIUM_DEVICE_NAME`
- `APPIUM_APP`

If `APPIUM_APP` is missing, the test falls back to launching an already-installed app by package/activity.

### Hybrid Appium CI

The hybrid pipeline is implemented in `.github/workflows/appium-hybrid-ci.yml`.

- `build-apk` runs on `ubuntu-latest` and uploads `app-debug.apk` as a GitHub Actions artifact.
- `appium-test` runs on a Windows `self-hosted` runner, downloads the APK artifact, starts Appium Server locally, and runs `pytest` Appium smoke tests from `tests/`.
- Reports, screenshots, and Appium logs are uploaded with `if: always()` so failed runs still produce demo evidence.

The Python Appium suite lives in:

- `tests/`: pytest test cases and fixtures
- `pages/`: Page Object Model wrappers
- `requirements.txt`: Python dependencies for the self-hosted runner

Recommended self-hosted runner prerequisites:

- JDK 17
- Android SDK and `adb`
- Node.js 20
- Appium 2 + `uiautomator2` driver
- Python 3.10 or 3.11

Reference commands:

```powershell
java -version
adb devices
node -v
appium -v
appium driver list --installed
python --version
pytest --version
```

### Optional Sauce Labs cloud run

If the repository defines the secrets below, the `Android CI` workflow also runs the existing Sauce Labs Espresso suite:

- `SAUCE_USERNAME`
- `SAUCE_ACCESS_KEY`

### Suggested branch protection

Protect `main` and require these status checks:

- `Build and Unit Tests`
- `Mandatory Android Tests`
- `Build APK`
- `Appium Test`