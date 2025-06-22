from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"
    ), nullable=False)

    user = relationship("User")

# sqlalchemy doesn't help in modifiying the table
""" So once the table is created it is not going to update any change we do in table 

ex:-
    suppose in pulbished column we haven't added server_default="TRUE" initially and once after running the server 

    ## models.Base.metadata.create_all(bind=engine)

    This line will create the server and after that if we add the server_default="TRUE", then there will be no change in the table and do make change we need to delete the table and only after that changes will be shown there.

    "" Even if we add a new column it will not shown there. ""

"""

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
