from dependency_injector.wiring import Provide

from hotel_management_system.src.container import Container

from hotel_management_system.src.core.services.i_accessibility_option_service import IAccessibilityOptionService


async def main(accessibility_option_service: IAccessibilityOptionService =
               Provide[Container.accessibility_option_service]):
    await accessibility_option_service.setup_accessibility_options()