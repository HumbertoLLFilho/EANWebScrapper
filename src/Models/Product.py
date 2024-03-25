import uuid

class Product:
  def __init__(self, codigo, ean, detail, brand, link, price, promotional_price) -> None:
    self.id = codigo
    self.ean = ean
    self.detail = detail
    self.brand = brand
    self.link = link
    self.price = price
    self.promotional_price = promotional_price

  def to_dict(self) -> dict[str,str]:
    product_dict = {}

    product_dict["id"] = self.id
    product_dict["EAN"] = self.ean
    product_dict["detail"] = self.detail
    product_dict["brand"] = self.brand
    product_dict["link"] = self.link

    product_dict["price"] = self.price
    product_dict["promotional price"] = self.promotional_price
    
    return product_dict