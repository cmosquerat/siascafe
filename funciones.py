from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import scipy.interpolate as si
import mysql.connector as connection
import pandas as pd
from datetime import date
import datetime
import os


año = date.today().year  # Obtener año actual para conexión a base de datos


def get_database(orden):
    """Obtiene la base de datos a partir de la orden

    Args:
        orden (_type_): Número de orden

    Returns:
        _type_: _description_
    """

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    años = [year]
    # años = [2021]
    mydb = connection.connect(
        host="190.147.28.95", database="multilab", user="root", passwd="d3f4g5h6"
    )
    for año in años:
        query = f"Select * from muestra_{año} WHERE orden={orden};"
        print("Obteniendo muestras")
        muestras = pd.read_sql(query, mydb)
        query = f"Select * from orden_{año};"
        print("Obteniendo Órdenes")
        ordenes = pd.read_sql(query, mydb)
        query = f"Select * from finca;"
        print("Obteniendo Fincas")
        finca = pd.read_sql(query, mydb)
        query = f"Select * from cliente;"
        print("Obteniendo Clientes")
        cliente = pd.read_sql(query, mydb)
        query = f"Select * from municipios;"
        print("Obteniendo Municipios")
        municipios = pd.read_sql(query, mydb)
        query = f"Select * from departamentos;"

        departamentos = pd.read_sql(query, mydb)
        query = f"Select * from tipo_analisis;"
        print("Obteniendo Analisis")
        tipo_analisis = pd.read_sql(query, mydb)

    mydb.close()  # close the connection
    return muestras, ordenes, cliente, municipios, finca, tipo_analisis, departamentos


def get_description(
    c_lab, muestras, ordenes, cliente, municipios, finca, tipo_analisis, departamentos
):

    n_orden = muestras[muestras["codigo"] == c_lab]["orden"].values[0]
    orden = ordenes[ordenes["codigo"] == n_orden]
    c_muestras = orden["muestras"].values[0]
    fecha_solicitud = orden["fecha_solicitud"].values[0]
    fecha_solicitud = np.datetime_as_string(fecha_solicitud, unit="D")
    fecha_entrega = datetime.datetime.today().strftime("%Y-%m-%d")
    proyecto = orden["proyecto"].values[0]
    codigo_solicitante = orden["codigo_solicitante"].values[0]
    solicitante = cliente[cliente["codigo"] == codigo_solicitante]["nombre"].values[0]
    codigo_propietario = orden["codigo_propietario"].values[0]
    propietario = cliente[cliente["codigo"] == codigo_propietario]["nombre"].values[0]
    codigo_finca = orden["codigo_finca"].values[0]
    nombre_finca = finca[finca["codigo"] == codigo_finca]["nombre"].values[0]
    vereda = finca[finca["codigo"] == codigo_finca]["vereda"].values[0]
    codigo_municipio = finca[finca["codigo"] == codigo_finca]["municipio"].values[0]

    analisis = "ph"

    municipio = municipios[municipios["codigo_municipio"] == codigo_municipio][
        "nombre"
    ].values[0]

    codigo_departamento = municipios[
        municipios["codigo_municipio"] == codigo_municipio
    ]["codigo_depto"].values[0]

    departamento = departamentos[departamentos["codigo"] == codigo_departamento][
        "nombre"
    ].values[0]

    diccionario1 = {
        "Solicitante:": solicitante,
        "Departamento:": departamento,
        "Propietario:": propietario,
        "Proyecto:": proyecto,
        "Finca:": nombre_finca,
        "Vereda:": vereda,
        "Municipio:": municipio,
    }
    diccionario2 = {
        "N. Orden:": n_orden,
        "N. Muestras:": c_muestras,
        "N. lab:": c_lab,
        "Fecha Recibo: ": fecha_solicitud,
        "Fecha Entrega:": fecha_entrega,
    }
    return diccionario1, diccionario2, analisis


