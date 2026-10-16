---
doc_id: CS101
title: Nhập môn lập trình
version: 2026-10-13
owner: Bộ môn Khoa học máy tính
---

# Nhập môn lập trình (CS101)

Tài liệu học tập mẫu cho môn CS101, dành cho sinh viên mới học lập trình. Nội dung bao gồm tư duy thuật toán, biến và kiểu dữ liệu, câu lệnh điều khiển, hàm, mảng, chuỗi và các kỹ thuật giải quyết bài toán cơ bản. Ví dụ mã nguồn sử dụng Python để minh họa; cú pháp có thể cần điều chỉnh nếu lớp học sử dụng ngôn ngữ khác.

## Tuần 1: Tổng quan lập trình và thuật toán

### Bài 1.1: Thuật toán và chương trình

#### Mục tiêu

Sinh viên mô tả được thuật toán như một chuỗi bước hữu hạn để giải quyết bài toán và phân biệt thuật toán với chương trình thực thi.

#### Nội dung

Một thuật toán cần có đầu vào, đầu ra và các bước xử lý rõ ràng. Trước khi viết mã, nên xác định yêu cầu, chia bài toán thành các bước nhỏ và kiểm tra kết quả mong đợi bằng ví dụ.

#### Bài tập

Viết thuật toán dạng giả mã để tính tổng hai số nguyên và tìm số lớn hơn trong hai số.

### Bài 1.2: Cấu trúc chương trình

#### Mục tiêu

Sinh viên nhận biết được cách một chương trình nhận dữ liệu, xử lý và xuất kết quả.

#### Nội dung

Một chương trình đơn giản thường gồm phần nhập dữ liệu, xử lý và in kết quả. Lỗi cú pháp xảy ra khi mã không tuân thủ quy tắc ngôn ngữ; lỗi logic xảy ra khi chương trình chạy nhưng cho kết quả sai.

## Tuần 2: Biến, kiểu dữ liệu và biểu thức

### Bài 2.1: Biến và kiểu dữ liệu

#### Mục tiêu

Sinh viên khai báo hoặc tạo biến phù hợp để lưu trữ dữ liệu và giải thích được vai trò của kiểu dữ liệu.

#### Nội dung

Biến là tên tham chiếu đến một giá trị trong chương trình. Các kiểu dữ liệu thường gặp gồm số nguyên, số thực, chuỗi ký tự và giá trị logic. Việc chọn kiểu dữ liệu phù hợp giúp phép tính và thao tác dữ liệu có ý nghĩa.

#### Bài tập

Viết chương trình nhập chiều dài và chiều rộng hình chữ nhật, sau đó in diện tích và chu vi.

### Bài 2.2: Toán tử và biểu thức

#### Mục tiêu

Sinh viên sử dụng được toán tử số học, so sánh và logic trong biểu thức.

#### Nội dung

Các toán tử số học thường gồm cộng, trừ, nhân, chia và chia lấy dư. Toán tử so sánh tạo ra kết quả đúng/sai; toán tử logic kết hợp các điều kiện. Cần chú ý thứ tự ưu tiên toán tử và dùng dấu ngoặc khi muốn làm rõ thứ tự tính.

## Tuần 3: Rẽ nhánh và vòng lặp

### Bài 3.1: Câu lệnh điều kiện

#### Mục tiêu

Sinh viên dùng cấu trúc `if`, `elif` và `else` để lựa chọn hành động dựa trên điều kiện.

#### Nội dung

Câu lệnh điều kiện cho phép chương trình thực hiện các nhánh khác nhau tùy theo biểu thức logic. Điều kiện cần được kiểm tra với cả trường hợp biên, chẳng hạn giá trị bằng ngưỡng, nhỏ hơn ngưỡng hoặc lớn hơn ngưỡng.

#### Bài tập

Viết chương trình phân loại một số nguyên là âm, dương hoặc bằng không.

### Bài 3.2: Vòng lặp

#### Mục tiêu

Sinh viên chọn và sử dụng vòng lặp để lặp lại một khối lệnh.

#### Nội dung

Vòng lặp `for` thường phù hợp khi duyệt qua một dãy phần tử hoặc một số lần xác định. Vòng lặp `while` tiếp tục chạy khi điều kiện còn đúng. Cần bảo đảm điều kiện dừng có thể đạt được để tránh vòng lặp vô hạn.

#### Bài tập

Viết chương trình tính tổng các số nguyên từ 1 đến n bằng vòng lặp.

## Tuần 4: Hàm và đệ quy

