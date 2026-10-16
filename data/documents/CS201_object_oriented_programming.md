---
doc_id: CS201
title: Lập trình hướng đối tượng
version: 2026-10-13
owner: Bộ môn Khoa học máy tính
---

# Lập trình hướng đối tượng (CS201)

Tài liệu mẫu giới thiệu các khái niệm lập trình hướng đối tượng (OOP). Ví dụ sử dụng cú pháp gần với Python; một số khái niệm cũng áp dụng trong Java, C++ và C#.

## Tuần 1: Lớp và đối tượng

### Bài 1.1: Lớp và đối tượng

#### Mục tiêu
Phân biệt được lớp (class) với đối tượng (object).

#### Nội dung
Lớp định nghĩa cấu trúc và hành vi chung; đối tượng là một thể hiện cụ thể của lớp. Thuộc tính biểu diễn trạng thái, còn phương thức biểu diễn hành vi.

```python
class Student:
    def __init__(self, name):
        self.name = name

student = Student("An")
```

Trong ví dụ, `Student` là lớp và `student` tham chiếu đến một đối tượng có thuộc tính `name`.

### Bài 1.2: Hàm khởi tạo

#### Mục tiêu
Hiểu vai trò của hàm khởi tạo khi tạo đối tượng.

#### Nội dung
Trong Python, `__init__` được gọi để khởi tạo trạng thái của đối tượng sau khi đối tượng được tạo. Tham số `self` tham chiếu đến đối tượng hiện tại.

## Tuần 2: Đóng gói và giao diện

### Bài 2.1: Đóng gói

#### Mục tiêu
Giải thích được lý do gom dữ liệu và hành vi trong một lớp.

#### Nội dung
Đóng gói tổ chức dữ liệu và phương thức liên quan trong cùng một đơn vị, đồng thời định hướng cách bên ngoài tương tác với trạng thái của đối tượng. Python sử dụng quy ước đặt tên và cơ chế truy cập thay vì áp dụng mức truy cập như một số ngôn ngữ khác.

### Bài 2.2: Thuộc tính và phương thức

#### Mục tiêu
Thiết kế được phương thức để thao tác với trạng thái đối tượng.

#### Nội dung
Phương thức thường dùng dữ liệu của đối tượng để thực hiện một hành động. Nên xác định rõ trách nhiệm của từng phương thức và tránh để nhiều phần của chương trình sửa trạng thái theo những cách không nhất quán.

## Tuần 3: Kế thừa và đa hình

### Bài 3.1: Kế thừa

#### Mục tiêu
Mô tả được quan hệ lớp cha và lớp con.

#### Nội dung
Kế thừa cho phép lớp con sử dụng hoặc mở rộng hành vi của lớp cha. Chỉ nên dùng kế thừa khi quan hệ giữa các lớp thể hiện hợp lý quan hệ “là một” (is-a).

### Bài 3.2: Đa hình

#### Mục tiêu
Giải thích được cách các đối tượng khác loại có thể cung cấp cùng một giao diện hành vi.

#### Nội dung
Đa hình cho phép cùng một lời gọi phương thức tạo ra hành vi khác nhau tùy theo đối tượng thực tế. Ví dụ, các lớp `Circle` và `Rectangle` có thể cùng triển khai phương thức `area()` nhưng tính diện tích theo công thức khác nhau.

## Tuần 4: Trừu tượng hóa và thiết kế lớp

### Bài 4.1: Trừu tượng hóa

#### Mục tiêu
Xác định được những đặc điểm quan trọng của đối tượng trong bài toán.

#### Nội dung
Trừu tượng hóa tập trung vào thông tin cần thiết cho yêu cầu và ẩn bớt chi tiết không liên quan. Khi thiết kế lớp, cần xem xét dữ liệu, hành vi, trách nhiệm và mối quan hệ giữa các lớp.

### Bài 4.2: Quan hệ giữa các đối tượng

#### Mục tiêu
Phân biệt liên kết, kết tập và hợp thành ở mức khái niệm.

#### Nội dung
Liên kết mô tả việc các đối tượng có quan hệ hoặc tương tác. Kết tập thể hiện quan hệ toàn thể–thành phần mà thành phần có thể tồn tại độc lập. Hợp thành thể hiện quan hệ sở hữu chặt hơn, trong đó vòng đời thành phần thường gắn với toàn thể theo mô hình thiết kế.

## Tuần 5: Ngoại lệ và kiểm thử

### Bài 5.1: Xử lý ngoại lệ

#### Mục tiêu
Sử dụng cấu trúc xử lý lỗi để tránh chương trình kết thúc ngoài dự kiến khi có lỗi có thể dự đoán.

#### Nội dung
Trong Python, `try` và `except` cho phép xử lý một số ngoại lệ. Nên bắt loại ngoại lệ phù hợp, không che giấu lỗi bằng cách bắt mọi ngoại lệ mà không ghi nhận hoặc xử lý.

### Bài 5.2: Kiểm thử lớp

#### Mục tiêu
Thiết kế ca kiểm thử cho thuộc tính và phương thức.

#### Nội dung
Kiểm thử lớp nên xem xét trạng thái khởi tạo, lời gọi phương thức hợp lệ, dữ liệu biên và hành vi khi nhận đầu vào không hợp lệ. Có thể kiểm thử từng lớp độc lập trước khi kiểm thử các lớp tương tác với nhau.

## Tuần 6: Ôn tập và bài tập tổng hợp

### Bài 6.1: Thiết kế chương trình nhỏ

#### Nội dung
Một bài tập tổng hợp có thể mô hình hóa hệ thống quản lý sinh viên với các lớp `Student`, `Course` và `Enrollment`. Cần xác định trách nhiệm của từng lớp, dữ liệu cần lưu và các phương thức để đăng ký hoặc hủy đăng ký học phần.

### Bài 6.2: Ôn tập

#### Nội dung
Nội dung ôn tập gồm lớp, đối tượng, thuộc tính, phương thức, đóng gói, kế thừa, đa hình, trừu tượng hóa, quan hệ giữa đối tượng, ngoại lệ và kiểm thử.
