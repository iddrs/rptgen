from enum import Enum

from typeguard import typechecked


@typechecked
class Escopo(Enum):
    PM = 'pm'
    RPPS = 'fpsm'
    FPSM = RPPS
    CM = 'cm'
    MUN = 'mun'
    LEG = CM
    EXEC = 'exec'

    @classmethod
    def names(cls) -> list[str]:
        return ['pm', 'fpsm', 'cm', 'mun', 'leg', 'exec']

    def __str__(self):
        return f'{self.value}'

    def get_entidade(self):
        if self.value == 'pm':
            return ['pm']
        if self.value == 'cm':
            return ['cm']
        if self.value == 'mun':
            return ['pm', 'cm', 'fpsm']
        if self.value == 'rpps':
            return ['fpsm']
        if self.value == 'fpsm':
            return ['fpsm']
        if self.value == 'leg':
            return ['cm']
        if self.value == 'exec':
            return ['pm', 'fpsm']
