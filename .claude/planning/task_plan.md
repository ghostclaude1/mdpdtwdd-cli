# Task Plan — mdpdtwdd-cli Bug Hunt (Phase: TOC Gap Diagnosis)

**Goal:** Xác định và fix bug khiến TOC gap còn +158% (actual 4260 vs paper 1654)
**Created:** 2026-05-25
**Baseline:** TOC=4260 | TC=1045 (3.4× paper) | PC=1311 | NV=9 | CT=4.3s

---

## Known State (sau commit dfb5df9)

| Component | Actual | Paper | Gap |
|-----------|--------|-------|-----|
| TC        | 1,045  | ~304  | 3.4× |
| PC        | 1,311  | ~0    | huge |
| MC        | 769    | 659   | NV=7 vs 6 |
| FC        | 691    | 691   | ✅ |
| TOC       | 4,260  | 1,654 | +158% |

**Verified clean:** data_loader, objectives, clustering, PMX, nondominated_sort, main loop

---

## Hypothesis Ranking (theo impact ước tính)

| # | Hypothesis | Impact | Khả năng | Phase |
|---|-----------|--------|---------|-------|
| H1 | Route decoding sai — open route DD→PD không được tạo đúng, mọi route đều closed → thêm leg về depot không cần thiết, tăng TC | HIGH | HIGH | Phase 1 |
| H2 | PC=1311 do l_i-sort không giải quyết được: paper có thể dùng actual arrival-time sort (không phải l_i sort) | HIGH | MEDIUM | Phase 2 |
| H3 | Clustering s/t=0.5 inferred sai → customers phân về sai depot → routes dài hơn | MEDIUM | MEDIUM | Phase 3 |
| H4 | NV=9 (paper 6) sau dynamic insertion — scenario_3 dispatch thêm vehicle cho mỗi dynamic customer | MEDIUM | HIGH | Phase 4 |
| H5 | B_v backward pass tính sai → B_v không optimal → PC tăng | LOW | LOW | Phase 5 |

---

## Phases

### Phase 1 — Open Route Handling Audit ⬅ CURRENT
**Question:** Routes DD→customers→PD có được tạo đúng không? Hay tất cả đều closed (về cùng depot)?
**What to check:**
- [ ] In `_get_route_endpoints`: điều kiện tạo open route (has_delivery AND has_pickup)
- [ ] Verify thực tế: sau 150 gen, có bao nhiêu open routes trong best solution?
- [ ] Tính manual: nếu toàn closed routes, TC extra = 2× (depot-return leg) cho mixed customers
- [ ] So sánh TC với và không có open route

**Expected outcome:** Nếu routes đang closed khi phải open → fix → TC giảm đáng kể

**Success criterion:** TC giảm ≥ 30% sau fix

---

### Phase 2 — PC=1311 Root Cause
**Question:** Tại sao l_i-sort không đủ để PC→0?
**What to check:**
- [ ] Verify paper's claim PC≈0: tính thử với perfect TW compliance route
- [ ] Check B_v computation: nếu B_v quá sớm/muộn, toàn bộ route bị penalty cascade
- [ ] Check TW data: l_i/r_i windows có đủ rộng không? Nếu quá chặt, ngay cả optimal route cũng bị PC
- [ ] Trace arrival times trên best solution route-by-route

**Blocked by:** Phase 1 (TC fix có thể thay đổi route structure, ảnh hưởng PC)

---

### Phase 3 — Clustering Quality
**Question:** s/t=0.5 có khiến customers về sai depot không?
**What to check:**
- [ ] Với Instance 1 (1 DD, 1 PD): clustering chỉ có 1 depot mỗi loại → không thể assign sai depot
- [ ] Với Instance 11+ (2 DD): kiểm tra xem customers có hợp lý không
- [ ] Thử s=0.7/t=0.3 và s=0.3/t=0.7, so sánh TOC

---

### Phase 4 — Dynamic Insertion NV Impact
**Question:** Tại sao NV=9 khi paper NV=6?
**What to check:**
- [ ] Before insertion: NV=? (pre-dynamic)
- [ ] Mỗi dynamic customer dùng scenario nào (1, 2, hay 3)?
- [ ] Scenario 3 (new vehicle) bị gọi bao nhiêu lần?
- [ ] Nếu ISSUE-009 fix làm scenario_1 reject nhiều hơn → scenario_3 nhiều hơn → NV tăng?

---

### Phase 5 — B_v Backward Pass Validation
**Question:** B_v tính có đúng không?
**What to check:**
- [ ] Verify B_v formula theo SRS §3.1 vs code
- [ ] Edge cases: route chỉ có 1 node, depot TW rất chặt

---

## Errors Encountered
| Error | Phase | Resolution |
|-------|-------|------------|
| — | — | — |
