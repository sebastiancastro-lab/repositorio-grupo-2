# SMSV – Sistema de Monitoreo de Signos Vitales (API REST)

**Práctica #1 – Ingeniería de Software · Bioingeniería · Universidad de Antioquia · 2026-II**

API REST construida con **Django** y **Django REST Framework** y base de datos **MySQL**. Centraliza pacientes, tipos de signos vitales, dispositivos de medición y los registros que los relacionan. Todas las respuestas son JSON y CORS está habilitado (`django-cors-headers`) para que cualquier frontend (Vue, React, etc.) pueda consumirla.

## Equipo

| Integrante | Recurso | Rama |
| --- | --- | --- |
| Paula Andrea Castaño | Paciente | `feature/paciente` |
| Lizeth Giraldo | TipoSigno | `feature/tipo-signo` |
| Todos | Dispositivo | `feature/dispositivo` |
| Juan Sebastian Castro | RegistroSigno | `feature/registro-signo` |

## Estructura del proyecto

```
repositorio-grupo-2/
├── manage.py
├── requirements.txt
├── index.html                  # Frontend de prueba (opcional, consume la API)
├── config/                     # Configuración de Django (settings, urls)
└── api/
    ├── models.py               # Paciente, TipoSigno, Dispositivo, RegistroSigno
    ├── serializers.py          # Validaciones y relaciones anidadas
    ├── views.py                # ViewSets (CRUD) y filtros
    ├── urls.py                 # Router de DRF
    ├── admin.py
    ├── tests.py                # Pruebas automáticas
    ├── migrations/
    └── fixtures/
        └── datos_iniciales.json  # Datos precargados
```

## Instalación

**Requisitos:** Python 3.12+, Git y XAMPP (Apache + MySQL).

1. Clonar el repositorio:

   ```powershell
   git clone https://github.com/sebastiancastro-lab/repositorio-grupo-2.git
   cd repositorio-grupo-2
   ```

2. Crear y activar el entorno virtual:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Instalar dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

4. Abrir **XAMPP** e iniciar **Apache** y **MySQL**.
5. Entrar a phpMyAdmin (`http://localhost/phpmyadmin`) y crear una base de datos **vacía** llamada exactamente `bd_grupo_2` (cotejamiento `utf8mb4_general_ci`).
6. Crear las tablas:

   ```powershell
   python manage.py migrate
   ```

7. Cargar los datos de ejemplo (BD precargada):

   ```powershell
   python manage.py loaddata datos_iniciales
   ```

8. Iniciar el servidor:

   ```powershell
   python manage.py runserver
   ```

La API queda en `http://127.0.0.1:8000/api/`. Se puede probar con la interfaz navegable de DRF (abrir la URL en el navegador), con Postman, o abriendo `index.html` en el navegador.

> Si MySQL tiene contraseña, se cambia en `config/settings.py` → `DATABASES['default']['PASSWORD']`.

## Base de datos precargada

El archivo `api/fixtures/datos_iniciales.json` contiene:

| Recurso | Cantidad |
| --- | --- |
| Pacientes | 5 |
| Tipos de signo | 4 (frecuencia cardíaca, presión arterial sistólica, temperatura, saturación de oxígeno) |
| Dispositivos | 4 (3 activos y 1 en mantenimiento) |
| Registros de signos | 14 (incluye valores normales, altos y bajos) |

Se carga con `python manage.py loaddata datos_iniciales` sobre una base de datos recién migrada (usa ids fijos, así que si ya hay datos con los mismos ids se sobrescriben).

**Respaldo SQL (opcional):** después de cargar los datos, en phpMyAdmin → base `bd_grupo_2` → **Exportar** → método *Rápido* → formato *SQL* → guardar como `database/bd_grupo_2.sql` y subirlo al repositorio.

## Endpoints

Prefijo común: `http://127.0.0.1:8000/api`

### Pacientes

| Método | URL | Descripción |
| --- | --- | --- |
| GET | `/api/pacientes/` | Lista todos los pacientes |
| POST | `/api/pacientes/` | Crea un paciente |
| GET | `/api/pacientes/{id}/` | Detalle de un paciente |
| PUT | `/api/pacientes/{id}/` | Actualiza un paciente (todos los campos) |
| PATCH | `/api/pacientes/{id}/` | Actualiza parcialmente un paciente |
| DELETE | `/api/pacientes/{id}/` | Elimina un paciente (409 si tiene registros asociados) |

### Tipos de signo

| Método | URL | Descripción |
| --- | --- | --- |
| GET | `/api/tipos-signo/` | Lista el catálogo de signos vitales |
| POST | `/api/tipos-signo/` | Crea un tipo de signo (nombre único; mínimo < máximo) |
| GET | `/api/tipos-signo/{id}/` | Detalle de un tipo de signo |
| PUT | `/api/tipos-signo/{id}/` | Actualiza un tipo de signo (todos los campos) |
| PATCH | `/api/tipos-signo/{id}/` | Actualiza parcialmente un tipo de signo |
| DELETE | `/api/tipos-signo/{id}/` | Elimina un tipo de signo (409 si tiene registros asociados) |

