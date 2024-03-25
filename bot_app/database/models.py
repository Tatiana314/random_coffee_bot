from typing import List, Optional

# from asyncpg import DatabaseDroppedError
from sqlalchemy.orm.session import make_transient
from sqlalchemy import (Boolean, Integer, String, select)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


USER = ('{name} '
        '{last_name}\n'
        '{email}\n'
        '{is_active}'
        '{is_admin}\n')


class Base(DeclarativeBase):
    """Base model."""
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class User(Base):
    """User model."""
    tg_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_sent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def __repr__(self):
        is_admin_text = ', админ' if self.is_admin else ''
        is_active_text = 'активен' if self.is_active else 'неактивен'
        return USER.format(
            id=self.id,
            name=self.name,
            last_name=self.last_name,
            email=self.email,
            is_active=is_active_text,
            tg_id=self.tg_id,
            is_admin=is_admin_text,
        )

    @staticmethod
    async def create(session: AsyncSession, data: dict):
        """Create an object."""
        session.add(User(**data))
        await session.commit()

    @staticmethod
    async def remove(session: AsyncSession, db_obj):
        """Delete object."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def get(session: AsyncSession, tg_id: int):
        """Getting an object by tg_id."""
        db_obj = await session.execute(select(User).where(User.tg_id == tg_id))
        return db_obj.scalars().one_or_none()

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str):
        """Receiving an object by email."""
        db_obj = await session.execute(select(User).where(User.email == email))
        return db_obj.scalars().one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession):
        """Retrieving all objects."""
        users = await session.execute(select(User))
        return users.scalars().all()

    @staticmethod
    async def activate_deactivate_user(session: AsyncSession, email: str):
        """Activate/deactivate an object."""
        result = await session.execute(
            select(User).filter(User.email == email)
        )
        obj = result.scalars().one_or_none()
        if obj:
            obj.is_active = not obj.is_active
            await session.commit()
            return True
        return False

    @staticmethod
    async def get_all_activated(session: AsyncSession):
        """Retrieving all active objects."""
        result = await session.execute(
            select(User).filter(User.is_active == 1)
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_is_sent(session: AsyncSession):
        """Receiving all objects to whom the mailing was sent."""
        result = await session.execute(select(User).filter(User.is_sent == 1))
        return result.scalars().all()

    @staticmethod
    async def first_to_end_db(user, session: AsyncSession):
        await User.remove(session, user)
        user.id = None
        session.expunge(user)
        make_transient(user)
        session.add(user)
        await session.commit()

    @staticmethod
    async def set_is_sent_status_true(users: List, session: AsyncSession):
        if len(users) > 0:
            for sent in users:
                sent.is_sent = True if not sent.is_sent else sent.is_sent
            await session.commit()

    @staticmethod
    async def set_is_sent_status_false(
        users: Optional[List],
        session: AsyncSession
    ):
        if users is not None:
            for sent in users:
                sent.is_sent = False
            await session.commit()
