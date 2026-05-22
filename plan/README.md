# CI/CD Plan

Tài liệu trong thư mục này mô tả kiến trúc và kế hoạch triển khai CI/CD cho project Android hiện tại, tập trung vào GitHub Actions, Espresso, Appium và Sauce Labs.

## Tài liệu

- `architecture.md`: kiến trúc tổng thể của pipeline
- `implementation.md`: kế hoạch triển khai, checklist cấu hình và rollout

## Mục tiêu

- Chuẩn hóa merge gate cho `main`/`master`
- Tách rõ test bắt buộc và test smoke
- Giảm flaky test trên pull request
- Giữ khả năng mở rộng sang Sauce Labs cloud
