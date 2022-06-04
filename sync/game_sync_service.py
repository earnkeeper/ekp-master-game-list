import asyncio
import logging
from ekp_sdk.services import TransactionSyncService, EtherscanService, CoingeckoService
from datetime import datetime



class GameSyncService:
    def __init__(
        self,
        coingecko_service: CoingeckoService,
        etherscan_service: EtherscanService,
        transaction_sync_service: TransactionSyncService,
    ):
        self.coingecko_service = coingecko_service
        self.etherscan_service = etherscan_service
        self.transaction_sync_service = transaction_sync_service

    async def sync_games(self):

        start_time = int(datetime.now().timestamp() - (7 * 1440 * 60))

        start_block = await self.etherscan_service.get_block_number_by_timestamp(start_time)

        contract_addresses = self.game_config_repo.get_all_bsc_addresses()

        coingecko_games = await self.coingecko_service.get_coin_markets(
            per_page=100,
            category="gaming"
        )

        coin_address_map = await self.coingecko_service.get_coin_address_map("binance-smart-chain")

        for coin in coingecko_games:
            coin_id = coin["id"]

            if coin_id not in coin_address_map:
                logging.warn(f"Skipping game {coin['name']}, no bsc address")
                continue

            address = coin_address_map[coin_id]

            if address not in contract_addresses:
                contract_addresses.append(address)

        futures = []

        for address in contract_addresses:
            futures.append(
                self.transaction_sync_service.sync_transactions(
                    address,
                    start_block
                )
            )

        await asyncio.gather(*futures)

        await self.activity_decoder_service.decode()
