from sqlalchemy import (
    mapped_column,
    Integer,
    String,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(50))
    email = mapped_column(String(150), unique=True, nullable=False)

    project_associations = relationship('ProjectUser', back_populates='user')
    projects = relationship('Project', secondary='project_user', back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class ProjectUser(Base):
    __tablename__ = 'project_user'

    user_id = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey('projects.id'), primary_key=True)

    user = relationship("User", back_populates="project_associations")
    project = relationship("Project", back_populates="user_associations")

    def __repr__(self):
        return f"<ProjectUser(user_id={self.user_id}, project_id={self.project_id})>"


class Project(Base):
    __tablename__ = 'projects'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(150), nullable=False)
    description = mapped_column(Text)

    user_associations = relationship('ProjectUser', back_populates='project')
    users = relationship('User', secondary='project_user', back_populates='projects')

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
