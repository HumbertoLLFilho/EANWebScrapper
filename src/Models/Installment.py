import uuid

from Models.Card import Card
from Models.Product import Product

class Installment:
  def __init__(self, product_id, card_id, installments_quantity, installment_price, refund_porcentage, is_interest_free, card = None, product = None) -> None:
    self.id = uuid.uuid4()

    self.product_id = product_id
    self.product: Product = product
    
    self.card_id = card_id
    self.card: Card = card

    self.installments_quantity = installments_quantity
    self.installment_price = installment_price
    self.refund_porcentage = refund_porcentage

    self.is_interest_free = is_interest_free


  def to_dict(self) -> dict[str, str]:
    installment_dict = {}

    installment_dict["CODIGO DO ARTICULO"] = int(self.product_id)
    if(self.product != None):
      installment_dict["EAN DO ARTICULO"] = float(self.product.ean)
      installment_dict["DETALHE DO ARTICULO"] = self.product.detail
      installment_dict["MARCA DO ARTICULO"] = self.product.brand
      installment_dict["LINK DO ARTICULO"] = self.product.link

      if(self.product.price != ''):
        installment_dict["PRECIO"] = float(self.product.price)
      else:
        installment_dict["PRECIO"] = 0.0

      if(self.product.promotional_price != ''):
        installment_dict["PRECIO PROMOCIONAL"] = float(self.product.promotional_price)
      else:
        installment_dict["PRECIO PROMOCIONAL"] = 0.0

      installment_dict["PRECIO CON TARJETA"] = float(self.final_price())
    else:
      installment_dict["EAN DO ARTICULO"] = ""
      installment_dict["DETALHE DO ARTICULO"] = ""
      installment_dict["MARCA DO ARTICULO"] = ""
      installment_dict["LINK DO ARTICULO"] = ""

      installment_dict["PRECIO"] = ""
      installment_dict["PRECIO PROMOCIONAL"] = ""
      installment_dict["PRECIO CON TARJETA"] = ""

    installment_dict["CODIGO DA TARJETA"] = self.card_id
    if(self.card != None):
      installment_dict["CODIGO DO BANCO"] = self.card.bank_id
      
      if(self.card.bank != None):
        installment_dict["NOMBRE DEL BANCO"] = self.card.bank.name
      
      installment_dict["NOMBRE DE TARJETA"] = self.card.name
    else:
      installment_dict["CODIGO DO BANCO"] = ""
      installment_dict["NOMBRE DEL BANCO"] = ""
      installment_dict["NOMBRE DE TARJETA"] = ""
      

    installment_dict["NÚMERO DE CUOTAS"] = int(self.installments_quantity)
    installment_dict["PRECIO POR CUOTA"] = float(self.installment_price)
    installment_dict["PORCENTAJE DE REEMBOLSO"] = int(self.refund_porcentage)

    installment_dict["SIN INTERÉS"] = self.is_interest_free

    return installment_dict

  def final_price(self):
    return round(float(self.installment_price) * int(self.installments_quantity), 2)