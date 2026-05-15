# 02 · Configuration Design — Đặt tên + Chốt knobs cho ≥3 Configs

> **Mục tiêu**: Biến phác thảo ở `01-base-flow.md` thành ≥3 configurations chi tiết, mỗi config có tên + 3 knobs đã chốt + lý do chọn.
>
> **Thời gian**: 15 phút (đầu phần Main, trước khi tính cost)

---

## Tại sao đặt tên + viết lý do?

Khi present, nhóm sẽ không muốn nói "Config 1, Config 2, Config 3". Đặt tên rõ cá tính giúp người nghe nhớ ngay tradeoff của từng phương án. Viết lý do cũng giúp nhóm tự kiểm tra xem config đó có hợp logic sản phẩm hay không.

---

## Cách điền

Với mỗi config: đặt tên + chốt 3 knobs + viết 2-3 câu lý do chọn. Mỗi lý do nên gắn với 1 tình huống thực tế như low season, peak season, volume tăng, khách hỏi visa nhiều, hoặc cần tiết kiệm chi phí.

---

## Config 1

**Tên config**:

```text
Budget Bot
```

### 3 Knobs

**① Model tier**:

```text
Response model: GPT-4o-mini → giá $0.15 / $0.60 per 1M tokens (input/output)
Classifier model: keyword / regex → $0 / $0 per 1M tokens
```

**② Web search**:

```text
☑ OFF
□ ON selective — bật cho intent: __________________
□ ON broad
```

**③ History management**:

```text
☑ Last 3
□ Last 5
□ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
Đây là phương án tối ưu chi phí mạnh nhất, phù hợp khi công ty muốn triển khai nhanh để kiểm tra demand hoặc dùng trong low season. Phần lớn câu hỏi Guide cơ bản vẫn có thể xử lý được bằng cheap model + RAG, trong khi Booking và Complaint vẫn handoff sang người nên không cần đầu tư model mạnh cho toàn bộ flow. Config này phù hợp nhất với tình huống volume cao nhưng doanh nghiệp muốn giữ cost cực thấp để thử nghiệm trước.
```

### Rủi ro lớn nhất của config này

```text
Visa và weather information có thể thiếu độ mới hoặc thiếu nuance vì web search tắt hoàn toàn và history chỉ giữ 3 lượt gần nhất.
```

---

## Config 2

**Tên config**:

```text
Premium Concierge
```

### 3 Knobs

**① Model tier**:

```text
Response model: GPT-5.5 → giá $5.00 / $30.00 per 1M tokens
Classifier model: Claude Haiku 4.5 → giá $1.00 / $5.00 per 1M tokens
```

**② Web search**:

```text
□ OFF
□ ON selective — bật cho intent: __________________
☑ ON broad
```

**③ History management**:

```text
□ Last 3
□ Last 5
☑ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
Đây là phương án chất lượng cao nhất, phù hợp khi công ty muốn tạo trải nghiệm chatbot gần với concierge thật và chấp nhận chi phí cao hơn để lấy độ chính xác, tự nhiên và khả năng giữ ngữ cảnh tốt. Full history giúp bot không quên thông tin khách đã cung cấp từ đầu conversation, còn web search broad làm giảm rủi ro thông tin cũ khi khách hỏi visa, thời tiết hoặc thông tin cập nhật. Config này phù hợp với nhóm khách quốc tế kỳ vọng dịch vụ cao cấp hoặc những giai đoạn doanh nghiệp ưu tiên trải nghiệm hơn là tối ưu cost.
```

### Rủi ro lớn nhất của config này

```text
Cost có thể tăng rất mạnh ở Scenario B do model premium, web search bật rộng và full history làm input tokens phình nhanh theo số turn.
```

---

## Config 3

**Tên config**:

```text
Smart Mix
```

### 3 Knobs

**① Model tier**:

```text
Response model: Mix
- Guide / basic FAQ: Gemini 2.5 Flash → giá $0.30 / $2.50 per 1M tokens
- Visa / more sensitive questions: DeepSeek V4 Pro → giá $1.74 / $3.48 per 1M tokens
Classifier model: keyword / regex → $0 / $0 per 1M tokens
```

**② Web search**:

```text
□ OFF
☑ ON selective — bật cho intent: Visa, Weather
□ ON broad
```

**③ History management**:

```text
□ Last 3
☑ Last 5
□ Full
□ Summarize every ___ turns
```

### Lý do nhóm chọn config này

```text
Đây là config cân bằng nhất giữa cost và quality. Nhóm chỉ dùng model mạnh hơn cho các câu hỏi có rủi ro cao như visa, còn guide questions phổ biến thì dùng model rẻ hơn để tiết kiệm. Web search chỉ bật cho Visa và Weather là 2 intent thật sự cần thông tin mới nhất, còn Last 5 giữ đủ ngữ cảnh cho phần lớn conversation mà chưa đắt như Full history.
```

### Rủi ro lớn nhất của config này

```text
Routing theo intent phải đủ chính xác; nếu câu hỏi visa hoặc multi-intent bị route nhầm sang model rẻ hơn thì chất lượng có thể giảm đáng kể.
```

---

## Config 4 (optional — nếu thời gian dư)

**Tên config**:

```text
Volume Safe
```

### 3 Knobs

```text
Model: Gemini 2.5 Flash
Web: ON selective cho Weather
History: Last 5
```

### Lý do

```text
Config này dành cho trường hợp công ty muốn giữ chi phí ổn định khi volume tăng mạnh nhưng vẫn không muốn chất lượng quá thấp như Budget Bot. Nó là phương án trung gian thực dụng nếu Smart Mix bị xem là quá phức tạp để triển khai.
```

---

## Bảng kiểm trước khi tính cost

- [x] ≥3 configs đã đặt tên
- [x] Mỗi config đã chốt rõ 3 knobs
- [x] Mỗi config có ≥2 câu lý do
- [x] 3 configs đủ khác biệt
- [x] Nhóm đồng thuận đây là 3 configs đáng so sánh

Xong → mở `03-cost-calculation.md` để bắt đầu tính cost.
