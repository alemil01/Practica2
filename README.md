# Practica2
Practica 2 PRPA 22/23

Esta es la entrega para la Práctica 2 de la asignatura de Programación Paralela relacionada con el Puente de Ambite de Alejandro Millán Arribas. 

En el fichero practica2_AlejandroMillan.py se encuentra implementada una solución al problema del paso de peatones y coches en dos direcciones por el puente utilizando monitores. El número de vehículos y peatones que van a cruzar el puente es un parámetro que se puede modificar al principio del archivo, así como el tiempo que tarda cada uno en cruzar el puente. En principio no hay límite para el número de peatones y coches que pueden cruzar el puente a la vez, pero para que sea así es suficiente con descomentar los parámetros max_car y max_ped y la parte comentada en las funciones asociadas a las variables condición.

En el fichero Practica2_PuenteAmbite_AlejandroMillan.pdf se puede ver la solución implementada escrita a mano en pseudocódigo, además dde las respuestas a las siguientes cuestiones que se plantean:
  - Escribe el invariante del monitor
  - Demuestra que el puente es seguro
  - Demuestra la ausencia de deadlocks
  - Demuestra la ausencia de inanición
