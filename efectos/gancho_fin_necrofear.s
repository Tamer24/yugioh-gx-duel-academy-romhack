@ Gancho en la End Phase (FUN_08064388, 0x08064920): dispara la posesion de Dark Necrofear.
@
@ FUN_08064388 es la parte de la End Phase que atiende los efectos "en la End Phase": en su paso 1
@ recorre las zonas del campo de los dos lados con un arbol de IDs (Goblin Attack Force, Swords of
@ Revealing Light, los Spirit que vuelven a la mano, Garuda the Wind Spirit...) y despues ejecuta
@ las acciones encoladas. Necrofear no esta en ese arbol y, ademas, a esa altura esta en el
@ cementerio, que el arbol no recorre.
@
@ El gancho pisa lo que sigue al recorrido,
@     bl process_card_actions ; ldr r0, =0x0201FD00 ; movs r1, #0xC0
@ lo repite al final y sigue en 0x08064928. Antes busca, en las cartas de cada lado, un Dark
@ Necrofear (ID 5222) que este en el cementerio (zona 0xD) y que este turno haya sido
@   - destruido en batalla (bandera 5 de ranura+0x60, la pone el motor), o
@   - destruido por un efecto del rival (bandera 6, que efectos/gancho_enviada_por_rival.s le pone
@     a Necrofear solo si la accion fue una destruccion).
@ La bandera 4 del motor ("destruida por un efecto") no sirve: Raigeki y Dark Hole no la ponen
@ [PROBADO]. Las banderas 5 y 6 se limpian al terminar el turno (FUN_0801D7DC), asi que valen
@ solo "este turno"; aca se apagan para que el efecto no se encole dos veces.
@ Si el rival controla algun monstruo boca arriba (FUN_08010C10(rival, 1, 0)) y el dueno tiene una
@ casilla libre de Magicas y Trampas (FUN_08011120, donde Necrofear va a quedar equipada), encola el efecto de
@ la carta con FUN_080314B4, como los disparadores "fue al cementerio" del motor pero con otro
@ momento: 0x54 << 21 = tipo de efecto 4 y momento 5 (el de los efectos de End Phase; el motor usa
@ 0xE4 << 21, momento 0xE, para los disparadores). Asi la fn_18 y la fn_04 de Necrofear distinguen
@ este pedido del que el motor hace por su cuenta apenas la carta es destruida.
@
@ Puede usar r0-r3, ip y lr; r4-r7 se guardan.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7}
    movs  r5, #0                  @ r5 = lado
.Llado:
    ldr   r6, =0x02022250
    ldr   r0, =0x00002B08
    muls  r0, r5, r0
    adds  r6, r6, r0              @ r6 = cartas de ese lado
    movs  r4, #0                  @ r4 = numero de ranura (100 en adelante son fichas)
.Lcarta:
    movs  r0, #0x50
    muls  r0, r4, r0
    adds  r7, r6, r0              @ r7 = ranura
    ldrh  r0, [r7, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16             @ indice * 2
    ldr   r1, =0x087A8624         @ indice -> ID de Konami
    ldrh  r0, [r0, r1]
    ldr   r1, =5222               @ Dark Necrofear
    cmp   r0, r1
    bne   .Lsiguiente
    ldr   r0, [r7, #0x30]
    lsls  r0, r0, #13
    lsrs  r0, r0, #25             @ zona
    cmp   r0, #0xd
    bne   .Lsiguiente             @ no esta en el cementerio
    ldr   r0, [r7, #0x60]
    movs  r1, #0x60
    tst   r0, r1
    beq   .Lsiguiente             @ ni en batalla ni por un efecto del rival
    bics  r0, r1
    str   r0, [r7, #0x60]
    movs  r0, #1
    subs  r0, r0, r5              @ el rival
    movs  r1, #1
    movs  r2, #0
    ldr   r3, =0x08010C11         @ FUN_08010C10(lado, 1, 0): monstruos boca arriba que controla
    bl    .Lllamar
    cmp   r0, #0
    ble   .Lsiguiente
    adds  r0, r5, #0
    ldr   r3, =0x08011121         @ FUN_08011120(lado): casilla libre de Magicas y Trampas, o -1
    bl    .Lllamar
    adds  r0, #1
    beq   .Lsiguiente             @ sin lugar para equiparse: no hay efecto
    lsls  r3, r5, #7
    orrs  r3, r4                  @ id de ranura
    ldr   r2, [r7, #0x30]
    lsls  r2, r2, #12
    lsrs  r2, r2, #24             @ zona actual y controlador
    lsls  r2, r2, #8
    orrs  r2, r3
    lsls  r1, r2, #16
    orrs  r1, r2
    lsls  r0, r5, #31
    orrs  r0, r3
    movs  r2, #0x54               @ tipo de efecto 4, momento 5
    lsls  r2, r2, #21
    orrs  r0, r2
    ldr   r3, =0x080314B5         @ FUN_080314B4: encola el efecto disparado
    bl    .Lllamar
.Lsiguiente:
    adds  r4, #1
    cmp   r4, #100
    blt   .Lcarta
    adds  r5, #1
    cmp   r5, #2
    blt   .Llado
    pop   {r4, r5, r6, r7}
    ldr   r3, =0x08016AED         @ process_card_actions
    bl    .Lllamar
    ldr   r0, =0x0201FD00
    movs  r1, #0xc0
    ldr   r3, =0x08064929
    bx    r3
.Lllamar:
    bx    r3
    .align 2
    .pool
