from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class Enrollment(Base):
    """Bảng lưu thông tin đăng ký lớp học phần và các cột điểm thành phần"""
    _tablename_ = 'enrollments'
    
    class_id = Column(String, ForeignKey('course_classes.class_id'), primary_key=True)
    student_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    
    chuyen_can = Column(Float, default=0.0)
    giua_ky = Column(Float, default=0.0)
    cuoi_ky = Column(Float, default=0.0)

    course_class = relationship("CourseClass", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")


class User(Base):
    _tablename_ = 'users'
    
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    _mapper_args_ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    def check_login(self, input_email, input_password) -> bool:
        return self.email == input_email and self.password == input_password

    def change_password(self, old_password, new_password) -> tuple[bool, str]:
        if self.password == old_password:
            self.password = new_password
            return True, "Thay đổi mật khẩu tài khoản thành công."
        return False, "Mật khẩu cũ nhập vào không chính xác."


class Student(User):
    rls = Column(Integer, default=0)
    credits = Column(Integer, default=0)
    attendance_rate = Column(Float, default=1.0)

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="student", cascade="all, delete-orphan")

    _mapper_args_ = {
        'polymorphic_identity': 'Student'
    }

    def check_academic_warning(self) -> tuple[bool, str]:
        if self.gpa < 2.8 or self.attendance_rate < 0.8:
            return True, f"Cảnh báo học tập: Sinh viên {self.name} có GPA thấp hoặc nghỉ học quá giới hạn quy định!"
        return False, "Trạng thái học tập bình thường."

    def calculate_scholarship_score(self) -> float:
        if self.credits >= 18 and self.rls > 80:
            return self.gpa * 0.8 + (self.rls) * 0.2 / 4
        return -1.0 


class Lecturer(User):
    assigned_classes = relationship("CourseClass", back_populates="lecturer")
    projects = relationship("Project", back_populates="lecturer")

    _mapper_args_ = {
        'polymorphic_identity': 'Lecturer'
    }

    def update_student_score(self, class_obj, student_obj, score_type: str, value: float) -> tuple[bool, str]:
        if class_obj not in self.assigned_classes:
            return False, f"Lỗi quyền hạn: Giảng viên không phụ trách lớp học phần {class_obj.class_id}."
        
        class_students = [en.student for en in class_obj.enrollments]
        if student_obj not in class_students:
            return False, f"Lỗi dữ liệu: Sinh viên không thuộc danh sách lớp {class_obj.class_id}."

        for en in class_obj.enrollments:
            if en.student_id == student_obj.user_id:
                if score_type == 'chuyen_can': en.chuyen_can = float(value)
                elif score_type == 'giua_ky': en.giua_ky = float(value)
                elif score_type == 'cuoi_ky': en.cuoi_ky = float(value)
                else: return False, "Lỗi: Loại điểm số yêu cầu cập nhật không hợp lệ."
                return True, f"Cập nhật thành công điểm {score_type} cho sinh viên {student_obj.name}."
        return False, "Không tìm thấy bản ghi đăng ký hợp lệ."


class AcademicStaff(User):
    _mapper_args_ = {
        'polymorphic_identity': 'staff'
    }

    def add_entity(self, target_list: list, entity_obj, id_attr_name: str) -> tuple[bool, str]:
        new_id = getattr(entity_obj, id_attr_name)
        for item in target_list:
            if getattr(item, id_attr_name) == new_id:
                return False, f"Lỗi: Thực thể có mã định danh {new_id} đã tồn tại trên hệ thống!"
        target_list.append(entity_obj)
        return True, "Thêm mới thực thể dữ liệu vào hệ thống thành công."

    def delete_entity(self, target_list: list, id_attr_name: str, target_id: str) -> tuple[bool, str]:
        for item in target_list:
            if getattr(item, id_attr_name) == target_id:
                target_list.remove(item)
                return True, f"Xóa thành công thực thể có mã định danh {target_id}."
        return False, f"Lỗi: Không tìm thấy thực thể mã {target_id} để thực hiện xóa."

    def get_gpa_classification_stats(self, student_list: list) -> dict:
        stats = {"Xuất sắc": 0, "Giỏi": 0, "Khá": 0, "Trung bình": 0}
        for s in student_list:
            if s.gpa >= 3.6: stats["Xuất sắc"] += 1
            elif s.gpa >= 3.2: stats["Giỏi"] += 1
            elif s.gpa >= 2.5: stats["Khá"] += 1
            else: stats["Trung bình"] += 1
        return stats



