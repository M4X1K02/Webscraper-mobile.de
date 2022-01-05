"""
@TIPP config = dict(list(tuple(tuple)))
"""

config = {  'from_mil': None,
            'to_mil': None,
            'from_price': None,
            'to_price': None,
            'no_dmg': None,
            'from_ez': None,  # [(('11000','3'),1990),(('17700','9'),1990)]
           'to_ez': [(('11000','3'),2000),  # honda civic
                     (('17700','9'),1999),  # mitsu eclipse
                     (('25200','14'),2005),  # vw golf
                     (('18700','58'),2005),  # nissan pulsar
                     (('18700','34'),2000),  # nissan sunny
                     (('17200','64'),1995)],  # mercedes e500 (v8)
            'from_pw': [(('11000','3'),74),  # honda civic
                        (('23500','8'),147),  # subaru impreza
                        (('23500','10'),147),  # subaru legacy
                        (('18700','58'),100),  # nissan pulsar
                        (('18700','34'),100),  # nissan sunny
                        (('18700','33'),147),  # nissan skyline
                        (('16800','5'),147),  # mazda 323
                        (('17700','16'),147),  # mitsu lancer
                        (('23600','19'),103),  # suzuki swift
                        (('17200','64'),221),  # mercedes e500
                        (('25200','14'),147)],  # vw golf
            'to_pw': None,
            'gas': [(('15200','5'),True),   # lexus is-series
                    (('15200','16'),True),
                    (('15200','6'),True),
                    (('15200','7'),True),
                    (('15200','28'),True),
                    (('25200','14'),True)],  # vw golf
            'trans': [(('11000','3'),True),  # honda civic
                      (('23500','10'),True),  # subaru legacy
                      (('25200','14'),True)]  # vw golf
            }