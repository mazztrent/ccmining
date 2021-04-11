from typing import Optional
from dependency_injector import containers, providers
from sde.TypesService import TypesService
from market.market_groups import MarketGroupService, MarketGroup
from fastapi import FastAPI, Depends

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    types_service = providers.Singleton(TypesService, sde_path=config.sde.sde_path)
    market_groups = providers.Singleton(MarketGroupService, sde_path=config.sde.sde_path)


def create_container() -> Container:
    container = Container()
    container.config.from_ini('config.ini', required=True)
    return container

app = FastAPI()
container = create_container()

@app.get("/marketGroupByName", tags=['Market'])
def get_market_groups(name: str) -> Optional[MarketGroup]:
    return container.market_groups().market_groups_by_name.get(name, None)


