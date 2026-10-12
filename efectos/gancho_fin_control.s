@ Gancho en la End Phase (FUN_08065BF8, 0x08065D20): "este monstruo vuelve ahora a su dueno".
@ El original pregunta por la bandera 0x15 del monstruo (la que pone Change of Heart) y, si
@ esta, devuelve el control con FUN_0801A8A4. El gancho pisa las 3 instrucciones
@     movs r1, #0x15 ; bl FUN_0800E158 ; lsls r0, r0, #0x10
@ y sigue en 0x08065D28 (cmp r0, #0) con el mismo resultado en r0, salvo que ademas contesta
@ que si cuando el monstruo tiene una entrada de modificador de tipo 5 con origen en
@ Electromagnetic Bagworm (ID 5040; la deja efectos/bagworm_control.s) y:
@   - el turno que termina es de quien lo controla,
@   - lo controla alguien que no es su dueno (el traspaso solo puede ser una devolucion), y
@   - la entrada no esta marcada "saltear" (nibble alto del tipo): si lo esta, se desmarca.
@ Al devolverlo quita la entrada con FUN_0800F050(ranura, 5).
@
@ Entrada: r0 = r4 = id de ranura del monstruo. Puede usar r0-r3, ip y lr.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    movs  r1, #0x15
    ldr   r3, =0x0800E159         @ FUN_0800E158(ranura, bandera)
    bl    .Lllamar
    lsls  r0, r0, #0x10
    bne   .Lvolver                @ bandera 0x15: como el original
    push  {r5, r6, r7}
    adds  r0, r4, #0
    bl    .Lranura
    adds  r5, r0, #0              @ r5 = ranura del monstruo
    adds  r0, #0x3e
    ldrb  r6, [r0]
    movs  r0, #0x0f
    ands  r6, r0                  @ r6 = cantidad de entradas
    movs  r7, #0
.Lbucle:
    cmp   r7, r6
    bge   .Lno
    lsls  r0, r7, #1
    adds  r0, #0x40
    ldrh  r1, [r5, r0]            @ entrada: tipo en el byte alto, ranura origen en el bajo
    lsrs  r2, r1, #8
    movs  r3, #0x0f
    ands  r2, r3
    cmp   r2, #5
    bne   .Lsiguiente
    movs  r0, #0xff
    ands  r0, r1
    bl    .Lranura
    ldrh  r0, [r0, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16             @ indice * 2
    ldr   r2, =0x087A8624         @ indice -> ID de Konami
    ldrh  r0, [r0, r2]
    ldr   r2, =5040               @ Electromagnetic Bagworm
    cmp   r0, r2
    beq   .Lhallada
.Lsiguiente:
    adds  r7, #1
    b     .Lbucle
.Lhallada:
    ldr   r2, [r5, #0x30]
    lsls  r2, r2, #12
    lsrs  r2, r2, #31             @ quien lo controla (bit 19)
    ldr   r3, =0x0202787E         @ J0 + 0x562E: bit 1 = jugador del turno
    ldrb  r3, [r3]
    lsls  r3, r3, #30
    lsrs  r3, r3, #31
    cmp   r2, r3
    bne   .Lno                    @ no es el turno de quien lo controla
    lsrs  r3, r4, #7              @ su dueno
    cmp   r2, r3
    beq   .Lno                    @ ya lo tiene su dueno
    lsrs  r2, r1, #12
    beq   .Lahora
    ldr   r2, =0x00000FFF         @ se activo en este mismo turno: cuenta desde el siguiente
    ands  r1, r2
    lsls  r0, r7, #1
    adds  r0, #0x40
    strh  r1, [r5, r0]
.Lno:
    pop   {r5, r6, r7}
    movs  r0, #0
    b     .Lvolver
.Lahora:
    adds  r0, r4, #0
    movs  r1, #5
    ldr   r3, =0x0800F051         @ FUN_0800F050(ranura, tipo): quita las entradas de ese tipo
    bl    .Lllamar
    pop   {r5, r6, r7}
    movs  r0, #1
    lsls  r0, r0, #0x10
.Lvolver:
    ldr   r3, =0x08065D29
    cmp   r0, #0                  @ deja las banderas como el lsls original
    bx    r3
.Lllamar:
    bx    r3

@ r0 = id de ranura (bit 7 = lado) -> r0 = direccion de la ranura. Usa r2, r3.
.Lranura:
    lsrs  r2, r0, #7
    movs  r3, #0x7f
    ands  r0, r3
    movs  r3, #0x50
    muls  r0, r3, r0
    ldr   r3, =0x00002B08
    muls  r3, r2, r3
    adds  r0, r0, r3
    ldr   r3, =0x02022250
    adds  r0, r0, r3
    bx    lr
    .align 2
    .pool
