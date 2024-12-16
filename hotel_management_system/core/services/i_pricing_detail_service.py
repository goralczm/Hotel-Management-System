"""Module containing pricing_detail service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from hotel_management_system.core.domains.pricing_detail import PricingDetail, PricingDetailIn


class IPricingDetailService(ABC):
    """A class representing pricing_detail repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[PricingDetail]:
        """The method getting all pricing_details from the repository.

        Returns:
            Iterable[pricing_detailDTO]: All pricing_details.
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
    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """The method getting accessibility_option by provided name.

        Args:
            pricing_detail_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

    @abstractmethod
    async def add_pricing_detail(self, data: PricingDetailIn) -> PricingDetail | None:
        """The method adding new pricing_detail to the data storage.

        Args:
            data (pricing_detailIn): The details of the new pricing_detail.

        Returns:
            pricing_detail | None: Full details of the newly added pricing_detail.
        """

    @abstractmethod
    async def update_pricing_detail(
            self,
            pricing_detail_id: int,
            data: PricingDetailIn,
    ) -> PricingDetail | None:
        """The method updating pricing_detail data in the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.
            data (pricing_detailIn): The details of the updated pricing_detail.

        Returns:
            pricing_detail | None: The updated pricing_detail details.
        """

    @abstractmethod
    async def delete_pricing_detail(self, pricing_detail_id: int) -> bool:
        """The method updating removing pricing_detail from the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            bool: Success of the operation.
        """