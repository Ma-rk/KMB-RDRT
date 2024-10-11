from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.Base import Base


class RequestLog(Base):
    __tablename__ = 'RequestLog'
    seq: Mapped[int] = mapped_column(primary_key=True)
    x_forwarded_for: Mapped[str] = mapped_column(String(255), name="X-Forwarded-For")
    x_forwarded_proto: Mapped[str] = mapped_column(String(255), name="X-Forwarded-Proto")
    x_forwarded_port: Mapped[str] = mapped_column(String(10), name="X-Forwarded-Port")
    host: Mapped[str] = mapped_column(String(255), name="Host")
    x_amzn_trace_id: Mapped[str] = mapped_column(String(255), name="X-Amzn-Trace-Id")
    upgrade_insecure_requests: Mapped[str] = mapped_column(String(5), name="Upgrade-Insecure-Requests")
    user_agent: Mapped[str] = mapped_column(String(1024), name="User-Agent")
    accept: Mapped[str] = mapped_column(String(1024), name="Accept")
    accept_encoding: Mapped[str] = mapped_column(String(255), name="Accept-Encoding")
    accept_language: Mapped[str] = mapped_column(String(255), name="Accept-Language")

    def __init__(self, headers):
        super().__init__()
        self.x_forwarded_for = headers.get('X-Forwarded-For')
        self.x_forwarded_proto = headers.get('X-Forwarded-Proto')
        self.x_forwarded_port = headers.get('X-Forwarded-Port')
        self.host = headers.get('Host')
        self.x_amzn_trace_id = headers.get('X-Amzn-Trace-Id')
        self.upgrade_insecure_requests = headers.get('Upgrade-Insecure-Requests')
        self.user_agent = headers.get('User-Agent')
        self.accept = headers.get('Accept')
        self.accept_encoding = headers.get('Accept-Encoding')
        self.accept_language = headers.get('Accept-Language')

    def __repr__(self) -> str:
        return (
            f"<RequestLog(id={self.seq}, "
            f"x_forwarded_for={self.x_forwarded_for}, "
            f"x_forwarded_proto={self.x_forwarded_proto}, "
            f"x_forwarded_port={self.x_forwarded_port}, "
            f"host={self.host}, "
            f"x_amzn_trace_id={self.x_amzn_trace_id}, "
            f"upgrade_insecure_requests={self.upgrade_insecure_requests}, "
            f"user_agent={self.user_agent}, "
            f"accept={self.accept}, "
            f"accept_encoding={self.accept_encoding}, "
            f"accept_language={self.accept_language})>"
        )
