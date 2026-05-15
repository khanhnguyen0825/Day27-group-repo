# 03 · Cost Calculation — Tính chi phí từng Config × 2 Scenarios

> **Mục tiêu**: Với mỗi config đã thiết kế ở `02-config-design.md`, tính cost/turn → cost/conversation → monthly cho cả 2 scenarios.
>
> **Thời gian**: 55 phút (phần lớn của Main phase)

---

## Cách làm

Nhóm dùng các giả định cố định của đề bài và tính cho 3 config đã chọn:

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
| Cost / conversation (avg) | $0.00143 | $0.00175 |
| Monthly cost | $12.90 | $63.05 |
| Human baseline | $4,500 | $18,000 |
| **Rẻ hơn human ___×** | 348.84× | 285.47× |
| **Savings %** | 99.71% | 99.65% |

**Sanity check**:

```text
Số này rất rẻ nhưng vẫn hợp lý vì config này dùng GPT-4o-mini, không web search, không LLM classifier và Booking/Complaint được handoff nên 15%-45% conversations gần như không tốn generation cost.
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
| Cost / conversation (avg) | $0.01566 | $0.01916 |
| Monthly cost | $140.90 | $689.73 |
| **Rẻ hơn human ___×** | 31.94× | 26.10× |
| **Savings %** | 96.87% | 96.17% |

**Sanity check**:

```text
Config này có cost cao hơn Budget Bot nhưng thấp hơn rất nhiều so với Premium. Điều này hợp logic vì nhóm chỉ bật web search cho Visa và Weather, và chỉ dùng model mạnh hơn cho Visa thay vì cho toàn bộ flow.
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

Guide/Visa/Weather 4 turns = $0.001686 / conv
Guide/Visa/Weather 7 turns = $0.0031845 / conv
Booking/Complaint = $0

avg_cost_A = 50%×0.001686 + 25%×0.001686 + 10%×0.001686 = $0.0014331
avg_cost_B = 30%×0.0031845 + 15%×0.0031845 + 10%×0.0031845 = $0.001751475
```

### Premium Concierge

```text
Model: GPT-5.5 ($5.00 / $30.00 per 1M)
Classifier: Claude Haiku 4.5 = ~$0.00025 / message
Web: ON broad
History: Full

Guide/Visa/Weather 4 turns = $0.1030 / conv
Guide/Visa/Weather 7 turns = $0.1939 / conv
Booking/Complaint = classifier only = $0.00025

avg_cost_A = 85%×0.1030 + 15%×0.00025 = $0.0875875
avg_cost_B = 55%×0.1939 + 45%×0.00025 = $0.1067575
```

### Smart Mix

```text
Guide model: Gemini 2.5 Flash ($0.30 / $2.50 per 1M)
Visa model: DeepSeek V4 Pro ($1.74 / $3.48 per 1M)
Weather model: Gemini 2.5 Flash
Classifier: keyword = $0
Web: ON selective cho Visa + Weather
History: Last 5

Guide 4 turns = $0.004464
Guide 7 turns = $0.008553
Visa 4 turns = $0.0435248
Visa 7 turns = $0.0804662
Weather 4 turns = $0.025424
Weather 7 turns = $0.045233
Booking/Complaint = $0

avg_cost_A = 50%×0.004464 + 25%×0.0435248 + 10%×0.025424 = $0.0156556
avg_cost_B = 30%×0.008553 + 15%×0.0804662 + 10%×0.045233 = $0.01915913
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Tất cả 3 configs đã có cost/conv + monthly cho cả 2 scenarios
- [x] Đã so sánh từng config với human baseline ($0.50/conv)
- [x] Có quality + speed estimate cho mỗi config
- [x] Đã sanity check, không có số quá lạ

Xong → mở `04-comparison-table.md`.
