# 05 · Recommendation + Justification — Kết luận & Chuẩn bị Present

> **Mục tiêu**: Chọn 1 config nhóm recommend deploy, viết justification ngắn gọn, và chuẩn bị 5 phút present.
>
> **Thời gian**: 10 phút (cuối phần Final)

---

## Bảng số ai cũng tính được. PM giỏi phải recommend và justify.

Đây là phần quan trọng nhất vì nhóm không chỉ so sánh giá rẻ hay đắt, mà phải đưa ra một lựa chọn thực tế cho doanh nghiệp.

---

## 4 câu hỏi nhóm phải trả lời

### Câu 1 — Recommend config nào?

```text
Nhóm recommend Smart Mix là config nên deploy mặc định cho cả hai scenario. Lý do là config này giữ được quality ở mức Med-High nhưng cost vẫn rất thấp so với human baseline: chỉ $97.99/tháng ở Scenario A và $403.96/tháng ở Scenario B. Nếu sếp bắt buộc chỉ chọn một config chạy quanh năm, Smart Mix là lựa chọn cân bằng nhất giữa độ chính xác, khả năng cập nhật thông tin và hiệu quả chi phí. Premium Concierge chỉ nên dùng cho phân khúc khách VIP hoặc khi doanh nghiệp muốn tối ưu trải nghiệm cao cấp hơn là tối ưu margin.
```

### Câu 2 — So với human baseline $0.50/conv → tiết kiệm bao nhiêu? Có đắt hơn human ở chỗ nào không?

```text
Với Smart Mix, nhóm tiết kiệm khoảng 97.82% ở Scenario A và 97.76% ở Scenario B so với human baseline. Cụ thể, human cost là $4,500/tháng ở Scenario A và $18,000/tháng ở Scenario B, trong khi Smart Mix chỉ tốn $97.99 và $403.96. Không có config nào trong bài toán này đắt hơn human, kể cả Premium Concierge. Tuy vậy, AI không thay thế hoàn toàn sales và complaint handling vì Booking và Complaint vẫn cần người thật để chốt và xử lý rủi ro.
```

### Câu 3 — Khi nào nên upgrade / downgrade config?

```text
Nên upgrade từ Smart Mix lên Premium Concierge khi doanh nghiệp bắt đầu phục vụ nhiều khách có giá trị cao, quality complaint tăng rõ rệt, hoặc conversion uplift đủ lớn để justify phần cost tăng thêm. Nên downgrade về Budget Bot khi đang ở low season, traffic lớn nhưng giá trị mỗi conversation thấp, và công ty chỉ muốn dùng chatbot như lớp FAQ đầu tiên. Một ngưỡng thực tế là nếu doanh nghiệp thấy khách thường chỉ hỏi guide cơ bản và ít hỏi visa hay weather real-time thì Budget Bot có thể đủ dùng tạm thời.
```

### Câu 4 — Rủi ro lớn nhất của config được chọn?

```text
Rủi ro lớn nhất của Smart Mix là routing sai intent, đặc biệt ở các câu hỏi nhiều ý như vừa hỏi weather vừa muốn booking hoặc visa có nuance mới. Nếu route nhầm sang model rẻ hơn hoặc không bật web đúng lúc, bot có thể trả lời thiếu chính xác. Mitigation là đặt rule rõ cho multi-intent, ưu tiên bật web search cho Visa và Weather, và fallback sang human nếu confidence thấp hoặc câu hỏi liên quan policy mới thay đổi.
```

---

## Final answer — Recommendation in 1 paragraph

```text
Nhóm recommend Smart Mix là phương án nên deploy mặc định vì đây là cấu hình cân bằng tốt nhất giữa cost, quality và khả năng vận hành thực tế. So với human baseline, Smart Mix chỉ tốn $97.99/tháng ở low season và $403.96/tháng ở high season, tương ứng tiết kiệm khoảng 97.82% và 97.76%, trong khi quality vẫn ở mức Med-High nhờ chỉ dùng model mạnh hơn cho các intent nhạy cảm như Visa. Budget Bot rẻ hơn nhiều nhưng rủi ro cao hơn ở các câu hỏi cần thông tin mới hoặc cần giữ ngữ cảnh tốt. Premium Concierge cho chất lượng cao nhất nhưng cost cao hơn đáng kể và chưa cần thiết cho phần lớn traffic phổ thông. Vì vậy Smart Mix là lựa chọn hợp lý nhất nếu công ty muốn triển khai thực tế, giữ trải nghiệm đủ tốt và vẫn bảo toàn economics. Nhóm chỉ đề xuất nâng lên Premium cho khách VIP hoặc giai đoạn cần tối đa hóa trải nghiệm hơn là tối đa hóa margin.
```

---

## Chuẩn bị Present (5 phút)

### Nhịp 0:00 – 0:30 — Base flow + 3 knobs đã chọn

Ai trình bày: Minh

Nói gì:

```text
Nhóm bắt đầu từ base flow gồm 4 bước: classify intent, route theo intent, assemble context và generate response. Từ flow đó, nhóm chọn 3 knobs ảnh hưởng economics nhiều nhất là model tier, web search và history management.
```

### Nhịp 0:30 – 1:00 — Config overview

Ai trình bày: Linh

Nói gì:

