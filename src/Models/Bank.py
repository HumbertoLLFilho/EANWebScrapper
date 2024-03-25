import uuid

class Bank:
  def __init__(self, name: str):
    self.id = uuid.uuid4()
    self.name = name

    self.cards = []

  def to_dict(self) -> dict[str,str]:
    bank_dict = {}

    bank_dict["bank id"] = self.id
    bank_dict["name"] = self.name

    return bank_dict