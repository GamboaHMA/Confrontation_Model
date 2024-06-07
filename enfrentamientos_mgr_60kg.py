class Clash():
    def __init__(self, a1_id:int, a2_id:int, result:str, w_id, year:str) -> None:
        self.athlete1_id = a1_id
        self.athlete2_id = a2_id
        self.result = result
        self.winner_id = w_id
        self.year = year

'''
def Get_Clashes():
    enfrentamientos = [Clash(a1_id=1, a2_id=2, result='11_2', w_id=1, year='2022'),
                       Clash(a1_id=1, a2_id=2, result='5_3', w_id=2, year='2023'),
                       Clash(a1_id=1, a2_id=3, result='9_0', w_id=1, year='2019'),
                       Clash(a1_id=1, a2_id=4, result='9_1', w_id=1, year='2022'),
                       Clash(a1_id=1, a2_id=4, result='13_7', w_id=4, year='2021'),
                       Clash(a1_id=1, a2_id=5, result='4_0', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=5, result='4_0', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=6, result='7_3', w_id=1, year='2023'),
                       Clash(a1_id=1, a2_id=10, result='9_3', w_id=10, year='2021'),
                       Clash(a1_id=1, a2_id=11, result='5_3', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=11, result='8_0', w_id=11, year='2022'),
                       Clash(a1_id=1, a2_id=11, result='5_2', w_id=1, year='2022'),
                       Clash(a1_id=1, a2_id=12, result='8_4', w_id=12, year='2019'),
                       Clash(a1_id=1, a2_id=12, result='6_5', w_id=1, year='2020'),
                       Clash(a1_id=1, a2_id=12, result='5_2', w_id=12, year='2022'),
                       Clash(a1_id=1, a2_id=12, result='8_0', w_id=1, year='2022'),
                       Clash(a1_id=1, a2_id=13, result='3_1', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=13, result='6_4', w_id=13, year='2021'),
                       Clash(a1_id=1, a2_id=14, result='9_0', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=14, result='6_3', w_id=14, year='2022'),
                       Clash(a1_id=1, a2_id=14, result='5_2', w_id=1, year='2022'),
                       Clash(a1_id=1, a2_id=15, result='6_4', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=15, result='5_3', w_id=15, year='2022'),
                       Clash(a1_id=1, a2_id=15, result='4_1', w_id=1, year='2022'),
                       Clash(a1_id=1, a2_id=16, result='6_4', w_id=1, year='2021'),
                       Clash(a1_id=1, a2_id=16, result='5_3', w_id=16, year='2022'),
                       Clash(a1_id=1, a2_id=16, result='4_1', w_id=1, year='2022'),
                       Clash(a1_id=2, a2_id=3, result='8_0', w_id=2, year='2019'),
                       Clash(a1_id=2, a2_id=3, result='5_1', w_id=2, year='2020'),
                       Clash(a1_id=2, a2_id=4, result='10_0', w_id=2, year='2019'),
                       Clash(a1_id=2, a2_id=4, result='8_0', w_id=2, year='2021'),
                       Clash(a1_id=2, a2_id=5, result='6_5', w_id=5, year='2022'),
                       Clash(a1_id=2, a2_id=5, result='7_4', w_id=2, year='2022'),
                       Clash(a1_id=2, a2_id=5, result='5_2', w_id=2, year='2021'),
                       Clash(a1_id=2, a2_id=5, result='4_3', w_id=5, year='2023'),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=),
                       Clash(a1_id=, a2_id=, result=, w_id=, year=)]
'''