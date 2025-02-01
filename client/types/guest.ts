import {AccessibilityOption} from "@/types/accessibility_option";

export interface Guest {
    first_name: string;
    last_name: string;
    address: string;
    city: string;
    country: string;
    zip_code: string;
    phone_number: string;
    email: string;
    id: number;
    accessibility_options: AccessibilityOption[];
}