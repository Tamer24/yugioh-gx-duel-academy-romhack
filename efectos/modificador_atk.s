@ Modificador de ATK de Goddess of Whim para el calculador del motor (tipo 4 de la lista +0x40).
@
@ El motor recalcula el ATK de cada monstruo recorriendo su lista de modificadores
@ (cuenta en +0x3E & 0xF, entradas de u16 en +0x40: byte alto = tipo, byte bajo = ranura de la
@ carta que lo causa) y aplicando un caso por tipo (tabla de saltos en 0x08012C58, 15 tipos).
@ El tipo 4 es "efecto de una carta, segun el ID de la carta origen" (arbol de IDs en
@ 0x08013B4C: Rush Recklessly +700, etc.) y el motor lo borra solo al terminar el turno.
@ Goddess of Whim (ID 4435) no tiene caso en ese arbol (esta recortada).
@
@ Esta rutina ocupa la entrada del tipo 4 de la tabla y atiende dos cartas recortadas; para
@ cualquier otra salta al original:
@  - Goddess of Whim (4435): x2 (nibble alto del tipo = 1) o mitad (nibble = 2) sobre el ATK.
@    FUN_0801A5BC(lado, ranura, ranura, (nibble << 4) | 4)
@  - Riryoku (5009): el nibble es (lado << 3 | zona) del monstruo que PIERDE. En ese monstruo
@    el ATK se divide por 2; en el otro (el que gana) se suma el ATK del primero, ya reducido.
@    Dos eventos: FUN_0801A5BC(lado, ranura de Riryoku, destino, (nibble << 4) | 4)
@
@ Se entra por "mov pc, r0" dentro del calculador: R4 = indice de la carta origen, IP =
@ nibble alto del tipo, [sp+0x30] = mascara de estadisticas (bit 0 = ATK), r7 apunta al
@ resultado ([r7+4] = ATK). Solo r0-r3 e IP se pueden usar. Como los demas casos, avanza el
@ indice (r5 / SB) y sigue en 0x08013FE4.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r1, =0x087A8624         @ indice -> ID de Konami
    lsls  r0, r4, #1
    ldrh  r1, [r0, r1]
    ldr   r0, =5009               @ Riryoku
    cmp   r1, r0
    beq   .Lriryoku
    ldr   r0, =4435               @ Goddess of Whim
    cmp   r1, r0
    bne   .Loriginal
    ldr   r0, [sp, #0x30]
    movs  r1, #1
    ands  r0, r1                  @ se pidio el ATK?
    adds  r5, #1                  @ indice de la lista, como los demas casos
    mov   sb, r5
    cmp   r0, #0
    beq   .Lfin
    mov   r1, ip                  @ nibble alto del tipo
    ldr   r0, [r7, #4]
    cmp   r1, #1
    bne   .Lmitad
    lsls  r0, r0, #1
    b     .Lguardar
.Lmitad:
    cmp   r1, #2
    bne   .Lfin
    lsrs  r0, r0, #1
.Lguardar:
    str   r0, [r7, #4]
.Lfin:
    ldr   r0, =0x08013FE5
    bx    r0
.Lriryoku:
    ldr   r0, [sp, #0x30]
    movs  r1, #1
    ands  r0, r1                  @ se pidio el ATK?
    adds  r5, #1
    mov   sb, r5
    cmp   r0, #0
    beq   .Lfin
    mov   r1, ip                  @ nibble: lado << 3 | zona del que pierde
    lsrs  r2, r1, #3              @ lado
    movs  r3, #7
    ands  r1, r3                  @ zona
    movs  r3, #11
    muls  r3, r2, r3
    adds  r3, r3, r1
    ldr   r0, =0x02022250 + 0x5610
    ldrb  r0, [r0, r3]            @ id de ranura del que pierde
    cmp   r0, #0xff
    beq   .Lfin
    ldr   r1, [sp, #0x2c]         @ ranura que se esta calculando
    cmp   r0, r1
    bne   .Lsuma
    ldr   r0, [r7, #4]            @ es el que pierde: ATK / 2
    lsrs  r0, r0, #1
    str   r0, [r7, #4]
    b     .Lfin
.Lsuma:                           @ es el que gana: + ATK (ya reducido) del otro
    push  {lr}
    sub   sp, #0x20
    mov   r1, sp
    movs  r2, #1
    ldr   r3, =0x08012461         @ FUN_08012460(ranura, &salida, mascara)
    bl    .Lllamar
    ldr   r0, [sp, #4]
    add   sp, #0x20
    pop   {r1}
    mov   lr, r1
    ldr   r1, [r7, #4]
    adds  r1, r1, r0
    str   r1, [r7, #4]
    b     .Lfin
.Lllamar:
    bx    r3
.Loriginal:
    ldr   r0, =ORIGINAL           @ 0x08013B4C | 1
    bx    r0
    .align 2
    .pool
