from sqlalchemy import String, Integer, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(model_class=Base)

class School(db.Model):
    """Models a school"""
    __tablename__ = "school"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    students: Mapped[list[Student]] = relationship(back_populates="school")

class Student(db.Model):
    """Models a student"""
    __tablename__ = "student"
    
    id: Mapped[str] = mapped_column(String(9), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"), nullable=False)
    
    school: Mapped[School] = relationship(back_populates="students")

    @hybrid_property
    def full_name(self) -> str:
        """Generates full name for a student"""
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    def full_name(cls):
        """Translates full_name logic into SQL"""
        return cls.first_name + " " + cls.last_name
