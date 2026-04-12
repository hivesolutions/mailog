#!/usr/bin/python
# -*- coding: utf-8 -*-

from appier_extras.parts.admin import Base


class MailogBase(Base):
    @classmethod
    def is_abstract(cls) -> bool:
        return True
