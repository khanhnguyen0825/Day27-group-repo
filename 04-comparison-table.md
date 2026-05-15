# 04 · Comparison Table — Bảng so sánh đầy đủ

> **Mục tiêu**: Tổng hợp tất cả số đã tính ở `03-cost-calculation.md` thành 1 bảng so sánh duy nhất.
>
> **Thời gian**: 10 phút (đầu phần Final)

---

## Vì sao có bảng so sánh?

Khi sếp hỏi "Nên deploy config nào?", nhóm cần một bảng duy nhất để so sánh trực diện cost, quality và speed giữa các phương án thay vì đọc từng config rời rạc.

---

## Bảng chính

| | Config 1 | Config 2 | Config 3 | (Config 4) |
|---|---|---|---|---|
| **Tên** | Budget Bot | Premium Concierge | Smart Mix | Volume Safe |
| **① Model** | GPT-4o-mini | GPT-5.5 | Gemini 2.5 Flash + DeepSeek V4 Pro | Gemini 2.5 Flash |
| **② Web search** | OFF | ON broad | ON selective (Visa, Weather) | ON selective (Weather) |
| **③ History** | Last 3 | Full | Last 5 | Last 5 |
| **Intent classifier** | Keyword | LLM (Claude Haiku 4.5) | Keyword | Keyword |
| **Cost / conv (Scenario A — 4 turns)** | $0.00150 | $0.08759 | $0.01089 | N/A |
| **Cost / conv (Scenario B — 7 turns)** | $0.00179 | $0.10676 | $0.01122 | N/A |
| **Monthly A** (300 conv/day × 30) | $13.49 | $788.29 | $97.99 | N/A |
| **Monthly B** (1,200 conv/day × 30) | $64.60 | $3,843.27 | $403.96 | N/A |
| **vs human $4,500/mo (A)** | rẻ 333.47× | rẻ 5.71× | rẻ 45.92× | N/A |
| **vs human $18,000/mo (B)** | rẻ 278.65× | rẻ 4.68× | rẻ 44.56× | N/A |
| **Savings % (A)** | 99.70% | 82.48% | 97.82% | N/A |
| **Savings % (B)** | 99.64% | 78.65% | 97.76% | N/A |
| **Quality estimate** | Low-Med | High | Med-High | Medium |
| **Speed estimate** | High | Low | Medium | Medium-High |
| **Điểm yếu chính** | Dễ trả lời thiếu chính xác ở Visa/Weather và dễ quên context cũ | Cost cao nhất và latency chậm nhất | Phụ thuộc vào routing đúng intent để chọn đúng model | Chất lượng không nổi bật ở các câu hỏi khó |
| **Best for** (khi nào nên dùng) | Pilot rẻ, low season, traffic lớn nhưng ngân sách thấp | Trải nghiệm cao cấp, khách VIP, ưu tiên chất lượng hơn chi phí | Triển khai thực tế cân bằng giữa cost và quality | Phương án trung gian nếu không muốn dùng routing mix |

---

## Quan sát nhanh từ bảng

### Câu 1 — Config rẻ nhất là gì? Đắt nhất là gì?

```text
Rẻ nhất: Budget Bot — monthly B = $64.60
Đắt nhất: Premium Concierge — monthly B = $3,843.27
Chênh: khoảng 59.49× lần
```

### Câu 2 — Knob nào ảnh hưởng cost nhiều nhất?

```text
Knob ảnh hưởng cost mạnh nhất là model tier. Chỉ riêng việc chuyển từ GPT-4o-mini sang GPT-5.5 và thêm classifier LLM đã đẩy cost từ $64.60/tháng lên $3,843.27/tháng ở Scenario B, tức tăng gần 60×. History và web search cũng làm cost tăng, nhưng mức tăng của chúng nhỏ hơn nhiều so với việc đổi từ cheap sang premium model.
```

### Câu 3 — Tại sao Scenario B không đắt ×4 lần Scenario A?

```text
Scenario B có volume cao hơn 4× và số turn dài hơn, nhưng tỷ lệ Booking + Complaint cũng tăng lên 45%, trong khi hai intent này gần như không tốn generation cost vì được handoff sang người. Vì vậy monthly cost tăng mạnh nhưng không tăng đúng theo công thức 4× volume × 1.75× turns.
```

### Câu 4 — Có config nào AI đắt hơn human không?

```text
Không. Cả 3 config đều rẻ hơn human baseline khá xa trong cả hai scenario. Premium Concierge là config đắt nhất nhưng vẫn thấp hơn human khoảng 4.68× ở Scenario B, nên nếu doanh nghiệp muốn trải nghiệm tốt hơn thì vẫn có thể justify được mà chưa vượt cost nhân sự.
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Bảng đầy đủ, không còn ô trống ở 3 config chính
- [x] Đã có 4 câu trả lời cho 4 quan sát ở trên
- [x] Nhóm đồng thuận về số trong bảng

Xong → mở `05-recommendation.md`.