class Course(Base):
    _tablename_ = 'courses'
    
    course_id = Column(String, primary_key=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    
    prerequisite_id = Column(String, ForeignKey('courses.course_id'), nullable=True)
    alternative_course_id = Column(String, ForeignKey('courses.course_id'), nullable=True)


class CourseClass(Base):
    _tablename_ = 'course_classes'
    
    class_id = Column(String, primary_key=True)
    course_id = Column(String, ForeignKey('courses.course_id'), nullable=False)
    lecturer_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    attendance_code = Column(String, nullable=True)

    lecturer = relationship("Lecturer", back_populates="assigned_classes")
    enrollments = relationship("Enrollment", back_populates="course_class", cascade="all, delete-orphan")


    def register_student(self, student_obj: Student, completed_courses: dict) -> tuple[bool, str]:
        prereq = self.course.prerequisite_id
        if prereq:
            if prereq not in completed_courses or completed_courses[prereq] == 'F':
                suggestion = f" Gợi ý lộ trình thay thế: Bạn có thể chọn học môn [{self.course.alternative_course_id}] trước." if self.course.alternative_course_id else ""
                return False, f"Hệ thống chặn tác vụ: Bạn chưa đạt môn tiên quyết bắt buộc ({prereq})!{suggestion}"

        class_students = [en.student_id for en in self.enrollments]
        if student_obj.user_id in class_students:
            return False, "Sinh viên đã thực hiện đăng ký lớp học phần này trước đó."

        
        new_enrollment = Enrollment(course_class=self, student=student_obj)
        self.enrollments.append(new_enrollment)
        return True, f"Đăng ký thành công vào lớp học phần {self.class_id}."

    def start_attendance_session(self, code: str) -> tuple[bool, str]:
        self.attendance_code = code
        return True, f"Kích hoạt thành công phiên điểm danh cho lớp {self.class_id}. Mã phiên: {code}"

    def student_check_in(self, student_obj: Student, input_code: str) -> tuple[bool, str]:
        if not self.attendance_code:
            return False, "Lỗi: Phiên điểm danh hiện không mở hoặc đã hết hạn dùng 5 phút."
        if input_code != self.attendance_code:
            return False, "Mã số bảo mật xác nhận điểm danh nhập vào không chính xác."

        for en in self.enrollments:
            if en.student_id == student_obj.user_id:
                en.chuyen_can = min(10.0, en.chuyen_can + 1.0)
                return True, "Xác nhận hiện diện portal thành công! Dữ liệu chuyên cần đã được đồng bộ trực tiếp."
        return False, "Lỗi: Bạn không nằm trong danh sách phân quyền của lớp học phần này."


class Project(Base):
    _tablename_ = 'projects'
    
    project_id = Column(String, primary_key=True)
    project_name = Column(String, nullable=False)
    student_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    lecturer_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    status = Column(String, default="Đang thực hiện")

    student = relationship("Student", back_populates="projects")
    lecturer = relationship("Lecturer", back_populates="projects")


class ScholarshipEngine:
    @staticmethod
    def process_scholarships(student_list: list, slots: int) -> list:
        eligible_students = [s for s in student_list if s.calculate_scholarship_score() > -1.0]
        
        sorted_students = sorted(eligible_students, key=lambda s: s.calculate_scholarship_score(), reverse=True)
        return sorted_students[:slots]



DATABASE_URL = "sqlite:///hms_database.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)###
    
    DATABASE_URL = "sqlite:///hms_database.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    """Hàm tạo file hms_database.db và cấu trúc các bảng"""
    Base.metadata.create_all(bind=engine)
    print("Đã khởi tạo thành công CSDL: hms_database.db bằng SQLAlchemy")

if "_name_" == "_main_":
    create_database()