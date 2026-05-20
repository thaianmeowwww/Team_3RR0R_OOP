# 1. PHÂN HỆ NGƯỜI DÙNG (USER ARCHITECTURE)
class User:
    PREFIX = ""  
    def __init__(self, id_num, name, email, password, role):
        self.user_id = f"{self.PREFIX}{id_num}"
        self.name = name
        self.email = email
        self.__password = password  
        self.role = role 

    def check_login(self, input_email, input_password) -> bool:
        return self.email == input_email and self.__password == input_password

    def change_password(self, old_password, new_password) -> tuple[bool, str]:
        if self.__password == old_password:
            self.__password = new_password
            return True, "Thay đổi mật khẩu tài khoản thành công."
        return False, "Mật khẩu cũ nhập vào không chính xác."

class Student(User):
    PREFIX = "SV"  
    def __init__(self, id_num, name, email, password, gpa=0.0, rls=0, credits=0, attendance_rate=1.0):
        super().__init__(id_num, name, email, password, role='Student')
        self.gpa = gpa                  
        self.rls = rls                 
        self.credits = credits          
        self.attendance_rate = attendance_rate  

    def check_academic_warning(self) -> tuple[bool, str]:
        if self.gpa < 2.8 or self.attendance_rate < 0.8:
            return True, f"Cảnh báo học tập: Sinh viên {self.name} có GPA thấp hoặc nghỉ học quá giới hạn quy định!"
        return False, "Trạng thái học tập bình thường."

    def calculate_scholarship_score(self) -> float:
        if self.credits >= 18 and self.rls > 80:
            return self.gpa*0.8+ (self.rls)*0.2/4
        return -1.0 

class Lecturer(User):
    PREFIX = "GV"  
    def __init__(self, id_num, name, email, password, assigned_classes=None):
        super().__init__(id_num, name, email, password, role='Lecturer')
        self.assigned_classes = assigned_classes if assigned_classes else []
    def update_student_score(self, class_obj, student_obj, score_type: str, value: float) -> tuple[bool, str]:
        if class_obj not in self.assigned_classes:
            return False, f"Lỗi quyền hạn: Giảng viên không phụ trách lớp học phần {class_obj.class_id}."
        if student_obj not in class_obj.students:
            return False, f"Lỗi dữ liệu: Sinh viên không thuộc danh sách lớp {class_obj.class_id}."

        # Khởi tạo bản ghi điểm nếu chưa tồn tại trong bảng điểm lớp học phần
        if student_obj.user_id not in class_obj.grades_db:
            class_obj.grades_db[student_obj.user_id] = {'chuyen_can': 0.0, 'giua_ky': 0.0, 'cuoi_ky': 0.0}

        if score_type in class_obj.grades_db[student_obj.user_id]:
            class_obj.grades_db[student_obj.user_id][score_type] = float(value)
            return True, f"Cập nhật thành công điểm {score_type} cho sinh viên {student_obj.name}."
        return False, "Lỗi: Loại điểm số yêu cầu cập nhật không hợp lệ."

class AcademicStaff(User):
    PREFIX = "AD"  # Tự động đồng bộ tiền tố mã giáo vụ

    def __init__(self, id_num, name, email, password):
        super().__init__(id_num, name, email, password, role='staff')

    def add_entity(self, target_list: list, entity_obj, id_attr_name: str) -> tuple[bool, str]:
        """[Tính năng cơ bản] Giáo vụ thực hiện thêm mới hồ sơ/môn học/lớp học phần (Create) [cite: 22]"""
        new_id = getattr(entity_obj, id_attr_name)
        for item in target_list:
            if getattr(item, id_attr_name) == new_id:
                return False, f"Lỗi: Thực thể có mã định danh {new_id} đã tồn tại trên hệ thống!"
        
        target_list.append(entity_obj)
        return True, "Thêm mới thực thể dữ liệu vào hệ thống thành công."

    def delete_entity(self, target_list: list, id_attr_name: str, target_id: str) -> tuple[bool, str]:
        """[Tính năng cơ bản] Giáo vụ thực hiện xóa hồ sơ/môn học/lớp học phần (Delete) [cite: 22]"""
        for item in target_list:
            if getattr(item, id_attr_name) == target_id:
                target_list.remove(item)
                return True, f"Xóa thành công thực thể có mã định danh {target_id}."
        return False, f"Lỗi: Không tìm thấy thực thể mã {target_id} để thực hiện xóa."

    def get_gpa_classification_stats(self, student_list: list) -> dict:
        """[Use Case 5] Xử lý thống kê phân loại học lực phục vụ hiển thị biểu đồ tròn [cite: 44, 45]"""
        stats = {"Xuất sắc": 0, "Giỏi": 0, "Khá": 0, "Trung bình": 0}
        for s in student_list:
            if s.gpa >= 3.6: stats["Xuất sắc"] += 1
            elif s.gpa >= 3.2: stats["Giỏi"] += 1
            elif s.gpa >= 2.5: stats["Khá"] += 1
            else: stats["Trung bình"] += 1
        return stats


# ==========================================
# 2. PHÂN HỆ CHỨC NĂNG (FUNCTIONAL & DATA)
# ==========================================

