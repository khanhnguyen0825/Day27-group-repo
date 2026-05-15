# 01 · Base Flow + Chốt 3 Knobs

> **Mục tiêu**: Hiểu chatbot hoạt động ra sao ở mức base và xác định 3 knobs nhóm sẽ tweak ở các bước sau.
>
> **Thời gian**: 7 phút (trong 15 phút phần Setup)

---

## Bước 1 — Đọc base flow trong cost reference card

Mở file `cost-reference-card.md` ở phần **2. Base Flow** để xem flow chatbot mặc định. Đây là cấu trúc mà mọi config sẽ build dựa trên.

Nhóm đã hiểu base flow như sau:

- Khi tourist gửi tin nhắn, hệ thống phải **classify intent trước**.
- Nếu là `Guide`, `Visa`, `Weather` thì bot mới dùng LLM để trả lời.
- Nếu là `Booking` hoặc `Complaint` thì ưu tiên **handoff sang người**, gần như không tốn cost generation.
- Sau khi route, hệ thống mới ráp context gồm system prompt, history, RAG, web search nếu có, rồi mới generate response.

---

## Bước 2 — Vẽ lại flow theo cách hiểu của nhóm

```text
Tourist sends message
        |
        v
Intent classification
        |
        +-------------------+-------------------+-------------------+-------------------+-------------------+
        |                   |                   |                   |                   |
        v                   v                   v                   v                   v
     Visa                Guide              Weather             Booking            Complaint
        |                   |                   |                   |                   |
        |                   |                   |                   |                   |
   RAG + selective      RAG only         Web search + RAG      Handoff to sales    Escalate to manager
   web search when      for itinerary     for real-time info    after first turn    after first turn
   policy may change    and destination
        |                   |                   |
        +-------------------+-------------------+
                            |
                            v
                    Context assembly
      System prompt + selected history + RAG chunks
      + web results (if enabled) + user message
                            |
                            v
                    Response generation
                  Model writes answer to tourist
```

Flow trên có đủ 4 bước:

1. **Intent classification**
2. **Route theo intent**
3. **Context assembly**
4. **Response generation**

---

## Bước 3 — Xác định 3 Knobs

3 knobs là 3 quyết định thiết kế nhóm có thể tweak. Mỗi config sau này sẽ là một tổ hợp của 3 knobs này.

### Knob 1 — Model tier

**Câu hỏi:** Chất lượng câu trả lời ở mức nào?

Options:

```text
□ Cheap        (Gemini Flash-Lite / DeepSeek V4 Flash / GPT-4o-mini)
□ Mid          (Gemini Flash / Claude Haiku 4.5)
□ Strong       (DeepSeek V4 Pro / Claude Sonnet 4.6)
□ Premium      (Claude Opus 4.7 / GPT-5.5)
□ Mix          (model khác nhau cho intent khác nhau)
```

**Suy nghĩ của nhóm**:

```text
Nhóm không nên dùng cùng 1 mức model cho mọi intent. Guide questions khá phổ biến và thường không quá khó, nên cheap hoặc mid model có thể đủ. Nhưng visa questions dễ rủi ro hơn vì cần chính xác và đôi khi có nuance về policy mới, nên strong model hoặc ít nhất smart mix sẽ hợp lý hơn. Vì bài lab cần so sánh tradeoff cost và quality, nhóm sẽ thử cả 3 hướng: cheap toàn bộ, premium toàn bộ và mix theo intent.
```

### Knob 2 — Web search

**Câu hỏi:** Có cần thông tin real-time không?

Options:

```text
□ OFF
□ ON selective    (bật cho 1-2 intent cần real-time: visa, weather)
□ ON broad
```

**Suy nghĩ của nhóm**:

```text
Web search không nên bật bừa cho mọi intent vì vừa tăng cost vừa tăng latency. Từ file 00, nhóm thấy visa và weather là 2 loại câu hỏi cần thông tin mới nhất rõ nhất. Guide questions chủ yếu dựa vào destination knowledge có thể lấy từ RAG. Vì vậy hướng hợp lý nhất về mặt sản phẩm là selective web search cho Visa và Weather; còn broad web search chỉ nên dùng trong config premium để so sánh cực trị.
```

### Knob 3 — History management

**Câu hỏi:** Chatbot cần nhớ bao nhiêu context của conversation?

Options:

```text
□ Last 3 turns
□ Last 5 turns
□ Full history
□ Summarize every 5
```

**Suy nghĩ của nhóm**:

```text
Từ user journey, nhiều câu hỏi có thể xong trong 3-4 lượt, nhưng cũng có những conversation dài hơn khi khách hỏi liên tiếp về lịch trình, thời tiết và booking trong cùng một chuỗi. Last 3 sẽ rẻ nhưng hơi dễ quên ngữ cảnh cũ. Full history thì an toàn hơn nhưng tốn hơn rõ ở Scenario B = 7 turns. Nhóm xem Last 5 là điểm cân bằng, còn Full sẽ được giữ cho config premium để so sánh.
```

---

## Bước 4 — Sơ bộ nhóm muốn thử những combo nào?

**Combo 1 (định hướng cheap)**:

```text
Model: Cheap
Web: OFF
History: Last 3
(đặt tên dự kiến: Budget Bot)
```

**Combo 2 (định hướng premium)**:

```text
Model: Premium
Web: ON broad
History: Full
(đặt tên dự kiến: Premium Concierge)
```

**Combo 3 (định hướng balanced / smart mix)**:

```text
Model: Mix (Cheap/Mid cho Guide, Strong cho Visa, cheap classifier)
Web: ON selective cho Visa + Weather
History: Last 5
(đặt tên dự kiến: Smart Mix)
```

**Combo 4** (optional):

```text
Model: Mid
Web: ON selective cho Weather
History: Last 5
(đặt tên dự kiến: Volume Safe)
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Đã vẽ flow base có đủ 4 bước (Intent → Route → Context → Response)
- [x] Hiểu Booking + Khiếu nại = $0 LLM cost (chuyển con người)
- [x] Đã phác thảo ≥3 combo khác nhau
- [x] Nhóm đồng thuận về hướng đi mỗi combo

Xong → mở `02-config-design.md`.
