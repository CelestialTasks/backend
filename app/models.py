from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class ProjectUser(Base):
    __tablename__ = 'project_user'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)

    user = relationship("User", back_populates="project_associations")
    project = relationship("Project", back_populates="user_associations")

    def __repr__(self):
        return f"<ProjectUser(id={self.id}, user_id={self.user_id}, project_id={self.project_id})>"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50))
    email = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp())

    owned_projects = relationship('Project', back_populates='owner')
    project_associations = relationship("ProjectUser", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship('User', back_populates='owned_projects')
    user_associations = relationship("ProjectUser", back_populates="project")
    clouds = relationship('Cloud', back_populates='project')

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"


class Cloud(Base):
    __tablename__ = 'clouds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    coordinate_x = Column(Integer)
    coordinate_y = Column(Integer)

    project = relationship('Project', back_populates='clouds')
    tasks = relationship('Task', back_populates='cloud')

    def __repr__(self):
        return f"<Cloud(id={self.id}, name={self.name})>"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    cloud_id = Column(Integer, ForeignKey('clouds.id'), nullable=False)

    cloud = relationship('Cloud', back_populates='tasks')

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name})>"
