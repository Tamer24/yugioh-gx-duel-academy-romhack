@ PLANTILLA de una fn_04 (el efecto de una carta). No esta en ninguna receta: se copia con el
@ nombre de la carta, se completa y se agrega a recetas/lote.json como "ID:fn_04:efectos/x.s".
@ El recetario de acciones (que llamar para cada cosa) esta en ACCIONES.md.
@
@ Cabecera que tiene que llevar cada pieza: nombre e ID de la carta, su texto, que traia el ROM
@ (stub, funcion recortada, formato viejo...), de que carta original se tomo el molde y que
@ simbolos del motor usa.
@
@ Entrada: r0 = p, el pedido (12 bytes):
@   p[0] bit 0             lado que activa
@   (u16(p) & 0x1FF) >> 1  id de ranura de esta carta (bit 7 = lado)
@   (p[1] >> 1) & 0xF      tipo de efecto: 3 volteo, 4 disparador
@   p[2] bit 3             anulada
@   p[4]                   dato del disparador (atacante, quien la destruyo)
@   p[8] & 0xF, p[9..11]   cuantos objetivos eligio la fn_18 y sus ids de ranura
@ Salida: r0 = estado siguiente (0 = termino). El estado actual esta en 0x020204C6 y empieza en
@ 0x80; una funcion de un solo paso lo ignora y devuelve 0.
@ Los simbolos del motor (MOVER_CARTA, EQUIPAR, TOMAR_CONTROL, EVENTO_MOD, A_CEMENTERIO...) y
@ ORIGINAL (lo que habia en la columna) llegan definidos: ver MOTOR en scripts/parches.py.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = p
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrb  r7, [r4]
    movs  r0, #1
    ands  r7, r0                  @ r7 = lado que activa
    ldrh  r6, [r4]
    lsls  r6, r6, #23
    lsrs  r6, r6, #24             @ r6 = id de ranura de esta carta
    ldrb  r0, [r4, #8]
    movs  r1, #0xf
    ands  r0, r1
    cmp   r0, #1
    bne   .Lfin                   @ hace falta 1 objetivo elegido
    ldrb  r5, [r4, #9]            @ r5 = id de ranura del objetivo

    @ Comprobar el objetivo otra vez: entre la eleccion y la resolucion puede haber cambiado.
    adds  r0, r5, #0
    bl    .Lranura
    adds  r2, r0, #0              @ r2 = ranura del objetivo
    ldr   r0, [r2, #0x30]
    lsls  r1, r0, #13
    lsrs  r1, r1, #25             @ zona
    bne   .Lfin                   @ ya no esta en una zona de monstruo
    lsls  r0, r0, #12
    lsrs  r0, r0, #31             @ quien lo controla
    cmp   r0, r7
    beq   .Lfin                   @ tiene que ser del rival (sacar si el efecto es sobre los propios)
    adds  r2, #0x33
    ldrb  r0, [r2]
    lsls  r0, r0, #27
    bpl   .Lfin                   @ boca abajo

    @ --- ACA VA EL EFECTO. Ejemplo: destruir el objetivo. ---
    adds  r0, r7, #0
    adds  r1, r5, #0
    adds  r2, r6, #0
    ldr   r3, =A_CEMENTERIO       @ (lado, id, ranura de la carta que lo causa)
    bl    .Lllamar

.Lfin:
    movs  r0, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lranura:                         @ r0 = id de ranura -> r0 = direccion (usa r1 y r2)
    movs  r1, #0x7f
    ands  r1, r0
    movs  r2, #0x50
    muls  r1, r2, r1
    lsrs  r0, r0, #7
    ldr   r2, =0x00002B08
    muls  r0, r2, r0
    adds  r0, r0, r1
    ldr   r1, =0x02022250
    adds  r0, r0, r1
    bx    lr
.Lllamar:
    bx    r3
    .align 2
    .pool
