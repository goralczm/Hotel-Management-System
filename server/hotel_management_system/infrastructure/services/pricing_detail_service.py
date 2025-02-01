"""
Module containing pricing_detail service implementation.
"""

from typing import Iterable

from hotel_management_system.core.domains.pricing_detail import PricingDetail, PricingDetailIn
from hotel_management_system.core.repositories.i_pricing_detail_repository import IPricingDetailRepository
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService


class PricingDetailService(IPricingDetailService):
    """
    A class implementing the pricing_detail service.
    """

    _repository: IPricingDetailRepository

    def __init__(self, repository: IPricingDetailRepository) -> None:
        """
        The initializer of the `pricing_detail service`.

        Args:
            repository (IPricingDetailRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[PricingDetail]:
        """
        Retrieve all pricing details from the data storage.

        Returns:
            List[PricingDetail]: A list of all pricing details.
        """

        return await self._repository.get_all_pricing_details()

    async def get_by_id(self, pricing_detail_id: int) -> PricingDetail | None:
        """
        Retrieve a pricing detail by its unique ID.

        Args:
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            PricingDetail | None: The details of the pricing detail if found, or None if not found.
        """

        return await self._repository.get_by_id(pricing_detail_id)

    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """
        Retrieve a pricing detail by its name.

        Args:
            pricing_detail_name (str): The name of the pricing detail.

        Returns:
            PricingDetail | None: The pricing detail details if found, or None if not found.
        """

        return await self._repository.get_by_name(pricing_detail_name)

    async def add_pricing_detail(self, data: PricingDetailIn) -> PricingDetail | None:
        """
        Add a new pricing detail to the data storage.

        Args:
            data (PricingDetailIn): The details of the new pricing detail.

        Returns:
            PricingDetail | None: The newly added pricing detail, or None if the operation fails.
        """

        return await self._repository.add_pricing_detail(data)

    async def update_pricing_detail(
            self,
            pricing_detail_id: int,
            data: PricingDetailIn,
    ) -> PricingDetail | None:
        """
        Update an existing pricing detail's data in the data storage.

        Args:
            pricing_detail_id (int): The ID of the pricing detail to update.
            data (PricingDetailIn): The updated details for the pricing detail.

        Returns:
            PricingDetail | None: The updated pricing detail details, or None if the pricing detail is not found.
        """

        return await self._repository.update_pricing_detail(
            pricing_detail_id=pricing_detail_id,
            data=data,
        )

    async def delete_pricing_detail(self, pricing_detail_id: int) -> bool:
        """
        Remove a pricing detail from the data storage.

        Args:
            pricing_detail_id (int): The ID of the pricing detail to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        return await self._repository.delete_pricing_detail(pricing_detail_id)