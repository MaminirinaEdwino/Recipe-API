from fastapi import APIRouter,Depends, HTTPException 
from security import *
from recipe.model import recipe, recipe_create, recipe_update 
from db import get_db
from requests import Session

recipe_router = APIRouter(prefix="/recipe", tags=['recipe'], dependencies=[Depends(get_current_active_user)])


@recipe_router.get("/")
async def get_all_recipe(db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).all()	
	return db_recipe

@recipe_router.get("/{id}")
async def get_recipe_by_id(id: int, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.id == id).first()
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	return db_recipe

@recipe_router.post("/")
async def create_recipe(recipe_post: recipe_create, db: Session = Depends(get_db)):
	db_recipe = recipe(**recipe_post.model_dump())
	db.add(db_recipe)
	db.commit()
	db.refresh(db_recipe)
	return db_recipe

@recipe_router.put("/{id}")
async def update_recipe(id: int, recipe_put: recipe_update, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.id == id).first()
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	for key, value in recipe_update.model_dump().items():
		if value is not None:
			setattr(recipe, key, value)
	db.commit()
	db.refresh(db_recipe)
	return db_recipe

@recipe_router.delete("/{id}")
async def delete_recipe(id: int, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.id == id).first()
	if not recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	db.delete(db_recipe)
	db.commit()
	return {"message": "recipe deleted successfully"}

@recipe_router.get("/{name}")
async def get_recipe_by_name(name: str, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.name == name).all()	
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	return db_recipe

@recipe_router.get("/{preparation}")
async def get_recipe_by_preparation(preparation: str, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.preparation == preparation).all()	
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	return db_recipe

@recipe_router.get("/{ingredients}")
async def get_recipe_by_ingredients(ingredients: str, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.ingredients == ingredients).all()	
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	return db_recipe

@recipe_router.get("/{cooking_time}")
async def get_recipe_by_cooking_time(cooking_time: str, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.cooking_time == cooking_time).all()	
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	return db_recipe

@recipe_router.get("/{difficulty}")
async def get_recipe_by_difficulty(difficulty: str, db: Session = Depends(get_db)):
	db_recipe = db.query(recipe).filter(recipe.difficulty == difficulty).all()	
	if not db_recipe:
		raise HTTPException(status_code=404, detail="recipe not found")
	return db_recipe