### Bài 4.1: Hàm, tham số và giá trị trả về

#### Mục tiêu

Sinh viên chia chương trình thành các hàm có nhiệm vụ rõ ràng, truyền tham số và trả về kết quả bằng `return`.

#### Nội dung

Hàm là một khối mã có thể được gọi nhiều lần. Tham số nhận dữ liệu đầu vào; giá trị trả về là kết quả mà hàm gửi lại cho nơi gọi. Hàm nên có tên mô tả nhiệm vụ và tránh đảm nhiệm quá nhiều công việc không liên quan.

#### Bài tập

Viết hàm nhận vào hai số và trả về số lớn hơn. Kiểm thử với số âm, hai số bằng nhau và các giá trị khác nhau.

### Bài 4.2: Hàm đệ quy (Recursive Functions)

#### Mục tiêu

Sinh viên giải thích được đệ quy, xác định trường hợp cơ sở và trường hợp đệ quy, đồng thời viết và kiểm thử được một hàm đệ quy đơn giản.

#### Nội dung

**Đệ quy** là kỹ thuật trong đó một hàm gọi lại chính nó để giải quyết một phiên bản nhỏ hơn của cùng bài toán. Một hàm đệ quy đúng cần có:

1. **Trường hợp cơ sở (base case):** điều kiện dừng, trả về kết quả mà không gọi tiếp chính hàm đó.
2. **Trường hợp đệ quy (recursive case):** chia bài toán thành bài toán nhỏ hơn và gọi lại hàm với đầu vào tiến gần đến trường hợp cơ sở.
3. **Tiến trình đến điểm dừng:** mỗi lời gọi cần làm cho bài toán nhỏ hơn hoặc tiến gần điều kiện dừng; nếu không, chương trình có thể gọi vô hạn cho đến khi xảy ra lỗi tràn ngăn xếp (recursion depth/stack overflow tùy ngôn ngữ).

#### Ví dụ 1: Tính giai thừa

Giai thừa của số nguyên không âm n được định nghĩa là `n! = 1` khi `n = 0`, và `n! = n × (n-1)!` khi `n > 0`.

```python
def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:                 # base case
        return 1
    return n * factorial(n - 1)  # recursive case
```

Với `factorial(4)`, các lời gọi lần lượt giảm đối số: `factorial(4)`, `factorial(3)`, `factorial(2)`, `factorial(1)`, `factorial(0)`. Trường hợp cơ sở trả về `1`, sau đó các lời gọi đang chờ trả về lần lượt `1`, `2`, `6` và `24`.

#### Ví dụ 2: Tính tổng từ 1 đến n

```python
def sum_to_n(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:             # base case
        return 0
    return n + sum_to_n(n - 1)  # recursive case
```

Ví dụ, `sum_to_n(4)` trả về `4 + 3 + 2 + 1 + 0 = 10`.

#### Cách phân tích một bài đệ quy

- Xác định đầu vào và kết quả cần trả về.
- Tìm trường hợp nhỏ nhất có thể trả lời trực tiếp.
- Viết quan hệ giữa kết quả hiện tại và lời gọi với đầu vào nhỏ hơn.
- Kiểm tra rằng đầu vào tiến đến trường hợp cơ sở.
- Lần theo các lời gọi bằng một ví dụ nhỏ trước khi kiểm thử đầu vào lớn hơn.

#### Lỗi thường gặp

- **Thiếu trường hợp cơ sở:** hàm tiếp tục gọi chính nó và không dừng đúng cách.
- **Trường hợp cơ sở không thể đạt tới:** đối số không giảm hoặc không tiến về điều kiện dừng.
- **Sai giá trị trả về:** dùng `print()` thay vì `return` khi cần kết quả để tính tiếp.
- **Sai công thức đệ quy:** ví dụ gọi `factorial(n)` thay vì `factorial(n - 1)` trong trường hợp đệ quy.
- **Không xử lý đầu vào biên:** cần xác định hàm sẽ làm gì với `n = 0`, `n = 1` hoặc đầu vào không hợp lệ.

#### Bài tập tự luyện

1. Viết hàm đệ quy tính tổng các chữ số của một số nguyên không âm.
2. Viết hàm đệ quy đếm số phần tử trong một danh sách.
3. Viết hàm đệ quy tìm số Fibonacci thứ n; xác định trường hợp cơ sở cho `n = 0` và `n = 1`.
4. Với mỗi hàm, chỉ rõ base case, recursive case và giải thích vì sao lời gọi sẽ dừng.
5. So sánh lời giải đệ quy với lời giải dùng vòng lặp về độ dễ hiểu và chi phí lời gọi hàm.

