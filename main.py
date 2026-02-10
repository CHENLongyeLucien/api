from dataclasses import dataclass, asdict
from typing import Union
import json
from fastapi import FastAPI, Path, HTTPException

with open("products.json", "r") as f:
    product_list = json.load(f)

list_product = {k+1:v for k, v in enumerate(product_list)}

@dataclass
class Product:
    id: int
    nom: str
    categorie: str
    sous_categorie: str
    prix: float
    disponibilite: bool
    description: str
    tags: list[str]
    stock: Union[int, None] = None

app = FastAPI()

@app.get("/total_products")
def get_total_products() -> dict:
    return {"total":len(list_product)}

@app.get("/products")
def get_all_products() -> list[Product]:
    temp = []
    for id in list_product:
        temp.append(Product(**list_product[id])) 
    return temp

@app.get("/products/{id}")
def get_product_id(id: int = Path(ge=1)) -> Product: 
    if id not in list_product :
        raise HTTPException(status_code=404, detail="Ce produit n'est pas disponible dans notre magasin.")
    return Product(**list_product[id])

@app.get("/nom")
def get_all_names() -> list[str]:
    temp=[]
    for product in product_list :
        for nom in product["nom"]:
            if nom not in temp:
                temp.append(nom)
    temp.sort()
    return temp

@app.post("/products/")
def create_product(product: Product) -> Product:
    if product.id in list_product:
        raise HTTPException(status_code=404, detail="Le produit {product.id} n'est pas disponible dans notre magasin.")

    list_product[product.id] = asdict(product)
    return product

@app.put("/products/{id}")
def update_product(product: Product, id: int= Path(ge=1)) -> Product:
    if id not in list_product :
        raise HTTPException(status_code=404, detail="Ce produit n'est pas disponible dans notre magasin.")
    
    list_product[id] = asdict(product)
    return product

@app.delete("/products/{id}")
def delete_product(id: int = Path(ge=1)) -> Product:
    if id in list_product:
        product=Product(**list_product[id])
        del list_product[id]
        return product
    raise HTTPException(status_code=404, detail="Ce produit n'est pas disponible dans notre magasin.")
    