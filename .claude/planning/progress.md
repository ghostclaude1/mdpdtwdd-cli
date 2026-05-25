# Progress Log — mdpdtwdd-cli TOC Gap Investigation

## Session 1 — 2026-05-25

### Completed
- [x] Read SKILL.md, CLAUDE.md, SRS.md
- [x] Audit tất cả 7 modules
- [x] Fix ISSUE-008, 009, 010 → commit dfb5df9 → pushed
- [x] Viết task_plan.md, findings.md

### Current state
- Baseline: TOC=4260, paper=1654, gap=+158%
- Phase 1 bắt đầu: kiểm tra open route handling
- findings.md F-005: hypothesis H1 có khả năng cao — clustering tách delivery/pickup ra 2 depot riêng → không bao giờ tạo mixed route → không có open route → thừa depot-return leg

### Next action
- Verify F-005: chạy code trace xem thực tế có open route nào không
- Nếu không có → fix clustering để cho phép mixed assignment hoặc force open route khi customer types cross depots
