from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Мushrooms API",
    description="API для работы с грибами и корзинками",
    version="1.1"
)

# разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========= Модели

# Модель Гриба
class Mushroom(BaseModel):
    id: int
    name: str            # название 
    edible: bool         # съедобность (True – съедобный, False – не съедобный)
    weight: float        # вес в граммах
    freshness: str       # описание свежести ("свежий", "застарелый")


# корзина
class BasketCreate(BaseModel):
    id: int
    owner: str           # кому принадлежит корзинка 
    capacity: float      # вместительность в граммах

# Модель корзинки, хранящей список грибов (храним id грибов)
class Basket(BaseModel):
    id: int
    owner: str
    capacity: float
    mushrooms: List[int] = []  # список id грибов, находящихся в корзинке



# Модель корзинки, хранящей список грибов (храним id грибов)
class BasketDetail(BaseModel):
    id: int
    owner: str
    capacity: float
    mushrooms: List[Mushroom] = []  # список id грибов, находящихся в корзинке


# Модель для добавления гриба в корзинку (требуется указать id гриба)
class AddMushroomToBasket(BaseModel):
    mushroom_id: int



# ========= Хранение данных в памяти
# ключ = id
mushrooms_db = {} 
baskets_db = {}





# ========= Методы для работы с грибами

@app.post("/mushrooms", response_model=Mushroom)
def create_mushroom(mushroom: Mushroom):
    if mushroom.id in mushrooms_db:
        raise HTTPException(status_code=400, detail="Гриб с таким id уже существует в БД.")
    else:
        mushrooms_db[mushroom.id] = mushroom
        return mushroom


@app.put("/mushrooms/{mushroom_id}", response_model=Mushroom)
def update_mushroom(mushroom_id: int, updated_data: Mushroom):
    if mushroom_id not in mushrooms_db:
        raise HTTPException(status_code=404, detail="Гриб не найден.")
    else:
        mushrooms_db[mushroom_id] = updated_data
        return updated_data



@app.get("/get_mushrooms/{mushroom_id}", response_model=Mushroom)
def get_mushroom(mushroom_id: int):
    if mushroom_id not in mushrooms_db:
        raise HTTPException(status_code=404, detail="Гриб не найден.")
    else:
        return mushrooms_db[mushroom_id]




# ========= Методы для работы с корзинками

@app.post("/baskets", response_model=Basket)
def create_basket(basket: BasketCreate):
    if basket.id in baskets_db:
        raise HTTPException(status_code=400, detail="Корзинка с таким id уже существует.")
    else:
        # При создании корзинки список грибов изначально пуст
        new_basket = Basket(**basket.dict(), mushrooms=[])
        baskets_db[basket.id] = new_basket
        return new_basket


@app.post("/baskets/{basket_id}/mushrooms", response_model=Basket)
def add_mushroom_to_basket(basket_id: int, data: AddMushroomToBasket):
    if data.mushroom_id not in mushrooms_db:
        raise HTTPException(status_code=404, detail="Гриб не найден.")
    
    elif basket_id not in baskets_db:
        raise HTTPException(status_code=404, detail="Корзинка не найдена.")
    else:
        basket = baskets_db[basket_id]

        # Дополнительная логика: проверяем, не превышен ли лимит вместительности.
        # Вычисляем суммарный вес уже добавленных грибов:
        current_weight = sum(mushrooms_db[mid].weight for mid in basket.mushrooms if mid in mushrooms_db) #Проверка , сколько граммов сейчас в корзине
        new_mushroom_weight = mushrooms_db[data.mushroom_id].weight

        if current_weight + new_mushroom_weight > basket.capacity:
            raise HTTPException(status_code=400, detail="Превышена вместительность корзинки.")

        # Спорный момент! - может ли быть в корзине 2 одинаковых гриба? - сделал чтоб можно было, но код снизу исключает одинаковые грибы
         
        # elif data.mushroom_id in basket.mushrooms:
        #     raise HTTPException(status_code=400, detail="Гриб уже находится в корзинке.")
        

        else:
            basket.mushrooms.append(data.mushroom_id)
            return basket


@app.delete("/baskets/{basket_id}/mushrooms/{mushroom_id}", response_model=Basket)
def remove_mushroom_from_basket(basket_id: int, mushroom_id: int):
    if basket_id not in baskets_db:
        raise HTTPException(status_code=404, detail="Корзинка не найдена.")
    
    else:
        basket = baskets_db[basket_id]
        if mushroom_id not in basket.mushrooms:
            raise HTTPException(status_code=404, detail="Гриб отсутствует в корзинке.")
        else:
            basket.mushrooms.remove(mushroom_id)
            return basket


@app.get("/baskets/{basket_id}", response_model=BasketDetail)
def get_basket(basket_id: int):
    if basket_id not in baskets_db:
        raise HTTPException(status_code=404, detail="Корзинка не найдена.")
    
    basket = baskets_db[basket_id]
    # Получаем подробную информацию по каждому грибу, который находится в корзинке.
    detailed_mushrooms = [mushrooms_db[mid] for mid in basket.mushrooms if mid in mushrooms_db]
    return BasketDetail(
        id=basket.id,
        owner=basket.owner,
        capacity=basket.capacity,
        mushrooms=detailed_mushrooms
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="57.129.138.22", port=1001, workers=2, reload=False) 
    # reload=False поставил для того, чтобы при работе с файлом request не перезагружалось приложение