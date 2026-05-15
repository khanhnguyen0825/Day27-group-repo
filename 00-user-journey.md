# 00 · User Journey Simulation — Đóng vai Tourist

> **Mục tiêu**: Trước khi tính chi phí, nhóm phải hình dung được khách hàng thật sự hỏi gì, hỏi như thế nào, và 1 conversation thực tế trông ra sao.
>
> **Thời gian**: 8 phút (trong 15 phút phần Setup)

---

## Tại sao phải làm bước này?

Nếu nhóm bắt đầu tính cost mà chưa biết tourist hỏi gì thì mọi con số chỉ là lý thuyết. Bước này buộc nhóm "chạm" sản phẩm trước khi mở phần thiết kế và tính toán.

---

## Bước 1 — Mỗi người đóng vai 1 tourist (4 phút)

Tưởng tượng mình là 1 khách du lịch nước ngoài đang lên kế hoạch đi Việt Nam. Bạn vừa mở website công ty du lịch và thấy chatbot ở góc màn hình. Bạn sẽ hỏi gì?

Trước khi viết, tự hỏi:

- Mình đến từ đâu? Mỹ, Anh, Hàn, Nhật, Úc?
- Đi một mình hay đi nhóm? Budget khoảng bao nhiêu?
- Đã biết gì về Việt Nam? Lần đầu đến hay đã đến rồi?
- Mình lo lắng điều gì nhất? visa, an toàn, ngôn ngữ, thời tiết, ẩm thực, lừa đảo?

Viết **5-7 câu hỏi bằng tiếng Anh** mà mình sẽ thật sự gửi cho chatbot. Viết câu hỏi tự nhiên, đúng giọng tourist.

### Tourist #1 Tên thành viên: Nguyễn Thành Đại Khánh

```text
Hi, I'm visiting Vietnam for the first time in July. Is Hoi An or Da Nang better for a 3-day trip?
What kind of weather should I expect in central Vietnam at that time?
Can you suggest a 3-day itinerary with food and cultural activities?
I'm traveling with my parents. Which places are easy for older travelers?
Is it easy to get from Da Nang airport to Hoi An at night?
What local dishes should we try if we only have a short trip?
```

### Tourist #2 Tên thành viên: Bùi Trọng Anh
```text
I'm from Australia and planning to stay in Vietnam for 12 days. Do I need a visa?
I heard visa rules changed recently. Can you check the latest update for me?
What are the best places to visit in the north if I like nature and photography?
Will it be very cold in Sapa in December?
Can you help me book a Ha Long Bay cruise for two people?
If I book through your company, can someone help us at the airport?
```

### Tourist #3 Tên thành viên: Nguyễn Tiến Thành

```text
I'm traveling solo on a backpacker budget. Which city in Vietnam gives the best value for money?
How much should I budget per day for food, transport, and a hostel?
Is it safe to use Grab late at night in Ho Chi Minh City?
What is the weather like in Ha Long Bay next week?
I booked a tour on another site and had a bad experience. Can your team help me plan something more reliable?
If something goes wrong during the tour, who should I contact for urgent support?
```

---

## Bước 2 — Gom lại và phân loại (4 phút)

Cả nhóm chụm vào, gom tất cả câu hỏi lại và phân loại theo 5 intent:

- **Visa/Policy** — chính sách, thủ tục nhập cảnh
- **Điểm đến/Guide** — gợi ý đi đâu, làm gì, ăn gì
- **Thời tiết/Sự kiện** — thông tin real-time
- **Tour/Booking** — đặt vé, đặt tour, đặt phòng
- **Khiếu nại** — phàn nàn, sự cố, hoàn tiền

Sau khi gom, điền bảng phân loại:

| # | Câu hỏi (1 dòng) | Intent thuộc loại nào | Cần bao nhiêu lượt chat để xong? | Bot trả lời hay chuyển người? |
|---|---|---|---|---|
| 1 | Is Hoi An or Da Nang better for a 3-day trip? | Điểm đến/Guide | 3 lượt | Bot |
| 2 | What kind of weather should I expect in central Vietnam in July? | Thời tiết/Sự kiện | 2 lượt | Bot |
| 3 | Can you suggest a 3-day itinerary with food and cultural activities? | Điểm đến/Guide | 4 lượt | Bot |
| 4 | Do I need a visa for a 12-day trip to Vietnam? | Visa/Policy | 3 lượt | Bot |
| 5 | I heard visa rules changed recently. Can you check the latest update? | Visa/Policy | 4 lượt | Bot |
| 6 | What are the best places in northern Vietnam for nature and photography? | Điểm đến/Guide | 3 lượt | Bot |
| 7 | Will it be very cold in Sapa in December? | Thời tiết/Sự kiện | 2 lượt | Bot |
| 8 | Can you help me book a Ha Long Bay cruise for two people? | Tour/Booking | 1 lượt | Người |
| 9 | Which city in Vietnam gives the best value for a backpacker? | Điểm đến/Guide | 3 lượt | Bot |
| 10 | If something goes wrong during the tour, who should I contact for urgent support? | Khiếu nại | 1 lượt | Người |

---

## Bước 3 — Rút insight cho nhóm

**Tổng số câu hỏi nhóm gom được**:

```text
18 câu hỏi
```

**Phân bố intent thực tế của nhóm** (% mỗi intent):

```text
Guide: 44%
Visa: 17%
Weather: 17%
Booking: 11%
Khiếu nại: 11%
```

**Số lượt chat trung bình để xong 1 chủ đề**:

```text
Khoảng 3-4 lượt cho Guide và Visa, 2-3 lượt cho Weather, và 1 lượt cho Booking/Khiếu nại trước khi handoff sang người.
```

**Đối chiếu với đề bài** (Scenario A = 4 lượt, Scenario B = 7 lượt):

```text
Khá hợp lý. Phần lớn câu hỏi thông tin có thể xử lý trong khoảng 3-4 lượt nên Scenario A phù hợp với low season. Scenario B = 7 lượt cũng hợp lý cho các conversation dài hơn, đặc biệt khi khách hỏi nhiều ý trong cùng một chuỗi chat.
```

**Insight bất ngờ — điều gì nhóm chỉ hiểu sau khi đóng vai?**

```text
Tourist thường không hỏi theo từng intent tách biệt mà hay gộp guide, weather và booking trong cùng một conversation. Ngoài ra, các câu hỏi visa và thời tiết có xu hướng cần thông tin mới nhất, nên chỉ dùng knowledge base có thể không đủ an toàn.
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Mỗi người trong nhóm đã viết ≥5 câu hỏi tourist
- [x] Đã gom + phân loại intent cho ≥10 câu
- [x] Đã có phân bố intent % của nhóm
- [x] Có ít nhất 1 insight về cách tourist thật sự dùng chatbot

Xong → mở `01-base-flow.md`.
