@ Dark Necrofear (ID 5222), fn_18: elige el monstruo rival que va a poseer.
@ La funcion de su fila (0x08052BE0, compartida con Snatch Steal, Change of Heart y Jowls of Dark
@ Demise) ya trae el caso de Necrofear: "Select and gain control of 1 opponent's face-up monster.",
@ y para la IA elige sola. La receta de prueba la anulaba porque no habia quien la usara.
@
@ Aca solo se la deja correr cuando el pedido es el de la posesion en la End Phase, que encola
@ efectos/gancho_fin_necrofear.s: tipo de efecto 4 ((p[1] >> 1) & 0xF) y momento 5
@ ((cabecera >> 13) & 0x3F; el 5 es el de los efectos de End Phase del motor), o sea
@ (cabecera & 0x7FE00) == 0xA800.
@ El motor dispara ademas por su cuenta el efecto de Necrofear apenas es destruida (tipo 4,
@ otro momento): con la fn_18 original a secas el aviso salia en plena Battle Phase y el control
@ se tomaba ahi mismo, no en la End Phase [PROBADO]. Para ese pedido, y para cualquier otro,
@ devuelve 1: no hay nada que elegir.
@ La receta ademas quita ese disparo del motor (B:0801786E, un beq del arbol de IDs): la carta ya
@ no se muestra al ser destruida. La guarda de aca queda igual, por si el parche no esta.
@ ORIGINAL = fn_18 original (con bit Thumb).

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r1, [r0]
    ldr   r2, =0x0007FE00
    ands  r1, r2
    ldr   r2, =0x0000A800         @ tipo de efecto 4, momento 5
    cmp   r1, r2
    beq   .Lposesion
    movs  r0, #1
    bx    lr
.Lposesion:
    ldr   r1, =ORIGINAL
    bx    r1
    .align 2
    .pool
