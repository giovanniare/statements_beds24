from utils.tools import Tools
from utils import consts as CS

class PropertyRules(object):
    def __init__(self) -> None:
        self.tools = Tools()
        self.property_rule_specific_map = {
            "132595": self.rule_rb_10_9_4,
            "143528": self.rule_rb_10_9_4,
            "180972": self.rule_rb_10_9_4,
            "188838": self.rule_2238,
            "143166": self.rule_3208,
            "143362": self.rule_4560,
            "106689": self.rule_4560
        }
        self.final_commission_exempt = [
            "107103"
        ]
        self.final_commission_map = {
            "102507": 0.18,     # 14 - Tulum
            "132599": 0.2,      # 15 - Tulum
            "132595": 0.25,     # RB 9 - Tulum
            "143528": 0.25,     # RB 10 - Tulum
            "180972": 0.25,     # RB 4 - Tulum
        }
        self.duplicate_listing = [
            ("106689", "143362"),
            ("138517", "196293"),
            ("159372", "185440")
        ]

    def get_total(self, charges, income, property_id, booking_from_beds=False) -> int:
        if property_id in self.property_rule_specific_map:
            return self.property_rule_specific_map[property_id](charges, income, booking_from_beds=False)

        if booking_from_beds:
            return self.booking_from_beds(charges, income)
        
        return self.booking_from_airbnb(charges, income)

    def generic_rule_calculation(self, property_info) -> int:
        pass

    def commission_collection(self, total, property_id, property_info) -> int:
        if property_id in self.final_commission_exempt:
            return total

        if property_id in self.final_commission_map:
            return total - (total * self.final_commission_map[property_id])

        location = property_info[CS.STATE]
        if location in CS.FLORIDA_IDS:
            return total - (total * CS.FL_COMMISSION)

        if location == CS.QROO:
            return total - (total * CS.TULUM_COMMISSION)

    def booking_from_airbnb(self, charges, income) -> int:
        total_charges_amount = 0
        for _, amount in charges.items():
            total_charges_amount += amount

        return income - total_charges_amount
            

    def booking_from_beds(self, charges, income) -> int:
        commission_per_card = charges.get(CS.CART_TRANSACTION_KEY_1, None)
        if not commission_per_card:
            commission_per_card = charges.get(CS.CART_TRANSACTION_KEY_2, None)
            charges.pop(CS.CART_TRANSACTION_KEY_2)
        else:
            charges.pop(CS.CART_TRANSACTION_KEY_1)

        sub_income = income - commission_per_card
        three_porcent_less = sub_income - (sub_income * CS.AIRBNB_COMMISSION)

        total_charges_amount = 0
        for _, amount in charges.items():
            total_charges_amount += amount

        return three_porcent_less - total_charges_amount

    def rule_rb_10_9_4(self, charges, income, booking_from_beds=False) -> int:
        """ 
        Cleaning fee and resort fee don't apply for RB 10, RB 9 and RB 4
        """
        if CS.CLEANING_KEY_1 in charges:
            charges.pop(CS.CLEANING_KEY_1)

        if CS.CLEANING_KEY_2 in charges:
            charges.pop(CS.CLEANING_KEY_2)

        if CS.RESORT_FEE_KEY_1 in charges:
            charges.pop(CS.RESORT_FEE_KEY_1)

        if CS.RESORT_FEE_KEY_2 in charges:
            charges.pop(CS.RESORT_FEE_KEY_2)

        if booking_from_beds:
            return self.booking_from_beds(charges, income)

        return self.booking_from_airbnb(charges, income)

    def rule_2238(self, charges, income, booking_from_beds=False) -> int:
        """
        Pet fee don't apply as charge and if booking is coming from beds, 3% don't apply neither for property 2238
        """
        if CS.PET_FEE_KEY in charges:
            charges.pop(CS.PET_FEE_KEY)

        if booking_from_beds:
            return self.booking_from_beds(charges, income)

        commission_per_card = charges.get(CS.CART_TRANSACTION_KEY_1, None)
        if not commission_per_card:
            commission_per_card = charges.get(CS.CART_TRANSACTION_KEY_2, None)
            charges.pop(CS.CART_TRANSACTION_KEY_2)
        else:
            charges.pop(CS.CART_TRANSACTION_KEY_1)

        sub_income = income - commission_per_card
        total_charges_amount = 0
        for des, amount in charges:
            total_charges_amount += amount

        return sub_income - total_charges_amount

    def rule_3208(self, charges, income, booking_from_beds=False) -> int:
        """
        Resort fee don't apply over property 3208
        """
        if CS.RESORT_FEE_KEY_1 in charges:
            charges.pop(CS.RESORT_FEE_KEY_1)

        if CS.RESORT_FEE_KEY_2 in charges:
            charges.pop(CS.RESORT_FEE_KEY_2)

        if booking_from_beds:
            return self.booking_from_beds(charges, income)

        return self.booking_from_airbnb(charges, income)

    def rule_4560(self, charges, income, booking_from_beds=False) -> int:
        """
        Always apply $150 USD of cleaning fee over property 4560 
        """
        if CS.CLEANING_KEY_1 in charges and charges[CS.CLEANING_KEY_1] != 0:
            charges[CS.CLEANING_KEY_1] = 150

        if CS.CLEANING_KEY_2 in charges and charges[CS.CLEANING_KEY_2] != 0:
            charges[CS.CLEANING_KEY_2] = 150

        if booking_from_beds:
            return self.booking_from_beds(charges, income)

        return self.booking_from_airbnb(charges, income)
            