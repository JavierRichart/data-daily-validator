# Data Daily Validator

## Objetivo

Automatizar validaciones sobre cierres diarios procedentes de un sistema ETRM y generar resultados claros para su revisión antes de preparar el informe diario.

## Estructura principal

```text
src/models.py                         Modelos de resultados
src/loader.py                         Carga de CSV y Excel
src/analyzer.py                       Ejecución conjunta de validadores
src/validators/                       Validadores independientes
tests/                                Pruebas automatizadas
data/closures.csv                     Datos de ejemplo
```

## Validadores implementados

- `RequiredFieldsValidator`: `REQUIRED_FIELD`
- `CommodityValidator`: `INVALID_COMMODITY`
- `BookValidator`: `INVALID_BOOK`
- `CommodityBookValidator`: `INVALID_COMMODITY_BOOK`
- `CompanyNameValidator`: `INVALID_COMPANY_NAME`
- `ContractDateRangeValidator`:
  - `INVALID_CONTRACT_DATE_FORMAT`
  - `INVALID_CONTRACT_DATE_RANGE`
  - `CONTRACT_DATE_OUT_OF_RANGE`

Todos devuelven una lista de `ValidationResult` y evitan modificar el `DataFrame` recibido.

## Ejecutar los tests

Desde la raíz del proyecto:

```bash
.venv/bin/python -m pytest -q
```

## Ejecutar la aplicación

Desde la raíz del proyecto:

```bash
.venv/bin/python app.py
```

La aplicación carga `data/closures.csv`, ejecuta los validadores configurados e imprime los errores encontrados.

## Limitaciones actuales

- Las reglas implementadas son reglas de ejemplo y deben ampliarse o ajustarse a la definición funcional definitiva.
- El proyecto todavía no está conectado a la fuente real de datos; actualmente utiliza archivos locales, incluido `data/closures.csv`.
