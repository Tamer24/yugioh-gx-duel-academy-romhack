@ Butterfly Dagger - Elma (ID 5724), fn_04: "A monster equipped with this card increases its ATK by
@ 300 points. When this card is destroyed and sent to the Graveyard, you can return this card to
@ your hand."
@
@ El +300 lo da el calculador de ATK (caso del equipo) y la activacion como equipo es la fn_04
@ original: todo pedido que no sea el de abajo va a ORIGINAL sin tocar nada.
@
@ La vuelta a la mano no estaba en el ROM. efectos/gancho_enviada_por_rival.s encola el efecto de
@ Elma con FUN_080314B4 (tipo de efecto 4, momento 0xE, como los disparadores "fue al cementerio"
@ del motor: (cabecera & 0x7FE00) == 0x1C800) cuando Elma va de la zona de Magicas y Trampas al
@ cementerio: destruida, o porque el monstruo equipado dejo el campo. Con ese pedido y el estado
@ 0x80, si Elma sigue en el cementerio la pasa a la mano de su dueno con
@ FUN_080188AC(ranura, lado << 15 | 0x3C08) (zona 0xF, la mano). Devuelve 0.
@ Simbolos: ORIGINAL, MOVER_CARTA.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r1, [r0]
    ldr   r2, =0x0007FE00
    ands  r1, r2
    ldr   r2, =0x0001C800         @ tipo 4, momento 0xE: el pedido del gancho
    cmp   r1, r2
    beq   .Lvolver_a_la_mano
    ldr   r3, =ORIGINAL           @ cualquier otro pedido: el equipo de siempre
    bx    r3
.Lvolver_a_la_mano:
    push  {r4, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lnada                  @ anulada
    ldr   r0, =0x020204C6
    ldrb  r0, [r0]
    cmp   r0, #0x80
    bne   .Lnada
    ldrh  r0, [r4]
    lsls  r0, r0, #23
    lsrs  r0, r0, #24             @ id de ranura de Elma: (u16(p) & 0x1FF) >> 1
    bl    .Lranura
    ldr   r1, [r0, #0x30]
    lsls  r1, r1, #13
    lsrs  r1, r1, #25             @ zona
    cmp   r1, #0xd
    bne   .Lnada                  @ ya no esta en el cementerio
    ldrh  r0, [r4]
    lsls  r0, r0, #23
    lsrs  r0, r0, #24
    lsrs  r1, r0, #7
    lsls  r1, r1, #15
    ldr   r2, =0x00003C08         @ destino: la mano
    orrs  r1, r2
    ldr   r3, =MOVER_CARTA
    bl    .Lllamar
.Lnada:
    movs  r0, #0
    pop   {r4}
    pop   {r1}
    bx    r1
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
    muls  r2, r3, r2
    adds  r0, r0, r2
    ldr   r3, =0x02022250
    adds  r0, r0, r3
    bx    lr
    .align 2
    .pool
