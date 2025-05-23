from utils.tools import Tools
from utils import consts as CS

class PropertyRules(object):
    def __init__(self) -> None:
        self.tools = Tools()
        self.duplicate_listing = self.tools.get_duplicate_properties()
        self.property_rule_specific_map = self.set_rule_specific_mapping()
        self.final_commission_exempt = self.properties_without_final_commission()
        self.final_commission_map = self.properties_final_commission()

    def set_rule_specific_mapping(self):
        properties = self.tools.get_full_properties_data()
        rule_specific_map = {}

        for id_, data in properties.items():
            p_num = data[CS.PROPERTY_NUMBER]
            if id_ in ["143528", "132595", "180972"]:
               rule = self.rule_rb_10_9_4

            elif p_num in ["2238"]:
                rule = self.rule_2238

            elif p_num in ["3208"]:
                rule = self.rule_3208

            elif id_ == CS.SIRENIS_ID:
                rule = self.rule_sirenis
            else:
                continue

            rule_specific_map[id_] = rule

        return rule_specific_map

    def properties_without_final_commission(self):
        properties = self.tools.get_full_properties_data()
        final_commission_exempt = []

        for id_, data in properties.items():
            p_num = data[CS.PROPERTY_NUMBER]
            name = data[CS.PROPERTY_NAME]

            if p_num in ["19"] or any(nstr in name for nstr in ["Temozon", "Sirenis"]):
                final_commission_exempt.append(id_)

        return final_commission_exempt

    def properties_final_commission(self):
        properties = self.tools.get_full_properties_data()
        final_commission = {}

        for id_ in properties.keys():
            # 25% de comision
            if id_ in CS.FINAL_COMMISSION_25:
                comsion = 0.25

            # 22% de comision
            elif id_ in CS.FINAL_COMMISSION_22:
                comsion = 0.22

            # 20% de comision
            elif id_ in CS.FINAL_COMMISSION_20:
                comsion = 0.2

            # 18% de comision
            elif id_ in CS.FINAL_COMMISSION_18:
                comsion = 0.18

            # 15% de comision
            elif id_ in CS.FINAL_COMMISSION_15:
                comsion = 0.15

            # 12% de comision
            elif id_ in CS.FINAL_COMMISSION_12:
                comsion = 0.12

            # 10% de comision
            elif id_ in CS.FINAL_COMMISSION_10:
                comsion = 0.1

            else:
                continue

            final_commission[id_] = comsion

        return final_commission

    def get_total(self, charges, income, property_id, booking_from_beds=False) -> int:
        if property_id in self.property_rule_specific_map:
            return self.property_rule_specific_map[property_id](charges, income, booking_from_beds)

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

        return total

    def booking_from_airbnb(self, charges, income) -> int:
        total_charges_amount = 0
        for _, amount in charges.items():
            total_charges_amount += amount

        return income - total_charges_amount
            

    def booking_from_beds(self, charges, income) -> int:
        commission_per_card_1 = charges.get(CS.CART_TRANSACTION_KEY_1, None)
        commission_per_card_2 = charges.get(CS.CART_TRANSACTION_KEY_2, None)

        commission_per_card = commission_per_card_2 or commission_per_card_1

        if commission_per_card_2:
            charges.pop(CS.CART_TRANSACTION_KEY_2)
        elif commission_per_card_1:
            charges.pop(CS.CART_TRANSACTION_KEY_1)

        sub_income = income - commission_per_card if commission_per_card is not None else income
        # three_porcent_less = sub_income - (sub_income * CS.AIRBNB_COMMISSION)

        total_charges_amount = 0
        for _, amount in charges.items():
            total_charges_amount += amount

        return sub_income - total_charges_amount

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

        return self.booking_from_airbnb(charges, income)

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

    def rule_4601(self, charges, income, booking_from_beds=False):
        if CS.RESORT_FEE_KEY_1 not in charges or CS.RESORT_FEE_KEY_2 not in charges:
            charges[CS.RESORT_FEE_KEY_1] = 20

        if booking_from_beds:
            return self.booking_from_beds(charges, income)

        return self.booking_from_airbnb(charges, income)

    def rule_sirenis(self, charges, income, booking_from_beds=False):
        cleaning = None
        for charge in charges.keys():
            if charge in [CS.CLEANING_KEY_1, CS.CLEANING_KEY_2] or "Cleaning fee" in charge:
                cleaning = charge

        if cleaning:
            charges.pop(cleaning)
        
        if booking_from_beds:
            return self.booking_from_beds(charges, income)

        return self.booking_from_airbnb({}, income)
