from typing import Optional, List
from abc import ABC, abstractmethod
import re
 
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        if not re.fullmatch("^[a-zA-Z]+\d+$",name): raise ValueError('Niepoprawna nazwa') #sprawdz czy dobry pattern
        self.name = name
        self.price = price
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  
 
    def __hash__(self):
        return hash((self.name, self.price))
 
 
class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
 
class Server(ABC):
    n_max_returned_entries: int = 6

    @abstractmethod
    def internal_get_entries(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError
    
    def get_entries(self, n_letter: int = 1) -> List[Product] | TooManyProductsFoundError:
        products = self.internal_get_entries(n_letter)
        #checked_products = [product.name for product in products if re.fullmatch("^[a-zA-Z]{n_letter}\d{2,3}$", product.name)]
        checked_products = []
        counter = 0
        for product in products:
            if re.fullmatch("^[a-zA-Z]{n_letter}\d{2,3}$", product.name):
                counter += 1
                checked_products.append(product.name)
            if counter > Server.n_max_returned_entries:
                raise TooManyProductsFoundError
        checked_products.sort(key = lambda product: product.price) #czy zadziala na pustej liscie
        return checked_products

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


class ListServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__() #czy Server.init? czy wgl potrzebne?
        self.products = products
    
    def internal_get_entries(self, n_letters: int = 1) -> List[Product]:
        
 
class MapServer:
    def __init__(self, products: List[Product]):
        super().__init__()
        self.products = {product.name : product for product in products}
 
 
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
 
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()