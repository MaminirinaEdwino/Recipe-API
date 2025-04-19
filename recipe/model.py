#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional
from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean
	
class recipe_create(BaseModel):

	name: str
	preparation: str
	ingredients: list
	cooking_time: int
	difficulty: str


class recipe_update(BaseModel):

	name: Optional[str] = None
	preparation: Optional[str] = None
	ingredients: Optional[list] = None
	cooking_time: Optional[int] = None
	difficulty: Optional[str] = None


class recipe(Base):

	__tablename__ = 'recipe'

	id = Column(Integer, primary_key=True, index=True)

	name= Column(String(255), nullable= False)
	preparation= Column(String(255), nullable= False)
	ingredients= Column(JSON, nullable= False)
	cooking_time= Column(Integer, nullable= False)
	difficulty= Column(String(255), nullable= False)
