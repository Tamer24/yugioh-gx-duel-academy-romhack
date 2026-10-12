@ Hiro's Shadow Scout (ID 4617): "FLIP: Your opponent draws 3 cards. Both players check the
@ cards and if there are any Spell Cards among them, they are discarded to the Graveyard."
@
@ El fn_04 original (0x0803B6E4) procesa UNA carta por llamada: en el estado 0x80 pone el
@ contador (0x020204C7) en 3 y sigue como 0x7F; mira el tope del mazo del rival y, si es una
@ Magica, la revela y la manda al cementerio; si no, el rival la roba. Pero devuelve siempre 0,
@ asi que el motor no vuelve a llamarla y nunca decrementa el contador: el rival robaba 1 sola.
@ Ademas lee la posicion en el mazo de r7, que nadie inicializa.
@
@ Esta version llama a la original con r7 = 0 (tope del mazo), decrementa el contador y devuelve
@ 0x7F mientras queden cartas por procesar y el mazo del rival no este vacio.
@ Simbolos: ORIGINAL.

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
    bne   .Lnada                  @ anulada
    ldr   r5, =0x020204C6         @ estado; el contador es el byte siguiente
    ldrb  r0, [r5]
    cmp   r0, #0x80
    beq   .Lprocesar
    cmp   r0, #0x7f
    bne   .Lnada
.Lprocesar:
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    eors  r0, r1                  @ lado del rival
    ldr   r6, =0x00002B08
    muls  r6, r0, r6
    ldr   r0, =0x02022250
    adds  r6, r6, r0              @ base del lado rival
    movs  r7, #0                  @ la original indexa el mazo con r7: 0 = tope
    adds  r0, r4, #0
    ldr   r1, =ORIGINAL
    mov   ip, r1
    bl    .Lllamar
    ldrb  r0, [r5, #1]
    cmp   r0, #0
    beq   .Lnada
    subs  r0, #1
    strb  r0, [r5, #1]
    beq   .Lnada                  @ ya fueron las 3
    ldrh  r0, [r6, #0x1c]         @ cartas en el mazo del rival: bits 6-12
    lsls  r0, r0, #0x13
    lsrs  r0, r0, #0x19
    beq   .Lnada
    movs  r0, #0x7f
    b     .Lsalir
.Lnada:
    movs  r0, #0
.Lsalir:
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    ip
    .align 2
    .pool