def execute_orden(orden, etapas, edad, densidad, sombrio):
    os.makedirs(f"Reportes/{orden}", exist_ok=True)
    path = os.getcwd() + f"/Reportes/{orden}"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", path)

    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/octet-stream"
    )

    c_orden = int(orden)
    etapa_ = {"Producción": "2", "Crecimiento": "0", "Zoca": "1"}
    texturas_ = {
        1: "7",
        2: "8",
        3: "1",
        4: "9",
        5: "6",
        6: "12",
        7: "11",
        8: "10",
        9: "5",
        10: "4",
        11: "3",
        12: "2",
        13: "11",
    }

    etapa = etapa_[etapas]
    (
        muestras,
        ordenes,
        cliente,
        municipios,
        finca,
        tipo_analisis,
        departamentos,
    ) = get_database(c_orden)
    muestras_t = muestras[muestras["orden"] == c_orden]

    # Curve base:
    points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
    points = np.array(points)

    x = points[:, 0]
    y = points[:, 1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)  # x interpolate values
    y_i = si.splev(ipl_t, y_list)  # y interpolate values

    PATH = "geckodriver.exe"
    driver = webdriver.Firefox(firefox_profile=profile)

    driver.get("https://www.cenicafe.org/es/index.php/us3r5/login")

    time.sleep(1)

    username = driver.find_element(by=By.NAME, value="username")
    password = driver.find_element(by=By.NAME, value="password")
    login = driver.find_element(by=By.CLASS_NAME, value="submit")

    username.send_keys("810004212")
    password.send_keys("Multilab2001")
    login.click()
    time.sleep(1)
    for c_lab in muestras_t.codigo:

        driver.get("https://www.cenicafe.org/es/index.php/servicios/siaskafe")

        print(c_lab)
        diccionario1, diccionario2, analisis = get_description(
            c_lab,
            muestras,
            ordenes,
            cliente,
            municipios,
            finca,
            tipo_analisis,
            departamentos,
        )

        muestras_d = muestras[muestras["codigo"] == c_lab]

        driver.maximize_window()
        departamento = driver.find_element(by=By.ID, value="nombredepartamento")
        municipio = driver.find_element(by=By.ID, value="nombremunicipio")
        sica = driver.find_element(by=By.ID, value="codigofinca")
        nombrefinca = driver.find_element(by=By.ID, value="nombrefinca")
        referencialote = driver.find_element(by=By.ID, value="referencialote")
        etapacultivo = Select(driver.find_element(by=By.ID, value="etapacultivo"))
        edadcultivo = Select(driver.find_element(by=By.ID, value="edadcultivo"))
        densidadsiembra = Select(driver.find_element(by=By.ID, value="densidadsiembra"))
        ph = driver.find_element(by=By.ID, value="ph")
        mo = driver.find_element(by=By.ID, value="mo")
        p = driver.find_element(by=By.ID, value="p")
        k = driver.find_element(by=By.ID, value="k")
        ca = driver.find_element(by=By.ID, value="ca")
        mg = driver.find_element(by=By.ID, value="mg")
        al = driver.find_element(by=By.ID, value="al")
        sulphur = driver.find_element(by=By.ID, value="sulphur")
        nivelsombrio = Select(driver.find_element(by=By.ID, value="nivelsombrio"))
        textura = Select(driver.find_element(by=By.ID, value="codigotextura"))
        OpcionFertilizanteS = Select(
            driver.find_element(by=By.ID, value="opcionFertilizanteSimple[]")
        )
        opcionFertilizanteCompuesto = Select(
            driver.find_element(by=By.ID, value="opcionFertilizanteCompuesto[]")
        )
        reportar = driver.find_element(by=By.ID, value="Reportar")
        borrar = driver.find_element(by=By.ID, value="reset")
        azufre = driver.find_element(by=By.ID, value="sulphur")

        departamento.send_keys(diccionario1["Departamento:"])
        municipio.send_keys(diccionario1["Municipio:"])
        nombrefinca.send_keys(diccionario1["Finca:"])
        referencialote.send_keys(str(c_lab))

        if muestras_d["ph"].values[0] is not None:
            ph.send_keys(muestras_d["ph"].values[0].replace(",", "."))

        if muestras_d["mo"].values[0] is not None:
            mo.send_keys(muestras_d["mo"].values[0].replace(",", "."))

        if muestras_d["p"].values[0] is not None:
            p.send_keys(muestras_d["p"].values[0].replace(",", "."))

        if muestras_d["k"].values[0] is not None:
            k.send_keys(muestras_d["k"].values[0].replace(",", "."))

        if muestras_d["ca"].values[0] is not None:
            ca.send_keys(muestras_d["ca"].values[0].replace(",", "."))

        if muestras_d["mg"].values[0] is not None:
            mg.send_keys(muestras_d["mg"].values[0].replace(",", "."))

        if muestras_d["al"].values[0] is not None:
            al.send_keys(muestras_d["al"].values[0].replace(",", "."))

        if muestras_d["s"].values[0] is not None:
            sulphur.send_keys(muestras_d["s"].values[0].replace(",", "."))

        etapacultivo.select_by_value(etapa)
        edadcultivo.select_by_value(edad)
        densidadsiembra.select_by_value(densidad)
        nivelsombrio.select_by_value(sombrio)

        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        if muestras_d["s"].values[0] is not None:

            azufre.send_keys(muestras_d["s"].values[0].replace(",", "."))

        if muestras_d["clasificacion"].values[0] is not None:
            id = texturas_[muestras_d["clasificacion"].values[0]]
            textura.select_by_value(id)

        else:
            textura.select_by_value("0")

        OpcionFertilizanteS.select_by_value("0")
        OpcionFertilizanteS.select_by_value("1")

        opcionFertilizanteCompuesto.select_by_value("21")
        opcionFertilizanteCompuesto.select_by_value("22")
        opcionFertilizanteCompuesto.select_by_value("23")

        action = webdriver.ActionChains(driver)
        action.move_to_element(azufre)
        action.perform()
        azufre.click()

        action = ActionChains(driver)

        # First, go to your start point or Element:
        action.move_to_element(reportar)
        action.perform()

        for mouse_x, mouse_y in zip(x_i[:5], y_i[:5]):
            # Here you should reset the ActionChain and the 'jump' wont happen:
            action = ActionChains(driver)
            action.move_by_offset(mouse_x, mouse_y)
            action.perform()

        reportar.click()

        time.sleep(1)

        driver.switch_to.window(driver.window_handles[1])
        enviar = driver.find_element(by=By.NAME, value="enviar")
        enviar.click()
        window_before = driver.window_handles[0]
        print(len(driver.window_handles))
        driver.switch_to.window(driver.window_handles[2])
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(window_before)
    print("Proceso Finalizado")
    driver.quit()
