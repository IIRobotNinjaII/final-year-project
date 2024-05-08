from enum import Enum

class UserType(Enum):
    STUDENT = 'student'
    UNAPPROVED_OFFICER = 'unapproved_officer'
    OFFICER = 'officer'
    ADMIN = 'admin'

class ComplaintType(Enum):
    ACCOUNT = "account"
    ACADEMIC = "academic"
    RESIDENTIAL = "residential"
    ADMIN = "admin"

class Residence(Enum):
    BOYSHOSTEL = 'boyshostel'
    GIRLSHOSTEL = 'girlshostel'
    DAYSCHOLAR = 'dayscholar'
    # None for officer

class Department(Enum):
    BIOTECHNOLOGY = 'biotechnology'
    CHEMICAL_ENGINEERING = 'chemical engineering'
    CHEMISTRY = 'chemistry'
    CIVIL_ENGINEERING = 'civil engineering'
    COMPUTER_SCIENCE_AND_ENGINEERING = 'computer science and engineering'
    ELECTRICAL_ENGINEERING = 'electrical engineering'
    ELECTRONICS_AND_COMMUNICATION = 'electronics and communication'
    HUMANITIES_AND_SOCIAL_SCIENCE = 'humanities and social science'
    MANAGEMENT_STUDIES = 'management studies'
    MATHEMATICS = 'mathematics'
    MECHANICAL_ENGINEERING = 'mechanical engineering'
    METALLURGICAL_AND_MATERIALS_ENGINEERING = 'metallurgical and materials engineering'
    PHYSICS = 'physics'
    PHYSICAL_EDUCATION = 'physical education'
    # None for officer

class AccountComplaintType(Enum):
    DUE = "due"
    REFUND = "refund"