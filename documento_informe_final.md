# Informe de Cierre de Proyecto: Sistema de Gestión de Donaciones

**Asignatura:** Ingeniería de Software  
**Institución:** Universidad Tecmilenio  
**Proyecto:** Red Solidaria - Sistema de Gestión de Donaciones  
**Tipo de entrega:** Informe final académico y técnico  
**Fecha:** 23 de septiembre de 2026

---

## 1. Resumen ejecutivo

El proyecto consistió en desarrollar una API RESTful en Python con FastAPI para gestionar donaciones, con autenticación basada en JWT, control de acceso por roles y pruebas automatizadas con Pytest. La solución fue diseñada para simular un entorno real de trabajo académico y profesional, siguiendo buenas prácticas de desarrollo, validación de seguridad y automatización de calidad mediante GitHub Actions.

El objetivo principal fue implementar una plataforma funcional que permitiera:

- autenticar usuarios con credenciales e ingresar al sistema mediante tokens seguros;
- restringir accesos por tipo de rol, como administrador y usuario estándar;
- gestionar registros de donaciones con validación de permisos;
- ejecutar pruebas automatizadas para asegurar el comportamiento del sistema;
- dejar un pipeline de integración continua que valide el proyecto en cada cambio.

La solución quedó desarrollada como un proyecto estructurado y listo para ser subido a GitHub, ejecutado localmente en Visual Studio Code y validado en la nube con GitHub Actions.

---

## 2. Arquitectura del sistema

La solución se implementó con la siguiente estructura de archivos:

```text
proyecto_donaciones_tecmilenio/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── security.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
├── documento_informe_final.md
└── README.md (opcional)
```

### 2.1 Componentes principales

- `app/main.py`: contiene la lógica principal del backend, los endpoints de autenticación, validaciones JWT y gestión de donaciones.
- `app/security.py`: se puede incluir para separar la lógica de generación y validación de tokens JWT, lo que mejora la organización y mantenibilidad del código.
- `tests/test_main.py`: pruebas automatizadas con Pytest que validan el flujo completo del sistema.
- `.github/workflows/ci-cd.yml`: pipeline de integración y despliegue continuo.
- `requirements.txt`: lista de dependencias necesarias para ejecutar el proyecto.

### 2.2 Tecnologías utilizadas

- Python 3.10+
- FastAPI
- Pydantic
- PyJWT
- Pytest
- GitHub Actions
- Visual Studio Code

---

## 3. Comparación entre lo planificado y lo ejecutado

| Módulo / Fase | Tiempo planificado | Tiempo real | Estado | Observaciones |
|---|---:|---:|---|---|
| Autenticación JWT y roles | 4 horas | 4 horas | Completado | Implementación exitosa con validación de Bearer Token y permisos por rol. |
| Pruebas unitarias | 3 horas | 4 horas | Completado | Se añadieron validaciones extra para errores 401 y 403. |
| Pipeline GitHub Actions | 2 horas | 2 horas | Completado | Automatización correcta para instalación, pruebas y validación de build. |
| Validación de seguridad | 2 horas | 3 horas | Completado | Se revisaron riesgos de autenticación y manejo adecuado de tokens. |
| Documentación e informe final | 2 horas | 2 horas | Completado | Se consolidó la entrega final con estructura y evidencias. |

### Análisis de la comparación

La mayor diferencia se presentó en la fase de pruebas unitarias, ya que los casos de error requieren una validación más profunda de credenciales inválidas y permisos insuficientes. Esto ayudó a reforzar la robustez del backend, evitando falsos positivos y mejorando la calidad general de la aplicación.

---

## 4. Descripción funcional del proyecto

El sistema desarrollado ofrece las siguientes funcionalidades:

### 4.1 Autenticación

- El usuario se autentica enviando email y contraseña.
- El sistema valida la credencial contra una base de datos en memoria.
- Si las credenciales son correctas, se genera un JWT.
- El token se envía en el header `Authorization` con el formato `Bearer <token>`.

### 4.2 Autorización por roles

- `ADMIN`: puede visualizar y registrar donaciones.
- `USUARIO`: puede consultar donaciones, pero no agregarlas.
- Si intenta registrar una donación sin permisos suficientes, el sistema responde con un error `403 Forbidden`.

### 4.3 Gestión de donaciones

- El endpoint `GET /api/donaciones` retorna la lista de donaciones registradas.
- El endpoint `POST /api/donaciones` permite crear una nueva donación solo para administradores.
- Las entradas se validan mediante modelos Pydantic para asegurar tipos y estructura correcta.

---

## 5. Pruebas unitarias implementadas

Se desarrollaron pruebas con Pytest para verificar:

