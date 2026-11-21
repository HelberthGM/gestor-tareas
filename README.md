# Juego de adivinar el número

Juego de consola en Python donde la computadora piensa un número y tú tienes
que descubrirlo con pistas de "mayor" o "menor". El objetivo del proyecto es
mostrar una arquitectura pequeña pero limpia, aplicando el patrón de diseño
**Strategy**.

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```bash
juego-numero                              # 1 a 100, 7 intentos
juego-numero --minimo 1 --maximo 50 -i 5  # rango e intentos personalizados
juego-numero --semilla 42                 # partida reproducible
python -m juego_numero                    # alternativa sin instalar el comando
```

Ejemplo:

```
Piensa un numero entre 1 y 100. Tienes 7 intentos.
[1/7] Tu numero: 50
El numero secreto es menor.
[2/7] Tu numero: 25
El numero secreto es mayor.
...
[6/7] Tu numero: 42
¡Correcto! Lo lograste en 6 intentos.
```

## Arquitectura

```
.
├── src/juego_numero/
│   ├── generadores.py   # Strategy: cómo se elige el número secreto
│   ├── juego.py         # Reglas de la partida (sin entrada/salida)
│   ├── consola.py       # Adaptador de consola + punto de entrada
│   └── __main__.py      # python -m juego_numero
└── tests/
    ├── test_generadores.py
    └── test_juego.py
```

| Capa | Responsabilidad | Depende de |
|---|---|---|
| `generadores` | Elegir el número secreto | Nada |
| `juego` | Intentos, pistas, fin de partida | `generadores` (abstracción) |
| `consola` | `input()`/`print()` y argumentos CLI | `juego`, `generadores` |

La lógica del juego no conoce ni la consola ni `random`, lo que permite
testearla de forma determinista y cambiar la interfaz sin tocarla.

## El patrón Strategy

`Juego` es el **contexto**: recibe un `Generador` por constructor y delega en
él la elección del número secreto. `Generador` es la **estrategia abstracta** y
`Aleatorio` / `Fijo` son las **estrategias concretas**.

```python
juego = Juego(Aleatorio())   # partida real
juego = Juego(Fijo(42))      # partida determinista para tests
```

Misma clase, comportamiento distinto: se elige por composición, sin `if` por
tipo y sin modificar `Juego` al agregar una estrategia nueva.

## Pruebas

```bash
pytest
ruff check .
```

## Autor

HelberthGM

## Licencia

Distribuido bajo la licencia GPL-3.0. Ver `LICENSE`.