### Bài 4.3: Theo dõi lời gọi hàm và ngăn xếp lời gọi

#### Mục tiêu

Sinh viên mô phỏng được thứ tự gọi hàm và trả kết quả khi có nhiều lời gọi lồng nhau.

#### Nội dung

Mỗi lần gọi hàm, chương trình cần theo dõi thông tin của lời gọi hiện tại, bao gồm tham số và vị trí tiếp tục thực thi sau khi hàm trả về. Trong đệ quy, nhiều lời gọi của cùng một hàm có thể đang chờ kết quả cùng lúc. Khi chạm trường hợp cơ sở, các lời gọi được hoàn tất theo thứ tự ngược lại với thứ tự chúng được tạo ra.

#### Bài tập

Vẽ sơ đồ lời gọi của `factorial(3)` và ghi kết quả trả về ở từng bước.

## Tuần 5: Mảng, danh sách và chuỗi

### Bài 5.1: Cấu trúc dữ liệu tuần tự

#### Mục tiêu

Sinh viên truy cập, duyệt và cập nhật phần tử trong mảng hoặc danh sách.

#### Nội dung

Mảng hoặc danh sách lưu nhiều phần tử theo thứ tự. Chỉ số thường bắt đầu từ 0 trong Python. Khi duyệt danh sách, cần tránh truy cập chỉ số ngoài phạm vi và phân biệt chỉ số với giá trị phần tử.

#### Bài tập

Viết hàm tìm giá trị lớn nhất trong danh sách số, có xử lý trường hợp danh sách rỗng.

### Bài 5.2: Xử lý chuỗi

#### Mục tiêu

Sinh viên sử dụng được các thao tác cơ bản để duyệt và xử lý chuỗi.

#### Nội dung

Chuỗi biểu diễn dãy ký tự. Các thao tác cơ bản gồm lấy độ dài, truy cập ký tự, cắt chuỗi và kiểm tra sự xuất hiện của chuỗi con. Khi xử lý văn bản, cần kiểm tra chuỗi rỗng và phân biệt chữ hoa với chữ thường nếu yêu cầu bài toán có quy định.

## Tuần 6: Kiểm thử, gỡ lỗi và ôn tập

### Bài 6.1: Kiểm thử và gỡ lỗi

#### Mục tiêu

Sinh viên xây dựng được các ca kiểm thử cơ bản và xác định nguyên nhân của lỗi cú pháp hoặc lỗi logic.

#### Nội dung

Một bộ kiểm thử nên bao gồm trường hợp thông thường, trường hợp biên và đầu vào không hợp lệ khi phù hợp. Với hàm đệ quy, đặc biệt kiểm tra trường hợp cơ sở, trường hợp sát cơ sở và đầu vào làm phát sinh nhiều lời gọi.

#### Bài tập

Viết các ca kiểm thử cho `factorial(n)` với `n = 0`, `n = 1`, `n = 4` và `n = -1`.

### Bài 6.2: Ôn tập và đánh giá

#### Nội dung

Nội dung ôn tập gồm thuật toán, biến và kiểu dữ liệu, biểu thức, rẽ nhánh, vòng lặp, hàm, đệ quy, cấu trúc dữ liệu tuần tự và kiểm thử. Khi giải bài, sinh viên nên giải thích cách tiếp cận, viết mã, chạy các ca kiểm thử và sửa lỗi dựa trên kết quả quan sát được.

## Ghi chú hỗ trợ nhanh: Hàm đệ quy trong CS101

Nếu cần hỗ trợ gấp về recursive functions, hãy kiểm tra ba câu hỏi sau:

1. **Dừng ở đâu?** Xác định điều kiện cơ sở, chẳng hạn `n == 0`.
2. **Gọi lại với bài toán nào nhỏ hơn?** Ví dụ `factorial(n - 1)`.
3. **Kết quả được kết hợp như thế nào?** Ví dụ `n * factorial(n - 1)`.

Mẫu tổng quát:

```python
def recursive_function(problem):
    if base_case(problem):
        return direct_answer(problem)
    smaller_result = recursive_function(smaller_problem(problem))
    return combine(problem, smaller_result)
```

Mẫu trên chỉ là sơ đồ ý tưởng; `base_case`, `direct_answer`, `smaller_problem` và `combine` cần được thay bằng điều kiện và phép tính cụ thể của từng bài toán.