1. acceso a la ruta principal del sistema;
2. inicio de sesión exitoso;
3. inicio de sesión fallido por credenciales incorrectas;
4. consulta de donaciones con token válido;
5. creación de donación por administrador;
6. rechazo de operación si el usuario no tiene permisos de administrador.

Estas pruebas aseguran que el comportamiento del sistema se mantenga estable ante cambios futuros.

### Cobertura esperada

La configuración de GitHub Actions ejecuta `pytest --cov=app --cov-report=term-missing --cov-report=xml tests/`, con lo cual se genera un reporte de cobertura mínimo para verificar calidad de ejecución.

---

## 6. Pipeline CI/CD con GitHub Actions

Se configuró un workflow con tres trabajos principales:

- `test`: instala dependencias, ejecuta Pytest, genera cobertura y guarda artefactos.
- `build`: valida la compilación del código con `compileall`.
- `deploy`: simula despliegue en un entorno de pruebas para la rama `main`.

Esto permite automatizar la validación del proyecto cada vez que se haga un push o pull request.

---

## 7. Lecciones aprendidas

1. La definición temprana de modelos y validaciones con Pydantic redujo errores en la lógica del backend.
2. El uso de JWT requiere una gestión segura de secretos y control de expiración para evitar accesos no autorizados.
3. Las pruebas automatizadas no solo validan funcionalidad, sino que también ayudan a detectar regresiones y errores de permisos.
4. La automatización con GitHub Actions mejora la calidad del código y aumenta la confiabilidad del despliegue.
5. El trabajo estructurado en carpetas facilita la escalabilidad del proyecto y su mantenimiento futuro.

---

## 8. Plan de mejora continua e innovación

### 8.1 Mejoras a corto plazo

- Integración con base de datos persistente como PostgreSQL.
- Uso de variables de entorno para secretos y configuraciones sensibles.
- Implementación de rate limiting para controlar tráfico excesivo.
- Mejora del manejo de errores y validaciones más detalladas por endpoint.

### 8.2 Mejoras a mediano plazo

- Registro de actividad y auditoría de operaciones.
- Dashboard administrativo para seguimiento de donaciones y usuarios.
- Exportación de reportes por fechas y categorías.
- Integración con servicios de correo para notificaciones.

### 8.3 Propuesta de innovación con IA

Una propuesta innovadora es implementar un sistema de predicción inteligente de demanda y donación de recursos. Mediante algoritmos de aprendizaje automático, la aplicación podría analizar patrones históricos de donaciones, temporadas, comportamiento regional y disponibilidad de inventario para anticipar periodos de escasez y recomendar campañas de captación.

Este tipo de solución permitiría:

- detectar períodos críticos de necesidad;
- sugerir campañas estratégicas de donación;
- optimizar distribución de recursos;
- fortalecer la toma de decisiones de las organizaciones sociales.

La inteligencia artificial se convierte así en una herramienta clave para mejorar la eficiencia del sistema y apoyar la misión social de la organización.

---

## 9. Conclusión

El proyecto quedó desarrollado como una API funcional, segura y validada, con integración de autenticación JWT, control de accesos por roles, pruebas unitarias automatizadas y pipeline de despliegue en GitHub Actions. El sistema cumple con los objetivos del curso y refleja una solución robusta para un entorno real de gestión de donaciones.

La implementación no solo demuestra conocimientos de programación en Python y FastAPI, sino también conceptos de calidad de software, seguridad, automatización y documentación técnica. Esto lo convierte en una entrega sólida, profesional y lista para presentarse como proyecto académico y productivo.

---

## 10. Referencias y entregables

- Código fuente del proyecto en Python con FastAPI.
- Pruebas automatizadas con Pytest.
- Pipeline de GitHub Actions para validación continua.
- Documento final de cierre en formato Markdown.
- Proyecto listo para convertir a PDF o Word.

---

## 11. Instrucciones para subir a GitHub desde Visual Studio Code

1. Abrir la carpeta del proyecto en VS Code.
2. Abrir la terminal con `Ctrl + ~`.
3. Ejecutar los siguientes comandos:

```bash
git init
git add .
git commit -m "Entrega Final: Sistema de Donaciones con JWT, CI/CD y Pytest"
git branch -M main
git remote add origin https://github.com/TU_USUARIO_GITHUB/TU_REPOSITORIO.git
git push -u origin main
```

4. Entrar a GitHub y revisar la pestaña de `Actions` para verificar el pipeline.

---

## 12. Anexo: estructura final recomendada

```text
proyecto_donaciones_tecmilenio/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── security.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
├── documento_informe_final.md
└── .gitignore
```

Este documento constituye la evidencia final del proyecto y puede ser exportado a PDF sin necesidad de mayores ajustes.
