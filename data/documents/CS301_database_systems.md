---
doc_id: CS301
title: Cơ sở dữ liệu
version: 2026-10-13
owner: Bộ môn Khoa học máy tính
---

# Cơ sở dữ liệu (CS301)

Tài liệu mẫu giới thiệu các khái niệm nền tảng về mô hình dữ liệu quan hệ và SQL. Các ví dụ truy vấn dùng cú pháp SQL phổ biến; một số chi tiết có thể khác nhau giữa các hệ quản trị cơ sở dữ liệu.

## Tuần 1: Khái niệm cơ sở dữ liệu

### Bài 1.1: Cơ sở dữ liệu và hệ quản trị cơ sở dữ liệu

#### Mục tiêu
Phân biệt cơ sở dữ liệu với hệ quản trị cơ sở dữ liệu (DBMS).

#### Nội dung
Cơ sở dữ liệu là tập hợp dữ liệu được tổ chức để lưu trữ và truy xuất. DBMS là phần mềm hỗ trợ định nghĩa, truy vấn, cập nhật và quản lý quyền truy cập dữ liệu.

### Bài 1.2: Mô hình quan hệ

#### Mục tiêu
Nhận biết bảng, hàng, cột và miền giá trị.

#### Nội dung
Trong mô hình quan hệ, bảng biểu diễn một quan hệ, hàng biểu diễn bản ghi và cột biểu diễn thuộc tính. Mỗi cột có miền giá trị được xác định theo kiểu dữ liệu hoặc quy tắc của hệ thống.

## Tuần 2: Khóa và ràng buộc

### Bài 2.1: Khóa chính và khóa ngoại

#### Mục tiêu
Giải thích được cách khóa xác định bản ghi và biểu diễn quan hệ giữa bảng.

#### Nội dung
Khóa chính (PRIMARY KEY) xác định duy nhất mỗi hàng và không được chứa giá trị NULL. Khóa ngoại (FOREIGN KEY) tham chiếu khóa được chỉ định ở bảng khác hoặc trong cùng bảng, nhằm duy trì toàn vẹn tham chiếu theo các ràng buộc đã khai báo.

### Bài 2.2: Ràng buộc dữ liệu

#### Mục tiêu
Nhận biết các ràng buộc phổ biến.

#### Nội dung
Các ràng buộc thường gặp gồm `NOT NULL`, `UNIQUE`, `CHECK`, `PRIMARY KEY` và `FOREIGN KEY`. Ràng buộc giúp DBMS từ chối những thao tác vi phạm quy tắc dữ liệu đã định nghĩa.

## Tuần 3: Truy vấn SQL cơ bản

### Bài 3.1: SELECT, WHERE và ORDER BY

#### Mục tiêu
Viết truy vấn lọc và sắp xếp dữ liệu.

#### Nội dung
`SELECT` chỉ định các cột cần trả về; `FROM` chỉ định bảng; `WHERE` lọc hàng theo điều kiện; `ORDER BY` sắp xếp kết quả.

```sql
SELECT student_id, full_name
FROM Student
WHERE major = 'CS'
ORDER BY full_name;
```

### Bài 3.2: Hàm tổng hợp và GROUP BY

#### Mục tiêu
Tính toán thống kê trên các nhóm bản ghi.

#### Nội dung
Các hàm tổng hợp thường dùng gồm `COUNT`, `SUM`, `AVG`, `MIN` và `MAX`. `GROUP BY` gom các hàng theo một hoặc nhiều cột; `HAVING` lọc các nhóm sau khi tổng hợp.

```sql
SELECT major, COUNT(*) AS student_count
FROM Student
GROUP BY major;
```

## Tuần 4: Kết nối bảng và truy vấn con

### Bài 4.1: JOIN

#### Mục tiêu
Kết hợp dữ liệu từ nhiều bảng dựa trên điều kiện liên kết.

#### Nội dung
`INNER JOIN` trả về các hàng thỏa điều kiện nối. `LEFT JOIN` giữ tất cả hàng từ bảng bên trái và ghép dữ liệu phù hợp từ bảng bên phải; nếu không có hàng phù hợp, các cột bên phải có thể là NULL.

```sql
SELECT s.full_name, e.course_id
FROM Student AS s
INNER JOIN Enrollment AS e
    ON s.student_id = e.student_id;
```

### Bài 4.2: Truy vấn con

#### Mục tiêu
Sử dụng truy vấn bên trong một truy vấn khác.

#### Nội dung
Truy vấn con có thể xuất hiện trong `WHERE`, `FROM` hoặc danh sách `SELECT`, tùy loại truy vấn và hệ quản trị. Khi có thể, nên đặt bí danh rõ ràng và kiểm tra truy vấn trả về một giá trị hay nhiều hàng.

## Tuần 5: Thiết kế và chuẩn hóa

### Bài 5.1: Phụ thuộc hàm

#### Mục tiêu
Hiểu khái niệm phụ thuộc hàm ở mức cơ bản.

#### Nội dung
Phụ thuộc hàm X → Y có nghĩa là trong quan hệ đang xét, giá trị X xác định duy nhất giá trị Y. Phân tích phụ thuộc hàm hỗ trợ xác định khóa và đánh giá thiết kế bảng.

### Bài 5.2: Chuẩn hóa

#### Mục tiêu
Giải thích lý do chuẩn hóa bảng dữ liệu.

#### Nội dung
Chuẩn hóa giúp giảm dư thừa và hạn chế bất thường khi thêm, sửa hoặc xóa dữ liệu. Dạng chuẩn 1NF yêu cầu các thuộc tính có giá trị nguyên tố theo mô hình quan hệ; 2NF loại bỏ phụ thuộc bộ phận của thuộc tính không khóa vào một phần khóa ghép; 3NF xử lý một số dạng phụ thuộc bắc cầu theo điều kiện xác định của dạng chuẩn.

## Tuần 6: Giao dịch và ôn tập

### Bài 6.1: Giao dịch và ACID

#### Mục tiêu
Nêu được bốn thuộc tính ACID.

#### Nội dung
Atomicity (tính nguyên tử) yêu cầu giao dịch được thực hiện toàn bộ hoặc không thực hiện. Consistency (tính nhất quán) yêu cầu giao dịch bảo toàn các ràng buộc. Isolation (tính cô lập) điều chỉnh mức độ ảnh hưởng lẫn nhau giữa các giao dịch đồng thời. Durability (tính bền vững) yêu cầu thay đổi đã xác nhận được duy trì theo bảo đảm của hệ thống.

### Bài 6.2: Ôn tập và kiểm thử truy vấn

#### Nội dung
Khi kiểm thử truy vấn, cần xem xét bảng rỗng, giá trị NULL, bản ghi trùng, trường hợp không có kết quả và dữ liệu có quan hệ khóa ngoại. Cần đọc kết quả thực tế và xác minh rằng truy vấn đáp ứng đúng yêu cầu nghiệp vụ.
