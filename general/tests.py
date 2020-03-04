# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase,LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time 

from .models import turnos
from entidades.models import *
from usuarios.models import *
from laboralsalud.utilidades import *


def select_from_chosen(driver, id, value):
    chosen = driver.find_element_by_id(id + '_chosen')
    results = chosen.find_elements_by_css_selector(".chosen-results li")

    found = False
    for result in results:
        if result.text == value:
            found = True
            break

    if found:
        chosen.find_element_by_css_selector("a").click()
        result.click()
    return found

class TestListados(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):    
        cls.browser = Chrome()
        cls.browser.maximize_window()
        cls.browser.get("http://localhost:8000/login")
        cls.browser.find_element(By.ID, "id_usuario").send_keys("admin")
        cls.browser.find_element(By.ID, "id_password").send_keys("battlehome")
        cls.browser.find_element(By.NAME, "login").click()
               
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


    def test_LoginHome(self):        
        assert 'ADMIN' in self.browser.page_source      

    def test_AusentismosListado(self):    
        self.browser.get("http://localhost:8000/ausentismos/")
        self.browser.find_element(By.CSS_SELECTOR, ".btn-circle").click()
        self.browser.find_element(By.ID, "id_estado").click()
        dropdown = self.browser.find_element(By.ID, "id_estado")
        dropdown.find_element(By.XPATH, "//option[. = 'TODOS']").click()
        self.browser.find_element(By.ID, "id_estado").click()
        self.browser.find_element(By.CSS_SELECTOR, ".col-sm-1 > .btn").click()
        elements = self.browser.find_elements(By.ID, "ausentismos_info")
        assert len(elements) > 0        

    def test_EmpleadosListado(self):
        self.browser.get("http://localhost:8000/entidades/empleado/")
        self.browser.find_element(By.CSS_SELECTOR, ".btn-circle").click()
        self.browser.find_element(By.ID, "id_estado").click()
        dropdown = self.browser.find_element(By.ID, "id_estado")
        dropdown.find_element(By.XPATH, "//option[. = 'TODOS']").click()
        self.browser.find_element(By.ID, "id_estado").click()
        self.browser.find_element(By.CSS_SELECTOR, ".col-sm-1 > .btn").click()
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".odd:nth-child(1) .caret")
        assert len(elements) > 0    

    def test_TurnosListado(self):
        self.browser.get("http://localhost:8000/turnos/")
        self.browser.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.browser.find_element(By.ID, "id_fdesde").send_keys("01/01/2019")
        self.browser.find_element(By.CSS_SELECTOR, ".btn-circle").click()
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".odd > td:nth-child(1)")
        assert len(elements) > 0        

# class TestTurnos(LiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):    
#         cls.browser = Chrome()
#         cls.browser.get("http://localhost:8000/login")
#         cls.browser.find_element(By.ID, "id_usuario").send_keys("admin")
#         cls.browser.find_element(By.ID, "id_password").send_keys("battlehome")
#         cls.browser.find_element(By.NAME, "login").click()
               
#     @classmethod
#     def tearDownClass(cls):
#         cls.browser.quit()

    def test_TurnosNuevo(self):
        self.browser.get("http://localhost:8000/turnos/")
        time.sleep(5)
        self.browser.find_element(By.LINK_TEXT, "Nuevo Turno").click()
        time.sleep(5)
        select = Select(self.browser.find_element_by_id("id_empresa"))
        select.select_by_visible_text('KILBEL')
        time.sleep(5)        
        self.browser.find_element(By.CSS_SELECTOR, "a.chosen-single").click()
        self.browser.find_element(By.XPATH,"//ul[@class='chosen-results']/li[contains(.,'ACEVEDO JUAN CARLOS - 14113562 - KILBEL')]").click();        
        time.sleep(3)
        self.browser.find_element(By.ID, "Aceptar").click()
        assert 'ACEVEDO JUAN CARLOS' in self.browser.page_source      
