@ Two-Pronged Attack (ID 4839): se destruyen 2 monstruos propios y 1 del rival, elegidos.
@
@ El fn_04 original solo validaba las tres elecciones (leyendo p[9..11] como lado/zona, formato
@ viejo) y despues recorria un bucle vacio: nunca destruia nada. fn_18 (la seleccion) si anda y
@ deja en p[9..11] los ids de ranura (bit 7 = lado) y en p[8] & 0xF la cantidad elegida.
@ Esta funcion, con las 3 elegidas, comprueba que las dos primeras sean propias y distintas y
@ la tercera del rival, y manda las tres al cementerio con FUN_08018518(lado, id, esta carta).
@ Simbolos: A_CEMENTERIO.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrb  r0, [r4, #8]
    movs  r1, #0xf
    ands  r0, r1
    cmp   r0, #3
    bne   .Lfin                   @ faltan elecciones
    ldrb  r5, [r4]
    movs  r1, #1
    ands  r5, r1                  @ r5 = mi lado
    ldrb  r0, [r4, #9]
    ldrb  r1, [r4, #10]
    ldrb  r2, [r4, #11]
    cmp   r0, #0xff
    beq   .Lfin
    cmp   r1, #0xff
    beq   .Lfin
    cmp   r2, #0xff
    beq   .Lfin
    cmp   r0, r1
    beq   .Lfin                   @ las dos propias deben ser distintas
    lsrs  r3, r0, #7
    cmp   r3, r5
    bne   .Lfin
    lsrs  r3, r1, #7
    cmp   r3, r5
    bne   .Lfin
    lsrs  r3, r2, #7
    cmp   r3, r5
    beq   .Lfin                   @ la tercera debe ser del rival
    ldrh  r6, [r4]
    lsls  r6, r6, #23
    lsrs  r6, r6, #24             @ r6 = ranura de esta carta
    movs  r7, #0                  @ r7 = indice 0..2
.Lbucle:
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r1, [r1, r7]            @ id a destruir
    adds  r0, r5, #0
    adds  r2, r6, #0
    ldr   r3, =A_CEMENTERIO
    mov   ip, r3
    bl    .Lllamar
    adds  r7, #1
    cmp   r7, #3
    blt   .Lbucle
.Lfin:
    movs  r0, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    ip
    .align 2
    .pool
