from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from dentalE.models import UserProfile, Paciente
from django.contrib.auth.models import User


class TestingPatients(LiveServerTestCase):

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

        # Creo paciente
        self.paciente_test = Paciente.objects.create(documento='86484086',
                                                     nombre='Paciente',
                                                     primer_apellido='Automatización',
                                                     genero='Otro',
                                                     direccion='Colegio Hogwarts de Magia y Hechicería, 1432',
                                                     ciudad='Colonia',
                                                     fecha_nacimiento='2000-11-11',
                                                     celular='091912219',
                                                     email='autotest@dental.com',
                                                     nucleo_activo=False)
        self.paciente_test.save()
        self.paciente_test_auto = Paciente.objects.create(documento='68239168',
                                                          nombre='Paciente2',
                                                          primer_apellido='Automatización2',
                                                          genero='M',
                                                          direccion='Colegio Hogwarts de Magia y Hechicería, 1433',
                                                          ciudad='Durazno',
                                                          fecha_nacimiento='1991-01-25',
                                                          celular='099112219',
                                                          email='autotest2@dental.com',
                                                          nucleo_activo=False)
        self.paciente_test_auto.save()

        # Creo cita del día

    def tearDown(self):
        self.browser.close()

    def test_lista_pacientes(self):
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
        lkn_pacientes = page_title = self.browser.find_element_by_xpath(
            "//li[contains(@class, 'nav-item')]//a[contains(@href, '/dentalE/listapacientes')]")
        self.assert_(lkn_pacientes.is_displayed())
        lkn_pacientes.click()
        tabla_pacientes = self.browser.find_element_by_xpath(
            '//table[@id="dataTable"]')
        self.assert_(tabla_pacientes.is_displayed())
        pacientes_tabla = self.browser.find_elements_by_xpath('//tbody//tr')
        pacientes = []
        for p in pacientes_tabla:
            paciente = p.text.replace(" Ver más información", "")
            pacientes.append(paciente)
        pacientes_esperados = ['{} {} {} {} {}'.
                                   format(self.paciente_test.documento,
                                          self.paciente_test.nombre,
                                          self.paciente_test.primer_apellido,
                                          self.paciente_test.email,
                                          self.paciente_test.celular),
                               '{} {} {} {} {}'.
                                   format(self.paciente_test_auto.documento,
                                          self.paciente_test_auto.nombre,
                                          self.paciente_test_auto.primer_apellido,
                                          self.paciente_test_auto.email,
                                          self.paciente_test_auto.celular)
                               ]
        self.assertEqual(pacientes, pacientes_esperados)
