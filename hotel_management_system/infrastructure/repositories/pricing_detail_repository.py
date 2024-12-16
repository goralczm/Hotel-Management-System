"""Module containing pricing_detail repository implementation."""

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
    """A class representing continent DB repository."""

    async def get_all_pricing_details(self) -> Iterable[Any]:
        """The method getting all pricing_details from the data storage.

        Returns:
            Iterable[Any]: pricing_details in the data storage.
        """

        query = (
            select(pricing_details_table)
            .order_by(pricing_details_table.c.name.asc())
        )
        pricing_details = await database.fetch_all(query)

        return [PricingDetail.from_record(pricing_detail) for pricing_detail in pricing_details]

    async def get_by_id(self, pricing_detail_id: int) -> Any | None:
        """The method getting pricing_detail by provided id.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            Any | None: The pricing_detail details.
        """
        pricing_detail = await self._get_by_id(pricing_detail_id)

        return PricingDetail.from_record(pricing_detail) if pricing_detail else None

    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """The method getting accessibility_option by provided name.

        Args:
            pricing_detail_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

        query = (
            pricing_details_table.select()
            .where(pricing_details_table.c.name == pricing_detail_name)
        )

        return await database.fetch_one(query)

    async def add_pricing_detail(self, data: PricingDetailIn) -> Any | None:
        """The method adding new pricing_detail to the data storage.

        Args:
            data (pricing_detailIn): The details of the new pricing_detail.

        Returns:
            pricing_detail: Full details of the newly added pricing_detail.

        Returns:
            Any | None: The newly added pricing_detail.
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
        """The method updating pricing_detail data in the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.
            data (pricing_detailIn): The details of the updated pricing_detail.

        Returns:
            Any | None: The updated pricing_detail details.
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
        """The method updating removing pricing_detail from the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            bool: Success of the operation.
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