```text
Config 1 là Budget Bot: cheap model, web OFF, history Last 3.
Config 2 là Premium Concierge: premium model, web broad, full history.
Config 3 là Smart Mix: model mix theo intent, web selective cho Visa và Weather, history Last 5.
```

### Nhịp 1:00 – 2:00 — Cost comparison

Ai trình bày: Khoa

Nói gì:

```text
Kết quả cho thấy Budget Bot rẻ nhất với monthly cost chỉ $64.60 ở Scenario B, còn Premium Concierge đắt nhất với $3,843.27. Smart Mix nằm ở giữa với $403.96 nhưng vẫn rẻ hơn human baseline hơn 44 lần ở high season. Điều quan trọng là cả 3 config đều rẻ hơn human, nhưng tradeoff về quality rất khác nhau.
```

### Nhịp 2:00 – 3:00 — Key insight

Ai trình bày: Minh

Nói gì:

```text
Knob ảnh hưởng cost lớn nhất là model tier, không phải web search hay history. Chỉ cần đổi từ cheap sang premium model thì monthly cost ở Scenario B tăng gần 60 lần. Vì vậy bài toán kinh tế của chatbot chủ yếu là dùng đúng mức intelligence cho đúng intent, thay vì bật model mạnh cho toàn bộ flow.
```

### Nhịp 3:00 – 4:30 — Recommendation + justification

Ai trình bày: Linh

Nói gì:

```text
Nhóm recommend Smart Mix là phương án nên deploy mặc định vì đây là cấu hình cân bằng tốt nhất giữa cost, quality và khả năng vận hành thực tế. So với human baseline, Smart Mix chỉ tốn $97.99/tháng ở low season và $403.96/tháng ở high season, tương ứng tiết kiệm khoảng 97.82% và 97.76%, trong khi quality vẫn ở mức Med-High nhờ chỉ dùng model mạnh hơn cho các intent nhạy cảm như Visa. Budget Bot rẻ hơn nhiều nhưng rủi ro cao hơn ở các câu hỏi cần thông tin mới hoặc cần giữ ngữ cảnh tốt. Premium Concierge cho chất lượng cao nhất nhưng cost cao hơn đáng kể và chưa cần thiết cho phần lớn traffic phổ thông. Vì vậy Smart Mix là lựa chọn hợp lý nhất nếu công ty muốn triển khai thực tế, giữ trải nghiệm đủ tốt và vẫn bảo toàn economics. Nhóm chỉ đề xuất nâng lên Premium cho khách VIP hoặc giai đoạn cần tối đa hóa trải nghiệm hơn là tối đa hóa margin.
```

### Nhịp 4:30 – 5:00 — Hardest question prep

Ai trình bày: Khoa

Nhóm dự đoán câu hỏi khó nhất sẽ bị hỏi là gì?

```text
Tại sao nhóm không chọn Budget Bot nếu nó rẻ hơn Smart Mix rất nhiều, trong khi cả hai đều vẫn rẻ hơn human?
```

Câu trả lời sẵn:

```text
Vì bài toán không chỉ là rẻ nhất mà là sustainable economics đi kèm trải nghiệm đủ tốt để khách vẫn tin và tiếp tục dùng. Budget Bot rẻ hơn, nhưng rủi ro trả lời sai ở Visa và Weather cao hơn do không có web search và history ngắn hơn. Smart Mix vẫn cực rẻ so với human nhưng giảm đáng kể rủi ro sản phẩm ở các intent nhạy cảm.
```

---

## Q&A — 2 phút sau khi present xong

**3 câu instructor thường hỏi**:

1. *"Knob nào ảnh hưởng cost nhiều nhất trong config của nhóm? Tại sao?"*
2. *"Nếu provider tăng giá API ×2 → config của nhóm còn sống được không?"*
3. *"So với nhóm X — tại sao nhóm bạn chọn khác?"*

Suy nghĩ trước câu trả lời ngắn:

```text
1. Knob ảnh hưởng cost mạnh nhất là model tier, vì chênh lệch giá giữa cheap và premium model lớn hơn rất nhiều so với web search hay history.
2. Nếu provider tăng giá API gấp 2 thì Smart Mix vẫn còn sống được vì monthly cost vẫn thấp hơn human baseline rất xa; tuy nhiên lúc đó nhóm sẽ theo dõi lại ROI và có thể giảm bớt số intent dùng model mạnh.
3. Nhóm chọn Smart Mix vì muốn tối ưu theo intent thay vì tối ưu toàn cục. Nếu nhóm khác chọn Budget hoặc Premium hoàn toàn, thì lựa chọn của nhóm em nằm ở giữa và thực tế hơn cho triển khai production.
```

---

## Bảng kiểm cuối cùng — trước 12:00 Pens Down

- [x] Đã trả lời 4 câu PM
- [x] Final answer paragraph viết gọn
- [x] Phân công 5 nhịp present cho mỗi thành viên
- [x] Có sẵn câu trả lời cho 3 câu Q&A dự đoán
- [x] Comparison table có sẵn để chiếu / chuyền tay khi present
- [ ] Repo đã commit + push (sẽ nộp link sau buổi học)

---

## Sau buổi học

1. **Commit + push repo** với tất cả file đã điền.
2. **Dán link repo** vào Discord `#day27-evidence-boards` trước 23:59.
3. **Chuẩn bị cho D28**: peer review giữa các nhóm.
