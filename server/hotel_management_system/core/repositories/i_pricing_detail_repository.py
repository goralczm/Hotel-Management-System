"""
Module for managing pricing_detail repository abstractions.
"""

from abc import ABC, abstractmethod
from typing import List
from hotel_management_system.core.domains.pricing_detail import PricingDetailIn, PricingDetail


class IPricingDetailRepository(ABC):
    """
    Abstract base class defining the interface for a pricing detail repository.
    """

    @abstractmethod
    async def get_all_pricing_details(self) -> List[PricingDetail]:
        """
        Retrieve all pricing details from the data storage.

        Returns:
            List[PricingDetail]: A list of all pricing details.
        """

    @abstractmethod
    async def get_by_id(self, pricing_detail_id: int) -> PricingDetail | None:
        """
        Retrieve a pricing detail by its unique ID.

        Args:
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            PricingDetail | None: The details of the pricing detail if found, or None if not found.
        """


    @abstractmethod
    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """
        Retrieve a pricing detail by its name.

        Args:
            pricing_detail_name (str): The name of the pricing detail.

        Returns:
            PricingDetail | None: The pricing detail details if found, or None if not found.
        """

    @abstractmethod
    async def add_pricing_detail(self, data: PricingDetailIn) -> PricingDetail | None:
        """
        Add a new pricing detail to the data storage.

        Args:
            data (PricingDetailIn): The details of the new pricing detail.

        Returns:
            PricingDetail | None: The newly added pricing detail, or None if the operation fails.
        """

    @abstractmethod
    async def update_pricing_detail(self, pricing_detail_id: int, data: PricingDetailIn) -> PricingDetail | None:
        """
        Update an existing pricing detail's data in the data storage.

        Args:
            pricing_detail_id (int): The ID of the pricing detail to update.
            data (PricingDetailIn): The updated details for the pricing detail.

        Returns:
            PricingDetail | None: The updated pricing detail details, or None if the pricing detail is not found.
        """

    @abstractmethod
    async def delete_pricing_detail(self, pricing_detail_id: int) -> bool:
        """
        Remove a pricing detail from the data storage.

        Args:
            pricing_detail_id (int): The ID of the pricing detail to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
