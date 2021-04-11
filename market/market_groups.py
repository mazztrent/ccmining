from typing import List, Optional
from pydantic import BaseModel
import yaml

class MarketGroup(BaseModel):
    id: int
    parent_group_id : Optional[int]
    name: str
    description: Optional[str]
    icon_id: Optional[int]


class MarketGroupService:

    def __init__(self, sde_path: str):
        self._sde_path = sde_path
        self._init_market_groups()


    def _parse_description(self, d: dict):
        desc = d.get('descriptionID', None)
        if desc is None: 
            return None
        return desc['en']


    def _init_market_groups(self):
        with open(self._sde_path + '/fsd/marketGroups.yaml', mode="r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            models = [MarketGroup(id=i, 
                    name=data[i]['nameID']['en'], 
                    description= self._parse_description(data[i]), 
                    icon_id=data[i].get('iconID', None), 
                    parent_group_id=data[i].get('parentGroupID', None)
            ) for i in data]
        
        self.market_groups_by_name = {m.name: m for m in models}
        self.market_groups_by_id = {m.id: m for m in models}

