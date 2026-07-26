from sqlalchemy import Column, Integer, String
from bot.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)

    # FREE или PRO
    tariff = Column(String, default="FREE")

    def is_pro(self):
        return self.tariff == "PRO"