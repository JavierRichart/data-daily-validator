# Data Daily Validator

## Objetivo

Este proyecto automatiza validaciones sobre cierres diarios procedentes de un sistema ETRM.

Debe detectar errores de datos y generar resultados claros que puedan revisarse antes de preparar el informe diario.

## Tecnologías

- Python
- pandas
- pytest

No añadir dependencias nuevas sin justificar su necesidad.

## Arquitectura

- `src/models.py`: modelos de resultados.
- `src/validators/`: validadores individuales.
- `src/run_validations.py`: ejecución conjunta de validadores.
- `tests/`: pruebas automatizadas.

Cada regla de negocio debe implementarse como un validador independiente.

## Validadores

Todos los validadores deben:

- heredar de `BaseValidator`;
- recibir un `DataFrame`;
- devolver una lista de `ValidationResult`;
- usar códigos de validación claros y estables;
- evitar modificar el `DataFrame` original.

## Calidad del código

Priorizar:

- simplicidad;
- nombres claros;
- funciones y clases pequeñas;
- tipado cuando aporte claridad;
- ausencia de código duplicado.

## Tests

Cada validador nuevo debe incluir pruebas para:

- datos válidos;
- datos inválidos;
- valores vacíos o nulos cuando corresponda;
- casos límite relevantes.

Antes de dar una tarea por terminada, ejecutar todos los tests.

## Reglas de negocio

No inventar reglas ni valores válidos.

Si una regla no está suficientemente definida, solicitar aclaración antes de implementarla.

## Al finalizar

Indicar:

- archivos modificados;
- comportamiento implementado;
- pruebas ejecutadas;
- posibles decisiones pendientes.