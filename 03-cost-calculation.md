# 03 · Cost Calculation — Tính chi phí từng Config × 2 Scenarios

> **Mục tiêu**: Với mỗi config đã thiết kế ở `02-config-design.md`, tính cost/turn → cost/conversation → monthly cho cả 2 scenarios.
>
> **Thời gian**: 55 phút (phần lớn của Main phase)

---

## Cách làm

Nhóm dùng các giả định cố định của đề bài và kiểm tra lại bằng tool `tools/calc_lab_cost.py`.

Các config được tính:

- `Budget Bot`
- `Premium Concierge`
- `Smart Mix`

**Giả định nhóm dùng khi tính**:

- System prompt: `500` tokens
- User message: `80` tokens
- Assistant response: `180` tokens
- 1 prior turn history: `260` tokens
- RAG top-5 chunks: `1,250` tokens
- Web search results: `800` tokens khi bật
- Web search API: `$0.005 / call`
- Booking + Complaint: `0` generation cost, chỉ còn classifier cost nếu config dùng LLM classifier

---

## Điền số cho từng config

### Config 1 — Budget Bot

| Item | Scenario A (4 turns) | Scenario B (7 turns) |
|---|---|---|
| Cost / conversation (avg) | $0.00150 | $0.00179 |
| Monthly cost | $13.49 | $64.60 |
| Human baseline | $4,500 | $18,000 |
| **Rẻ hơn human ___×** | 333.47× | 278.65× |
| **Savings %** | 99.70% | 99.64% |

**Sanity check**:

```text
Số này rất rẻ nhưng vẫn hợp lý vì config này dùng GPT-4o-mini, không web search, không LLM classifier và Booking/Complaint được handoff nên một phần đáng kể volume gần như không tốn generation cost.
```

---

### Config 2 — Premium Concierge

| Item | Scenario A | Scenario B |
|---|---|---|
| Cost / conversation (avg) | $0.08759 | $0.10676 |
| Monthly cost | $788.29 | $3,843.27 |
| **Rẻ hơn human ___×** | 5.71× | 4.68× |
| **Savings %** | 82.48% | 78.65% |

**Sanity check**:

```text
Config này đắt nhất là hợp lý vì dùng GPT-5.5 cho response, Claude Haiku làm classifier, web broad và full history. Scenario B tăng mạnh vì conversation dài hơn và full history làm input tokens phình rõ rệt.
```

---

### Config 3 — Smart Mix

| Item | Scenario A | Scenario B |
|---|---|---|
| Cost / conversation (avg) | $0.01089 | $0.01122 |
| Monthly cost | $97.99 | $403.96 |
| **Rẻ hơn human ___×** | 45.92× | 44.56× |
| **Savings %** | 97.82% | 97.76% |

**Sanity check**:

```text
Config này cao hơn Budget Bot nhưng thấp hơn rất nhiều so với Premium. Điều này hợp logic vì nhóm chỉ bật web search có chọn lọc và chỉ dùng model mạnh hơn cho Visa thay vì cho toàn bộ flow.
```

---

### Config 4 (optional)

| Item | Scenario A | Scenario B |
|---|---|---|
| Cost / conversation (avg) | $________ | $________ |
| Monthly cost | $________ | $________ |
| **Rẻ hơn human ___×** | _____× | _____× |
| **Savings %** | ___% | ___% |

---

## Quality + Speed estimate (qualitative)

| Config | Quality (Low/Med/High) | Speed (Low/Med/High) | Lý do |
|---|---|---|---|
| 1: Budget Bot | Low-Med | High | Cheap model, web OFF, history ngắn nên nhanh và rẻ nhưng dễ hụt chất lượng ở câu hỏi khó |
| 2: Premium Concierge | High | Low | Premium model + web broad + full history cho chất lượng cao nhất nhưng latency chậm nhất |
| 3: Smart Mix | Med-High | Medium | Dùng model mạnh đúng chỗ và selective web nên giữ được cân bằng giữa trải nghiệm và chi phí |
| 4: ___ | ___ | ___ | ___ |

---

## Ghi chú cách ra số chính

### Budget Bot

```text
Model: GPT-4o-mini ($0.15 / $0.60 per 1M)
Classifier: keyword = $0
Web: OFF
History: Last 3

Guide/Visa/Weather 4 turns = $0.00176 / conv
Guide/Visa/Weather 7 turns = $0.00326 / conv
Booking/Complaint = $0

avg_cost_A = 85% × 0.00176 = $0.00150
avg_cost_B = 55% × 0.00326 = $0.00179
```

### Premium Concierge

```text
Model: GPT-5.5 ($5.00 / $30.00 per 1M)
Classifier: Claude Haiku 4.5 = ~$0.00025 / message
Web: ON broad
History: Full

Guide/Visa/Weather 4 turns = $0.10300 / conv
Guide/Visa/Weather 7 turns = $0.19390 / conv
Booking/Complaint = classifier only = $0.00025

avg_cost_A = 85% × 0.10300 + 15% × 0.00025 = $0.08759
avg_cost_B = 55% × 0.19390 + 45% × 0.00025 = $0.10676
```

### Smart Mix

```text
Guide model: Gemini 2.5 Flash ($0.30 / $2.50 per 1M)
Visa model: DeepSeek V4 Pro ($1.74 / $3.48 per 1M)
Weather model: Gemini 2.5 Flash
Classifier: keyword = $0
Web: ON selective cho Visa + Weather
History: Last 5

Guide 4 turns = $0.00446
Guide 7 turns = $0.00855
Visa 4 turns = $0.03074
Visa 7 turns = $0.04851
Weather 4 turns = $0.00970
Weather 7 turns = $0.01379
Booking/Complaint = $0

avg_cost_A = 50%×0.00446 + 25%×0.03074 + 10%×0.00970 = $0.01089
avg_cost_B = 30%×0.00855 + 15%×0.04851 + 10%×0.01379 = $0.01122
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Tất cả 3 configs đã có cost/conv + monthly cho cả 2 scenarios
- [x] Đã so sánh từng config với human baseline ($0.50/conv)
- [x] Có quality + speed estimate cho mỗi config
- [x] Đã sanity check, không có số quá lạ

Xong → mở `04-comparison-table.md`.
