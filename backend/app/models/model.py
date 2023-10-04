from sqlalchemy import Column, Integer, String, Date, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    country_code = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    date_added = Column(DateTime, default=datetime.now)
    which_user = relationship('UserRole', back_populates="which_role")
    which_department = relationship(
        'Department', back_populates="user_department")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(655))
    description = Column(String(655))
    date_created = Column(DateTime, default=datetime.now)
    roles = relationship('UserRole',  back_populates="user_role")


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    date_modified = Column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    which_role = relationship('User', back_populates="which_user")
    user_role = relationship('Role',  back_populates="roles")


class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    which_user = relationship('UserDepartment',  back_populates="department")


class UserDepartment(Base):
    __tablename__ = 'user_departments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    department_id = Column(Integer, ForeignKey('department.department_id'))
    date_modified = Column(
        DateTime, default=datetime.now, onupdate=datetime.now)

    department = relationship('Department', back_populates="which_which_user")
    user_department = relationship('User',  back_populates="which_department")


class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    contact_number = Column(String(20))
    address = Column(String(255))
    emergency_contact_name = Column(String(255))
    emergency_contact_phone_number = Column(String(255))
    health_insurance_number = Column(String(255))
    health_insurance_provider = Column(String(255))
    medical_history = Column(Text)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date_added = Column(DateTime, default=datetime.now)


class Appointment(Base):
    __tablename__ = 'appointments'

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    appointment_details = Column(Text)
    appointment_date = Column(DateTime, default=datetime.now)
    appointment_type = Column(String(20))
    status = Column(String(20))
    patient = relationship('Patient')
    user = relationship('User')


class VitalSign(Base):
    __tablename__ = 'vital_signs'

    vital_signs_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    heart_rate = Column(Integer, nullable=True)
    blood_pressure = Column(String(20), nullable=True)
    temperature = Column(Float, nullable=True)
    respiratory_rate = Column(Integer, nullable=True)
    oxygen_level = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    recorded_at = Column(DateTime, default=datetime.now)
    patient = relationship('Patient')
    doctor = relationship('User')


class Prescription(Base):
    __tablename__ = 'prescriptions'

    prescription_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    prescription_type = Column(String(255))
    item_id = Column(Integer)
    prescription_details = Column(Text)
    date_prescribed = Column(DateTime, default=datetime.now)

    appointment = relationship('Appointment')
    user = relationship('User')
    patient = relationship('Patient')


class MedicalTest(Base):
    __tablename__ = 'medical_tests'

    test_id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String(255))
    test_details = Column(Text)
    date_added = Column(DateTime, default=datetime.now)
    test_price = Column(Float)


class MedicalTestResult(Base):
    __tablename__ = 'medical_tests'

    result_id = Column(Integer, primary_key=True, index=True)
    medical_test_id = Column(Integer, ForeignKey('users.doctor_id'))
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    date_performed = Column(DateTime, default=datetime.now)


class Drug(Base):
    __tablename__ = 'drugs'

    drug_id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String(255))
    manufacturer = Column(String(255))
    expiry_date = Column(Date)
    price = Column(Float)
    quantity_available = Column(Integer)
    date_added = Column(DateTime, default=datetime.now)


class Ward(Base):
    __tablename__ = 'wards'

    ward_id = Column(Integer, primary_key=True, index=True)
    ward_number = Column(Integer)
    ward_type = Column(String(255))
    price_per_night = Column(String(255))
    date_added = Column(DateTime, default=datetime.now)


class Admission(Base):
    __tablename__ = 'admissions'

    admission_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    ward_id = Column(Integer, ForeignKey('wards.ward_id'))
    admission_date = Column(DateTime, default=datetime.now)
    discharge_date = Column(Date, Nullable=True)
    admitted_by = Column(Integer, ForeignKey('users.user_id'))
    admitted_note = Column(Text, Nullable=True)
    status = Column(String(20))
    patient = relationship('Patient')
    ward = relationship('Ward')


class PatientExpenses(Base):
    __tablename__ = 'patient_expenses'

    expense_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id'))
    item_id = Column(String(255))
    total_amount = Column(Float)
    expense_type = Column(String(255))
    date_created = Column(DateTime, default=datetime.now)

    patient = relationship('Patient')


class Billing(Base):
    __tablename__ = 'billings'

    bill_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    admission_id = Column(Integer, ForeignKey('admissions.admission_id'))
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id'))
    total_amount = Column(Float)
    billing_date = Column(DateTime, default=datetime.now)

    patient = relationship('Patient')
    doctor = relationship('Doctor')
    admission = relationship('Admission')
    appointment = relationship('Appointment')


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id'))
    transaction_date = Column(DateTime, default=datetime.now)
    transaction_type = Column(String(20))
    amount = Column(Float)
    payment_method = Column(String(255))
    transaction_details = Column(Text)


"""
In a hospital, there are various user roles with specific responsibilities and access levels to the hospital management system. Here are some common user roles in a hospital setting:

Administrator:

Manages user accounts and roles.
Has access to all features and functionalities of the system.
Can add, edit, and remove users.

Doctor:

Manages patient appointments.
Views and updates patient records.
Prescribes medications and treatments.
Can view and manage test results.
May have access to billing and financial information.

Nurse:

Records and monitors vital signs.
Administers medications and treatments as prescribed by doctors.
Updates patient charts and records.
Manages patient admissions and discharges.
Provides general patient care and support.

Receptionist:

Schedules patient appointments.
Registers new patients and updates patient information.
Directs patients to appropriate departments or doctors.
Manages phone calls and inquiries.

Accountant:

Manages billing and payments.
Generates and sends invoices to patients.
Tracks financial transactions and payments.
Manages insurance claims and reimbursements.
Laboratory Technician:

Conducts medical tests as prescribed by doctors.
Records and analyzes test results.
Manages lab equipment and supplies.

Pharmacist:

Dispenses medications to patients.
Monitors medication stocks and orders supplies.
Provides medication-related information to patients and healthcare providers.

Security Personnel:

Monitors hospital premises for security.
Ensures the safety of patients, visitors, and staff.
Assists in emergency situations.

IT Support:

Manages and maintains the hospital management system.
Provides technical support to users.
Ensures the system's security and integrity.
Each of these roles has specific permissions and responsibilities tailored to the needs of the hospital. Access to sensitive patient data and financial information is typically restricted and carefully managed to comply with privacy regulations and ensure the security of patient information.

"""
