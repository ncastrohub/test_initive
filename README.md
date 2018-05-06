## Test Entrevista Intive

### Aclaraciones
* Las semanas se cuentan como semanas iniciadas, es decir, si son 9 dias, cuenta como 2 semanas.
* Todos los precios son parametrizables mediantes configuración, en esta implementación estan
definidos en variables globales pero podrian ser parte de un archivo de configuración.
* Es necesario Correr los test con python3.5.

### Coverage
El proyecto fue echo enteramente con TDD por lo que deberia estar
cubierto en  un 100% de test

### Diseño
#### El diseño esta basado en dos patrones basicos de objetos, Template Method y Composite.
* Template Method: lo usé para generalizar algunas cuestiones de validación y calculos que 
afectan a todas las reservas. Por ejemplo la diferencia entre la fecha inicial y la fecha final
* Composite: en este patron incluí la relacion entre las reservas "comunes" y las reservas familiares.
De esta manera, es trasparente para el que usa las clases el uso del metodo "final_price".

### Practicas
La principal herramienta de desarrollo de software que use fue TDD, basicamente transcribí los requerimientos
que me pasaron a test, y luego comence a escribir el modelo.
Por otro lado use patrones de diseño de objetos, no solo para que sea mejor el diseño, sino para que cualquiera 
que vea la implementación entienda rapidamente como esta echo, ya que todos conocemos los patrones de diseño.


### Correr los test

`python3 -m unittest test`

