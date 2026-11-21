"""Reglas de la partida, independientes de cualquier interfaz."""

from __future__ import annotations

from enum import Enum

from .generadores import Generador


class Resultado(Enum):
    """Resultado de un intento."""

    MAYOR = "mayor"  # el numero secreto es mayor que el intento
    MENOR = "menor"  # el numero secreto es menor que el intento
    GANASTE = "ganaste"
    PERDISTE = "perdiste"


class PartidaNoIniciadaError(RuntimeError):
    """Se intento jugar antes de llamar a ``nueva_partida``."""


class PartidaTerminadaError(RuntimeError):
    """Se intento jugar una partida ya ganada o perdida."""


class Juego:
    """Contexto del patron Strategy.

    La eleccion del numero secreto se delega en el ``Generador`` inyectado
    por el constructor. El resto de las reglas (intentos, pistas, fin de
    partida) viven aqui y no saben nada de la consola.
    """

    def __init__(
        self,
        generador: Generador,
        *,
        minimo: int = 1,
        maximo: int = 100,
        max_intentos: int = 7,
    ) -> None:
        if minimo >= maximo:
            raise ValueError("'minimo' debe ser menor que 'maximo'")
        if max_intentos < 1:
            raise ValueError("'max_intentos' debe ser al menos 1")

        self._generador = generador
        self.minimo = minimo
        self.maximo = maximo
        self.max_intentos = max_intentos
        self._objetivo: int | None = None
        self._resultado: Resultado | None = None
        self.intentos = 0

    def nueva_partida(self) -> None:
        """Genera un numero secreto nuevo y reinicia los intentos."""
        self._objetivo = self._generador.obtener(self.minimo, self.maximo)
        self._resultado = None
        self.intentos = 0

    @property
    def objetivo(self) -> int:
        """Numero secreto de la partida en curso."""
        if self._objetivo is None:
            raise PartidaNoIniciadaError(
                "Llama a 'nueva_partida' antes de consultar el objetivo"
            )
        return self._objetivo

    @property
    def en_curso(self) -> bool:
        """``True`` mientras queden intentos y nadie haya acertado."""
        return self._objetivo is not None and self._resultado is None

    @property
    def intentos_restantes(self) -> int:
        return max(0, self.max_intentos - self.intentos)

    @property
    def resultado(self) -> Resultado | None:
        """Resultado final de la partida, o ``None`` si sigue en curso."""
        return self._resultado

    def adivinar(self, numero: int) -> Resultado:
        """Registra un intento y devuelve el resultado."""
        if self._objetivo is None:
            raise PartidaNoIniciadaError(
                "Llama a 'nueva_partida' antes de adivinar"
            )
        if self._resultado is not None:
            raise PartidaTerminadaError("La partida ya termino")
        if not self.minimo <= numero <= self.maximo:
            raise ValueError(
                f"El numero debe estar entre {self.minimo} y {self.maximo}"
            )

        self.intentos += 1

        if numero == self._objetivo:
            self._resultado = Resultado.GANASTE
            return self._resultado
        if self.intentos >= self.max_intentos:
            self._resultado = Resultado.PERDISTE
            return self._resultado
        return Resultado.MAYOR if numero < self._objetivo else Resultado.MENOR
