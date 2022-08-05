from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError
import re
import numpy as np


def Link(uri, label=None):
    """Transform string to be view as a link in terminal
    Args:
        uri (String): URL Link to convert
        label (String, optional): Label. Defaults to None.
    Returns:
        _type_: _description_
    """
    if label is None:
        label = uri
    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)


def ReturnStyle():
    """When used returns style dict for prompt
    Returns:
        dict: Style dict
    """

    style = style_from_dict(
        {
            Token.QuestionMark: "#E91E63 bold",
            Token.Selected: "#673AB7 bold",
            Token.Instruction: "",  # default
            Token.Answer: "#2196f3 bold",
            Token.Question: "",
        }
    )
    return style


class NumberValidator(Validator):
    """Validates if the propmt input is a int
    Args:
        Validator (_type_): input validator
    """

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message="Por favor ingrese un número",
                cursor_position=len(document.text),
            )  # Move cursor to end


class DensidadValidator(Validator):
    """Validates if the propmt input is a int
    Args:
        Validator (_type_): input validator
    """

    def validate(self, document):
        arreglo = np.arange(2000, 22000, 200)
        try:
            int(document.text)
            if int(document.text) not in arreglo:
                raise ValidationError(
                    message="Por favor ingrese una densidad válida",
                    cursor_position=len(document.text),
                )  # Move cursor to end
        except:
            raise ValidationError(
                message="Por favor ingrese una densidad válida",
                cursor_position=len(document.text),
            )  #


class SombrioValidator(Validator):
    """Validates if the propmt input is a int
    Args:
        Validator (_type_): input validator
    """

    def validate(self, document):
        arreglo = np.arange(0, 101, 1)
        try:
            int(document.text)
            if int(document.text) not in arreglo:
                raise ValidationError(
                    message="Por favor un sombrio válido",
                    cursor_position=len(document.text),
                )  # Move cursor to end
        except:
            raise ValidationError(
                message="Por favor ingrese una densidad válido",
                cursor_position=len(document.text),
            )  #


class EdadValidator(Validator):
    """Validates if the propmt input is a int
    Args:
        Validator (_type_): input validator
    """

    def validate(self, document):
        arreglo = np.arange(0, 1201, 1)
        try:
            int(document.text)
            if int(document.text) not in arreglo:
                raise ValidationError(
                    message="Por favor una edad válida",
                    cursor_position=len(document.text),
                )  # Move cursor to end
        except:
            raise ValidationError(
                message="Por favor ingrese una edad válida",
                cursor_position=len(document.text),
            )  #


class ExistValidator(Validator):
    """Validates if the propmt input exist
    Args:
        Validator (_type_): input validator
    """

    def validate(self, document):
        if not document.text:
            raise ValidationError(
                message="Please enter the value", cursor_position=len(document.text)
            )  # Move cursor to end


class MailValidator(Validator):
    """Validates if the propmt input is a email
    Args:
        Validator (_type_): input validator
    """

    def validate(self, document):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Regex email
        if not re.fullmatch(regex, document.text):
            raise ValidationError(
                message="Please enter a valid email address",
                cursor_position=len(document.text),
            )  # Move cursor to end
