from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    Table,
    Column
)
from sqlalchemy.orm import relationship, declarative_base, mapped_column

Base = declarative_base()


project_user = Table(
    'project_user',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    clerk_id = mapped_column(String, unique=True, index=True, nullable=False)
    username = mapped_column(String(50))
    email = mapped_column(String(150), unique=True, nullable=False)

    projects = relationship('Project', secondary=project_user, back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Project(Base):
    __tablename__ = 'projects'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(150), nullable=False)
    description = mapped_column(Text)

    users = relationship('User', secondary=project_user, back_populates='projects')

    clouds = relationship('Cloud', back_populates='project')

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"


class Cloud(Base):
    __tablename__ = 'clouds'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(150), nullable=False)
    project_id = mapped_column(Integer, ForeignKey('projects.id'), nullable=False)
    coordinate_x = mapped_column(Integer)
    coordinate_y = mapped_column(Integer)

    project = relationship('Project', back_populates='clouds')
    tasks = relationship('Task', back_populates='cloud')

    def __repr__(self):
        return f"<Cloud(id={self.id}, name={self.name})>"


class Task(Base):
    __tablename__ = 'tasks'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(150), nullable=False)
    description = mapped_column(Text)
    cloud_id = mapped_column(Integer, ForeignKey('clouds.id'), nullable=False)

    cloud = relationship('Cloud', back_populates='tasks')

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name})>"
