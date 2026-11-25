# Schemas imported by 05_meta_prompting.py as TOOLS.
# That lesson pastes this list into the prompt that writes a routine, and passes
# the same list as tools= so the agent can request these names.
# Each entry is what the model sees: a name, a description, and parameters. Nothing here runs.
# Some names are lookups: the eval answers and the conversation continues. Each of those says how.
# Any other name is a graded final action: the eval stops and compares the arguments to the row.
# The conversion prompt also requires a routine to end by calling case_resolution.
TOOLS = [
    # Lookup. The eval answers with the string True and keeps going.
    # The model is asked for booking_reference, full_name, and flight_number.
    {
        "type": "function",
        "function": {
            "name": "verify_identity",
            "description": "Verifies the customer's identity using booking reference, full name, and flight number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    },
                    "full_name": {
                        "type": "string",
                        "description": "Customer's full name."
                    },
                    "flight_number": {
                        "type": "string",
                        "description": "Flight number."
                    }
                },
                "required": ["booking_reference", "full_name", "flight_number"],
                "additionalProperties": False
            }
        }
    },
    # Lookup. The eval speaks the prompt argument to the customer and keeps going.
    # It does not send a tool result for this name.
    {
        "type": "function",
        "function": {
            "name": "ask_clarification",
            "description": "Prompts the customer for clarification on their request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to ask the customer."
                    }
                },
                "required": ["prompt"],
                "additionalProperties": False
            }
        }
    },
    # Lookup. The eval answers with the row's ticket type and fare rules, then continues.
    {
        "type": "function",
        "function": {
            "name": "check_ticket_type",
            "description": "Retrieves the type of ticket (non-refundable, refundable, flexible) based on the booking reference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    }
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action. The eval stops and scores this name plus booking_reference.
    {
        "type": "function",
        "function": {
            "name": "process_full_refund",
            "description": "Processes a full refund to the original payment method.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    }
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Lookup. The eval answers with the row's ticket type and fare rules, and continues.
    # When the fare is partial_refund, that answer also includes the refund amount.
    {
        "type": "function",
        "function": {
            "name": "check_fare_rules",
            "description": "Retrieves specific fare rules to determine applicable refund amounts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    }
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and refund_amount.
    {
        "type": "function",
        "function": {
            "name": "process_partial_refund",
            "description": "Processes a partial refund based on fare rules.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    },
                    "refund_amount": {
                        "type": "number",
                        "description": "The amount to refund."
                    }
                },
                "required": ["booking_reference", "refund_amount"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "offer_flight_credit",
            "description": "Offers flight credit for future use, subject to an administration fee.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    }
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "rebook_without_fee",
            "description": "Rebooks the customer on the next available flight without additional charges.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    }
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "offer_accommodation",
            "description": "Offers hotel accommodation to the customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {
                        "type": "string",
                        "description": "Customer's booking reference."
                    }
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # booking_reference is required. new_flight is described to the model and is not required.
    {
        "type": "function",
        "function": {
            "name": "process_change_no_fee",
            "description": "Processes flight rebooking without any fees, subject to availability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "new_flight": {"type": "string", "description": "Flight code for the new flight."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "apply_change_fee",
            "description": "Applies necessary change fees and any fare differences after rebooking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "apply_lesser_change_fee",
            "description": "Applies a lesser or no change fee based on ticket type for changes beyond 7 days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Lookup. The eval answers with a fixed next flight, FR9876 at 5:00 PM tomorrow, and continues.
    {
        "type": "function",
        "function": {
            "name": "provide_alternative_options",
            "description": "Provides alternative flight options to the customer upon request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Functions related to rebooking
    # Lookup. The eval answers with a fixed next flight, LMG091 at 10:00 AM tomorrow, and continues.
    {
        "type": "function",
        "function": {
            "name": "check_next_available_flight",
            "description": "Retrieves the next available flight operated by our airline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. The model must send flight_details.
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "description": "Books the customer on the specified flight. New flights only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_details": {"type": "string", "description": "Details of the flight to book."}
                },
                "required": ["flight_details"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "check_interline_partners",
            "description": "Checks interline partners for alternative flight connections.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. The model must send interline_flight.
    {
        "type": "function",
        "function": {
            "name": "book_interline_flight",
            "description": "Books the customer on an interline partner's flight.",
            "parameters": {
                "type": "object",
                "properties": {
                    "interline_flight": {"type": "string", "description": "Details of the interline partner flight."}
                },
                "required": ["interline_flight"],
                "additionalProperties": False
            }
        }
    },
    # Functions related to refunds and compensation
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "determine_refund_method",
            "description": "Determines whether to refund to the original payment method or offer travel credits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and original_payment_method.
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Processes the refund to the original payment method.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "original_payment_method": {"type": "string", "description": "Original payment method used."}
                },
                "required": ["booking_reference", "original_payment_method"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and bonus_percentage.
    {
        "type": "function",
        "function": {
            "name": "apply_travel_credit",
            "description": "Applies travel credits to the customer's account with a bonus percentage incentive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "bonus_percentage": {"type": "number", "description": "Bonus percentage to apply to the travel credit."}
                },
                "required": ["booking_reference", "bonus_percentage"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "check_compensation_eligibility",
            "description": "Determines the customer's eligibility for compensation based on various factors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Functions for special circumstances
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and medical_certificate.
    {
        "type": "function",
        "function": {
            "name": "process_flexible_cancellation",
            "description": "Processes full cancellation or flight credit without fees upon receiving a medical certificate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "medical_certificate": {"type": "string", "description": "Medical certificate provided by the customer."}
                },
                "required": ["booking_reference", "medical_certificate"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and documentation.
    {
        "type": "function",
        "function": {
            "name": "waive_change_fees",
            "description": "Waives change fees due to medical emergencies or military orders.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "documentation": {"type": "string", "description": "Relevant documentation provided by the customer."}
                },
                "required": ["booking_reference", "documentation"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and bereavement_documentation.
    {
        "type": "function",
        "function": {
            "name": "apply_bereavement_flexibility",
            "description": "Offers flexibility on cancellations or changes for bereavement cases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "bereavement_documentation": {"type": "string", "description": "Bereavement documentation provided by the customer."}
                },
                "required": ["booking_reference", "bereavement_documentation"],
                "additionalProperties": False
            }
        }
    },
    # Functions for group bookings
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "process_partial_group_cancellation",
            "description": "Allows individual cancellations within a group booking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Group booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "permit_name_change",
            "description": "Permits one name change per passenger at no additional cost if made 7+ days before departure.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Booking reference."},
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Functions for unaccompanied minors
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "arrange_supervision",
            "description": "Ensures proper supervision is arranged for flight changes involving unaccompanied minors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Booking reference of the unaccompanied minor."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "prioritize_minors_rebooking",
            "description": "Prioritizes rebooking for unaccompanied minors on the next available flight.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Booking reference of the unaccompanied minor."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Functions for handling FAQs
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "prioritize_missed_connections",
            "description": "Rebooks customers on missed connections caused by airline delays without additional fees.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "offer_available_upgrades",
            "description": "Offers available upgrades based on fare class availability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund.
    # The model must send booking_reference and new_destination.
    {
        "type": "function",
        "function": {
            "name": "process_destination_change",
            "description": "Allows changes to a different destination, applying any fare differences and change fees.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "new_destination": {"type": "string", "description": "New destination requested by the customer."}
                },
                "required": ["booking_reference", "new_destination"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "assist_third_party_booking",
            "description": "Assists with third-party bookings if eligible for direct airline handling.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Third-party booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Graded final action, as with process_full_refund. Requires booking_reference.
    {
        "type": "function",
        "function": {
            "name": "assess_compensation_request",
            "description": "Evaluates the customer's compensation request based on airline policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."}
                },
                "required": ["booking_reference"],
                "additionalProperties": False
            }
        }
    },
    # Final case resolution function
    # The name a generated routine must end on.
    # If the agent calls it, the eval grades booking_reference and resolution_details.
    {
        "type": "function",
        "function": {
            "name": "case_resolution",
            "description": "Finalizes and closes the customer case with all resolution details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_reference": {"type": "string", "description": "Customer's booking reference."},
                    "resolution_details": {"type": "string", "description": "Details of how the case was resolved."}
                },
                "required": ["booking_reference", "resolution_details"],
                "additionalProperties": False
            }
        }
    }
]