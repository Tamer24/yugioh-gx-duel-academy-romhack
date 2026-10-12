@ Fairy Guardian (ID 5202): "Offer this face-up card as a Tribute to return 1 Spell Card sent to
@ your Graveyard during this turn by your opponent's card effect to the bottom of your Deck."
@
@ El fn_04 original (0x08043904) es el de Lady Panther (0x080430AC) sin el final: 0x80 registra
@ las candidatas y avisa, 0x7F abre la lista "Your Graveyard", y 0x7E devuelve 0x78 sin mover
@ nada. Lady Panther en 0x7E hace: cleanup_card_actions(); send_card_to_graveyard(elegida,
@ banderas, ranura propia); process_card_actions(); con banderas 0x10 (tope del mazo). La misma
@ funcion usa 0x20 para Crimson Sentry, que es "al fondo del mazo": es lo que pide esta carta.
@ Esta version agrega ese paso y delega el resto en la original.
@ La condicion (fn_10 original) pide una Magica con la bandera 6, que pone
@ efectos/gancho_enviada_por_rival.s; el menu del campo la ofrece por las listas de
@ gancho_lista_campo.s y gancho_menu_campo.s.
@ Simbolos: ORIGINAL, LIMPIAR_ACCIONES, ENVIAR, PROCESAR_ACCIONES.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, lr}
    adds  r4, r0, #0
    ldr   r0, =0x020204C6
    ldrb  r0, [r0]
    cmp   r0, #0x7e
    beq   .Lresolver
    adds  r0, r4, #0
    ldr   r3, =ORIGINAL
    bl    .Lllamar
    b     .Lfin
.Lresolver:
    ldr   r3, =LIMPIAR_ACCIONES
    bl    .Lllamar
    ldr   r0, =0x02019F24         @ carta elegida en la lista
    ldr   r0, [r0]
    lsls  r0, r0, #13
    lsrs  r0, r0, #24
    cmp   r0, #0xff
    beq   .Lcerrar                @ sin eleccion
    movs  r1, #0x20               @ al fondo del mazo
    ldrh  r2, [r4]
    lsls  r2, r2, #23
    lsrs  r2, r2, #24             @ ranura propia
    ldr   r3, =ENVIAR
    bl    .Lllamar
    ldr   r3, =PROCESAR_ACCIONES
    bl    .Lllamar
.Lcerrar:
    movs  r0, #0x78
.Lfin:
    pop   {r4}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    r3
    .align 2
    .pool
