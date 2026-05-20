# Team_3RR0R_OOP
# [cite_start]Hệ thống Quản lý Học tập Số cho Sinh viên BCSE [cite: 3]

## 📌 Tổng quan dự án
[cite_start]Dự án xây dựng một hệ thống quản lý học vụ số tích hợp và số hóa toàn diện dành riêng cho ngành BCSE[cite: 11, 12]. [cite_start]Hệ thống được phát triển dựa trên kiến trúc lập trình hướng đối tượng (OOP), áp dụng mô hình phân quyền (RBAC) cho 3 nhóm người dùng cơ bản và triển khai theo cấu trúc thiết kế MVC chuẩn hóa[cite: 12, 13, 67].

* [cite_start]**Tên nhóm:** 3RROR - Lớp C1 [cite: 4]
* [cite_start]**Thành viên:** * Hoàng Việt Anh (Trưởng nhóm) [cite: 6]
    * [cite_start]Lê Văn Thái An [cite: 7]
    * [cite_start]Nguyễn Vũ Hương Ly [cite: 8]
    * [cite_start]Hoàng Phương Đông Hòa [cite: 9]

---

## 🛠️ Stack Công nghệ
* [cite_start]**Ngôn ngữ chính:** Python 3.x [cite: 47]
* [cite_start]**Giao diện người dùng (UI/UX):** CustomTkinter (Phong cách Modern Minimalist, hỗ trợ Dark/Light mode tự động) [cite: 48, 49]
* [cite_start]**Cơ sở dữ liệu:** SQLite (Lưu trữ cục bộ gọn nhẹ dưới dạng tệp đơn nhất) [cite: 51]
* [cite_start]**Thư viện ORM:** SQLAlchemy ORM (Ánh xạ các bảng dữ liệu thành các lớp đối tượng Python) [cite: 52]
* [cite_start]**Hiển thị đồ thị:** Matplotlib (Nhúng trực tiếp biểu đồ thống kê lên giao diện) [cite: 50]

---

## 🚀 Các Tính năng Chính
[cite_start]Hệ thống kế thừa lớp cơ sở `User` thành 3 lớp con (`Student`, `Lecturer`, `AcademicStaff`) để thực thi các nhóm chức năng phân quyền[cite: 19]:

### [cite_start]1. Nhóm tính năng cơ bản [cite: 20]
* [cite_start]**Hệ thống chung:** Xác thực tài khoản qua Form đăng nhập và tự động điều hướng giao diện theo quyền hạn[cite: 21].
* [cite_start]**Giáo vụ (AcademicStaff):** Thực hiện các tác vụ CRUD quản lý hồ sơ Sinh viên, Giảng viên, Môn học và các Lớp học phần[cite: 22].
* [cite_start]**Giảng viên (Lecturer):** Xem lịch giảng dạy cá nhân, quản lý danh sách sinh viên lớp học phần và cập nhật các cột điểm thành phần[cite: 23, 24].
* [cite_start]**Sinh viên (Student):** Tra cứu thời khóa biểu lịch học/thi, xem bảng điểm chi tiết và theo dõi điểm GPA hiện tại[cite: 25, 26].

### [cite_start]2. Nhóm tính năng thông minh [cite: 27]
* [cite_start]**Xét học bổng tự động (`ScholarshipEngine`):** Tính toán điểm xét học bổng (80% GPA + 20% ĐRL) với điều kiện $\ge 18$ tín chỉ và ĐRL $> 80$[cite: 30, 31, 32]. [cite_start]Ứng dụng nạp chồng toán tử so sánh để tự động sắp xếp và sàng lọc danh sách nhận giải[cite: 33].
* [cite_start]**Cảnh báo học tập tự động:** Tự động quét và gán nhãn, hiển thị thông báo nhắc nhở trực tiếp khi sinh viên có GPA dưới 2.8 hoặc tỷ lệ nghỉ học vượt quá 20%[cite: 36].
* [cite_start]**Quản lý điểm danh thông minh:** Giảng viên tạo phiên điểm danh ngẫu nhiên bằng mã số bảo mật ngắn hạn (hạn 5 phút) để sinh viên nhập portal xác nhận[cite: 38, 39]. [cite_start]Dữ liệu tự động cộng dồn và đồng bộ vào cột điểm chuyên cần[cite: 40].
* [cite_start]**Đăng ký học phần tiên quyết:** Tự động kiểm tra lịch sử điểm số và chủ động chặn tác vụ đăng ký, đồng thời gợi ý lộ trình thay thế nếu sinh viên chưa đạt môn tiên quyết (điểm F)[cite: 42, 43].
* [cite_start]**Thống kê trực quan:** Xử lý và hiển thị biểu đồ cột (phổ điểm lớp học phần) và biểu đồ tròn (tỷ lệ phân loại học lực toàn khóa) dành cho Giảng viên và Giáo vụ[cite: 45].

---

## 📁 Cấu trúc Thư mục Dự án
[cite_start]Mã nguồn được phân chia module chuẩn hóa theo mô hình kiến trúc MVC[cite: 67]:
```text
├── models/          # Định nghĩa cấu trúc dữ liệu và các lớp thực thể (SQLAlchemy) [cite: 56, 67]
├── views/           # Giao diện người dùng layout CustomTkinter [cite: 60, 67]
├── controllers/     # Logic xử lý nghiệp vụ, thuật toán thông minh và điều hướng [cite: 58, 67]
├── database/        # Tệp dữ liệu cục bộ (.db) chứa dữ liệu giả lập [cite: 51, 68]
├── requirements.txt # Danh sách các thư viện cần cài đặt [cite: 67]
└── main.py          # Điểm chạy kịch bản chính của ứng dụng [cite: 68]