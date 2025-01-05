"""Module containing pricing_detail repository abstractions."""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.pricing_detail import PricingDetailIn, PricingDetail


class IPricingDetailRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_pricing_details(self) -> List[PricingDetail]:
        """The abstract getting all pricing_details from the data storage.

        Returns:
            List[PricingDetail]: PricingDetails in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, pricing_detail_id: int) -> PricingDetail | None:
        """The method getting pricing_detail by provided id.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            pricing_detailDTO | None: The pricing_detail details.
        """

    @abstractmethod
    async def add_pricing_detail(self, data: PricingDetailIn) -> PricingDetail | None:
        """The abstract adding new pricing_detail to the data storage.

        Args:
            data (PricingDetailIn): The details of the new pricing_detail.

        Returns:
            PricingDetail | None: The newly added pricing_detail.
        """

    @abstractmethod
    async def update_pricing_detail(
            self,
            pricing_detail_id: int,
            data: PricingDetailIn,
    ) -> PricingDetail | None:
        """The abstract updating pricing_detail data in the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.
            data (PricingDetailIn): The details of the updated pricing_detail.

        Returns:
            PricingDetail | None: The updated pricing_detail details.
        """

    @abstractmethod
    async def delete_pricing_detail(self, pricing_detail_id: int) -> bool:
        """The abstract updating removing pricing_detail from the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """The method getting accessibility_option by provided name.

        Args:
            pricing_detail_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """