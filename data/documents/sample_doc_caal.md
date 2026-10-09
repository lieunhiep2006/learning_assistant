---
doc_id: CA101
title: Kiến trúc máy tính và hợp ngữ
version: 2026-09-01
owner: Bộ môn Kỹ thuật máy tính
---

# Kiến trúc máy tính và hợp ngữ (CA101)

Môn học 3 tín chỉ, kéo dài 6 tuần, dành cho sinh viên năm hai ngành Khoa học máy tính. Môn học tiên quyết là Nhập môn lập trình. Công cụ sử dụng trong phòng lab là trình biên dịch NASM và trình gỡ lỗi GDB trên Linux, kiến trúc x86-64.

## Tuần 1: Tổng quan kiến trúc máy tính

### Bài 1.1: Các thành phần của máy tính

#### Mục tiêu

Sinh viên mô tả được bốn thành phần chính của máy tính theo mô hình von Neumann: bộ xử lý trung tâm (CPU), bộ nhớ, thiết bị vào ra và hệ thống bus.

#### Nội dung

Mô hình von Neumann lưu chương trình và dữ liệu trong cùng một bộ nhớ. CPU gồm đơn vị điều khiển, đơn vị số học và logic (ALU) và tập thanh ghi. Bus được chia thành bus địa chỉ, bus dữ liệu và bus điều khiển.

#### Bài tập

Bài tập 1 là phiếu trả lời ngắn về các thành phần của máy tính. Hạn nộp là cuối Tuần 1.

### Bài 1.2: Chu kỳ lệnh

#### Mục tiêu

Sinh viên trình bày được các giai đoạn của chu kỳ lệnh: nạp lệnh, giải mã, thực thi và ghi kết quả.

#### Nội dung

Thanh ghi bộ đếm chương trình (PC) giữ địa chỉ của lệnh kế tiếp. Sau mỗi lần nạp lệnh, PC tăng lên để trỏ đến lệnh sau. Một số lệnh nhảy làm thay đổi giá trị PC trực tiếp.

## Tuần 2: Biểu diễn dữ liệu

### Bài 2.1: Hệ cơ số và số nguyên

#### Mục tiêu

Sinh viên chuyển đổi được giữa hệ nhị phân, thập phân và thập lục phân.

#### Nội dung

Số nguyên không dấu dùng toàn bộ các bit để biểu diễn giá trị. Số nguyên có dấu dùng biểu diễn bù hai, trong đó bit cao nhất là bit dấu. Với 8 bit, số có dấu biểu diễn được từ -128 đến 127.

#### Bài tập

Bài tập 2 gồm 15 câu chuyển đổi cơ số và biểu diễn bù hai. Hạn nộp là cuối Tuần 2.

### Bài 2.2: Số thực và ký tự

#### Mục tiêu

Sinh viên nhận biết được cách biểu diễn số thực dấu phẩy động theo chuẩn IEEE 754 và cách mã hóa ký tự ASCII.

#### Nội dung

Số thực dấu phẩy động 32 bit gồm 1 bit dấu, 8 bit mũ và 23 bit phần định trị. Bảng mã ASCII dùng 7 bit để biểu diễn 128 ký tự.

## Tuần 3: Tập lệnh và thanh ghi

### Bài 3.1: Thanh ghi trong x86-64

#### Mục tiêu

Sinh viên liệt kê được các thanh ghi đa dụng của x86-64 và vai trò của chúng.

#### Nội dung

Kiến trúc x86-64 có 16 thanh ghi đa dụng 64 bit, trong đó có RAX, RBX, RCX, RDX, RSI, RDI, RSP và RBP. Thanh ghi RSP trỏ đến đỉnh ngăn xếp. Thanh ghi cờ lưu các cờ như cờ không (ZF) và cờ nhớ (CF).

### Bài 3.2: Các lệnh cơ bản

#### Mục tiêu

Sinh viên sử dụng được các lệnh chuyển dữ liệu và lệnh số học cơ bản.

#### Nội dung

Lệnh MOV sao chép dữ liệu giữa thanh ghi và bộ nhớ. Lệnh ADD và SUB thực hiện phép cộng và phép trừ. Lệnh CMP so sánh hai toán hạng và đặt các cờ tương ứng.

