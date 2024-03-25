from Models.Bank import Bank
import uuid

class Card:
  def __init__(self, bank_id, name, bank = None) -> None:
    self.id = uuid.uuid4()
    self.bank_id = bank_id
    self.bank: Bank = bank

    self.name = name

  def to_dict(self) -> dict[str,str]:
    card_dict: dict[str,str] = {}

    card_dict["card ID"] = self.id
    card_dict["bank ID"] = self.bank_id
    card_dict["name"] = self.name

    return card_dict