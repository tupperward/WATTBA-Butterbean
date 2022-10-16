from enum import unique
from tabnanny import check
from sqlalchemy import CheckConstraint, DefaultClause, create_engine, String, Integer, Table,Column, MetaData
from sqlalchemy.orm import Session

engine = create_engine('sqlite+pysqlite:///db/butterbean.db', echo=True, future=True)
meta = MetaData()

# Transliterated from @JinxedFeline's work at https://gist.github.com/jinxedfeline/fc2e2aa25471d3ade5527bbdf6ad77d9
# Create table permissions 
permissions = Table(
  'permissions', meta,
  Column('user', String, unique=True, nullable=True, default=None), # A user name, Tupperward#5115 for example. One entry per user.
  Column('role', String, unique=True, nullable=True, default=None), # A role name, she/her for example. One entry per role.
  # -- We use Integer because Sqlite does not know Booleans and represents it with 1 and 0.
  Column('manage_memes', Integer, default=0), # User may add/remove memes
  Column('assign_roles', Integer, default=0), # User may add/remove roles on users
  Column('bot_admin', Integer, default=0), # Has admin bot permissions. Probably should not guarantee right to assign roles.
  # -- This role is not assignable by users on themselves
  Column('is_user_settable', Integer, nullable=False, default=0),
  # Ensure this is only set on roles
  CheckConstraint('(("is_user_settable" == 1) AND ("role" IS NOT NULL)) OR ("is_user_settable" == 0)', name='is_user_settable requires a role'),
  # This role can be set on users by someone with the assign_roles permission
  # Note that this will not override permissions on the discord side, the bot is bound by which roles it as permissions to assign there 
  Column('is_assignable', Integer, nullable=False, default=0),
  # Ensure this is only set on roles
  CheckConstraint('(("is_assignable" == 1) AND ("role" IS NOT NULL)) OR ("is_assignable" == 0)',name='is_assignable_requires_a_role'),
  CheckConstraint('(("user" IS NOT NULL) AND ("role" IS NULL)) OR(("user" IS NULL) AND ("role" IS NOT NULL))',name='provide only one of: user or role'),
)

meta.create_all(engine)

