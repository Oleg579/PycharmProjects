from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор должности"
    )
    title = Column(
        String(100),  # Лучше указать максимальную длину
        unique=True,
        nullable=False,
        comment="Название должности"
    )

    # Связь один-ко-многим с сотрудниками
    employees = relationship("Employee", back_populates="position")

    def __repr__(self):
        return f"<Position(id={self.id}, title='{self.title}')>"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор сотрудника"
    )
    full_name = Column(
        String(150),  # Рекомендуется указывать длину для строк
        nullable=False,
        comment="Полное ФИО сотрудника"
    )
    position_id = Column(
        Integer,
        ForeignKey("positions.id", ondelete="CASCADE"),
        nullable=False,
        comment="Ссылка на должность"
    )

    # Связь многие-к-одному с должностью
    position = relationship("Position", back_populates="employees")

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.full_name}', position_id={self.position_id})>"