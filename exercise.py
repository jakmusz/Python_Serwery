from typing import Optional, List
from abc import ABC, abstractmethod
import re
 
class Product:
    def __init__(self, name: str, price: float):
        if not re.fullmatch("^[a-zA-Z]+\d+$",name): raise ValueError('Niepoprawna nazwa') 
        self.name = name
        self.price = price
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  
 
    def __hash__(self):
        return hash((self.name, self.price))
 
class ServerError(Exception):
    pass
 
class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
 
class Server(ABC):
    n_max_returned_entries: int = 6

    @abstractmethod
    def internal_get_entries(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError
    
    def get_entries(self, n_letters: int = 1) -> List[Product] | TooManyProductsFoundError:
        products = self.internal_get_entries(n_letters)
        #checked_products = [product.name for product in products if re.fullmatch("^[a-zA-Z]{n_letter}\d{2,3}$", product.name)]
        checked_products = []
        counter = 0
        for product in products:
            if re.fullmatch('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), product.name):
                counter += 1
                checked_products.append(product)
            if counter > Server.n_max_returned_entries:
                raise TooManyProductsFoundError
        checked_products.sort(key = lambda product: product.price) 
        return checked_products

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


class ListServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__() 
        self.products = products
    
    def internal_get_entries(self, n_letters: int = 1) -> List[Product]:
        return [product for product in self.products if re.fullmatch('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), product.name)]
    
class MapServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__()
        self.products = {product.name : product for product in products}
 
    def internal_get_entries(self, n_letters: int = 1) -> List[Product]:
        return [product for product in self.products.values() if re.fullmatch('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), product.name)]
 
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            products = self.server.get_entries(n_letters)
        except(ServerError, TypeError):
            return None
        else:
            if not products: return None
            return sum(product.price for product in products)