class Course:
    def __init__(self, course_id: str, course_name: str, credits: int, prerequisite_id: str = None, alternative_course_id: str = None):
        self.course_id = course_id                  # Mã môn học [cite: 22]
        self.course_name = course_name              # Tên môn học [cite: 22]
        self.credits = credits                      # Số tín chỉ
        self.prerequisite_id = prerequisite_id      # Mã môn tiên quyết [cite: 42]
        self.alternative_course_id = alternative_course_id  # Lộ trình học thay thế gợi ý khi bị chặn đăng ký [cite: 43]


class CourseClass:
    def __init__(self, class_id: str, course_obj: Course, lecturer_obj: Lecturer):
        self.class_id = class_id            # Mã lớp học phần mở trong kỳ [cite: 22]
        self.course = course_obj            # Đối tượng môn học tương ứng (Course)
        self.lecturer = lecturer_obj        # Đối tượng giảng viên phụ trách (Lecturer)
        self.students = []                  # Danh sách sinh viên thuộc lớp học phần [cite: 23]
        self.attendance_code = None         # Mã điểm danh bảo mật ngắn hạn [cite: 38]
        self.grades_db = {}                 # {student_id: {'chuyen_can': 0.0, 'giua_ky': 0.0, 'cuoi_ky': 0.0}} [cite: 24]

    def register_student(self, student_obj: Student, completed_courses: dict) -> tuple[bool, str]:
        """[Use Case 4] Đăng ký Học phần và chủ động kiểm tra môn tiên quyết [cite: 41, 42]"""
        prereq = self.course.prerequisite_id
        if prereq:
            # Nếu chưa đạt môn tiên quyết (chưa học hoặc bị điểm F) [cite: 42, 43]
            if prereq not in completed_courses or completed_courses[prereq] == 'F':
                suggestion = f" Gợi ý lộ trình thay thế: Bạn có thể chọn học môn [{self.course.alternative_course_id}] trước." if self.course.alternative_course_id else ""
                return False, f"Hệ thống chặn tác vụ: Bạn chưa đạt môn tiên quyết bắt buộc ({prereq})!{suggestion}" [cite: 43]

        if student_obj in self.students:
            return False, "Sinh viên đã thực hiện đăng ký lớp học phần này trước đó."

        self.students.append(student_obj)
        self.grades_db[student_obj.user_id] = {'chuyen_can': 0.0, 'giua_ky': 0.0, 'cuoi_ky': 0.0}
        return True, f"Đăng ký thành công vào lớp học phần {self.class_id}."

    def start_attendance_session(self, code: str) -> tuple[bool, str]:
        """[Use Case 3] Giảng viên kích hoạt tạo phiên điểm danh ngẫu nhiên kèm mã số bảo mật [cite: 37, 38]"""
        self.attendance_code = code
        return True, f"Kích hoạt thành công phiên điểm danh cho lớp {self.class_id}. Mã phiên: {code}"

    def student_check_in(self, student_obj: Student, input_code: str) -> tuple[bool, str]:
        """[Use Case 3] Sinh viên nhập mã xác nhận hiện diện, tự động cộng dồn và đồng bộ chuyên cần [cite: 39, 40]"""
        if not self.attendance_code:
            return False, "Lỗi: Phiên điểm danh hiện không mở hoặc đã hết hạn dùng 5 phút." [cite: 38]
        if input_code != self.attendance_code:
            return False, "Mã số bảo mật xác nhận điểm danh nhập vào không chính xác." [cite: 39]
        if student_obj not in self.students:
            return False, "Lỗi: Bạn không nằm trong danh sách phân quyền của lớp học phần này."

        # Tự động cộng dồn dữ liệu, tính tỷ lệ phần trăm và đồng bộ trực tiếp vào cột điểm chuyên cần [cite: 40]
        current_score = self.grades_db[student_obj.user_id]['chuyen_can']
        self.grades_db[student_obj.user_id]['chuyen_can'] = min(10.0, current_score + 1.0)
        return True, "Xác nhận hiện diện portal thành công! Dữ liệu chuyên cần đã được đồng bộ trực tiếp." [cite: 39, 40]


class Project:
    """Mô-đun quản lý danh sách đồ án dành riêng cho Sinh viên và Giảng viên [cite: 14, 15]"""
    def __init__(self, project_id: str, project_name: str, student_obj: Student, lecturer_obj: Lecturer):
        self.project_id = project_id
        self.project_name = project_name
        self.student = student_obj
        self.lecturer = lecturer_obj
        self.status = "Đang thực hiện"


# ==========================================
# 3. PHÂN HỆ THUẬT TOÁN (CORE ENGINES)
# ==========================================

class ScholarshipEngine:
    @staticmethod
    def process_scholarships(student_list: list, slots: int) -> list:
        """[Use Case 1] Thuật toán lọc điều kiện cần và tự động sắp xếp xét học bổng [cite: 28, 29]"""
        # Bước 1: Lọc ra danh sách sinh viên đủ điều kiện cần học vụ [cite: 30, 32]
        eligible_students = [s for s in student_list if s.calculate_scholarship_score() > -1.0]
        
        # Bước 2: Sắp xếp giảm dần. Python tự động gọi hàm __lt__ nạp chồng ở lớp Student để so sánh [cite: 33]
        sorted_students = sorted(eligible_students, reverse=True)
        
        # Bước 3: Cắt mốc chọn ra các sinh viên đạt giải theo chỉ tiêu suất học bổng [cite: 29, 33]
        return sorted_students[:slots]