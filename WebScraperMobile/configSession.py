# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 13:08:40 2021

@author: maxik
"""
from updateDB import DBcheck
import random

"""proxy list"""
proxies = [('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[8]/div[1]/div[1]/div[2]', 'Österreich'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[10]/div[1]/div[1]/div[2]', 'Belgien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[11]/div[1]/div[1]/div[2]','Bosnien Herzegowina'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[13]/div[1]/div[1]/div[2]','Bulgarien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[19]/div[1]/div[1]/div[2]','Kroatien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[20]/div[1]/div[1]/div[2]','Zypern'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[21]/div[1]/div[1]/div[2]','Tschechien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[22]/div[1]/div[1]/div[2]','Dänemark'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[23]/div[1]/div[1]/div[2]','Estland'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[24]/div[1]/div[1]/div[2]','Finnland'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[25]/div[1]/div[1]/div[2]','Marseille'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[26]/div[1]/div[1]/div[2]','Paris'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[27]/div[1]/div[1]/div[2]','Bordeaux'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[28]/div[1]/div[1]/div[2]','Georgien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[29]/div[1]/div[1]/div[2]','Berlin'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[30]/div[1]/div[1]/div[2]','FaM'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[31]/div[1]/div[1]/div[2]','Griechenland'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[33]/div[1]/div[1]/div[2]','Ungarn'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[34]/div[1]/div[1]/div[2]','Island'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[39]/div[1]/div[1]/div[2]','Irland'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[40]/div[1]/div[1]/div[2]','Israel'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[41]/div[1]/div[1]/div[2]','Mailand'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[42]/div[1]/div[1]/div[2]','Rom'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[45]/div[1]/div[1]/div[2]','Lettland'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[46]/div[1]/div[1]/div[2]','Litauen'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[47]/div[1]/div[1]/div[2]','Luxemburg'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[50]/div[1]/div[1]/div[2]','Moldau'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[51]/div[1]/div[1]/div[2]','Niederlande'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[55]/div[1]/div[1]/div[2]','Norwegen'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[59]/div[1]/div[1]/div[2]','Danzig'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[60]/div[1]/div[1]/div[2]','Warschau'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[61]/div[1]/div[1]/div[2]','Lissabon'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[62]/div[1]/div[1]/div[2]','Porto'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[63]/div[1]/div[1]/div[2]','Rumänien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[64]/div[1]/div[1]/div[2]','Russland'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[65]/div[1]/div[1]/div[2]','Serbien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[67]/div[1]/div[1]/div[2]','Slowakei'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[68]/div[1]/div[1]/div[2]','Slowenien'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[71]/div[1]/div[1]/div[2]','Madrid'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[72]/div[1]/div[1]/div[2]','Barcelona'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[73]/div[1]/div[1]/div[2]','Valencia'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[74]/div[1]/div[1]/div[2]','Schweden'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[75]/div[1]/div[1]/div[2]','Schweiz'),
           ('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[78]/div[1]/div[1]/div[2]','Türkei')]

"""random sample of proxy list"""
proxies_sample = random.sample(proxies, len(proxies))

"""checks for new models/entries"""
check = DBcheck()
check.update()