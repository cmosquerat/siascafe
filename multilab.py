from pyfiglet import Figlet
from pyfiglet import Figlet
import six
from termcolor import colored
from PyInquirer import prompt
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError
from funciones import execute_orden
from styles import *
import os


def PrintHeader():
    """Prints CLI BIOS Header"""

    os.system("cls" if os.name == "nt" else "clear")  # Clears Console
    f = Figlet(font="slant")  # Define Header Font

    print(colored(f.renderText("AUTO SIASCAFE"), color="green"))
    print(
        colored(
            "Multilab Agroanalítica SAS\n \n",
            color="blue",
        )
    )

    print(
        colored(
            "Herramienta para automatizar el generado de reportes en SIASCAFÉ \n \ncmosquerat \\n",
            color="green",
        )
    )


PrintHeader()

questions = [
    {
        "type": "input",
        "name": "orden",
        "message": "Por favor ingrese el número de orden",
        "validate": NumberValidator,
    },
    {
        "type": "input",
        "name": "edad",
        "message": "Por favor la edad del cultivo",
        "validate": EdadValidator,
    },
    {
        "type": "list",
        "message": "Seleccione la etapa del cultivo",
        "name": "etapa",
        "choices": [
            Separator("=ETAPA="),
            {"name": "Producción"},
            {"name": "Crecimiento"},
            {"name": "Zoca"},
        ],
    },
    {
        "type": "input",
        "name": "densidad",
        "message": "Por favor la densidad del cultivo",
        "validate": DensidadValidator,
    },
    {
        "type": "input",
        "name": "sombrio",
        "message": "Por favor ingrese el porcentaje de sombrío",
        "validate": SombrioValidator,
    },
]
answers = prompt(questions, style=ReturnStyle())


execute_orden(
    answers["orden"],
    answers["etapa"],
    answers["edad"],
    answers["densidad"],
    answers["sombrio"],
)
