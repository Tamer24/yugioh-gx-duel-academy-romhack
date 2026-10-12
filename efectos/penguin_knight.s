@ Penguin Knight (ID 4205): "When this card is sent directly from your Deck to the Graveyard by
@ your opponent's card effect, combine your Graveyard with your Deck and shuffle them to form a
@ new Deck."
@
@ El fn_04 original (0x08039300) solo encola el evento 0x24 (barajar el mazo): la parte de
@ pasar el cementerio al mazo no esta en este ROM. Esta version toma el molde de Fiber Jar
@ (original, 0x0804587C), que hace lo mismo con campo, mano y cementerio:
@   estado 0x80: cada carta de mi cementerio va al mazo de su dueno,
@                FUN_080188AC(ranura, lado << 15 | 0x3008); devuelve 0x7F
@   estado 0x7F: la original (barajar); devuelve 0
@ La lista del cementerio se copia antes de mover nada, por si el motor la compacta al sacar.
@ El disparador lo pone efectos/gancho_enviada_por_rival.s.
@ Simbolos: ORIGINAL, MOVER_CARTA.

    .syntax unified
    .thumb
    .text
    .global _start
    .set MAXIMO, 64
_start:
    push  {r4, r5, r6, r7, lr}
    sub   sp, #MAXIMO
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lnada                  @ anulada
    ldr   r0, =0x020204C6
    ldrb  r0, [r0]
    cmp   r0, #0x80
    beq   .Lal_mazo
    cmp   r0, #0x7f
    bne   .Lnada
    adds  r0, r4, #0
    ldr   r3, =ORIGINAL           @ barajar
    bl    .Lllamar
    b     .Lnada
.Lal_mazo:
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    ldr   r5, =0x00002B08
    muls  r5, r0, r5
    ldr   r0, =0x02022250
    adds  r5, r5, r0              @ r5 = base de mi lado
    ldr   r6, [r5, #0x1c]
    lsls  r6, r6, #12
    lsrs  r6, r6, #25             @ r6 = cartas en mi cementerio (bits 13-19)
    cmp   r6, #MAXIMO
    ble   .Lcopiar
    movs  r6, #MAXIMO
.Lcopiar:
    ldr   r0, =0x00002924         @ lista del cementerio
    adds  r5, r5, r0
    movs  r7, #0
.Lcopia:
    cmp   r7, r6
    bge   .Lmover
    ldrb  r0, [r5, r7]
    mov   r1, sp
    strb  r0, [r1, r7]
    adds  r7, #1
    b     .Lcopia
.Lmover:
    movs  r7, #0
.Lbucle:
    cmp   r7, r6
    bge   .Lhecho
    mov   r1, sp
    ldrb  r0, [r1, r7]
    adds  r7, #1
    cmp   r0, #0xff
    beq   .Lbucle
    lsrs  r1, r0, #7
    lsls  r1, r1, #15
    ldr   r2, =0x00003008         @ destino: mazo
    orrs  r1, r2
    ldr   r3, =MOVER_CARTA
    bl    .Lllamar
    b     .Lbucle
.Lhecho:
    movs  r0, #0x7f
    b     .Lfin
.Lnada:
    movs  r0, #0
.Lfin:
    add   sp, #MAXIMO
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    r3
    .align 2
    .pool
