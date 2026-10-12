@ Neo-Spacian Air Hummingbird (ID 6769, carta nueva): una vez por turno, ganas 500 LP por cada
@ carta en la mano del rival.
@
@ Primera carta con efecto que el juego nunca tuvo: su fila de la tabla de efectos es nueva
@ (receta, "filas_efecto": columnas copiadas de Goddess of Whim, 4435, que ya se activa una vez
@ por turno desde el menu del campo) y esta funcion reemplaza su fn_04. Su ID esta en las dos
@ listas del menu del campo (gancho_lista_campo.s y gancho_menu_campo.s).
@
@ Molde: plantilla_fn04.s. Cuenta de la mano: ACCIONES.md, "Datos del lado".
@ Simbolos del motor: GANAR_LP(lado, cantidad).

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, lr}
    adds  r4, r0, #0              @ r4 = p
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1                  @ r0 = lado que activa
    adds  r5, r0, #0
    eors  r0, r1                  @ r0 = lado del rival
    ldr   r1, =0x00002B08
    muls  r0, r1, r0
    ldr   r1, =0x02022250
    adds  r1, r1, r0              @ datos del rival
    ldrb  r0, [r1, #0x1c]
    movs  r2, #0x3f
    ands  r0, r2
    lsls  r0, r0, #1
    ldrb  r2, [r1, #0x1b]
    lsrs  r2, r2, #7
    orrs  r0, r2                  @ cartas en la mano del rival
    beq   .Lfin
    movs  r1, #0xfa
    lsls  r1, r1, #1              @ 500
    muls  r1, r0, r1              @ cantidad
    adds  r0, r5, #0              @ lado
    ldr   r3, =GANAR_LP
    bl    .Lllamar
    @ Una vez por turno: quita la bandera 14 ("efecto de campo disponible") de esta carta con el
    @ evento 0x3C. Sin esto el menu la sigue ofreciendo (el original de Goddess lo hace solo).
    ldrh  r1, [r4]
    lsls  r1, r1, #23
    lsrs  r1, r1, #24             @ id de ranura de esta carta
    movs  r0, #0x3c
    movs  r2, #14
    ldr   r3, =EVENTO
    bl    .Lllamar
.Lfin:
    movs  r0, #0
    pop   {r4, r5}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    r3
    .align 2
    .pool