### Dispositivos

| Método | URL | Descripción |
| --- | --- | --- |
| GET | `/api/dispositivos/` | Lista dispositivos. Filtro opcional: `?estado=activo` |
| POST | `/api/dispositivos/` | Crea un dispositivo (`numero_serie` único; `estado` válido) |
| GET | `/api/dispositivos/{id}/` | Detalle de un dispositivo |
| PUT | `/api/dispositivos/{id}/` | Actualiza un dispositivo (todos los campos) |
| PATCH | `/api/dispositivos/{id}/` | Actualiza parcialmente (por ejemplo, cambiar el estado) |
| DELETE | `/api/dispositivos/{id}/` | Elimina un dispositivo (409 si tiene registros asociados) |

Estados permitidos: `activo`, `en mantenimiento`, `fuera de servicio`.

### Registros de signos

| Método | URL | Descripción |
| --- | --- | --- |
| GET | `/api/registros/` | Lista registros con paciente, tipo de signo y dispositivo anidados. Filtros opcionales: `?paciente=1&tipo_signo=2&dispositivo=3` |
| POST | `/api/registros/` | Crea un registro (el dispositivo debe estar `activo`) |
| GET | `/api/registros/{id}/` | Detalle de un registro |
| PUT | `/api/registros/{id}/` | Actualiza un registro (todos los campos) |
| PATCH | `/api/registros/{id}/` | Actualiza parcialmente un registro |
| DELETE | `/api/registros/{id}/` | Elimina un registro |

**Ejemplo `POST /api/registros/`**

```json
{
  "paciente": 1,
  "tipo_signo": 1,
  "dispositivo": 1,
  "valor_medido": 78,
  "responsable": "Enf. Carolina Restrepo"
}
```

`fecha_hora` es opcional (si no se envía, se usa la fecha y hora actual) y no puede estar en el futuro.

**Ejemplo de respuesta** (la información de las relaciones va incluida):

```json
{
  "id": 14,
  "paciente": 5,
  "paciente_detalle": { "id": 5, "documento": "43876210", "nombres": "Gloria Inés", "apellidos": "Vélez Zapata", "edad": 72, "genero": "Femenino", "eps": "Compensar" },
  "tipo_signo": 3,
  "tipo_signo_detalle": { "id": 3, "nombre": "Temperatura Corporal", "unidad_medida": "°C", "valor_min_normal": 36.1, "valor_max_normal": 37.2 },
  "dispositivo": 3,
  "dispositivo_detalle": { "id": 3, "nombre": "Termómetro infrarrojo", "marca": "Braun", "modelo": "ThermoScan 7", "numero_serie": "BR-IRT6520-0310", "estado": "activo" },
  "valor_medido": 36.4,
  "estado_valor": "normal",
  "fecha_hora": "2026-10-01T06:50:00-05:00",
  "responsable": "Enf. Julián Osorio"
}
```

`estado_valor` es un campo calculado: `bajo`, `normal` o `alto` según el rango del tipo de signo.

## Reglas de validación

| Recurso | Regla | Respuesta |
| --- | --- | --- |
| TipoSigno | `nombre` único; `valor_min_normal` < `valor_max_normal` | 400 |
| Dispositivo | `numero_serie` único; `estado` ∈ {activo, en mantenimiento, fuera de servicio} | 400 |
| RegistroSigno | Dispositivo `activo` al crear o al cambiar de dispositivo | 400 |
| RegistroSigno | `valor_medido` ≥ 0, `fecha_hora` no futura, `responsable` obligatorio | 400 |
| Paciente / TipoSigno / Dispositivo | No se pueden eliminar si tienen registros de signos asociados (protege el historial) | 409 |

## Pruebas

```powershell
python manage.py test
```

Django crea una base de datos temporal `test_bd_grupo_2` en MySQL y la elimina al terminar. Las pruebas cubren el CRUD de TipoSigno, Dispositivo y RegistroSigno, las validaciones anteriores, las relaciones anidadas y que la BD precargada cumpla el mínimo del enunciado.

## Flujo de trabajo en Git

Nadie trabaja directamente sobre `main`.

```powershell
git checkout main
git pull origin main
git checkout -b feature/nombre-de-su-tarea
# ... cambios ...
git add .
git commit -m "feat: descripción del cambio"
git push origin feature/nombre-de-su-tarea
```

Luego se abre un **Pull Request** en GitHub para revisión cruzada antes de unir a `main`. Cada vez que cambie `api/models.py`: `python manage.py makemigrations` y `python manage.py migrate`.