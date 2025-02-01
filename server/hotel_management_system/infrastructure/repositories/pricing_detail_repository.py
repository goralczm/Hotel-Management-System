"""
Module containing pricing_detail repository implementation.
"""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_pricing_detail_repository import IPricingDetailRepository
from hotel_management_system.core.domains.pricing_detail import PricingDetail, PricingDetailIn
from hotel_management_system.db import (
    pricing_details_table,
    database,
)


class PricingDetailRepository(IPricingDetailRepository):
    """
    A class representing pricing_detail DB repository.
    """

    async def get_all_pricing_details(self) -> Iterable[Any]:
        """
        Retrieve all pricing details from the data storage.

        Returns:
            List[PricingDetail]: A list of all pricing details.
        """

        query = (
            select(pricing_details_table)
            .order_by(pricing_details_table.c.name.asc())
        )
        pricing_details = await database.fetch_all(query)

        return [PricingDetail.from_record(pricing_detail) for pricing_detail in pricing_details]

    async def get_by_id(self, pricing_detail_id: int) -> Any | None:
        """
        Retrieve a pricing detail by its unique ID.

        Args:
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            PricingDetail | None: The details of the pricing detail if found, or None if not found.
        """

        pricing_detail = await self._get_by_id(pricing_detail_id)

        return PricingDetail.from_record(pricing_detail) if pricing_detail else None

    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """
        Retrieve a pricing detail by its name.

        Args:
            pricing_detail_name (str): The name of the pricing detail.

        Returns:
            PricingDetail | None: The pricing detail details if found, or None if not found.
        """

        query = (
            pricing_details_table.select()
            .where(pricing_details_table.c.name == pricing_detail_name)
        )

        return await database.fetch_one(query)

    async def add_pricing_detail(self, data: PricingDetailIn) -> Any | None:
        """
        Add a new pricing detail to the data storage.

        Args:
            data (PricingDetailIn): The details of the new pricing detail.

        Returns:
            PricingDetail | None: The newly added pricing detail, or None if the operation fails.
        """

        query = pricing_details_table.insert().values(**data.model_dump())
        new_pricing_detail_id = await database.execute(query)
        new_pricing_detail = await self._get_by_id(new_pricing_detail_id)

        return PricingDetail(**dict(new_pricing_detail)) if new_pricing_detail else None

    async def update_pricing_detail(
            self,
            pricing_detail_id: int,
            data: PricingDetailIn,
    ) -> Any | None:
        """
        Update an existing pricing detail's data in the data storage.

        Args:
            pricing_detail_id (int): The ID of the pricing detail to update.
            data (PricingDetailIn): The updated details for the pricing detail.

        Returns:
            PricingDetail | None: The updated pricing detail details, or None if the pricing detail is not found.
        """

        if self._get_by_id(pricing_detail_id):
            query = (
                pricing_details_table.update()
                .where(pricing_details_table.c.id == pricing_detail_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            pricing_detail = await self._get_by_id(pricing_detail_id)

            return PricingDetail(**dict(pricing_detail)) if pricing_detail else None

        return None

    async def delete_pricing_detail(self, pricing_detail_id: int) -> bool:
        """
        Remove a pricing detail from the data storage.

        Args:
            pricing_detail_id (int): The ID of the pricing detail to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        if self._get_by_id(pricing_detail_id):
            query = pricing_details_table \
                .delete() \
                .where(pricing_details_table.c.id == pricing_detail_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, pricing_detail_id: int) -> Record | None:
        """A private method getting pricing_detail from the DB based on its ID.

        Args:
            pricing_detail_id (int): The ID of the pricing_detail.

        Returns:
            Any | None: pricing_detail record if exists.
        """

        query = (
            pricing_details_table.select()
            .where(pricing_details_table.c.id == pricing_detail_id)
        )

        return await database.fetch_one(query)
