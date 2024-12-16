"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.pricing_detail import PricingDetail, PricingDetailIn
from hotel_management_system.core.repositories.i_pricing_detail_repository import IPricingDetailRepository
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService


class PricingDetailService(IPricingDetailService):
    """A class implementing the pricing_detail service."""

    _repository: IPricingDetailRepository

    def __init__(self, repository: IPricingDetailRepository) -> None:
        """The initializer of the `pricing_detail service`.

        Args:
            repository (Ipricing_detailRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[PricingDetail]:
        """The method getting all pricing_details from the repository.

        Returns:
            Iterable[pricing_detailDTO]: All pricing_details.
        """

        return await self._repository.get_all_pricing_details()

    async def get_by_id(self, pricing_detail_id: int) -> PricingDetail | None:
        """The method getting pricing_detail by provided id.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            pricing_detailDTO | None: The pricing_detail details.
        """

        return await self._repository.get_by_id(pricing_detail_id)

    async def get_by_name(self, pricing_detail_name: str) -> PricingDetail | None:
        """The method getting accessibility_option by provided name.

        Args:
            pricing_detail_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

        return await self._repository.get_by_name(pricing_detail_name)

    async def add_pricing_detail(self, data: PricingDetailIn) -> PricingDetail | None:
        """The method adding new pricing_detail to the data storage.

        Args:
            data (pricing_detailIn): The details of the new pricing_detail.

        Returns:
            pricing_detail | None: Full details of the newly added pricing_detail.
        """

        return await self._repository.add_pricing_detail(data)

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

        return await self._repository.update_pricing_detail(
            pricing_detail_id=pricing_detail_id,
            data=data,
        )

    async def delete_pricing_detail(self, pricing_detail_id: int) -> bool:
        """The method updating removing pricing_detail from the data storage.

        Args:
            pricing_detail_id (int): The id of the pricing_detail.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_pricing_detail(pricing_detail_id)