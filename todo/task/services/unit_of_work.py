from __future__ import annotations
import abc


class AbstractUnitOfWork(abc.ABC):  # pragma: no cover
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


"""
The project uses the Django atomicity feature as Unit of Work. 
See https://docs.djangoproject.com/en/dev/topics/db/transactions/#controlling-transactions-explicitly

We could implement nossa UOW usando um outro ORM. Examplo usando SQLAlchemy: 

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory  #(1)

    def __enter__(self):
        self.session = self.session_factory()  # type: Session  #(2)
        self.batches = repository.SqlAlchemyRepository(self.session)  #(2)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  #(3)

    def commit(self):  #(4)
        self.session.commit()

    def rollback(self):  #(4)
        self.session.rollback()
"""


