@ Reasoning (ID 5530): "Your opponent declares a monster Level. Reveal cards from the top of your
@ Deck until you reveal a monster that can be Normal Summoned. If its Level is the declared one,
@ send all revealed cards to the Graveyard. If not, Special Summon it and send the rest to the
@ Graveyard."
@
@ El fn_04 original (0x08046B80) abre en 0x80 el menu de modo 9 para el rival y en 0x7F no hace
@ nada; ademas el manejador del modo 9 es un stub. Esta version lo reemplaza entero:
@   0x80  el rival declara un nivel. No hay menu: lo elige el juego (4 las mas de las veces, que
@         es el nivel mas comun) y queda en 0x020204C7. Avisa "Your opponent declares Level N."
@         y devuelve 0x7F.
@   0x7F  recorre mi mazo desde el tope hasta el primer monstruo que se puede Invocar de forma
@         Normal (no esta en la lista de FUN_080DD328: Fusion, Ritual y los de invocacion
@         especial obligada). Molde: Cyber Jar (original, 0x0803FA8C). Revela cada carta
@         (FUN_0801AB04), manda las anteriores al cementerio (FUN_08018518) y, con el monstruo:
@         nivel declarado, o Spirit (FUN_080DCE18: no admite invocacion especial) -> cementerio;
@         si no -> record_monster_set(lado, id, 1, 0) y devuelve 0x0A, como Monster Reborn.
@         Sin ningun monstruo asi en el mazo no hace nada.
@ La lista de cartas a revelar se copia antes de mover nada (el mazo se corre al sacar cartas).
@ Quien declara es siempre el juego, tambien si la carta la activa el rival.
@ Simbolos: AZAR, ASK_QUESTION, REVELAR, A_CEMENTERIO, INVOCAR, SOLO_ESPECIAL, ES_SPIRIT.

    .syntax unified
    .thumb
    .text
    .global _start
    .set MAXIMO, 64
_start:
    push  {r4, r5, r6, r7, lr}
    mov   r7, r8
    push  {r7}
    sub   sp, #MAXIMO
    adds  r4, r0, #0              @ r4 = carta
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lnada                  @ anulada
    ldr   r5, =0x020204C6         @ estado; el nivel declarado va en el byte siguiente
    ldrb  r0, [r5]
    cmp   r0, #0x80
    beq   .Ldeclarar
    cmp   r0, #0x7f
    beq   .Lresolver
.Lnada:
    movs  r0, #0
.Lfin:
    add   sp, #MAXIMO
    pop   {r3}
    mov   r8, r3
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

