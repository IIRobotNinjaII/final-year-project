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
    CHEMICALENGINEERING = 'chemical engineering'
    CHEMISTRY = 'chemistry'
    CIVILENGINEERING = 'civil engineering'
    COMPUTERSCIENCEANDENGINEERING = 'computer science and engineering'
    ELECTRICALENGINEERING = 'electrical engineering'
    ELECTRONICSANDCOMMUNICATION = 'electronics and communication'
    HUMANITIESANDSOCIALSCIENCE = 'humanities and social science'
    MANAGEMENTSTUDIES = 'management studies'
    MATHEMATICS = 'mathematics'
    MECHANICALENGINEERING = 'mechanical engineering'
    METALLURGICALANDMATERIALSENGINEERING = 'metallurgical and materials engineering'
    PHYSICS = 'physics'
    PHYSICALEDUCATION = 'physical education'
    # None for officer

class AccountComplaintType(Enum):
    DUE = "due"
    REFUND = "refund"

class ResidentialComplaintType(Enum):
    ELECTRIC = "electric"
    PLUMBING = "plumbing"
    NETWORK = "network"