#### Bài tập

Lab 1 yêu cầu viết chương trình hợp ngữ tính tổng của một mảng số nguyên bằng NASM. Hạn nộp là cuối Tuần 3.

## Tuần 4: Luồng điều khiển và ngăn xếp

### Bài 4.1: Lệnh nhảy và vòng lặp

#### Mục tiêu

Sinh viên viết được cấu trúc rẽ nhánh và vòng lặp bằng các lệnh nhảy có điều kiện.

#### Nội dung

Lệnh JMP nhảy vô điều kiện. Lệnh JE và JNE nhảy dựa vào cờ ZF. Vòng lặp được xây dựng bằng cách kết hợp lệnh CMP với một lệnh nhảy có điều kiện quay về nhãn đầu vòng lặp.

### Bài 4.2: Ngăn xếp và lời gọi hàm

#### Mục tiêu

Sinh viên giải thích được cách ngăn xếp lưu địa chỉ trả về và các biến cục bộ khi gọi hàm.

#### Nội dung

Lệnh PUSH đặt một giá trị lên ngăn xếp và giảm RSP. Lệnh POP lấy giá trị ra và tăng RSP. Lệnh CALL lưu địa chỉ trả về lên ngăn xếp, và lệnh RET lấy địa chỉ đó ra để quay lại nơi gọi.

#### Bài tập

Lab 2 yêu cầu viết một hàm hợp ngữ tính giai thừa và gọi hàm đó từ chương trình chính. Hạn nộp là cuối Tuần 4.

## Tuần 5: Kiểm tra giữa kỳ và phân cấp bộ nhớ

### Bài 5.1: Kiểm tra giữa kỳ

#### Nội dung

Bài kiểm tra giữa kỳ là bài viết trên giấy, thời gian 60 phút, diễn ra vào buổi học đầu tiên của Tuần 5. Phạm vi gồm nội dung từ Tuần 1 đến Tuần 4. Sinh viên không được sử dụng tài liệu.

### Bài 5.2: Phân cấp bộ nhớ

#### Mục tiêu

Sinh viên giải thích được vì sao máy tính dùng nhiều tầng bộ nhớ.

#### Nội dung

Phân cấp bộ nhớ gồm thanh ghi, bộ nhớ đệm (cache), bộ nhớ chính (RAM) và bộ nhớ ngoài. Tầng càng gần CPU thì truy cập càng nhanh nhưng dung lượng càng nhỏ và giá thành mỗi byte càng cao.

## Tuần 6: Bộ nhớ đệm và ôn tập

### Bài 6.1: Nguyên lý cục bộ và bộ nhớ đệm

#### Mục tiêu

Sinh viên phân biệt được cục bộ về thời gian và cục bộ về không gian, và tính được tỷ lệ trúng cache.

#### Nội dung

Cục bộ về thời gian nghĩa là dữ liệu vừa được truy cập có xu hướng được truy cập lại sớm. Cục bộ về không gian nghĩa là các ô nhớ lân cận có xu hướng được truy cập tiếp theo. Tỷ lệ trúng cache bằng số lần trúng chia cho tổng số lần truy cập.

#### Bài tập

Bài tập 3 gồm 8 câu tính tỷ lệ trúng cache và thời gian truy cập trung bình. Hạn nộp là cuối Tuần 6.

### Bài 6.2: Ôn tập và đánh giá

#### Nội dung

Buổi ôn tập diễn ra vào buổi học cuối của Tuần 6. Thi cuối kỳ diễn ra sau Tuần 6, hình thức thi viết 90 phút.

## Đánh giá môn học

### Cơ cấu điểm

#### Nội dung

Điểm chuyên cần chiếm 10 phần trăm. Điểm lab và bài tập chiếm 20 phần trăm. Điểm kiểm tra giữa kỳ chiếm 30 phần trăm. Điểm thi cuối kỳ chiếm 40 phần trăm. Sinh viên cần đạt tối thiểu 4 trên 10 điểm thi cuối kỳ để đậu môn học.