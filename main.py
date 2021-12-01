from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.support.ui import Select

def Generar_Json(separado,ult_fecha_actuacion):
    fecha_actuacion = separado[0]
    if fecha_actuacion==ult_fecha_actuacion:
        actuacion = separado[1]
        anotacion = separado[2]
        fecha_inicia_termino = separado[3]
        fecha_finaliza_termino =separado[4]
        fecha_registro = separado[5]

        value = {
                "fecha_actuacion": fecha_actuacion,
                "actuacion": actuacion,
                "anotacion": anotacion,
                "fecha_inicia_termino": fecha_inicia_termino,
                "fecha_finaliza_termino": fecha_finaliza_termino,
                "fecha_registro": fecha_registro
        }
        return value
    return ''

def Seleccionar_ciudad(driver,ciudad):
    try:
       # Selección de la ciudad
        aux = driver.find_element_by_id('ddlCiudad')
        aux.click()
        select = Select(aux)
        select.select_by_visible_text(ciudad)
        # Value según la ciudad
        #driver.find_element_by_xpath('//table[@class="contenedor"]//select[@class="campos"]//option[@value='+value+']').click()

    except TimeoutException:
       # print('Mucha en los campos de seleccionar la ciudad y entidad/Especialidad')
        return False
    return True

def Seleccionar_Entidad_Especialidad(driver,entidad_especialidad):
    try:
        aux = driver.find_element_by_id('ddlEntidadEspecialidad')
        aux.click()
        select = Select(aux)
        select.select_by_visible_text(entidad_especialidad)

    except TimeoutException:
        #print('Mucha demora en cargar')
        return False
    return True

def Diligenciar_y_Consultar(id,driver):
    aux = driver.find_element_by_xpath('//div[@id="divNumRadicacion"]')
    aux.find_element_by_xpath('//input[@onkeypress=" return num(event)"]').send_keys(id)
    slider = driver.find_element_by_xpath('//div[@class="ajax__slider_h_handle"]')
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(60, 0).release().perform()
    aux.find_element_by_xpath('//input[@value="Consultar"]').click()
    return True


def iniciar(id,fecha,ciudad,entidad_especialidad):
    Json = "Error de carga"
    url = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=YtExgTScBbCqSdjRAx0PEayOJM8%3d'
    capabilities = {
        "browserName": "firefox",
        "version": "92.0",
        "platform": "LINUX",
        #"enableVNC": True,
        #"enableVideo": True,
    }

    driver = webdriver.Remote(
        command_executor='http://34.102.0.97:4444/wd/hub',
        desired_capabilities=capabilities
    )

    driver.get(url)
    if Seleccionar_ciudad(driver,ciudad):
        print("Ciudad seleccionada")

    time.sleep(2)
    try:
        if Seleccionar_Entidad_Especialidad(driver,entidad_especialidad):
            print("Entidad/Especialidad seleccionada")
    except:
        print("Se demoró cargar la entidad")

    try:
        # Consultar con los parametros
        if Diligenciar_y_Consultar(id, driver):
            print("Diligenciamiento y consulta enviada")
    except:
        print("Se demoró enviar la consulta")

    try:
        time.sleep(4)
        _contenido = driver.find_elements_by_xpath('//tr[@class="tr_contenido"]')
        _contenido = _contenido[4].text
        _Scontenido = _contenido.split('\n')
        if (len(_Scontenido) == 4):
            aux_s = _Scontenido[3]
            _Scontenido[3] = ''
            _Scontenido.append("")
            _Scontenido.append(aux_s)

        Json = Generar_Json(_Scontenido, fecha)
    except:
        print("Se demoró cargar el contenido")
    try:
        driver.quit()
    except:
        print("Ya se cerró")

    return Json
