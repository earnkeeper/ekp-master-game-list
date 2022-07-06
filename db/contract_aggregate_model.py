from typing import TypedDict



class ContractAggregateModel(TypedDict):
    id: str
    updated: int
    contract_address: str
    timestamp: int
    cursor_timestamp: int
    chain: str

    active_users: int
    total_transfers: float

    total_value_usd: float

    churn_24h: int
    churn_28d: int
    new_users: int
    retained_24h: int
    retained_28d: int
