@ Gancho en el procesador de acciones (FUN_08016C36, 0x080171B0): Dark Necrofear equipada deja
@ el campo.
@
@ Despues de mover cada carta, el procesador mira su ID en un arbol chico. Para Snatch Steal
@ (0x1322), si la carta esta en la zona de Magicas y Trampas (zona 5) y tiene un monstruo
@ equipado (ranura+0x3C) que sigue en el campo bajo el control de quien controla el equipo, lo
@ devuelve al otro lado con FUN_0801A8A4 (o lo manda al cementerio si no hay zona libre). Es todo
@ lo que hace falta para la Necrofear que efectos/necrofear_posesion.s dejo equipada.
@
@ El gancho pisa las 4 instrucciones que leen el ID,
@     ldr r5, =0x087A8624 ; adds r0, r0, r5 ; ldrh r1, [r0] ; ldr r0, =0x1432
@ las repite y, si el ID es el de Necrofear (5222), le pasa al arbol el de Snatch Steal. Sigue en
@ 0x080171B8. El arbol solo se usa para esa devolucion (y para Ground Collapse y 0x17EE, que no
@ cambian): Necrofear no hereda nada mas de Snatch Steal. En la zona de monstruos (zona 0) la rama
@ no hace nada, porque pide zona 5.
@
@ Entrada: r0 = indice * 2, r2 = 0x02022250 y r3 = 0x2B08 (los usa lo que sigue), r4 = 0x80,
@ r7 = 0x7F, r8 = ranura de la carta. El salto del gancho piso r3: se repone. No se puede tocar
@ ningun otro registro; se vuelve por ip.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r5, =0x087A8624         @ indice -> ID de Konami
    adds  r0, r0, r5
    ldrh  r1, [r0]
    ldr   r0, =5222               @ Dark Necrofear
    cmp   r1, r0
    bne   .Lseguir
    ldr   r1, =0x1322             @ como Snatch Steal
.Lseguir:
    ldr   r3, =0x00002B08
    ldr   r0, =0x080171B9
    mov   ip, r0
    ldr   r0, =0x1432
    bx    ip
    .align 2
    .pool
