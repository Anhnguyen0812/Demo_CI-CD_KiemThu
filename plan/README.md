# CI/CD Plan

Tai lieu trong thu muc nay mo ta kien truc va ke hoach trien khai CI/CD cho project Android hien tai, tap trung vao GitHub Actions, Espresso, Appium va Sauce Labs.

## Tai lieu

- `architecture.md`: kien truc tong the cua pipeline
- `implementation.md`: ke hoach trien khai, checklist cau hinh va rollout
- `appium-cicd-guide.md`: huong dan tong quan cho Appium CI/CD
- `hybrid-appium-implementation.md`: huong dan trien khai hybrid Appium voi Windows self-hosted runner

## Muc tieu

- Chuan hoa merge gate cho `main`/`master`
- Tach ro test bat buoc va test smoke
- Giam flaky test tren pull request
- Giu kha nang mo rong sang Sauce Labs cloud
- Co san tai lieu de demo hybrid Appium CI/CD cho bao cao cuoi ky