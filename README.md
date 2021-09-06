# Promotions
Proyecto basal para gestión de campañas de sorteo en base a emails

## Arquitectura

Aplicación basada en micro servicios que cumplen los siguientes roles:

### Container Web
Contiene la aplicación Django y los endpoints expuestos para ser accedidos desde el cliente que soporte REST.

#### Endpoints

El proyecto se centra en la construcción de tres endpoints:
- POST - add_subscriber: Permite registrar a un usuario en el sorteo usando su email, con la limitante de que cada email se puede ingresar sólo una vez se debe enviar un email con el código para que funcione.
- GET - verify_subscriber: Verifica el email mediante en base a un código único generado a partir de la información entregada por el usuario, es un GET para poder ser agregada en un email.
- GET(Auth) - finish_campaign: Finaliza la campaña en el caso de que exista al menos un usuario con el email correctamente validado.

Se comunica con los workers mediante RabbitMQ usando el framework de tareas de Celery.

### Container Worker
Contiene un worker basado en Celery con acceso a los modelos de Django para el envío de correos de verificación.

#### Tasks

- Send validation email: Envia un correo de validación de usuario.
- Create subscriber (a evaluar por performance): Creación de un nuevo usuario en forma asíncrona.
- Finish Campaign (a evaluar por performance): Finalización de campaña en forma asíncrona con envío de correo al ganador y al administrador de la campaña. 

### Modelo
Se establecen dos clases principales para el proyecto:
#### Campaign 
Representa una campaña de sorteo, permite almacenar el estado de la campaña e información adicional tal cómo template del correo a enviar, etc, etc.
#### Subscriber
Representa un concursante de una determinada campaña la idea es que almacene los datos de contacto del usuario en forma flexible, email del usuario, token de verificación del correo y estado de la verificación.

### Consideraciones de performance:

Se usó una clase manager para gestionar la lógica de validación de modo de evitar acceder al ORM de Django para manejar la app. 
- Esto permitiría usar Redis o un cache para acceder a las campañas activas y a los emails de modo de poder disminuir el acceso a la BD que suele ser el principal cuello de botella.
- Permite enviar todos los procesos de escritura a BD al worker para poder ser ejecutados de forma asíncrona sin necesidad de cambios para la arquitectura del código.

