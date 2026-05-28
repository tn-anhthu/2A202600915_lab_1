# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Ở mức temperature 0.0, mô hình cho ra câu trả lời mang tính chất xác định (deterministic), thông tin chuẩn mực và giống nhau qua các lần. Khi tăng lên 0.5 và 1.0, câu trả lời trở nên đa dạng từ ngữ hơn. Tuy nhiên khi đẩy lên 1.5, mô hình bắt đầu bị quá đà dẫn đến shỗn loạn, lặp từ vô, nghĩa hoặc gặp hallucination.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Cho chatbot hỗ trợ khách hàng, nên sẽ đặt temperature từ 0.0 đến 0.3. Bởi vì CS đòi hỏi tính chính xác, thông tin đồng nhất, đáng tin cậy dựa theo tài liệu doanh nghiệp và không cho phép sáng tạo thông tin.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Dựa vào bảng giá trị định nghĩa trong mã nguồn ($0.010 cho gpt-4o so với $0.0006 cho gpt-4o-mini trên mỗi 1K output token), có tỷ lệ $0.010 / 0.0006 khoảng 16.67$. Vậy mô hình GPT-4o đắt hơn GPT-4o-mini khoảng 16.6 lần cho workload này.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> - GPT-4o: Cần xử lý các bài toán logic phức tạp, viết hoặc fix bug nâng cao, hay phân tích dữ liệu cần nhiều bước cần độ thông minh tối đa.
> - GPT-4o-mini: Tác vụ đơn giản, lặp đi lặp lại với số lượng lớn như tóm tắt văn bản ngắn, FAQs chatbot vì tiết kiệm.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng trong các ứng dụng cần tương tác thời gian thực với con người như ChatGPT vì người dùng không cần chờ đợi lâu. Non-streaming phù hợp cho các tác vụ chạy ngầm, xử lý dữ liệu hàng loạt hoặc khi hệ thống xử lý các cấu trúc dữ liệu phức tạp để phân tích tự động bằng code mà không có con người ngồi đợi.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
