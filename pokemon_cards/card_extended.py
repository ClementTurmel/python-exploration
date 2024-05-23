
from dataclasses import dataclass
from typing import Optional, List

from pokemontcgsdk import Card, Set
from pokemontcgsdk.attack import Attack

@dataclass
class CardExtented(Card):
    set: Optional[Set]
    level: Optional[str]
    set_id: Optional[str]
    attacks: Optional[List[Attack]]

    def __post_init__(self):
        self.set_id = self.id.split("-")[0]