---
doc_id: CS102
title: Cấu trúc dữ liệu và giải thuật
version: 2026-10-13
owner: Bộ môn Khoa học máy tính
---

# Cấu trúc dữ liệu và giải thuật (CS102)

Tài liệu học tập mẫu về cách tổ chức dữ liệu và thiết kế thuật toán cơ bản. Ví dụ minh họa sử dụng Python.

## Tuần 1: Phân tích thuật toán

### Bài 1.1: Độ phức tạp thời gian

#### Mục tiêu
Sinh viên mô tả được chi phí thực thi của thuật toán khi kích thước đầu vào tăng.

#### Nội dung
Độ phức tạp thời gian biểu diễn xu hướng tăng số phép toán theo kích thước đầu vào. Ký hiệu Big-O thường dùng để mô tả cận trên tiệm cận. Ví dụ, duyệt một danh sách n phần tử thường có độ phức tạp O(n), còn hai vòng lặp lồng nhau cùng chạy n lần thường tạo ra O(n²).

#### Bài tập
So sánh số lần lặp của một vòng lặp đơn với hai vòng lặp lồng nhau.

### Bài 1.2: Tìm kiếm

#### Mục tiêu
Phân biệt tìm kiếm tuyến tính và tìm kiếm nhị phân.

#### Nội dung
Tìm kiếm tuyến tính kiểm tra từng phần tử, có thời gian O(n) trong trường hợp xấu nhất. Tìm kiếm nhị phân liên tục chia đôi phạm vi tìm kiếm và có thời gian O(log n), nhưng yêu cầu dữ liệu đã được sắp xếp.

## Tuần 2: Mảng, danh sách liên kết và ngăn xếp

### Bài 2.1: Mảng và danh sách liên kết

#### Mục tiêu
Giải thích được sự khác nhau giữa truy cập phần tử theo chỉ số và duyệt qua các nút.

#### Nội dung
Mảng hỗ trợ truy cập theo chỉ số trong thời gian O(1) trong mô hình thông thường. Danh sách liên kết lưu các nút có liên kết đến nút tiếp theo; muốn đến một vị trí thường phải duyệt từ đầu, mất O(n).

### Bài 2.2: Ngăn xếp và hàng đợi

#### Mục tiêu
Sử dụng được hai cấu trúc dữ liệu tuyến tính cơ bản.

#### Nội dung
Ngăn xếp hoạt động theo nguyên tắc LIFO (vào sau, ra trước), với các thao tác push và pop. Hàng đợi hoạt động theo nguyên tắc FIFO (vào trước, ra trước), với các thao tác enqueue và dequeue.

#### Bài tập
Mô phỏng thứ tự phần tử sau một chuỗi thao tác push/pop và enqueue/dequeue.

## Tuần 3: Sắp xếp

### Bài 3.1: Thuật toán sắp xếp cơ bản

#### Mục tiêu
Mô tả được ý tưởng của bubble sort, selection sort và insertion sort.

#### Nội dung
Bubble sort đổi chỗ các phần tử kề nhau nếu sai thứ tự. Selection sort tìm phần tử nhỏ nhất trong phần chưa sắp xếp rồi đưa về vị trí kế tiếp. Insertion sort lần lượt chèn từng phần tử vào vị trí thích hợp trong phần đã sắp xếp. Các thuật toán này thường có thời gian O(n²) trong trường hợp trung bình hoặc xấu nhất.

#### Bài tập
Sắp xếp danh sách [5, 2, 4, 1] bằng insertion sort và ghi lại trạng thái sau mỗi lượt.

### Bài 3.2: Merge sort và quicksort

#### Mục tiêu
Trình bày được ý tưởng chia để trị trong sắp xếp.

#### Nội dung
Merge sort chia dữ liệu thành các phần nhỏ, sắp xếp từng phần rồi trộn lại; thời gian điển hình O(n log n). Quicksort chọn pivot, phân hoạch dữ liệu rồi sắp xếp đệ quy các phần; thời gian trung bình O(n log n), nhưng trường hợp xấu nhất có thể là O(n²).

## Tuần 4: Cây và bảng băm

### Bài 4.1: Cây tìm kiếm nhị phân

#### Mục tiêu
Giải thích cấu trúc nút, cây con trái và cây con phải.

#### Nội dung
Trong cây tìm kiếm nhị phân, các khóa ở cây con trái nhỏ hơn khóa nút theo quy ước so sánh, còn các khóa ở cây con phải lớn hơn. Thời gian thao tác phụ thuộc vào chiều cao cây; cây cân bằng thường cho thao tác tìm kiếm O(log n), trong khi cây lệch có thể cần O(n).

### Bài 4.2: Bảng băm

#### Mục tiêu
Giải thích cách ánh xạ khóa thành vị trí lưu trữ.

#### Nội dung
Hàm băm chuyển khóa thành giá trị dùng để xác định vị trí trong bảng. Va chạm xảy ra khi nhiều khóa ánh xạ đến cùng vị trí. Hai chiến lược xử lý phổ biến là chaining và open addressing.

## Tuần 5: Đồ thị

### Bài 5.1: Biểu diễn đồ thị

#### Mục tiêu
Phân biệt danh sách kề và ma trận kề.

#### Nội dung
Danh sách kề lưu các đỉnh kề với từng đỉnh và thường tiết kiệm bộ nhớ cho đồ thị thưa. Ma trận kề dùng ma trận để thể hiện cạnh giữa các cặp đỉnh và có thể truy vấn sự tồn tại của cạnh trong O(1), nhưng cần O(V²) bộ nhớ.

### Bài 5.2: BFS và DFS

#### Mục tiêu
Mô tả được tìm kiếm theo chiều rộng và chiều sâu.

#### Nội dung
BFS duyệt theo từng lớp khoảng cách và thường dùng hàng đợi. DFS đi sâu theo một nhánh trước khi quay lui, thường triển khai bằng đệ quy hoặc ngăn xếp.

## Tuần 6: Ôn tập và kiểm thử

### Bài 6.1: Chọn thuật toán

#### Nội dung
Việc lựa chọn thuật toán cần cân nhắc kích thước dữ liệu, yêu cầu đầu ra, độ phức tạp thời gian và bộ nhớ, cũng như mức độ đơn giản khi triển khai.

### Bài 6.2: Kiểm thử

#### Nội dung
Kiểm thử nên bao gồm đầu vào thông thường, trường hợp biên và dữ liệu có thể làm lộ lỗi. Với thuật toán sắp xếp, cần kiểm tra danh sách rỗng, một phần tử, phần tử trùng nhau và dữ liệu đã được sắp xếp.