.Ldeclarar:
    ldr   r3, =AZAR
    bl    .Lllamar
    movs  r1, #7
    ands  r0, r1
    ldr   r1, =.Lniveles
    ldrb  r0, [r1, r0]
    strb  r0, [r5, #1]
    subs  r0, #2                  @ niveles 2..4 -> texto 0..2
    lsls  r0, r0, #2
    ldr   r1, =.Ltextos
    ldr   r0, [r1, r0]
    ldr   r3, =ASK_QUESTION
    bl    .Lllamar
    movs  r0, #0x7f
    b     .Lfin

.Lresolver:
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    mov   r8, r0                  @ r8 = mi lado
    ldr   r6, =0x00002B08
    muls  r6, r0, r6
    ldr   r0, =0x02022250
    adds  r6, r6, r0              @ r6 = base de mi lado
    ldrh  r7, [r6, #0x1c]
    lsls  r7, r7, #19
    lsrs  r7, r7, #25             @ r7 = cartas en mi mazo (bits 6-12)
    cmp   r7, #MAXIMO
    ble   .Lbuscar
    movs  r7, #MAXIMO
.Lbuscar:
    ldr   r0, =0x000028A4         @ lista del mazo: la primera es el tope
    adds  r6, r6, r0
    movs  r5, #0                  @ r5 = posicion
.Lsiguiente:
    cmp   r5, r7
    bge   .Lnada                  @ no hay monstruo que se pueda invocar de forma Normal
    ldrb  r0, [r6, r5]
    mov   r1, sp
    strb  r0, [r1, r5]
    bl    .Lindice
    lsls  r1, r0, #2
    ldr   r2, =0x08F243CC         @ estadisticas
    ldr   r1, [r2, r1]
    lsls  r1, r1, #7
    lsrs  r1, r1, #27             @ tipo
    cmp   r1, #0x15
    bge   .Lno_sirve              @ Magica o Trampa
    ldr   r3, =SOLO_ESPECIAL
    bl    .Lllamar
    cmp   r0, #0
    beq   .Lhallado
.Lno_sirve:
    adds  r5, #1
    b     .Lsiguiente

.Lhallado:                        @ sp[0..r5] = cartas reveladas; la ultima es el monstruo
    movs  r7, #0
.Lrevelar:
    mov   r0, r8
    mov   r1, sp
    ldrb  r1, [r1, r7]
    ldr   r3, =REVELAR
    bl    .Lllamar
    adds  r7, #1
    cmp   r7, r5
    ble   .Lrevelar
    movs  r7, #0
.Lal_cementerio:                  @ las anteriores al monstruo
    cmp   r7, r5
    bge   .Lmonstruo
    mov   r1, sp
    ldrb  r1, [r1, r7]
    bl    .Lcementerio
    adds  r7, #1
    b     .Lal_cementerio
.Lmonstruo:
    mov   r1, sp
    ldrb  r6, [r1, r5]            @ r6 = ranura del monstruo
    adds  r0, r6, #0
    bl    .Lindice
    adds  r7, r0, #0              @ r7 = su indice
    lsls  r1, r0, #2
    ldr   r2, =0x08F243CC
    ldr   r1, [r2, r1]
    lsls  r1, r1, #3
    lsrs  r1, r1, #28             @ nivel
    ldr   r2, =0x020204C7
    ldrb  r2, [r2]
    cmp   r1, r2
    beq   .Lmonstruo_fuera        @ acerto el nivel: todo al cementerio
    adds  r0, r7, #0
    ldr   r3, =ES_SPIRIT
    bl    .Lllamar
    cmp   r0, #0
    bne   .Lmonstruo_fuera        @ no admite invocacion especial
    mov   r0, r8
    adds  r1, r6, #0
    movs  r2, #1
    movs  r3, #0
    ldr   r7, =INVOCAR
    mov   ip, r7
    bl    .Lllamar_ip
    movs  r0, #0x0a               @ como Monster Reborn tras registrar la invocacion
    b     .Lfin
.Lmonstruo_fuera:
    adds  r1, r6, #0
    bl    .Lcementerio
    b     .Lnada

.Lllamar:
    bx    r3
.Lllamar_ip:
    bx    ip

@ r1 = id de ranura -> FUN_08018518(mi lado, id, esta carta)
.Lcementerio:
    push  {lr}
    mov   r0, r8
    ldrh  r2, [r4]
    lsls  r2, r2, #23
    lsrs  r2, r2, #24
    ldr   r3, =A_CEMENTERIO
    bl    .Lllamar
    pop   {r3}
    bx    r3

@ r0 = id de ranura (bit 7 = lado) -> r0 = indice de la carta. Usa r1, r2.
.Lindice:
    lsrs  r2, r0, #7
    movs  r1, #0x7f
    ands  r0, r1
    movs  r1, #0x50
    muls  r0, r1, r0
    ldr   r1, =0x00002B08
    muls  r1, r2, r1
    adds  r0, r0, r1
    ldr   r1, =0x02022250
    adds  r0, r0, r1
    ldrh  r0, [r0, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #17
    bx    lr

    .align 2
    .pool
.Ltextos:
    .word .Lt2, .Lt3, .Lt4
.Lniveles:
    .byte 4, 4, 4, 4, 4, 3, 3, 2
.Lt2:
    .asciz "Your opponent declares Level 2."
.Lt3:
    .asciz "Your opponent declares Level 3."
.Lt4:
    .asciz "Your opponent declares Level 4."
    .align 2
