from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from dentalE.models import UserProfile, Paciente
from django.contrib.auth.models import User
import time


class TestingLogin(LiveServerTestCase):

    def setUp(self):
        # Defino el driver a utilizar

        self.browser = webdriver.Chrome(
            'dentalE/functionalTests/chromedriver.exe')

        # Creo usuario con perfil Doctor
        self.username = 'testProfUser'
        self.password = '@lmaProf'
        test_user = User.objects.create(username=self.username)
        test_user.set_password(self.password)
        test_user.save()
        user = User.objects.filter(username=self.username).last()
        profile = UserProfile.objects.create(user=user,
                                             user_tipo='DOCTOR',
                                             user_especialidad='ORTODONCIA',
                                             user_celular='091741852')
        profile.save()

    def tearDown(self):
        self.browser.close()

    def test_main_page_is_displayed(self):
        self.browser.get(self.live_server_url)
        img_logo_dental = self.browser.find_element_by_xpath(
            "//img[contains(@src, '/LogoHAlma_2')]")
        txt_usuario = self.browser.find_element_by_id('user')
        txt_pswd = self.browser.find_element_by_id('password')
        btn_google_login = self.browser.find_element_by_xpath(
            "//a[contains(@href, '/google')]")
        btn_ingresar = self.browser.find_element_by_xpath(
            "//button[contains(@class, 'btn-user')]")
        self.assert_(img_logo_dental.is_displayed())
        self.assert_(txt_usuario.is_displayed())
        self.assert_(txt_pswd.is_displayed())
        self.assert_(btn_google_login.is_displayed())
        self.assert_(btn_ingresar.is_displayed())
        txt_usuario_placeholder = txt_usuario.get_attribute('placeholder')
        self.assertEqual(txt_usuario_placeholder, 'Ingrese usuario...',
                         'El placeholder para campo usuario no es el esperado')

    def test_successful_user_login(self):
        self.browser.get(self.live_server_url)
        txt_usuario = self.browser.find_element_by_id('user')
        txt_pswd = self.browser.find_element_by_id('password')
        btn_ingresar = self.browser.find_element_by_xpath(
            "//button[contains(@class, 'btn-user')]")
        txt_usuario.send_keys(self.username)
        txt_pswd.send_keys(self.password)
        btn_ingresar.click()
        page_title = self.browser.find_element_by_xpath(
            "//h3[contains(@class, 'text-dark')]")
        self.assert_(page_title.is_displayed())
        page_title = page_title.text
        self.assertEqual(page_title,
                         'Citas del día')
