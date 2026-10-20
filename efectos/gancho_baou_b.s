@ Wicked-Breaking Flamberge - Baou (ID 5727): "If the equipped monster destroys an opponent's monster
@ as a result of battle, negate the effect(s) of the destroyed monster." El +500 de ATK (con
@ descarte) lo da el motor; la anulacion no estaba en el ROM.
@
@ Los efectos encadenados se resuelven en FUN_08023xxx (0x080245xx): para el eslabon de turno
@ llama a la fn_04 con call_function_bx_r2 (0x080F23D8) y una entrada del arreglo de eslabones
@ (r8 + 24 x indice; medido: 0x02020004 para el disparo de Mystic Tomato al ir al cementerio). Toda
@ fn_04 mira la bandera "anulada" (bit 3 de p[2]) y no hace nada si esta; la de Mystic Tomato
@ tambien (0x0803FD40). El gancho marca anulada esa entrada antes de la llamada cuando su carta
@ (id de ranura en los bits 1-8 de u16(p)):
@   - fue destruida en batalla este turno (bandera 5 de ranura+0x60, la pone el motor y la borra el
@     fin de turno),
@   - es uno de los dos monstruos de la ultima batalla (registro 0x02020C20: atacante en los bits
@     13-20 de u32(+0), defensor en los bits 5-12 de u16(+2)), y
@   - el otro monstruo de esa batalla tiene equipada una Baou boca arriba (ID 5727 en la zona de
@     Magicas y Trampas con objetivo, ranura+0x3C, en ese monstruo).
@ Hay dos llamadas, segun el eslabon: 0x080245D6 (efectos/gancho_baou_a.s) y 0x080245B6
@ (efectos/gancho_baou_b.s). Las dos piezas tienen el mismo chequeo.
@
@ Esta pieza: gancho en 0x08024598 (eslabones 2 en adelante). Pisa
@     adds r3, r6, r5 ; adds r1, r0, #0 ; lsls r0, r1, #1 ; adds r0, r0, r1
@ y sigue en 0x080245A0, que termina de calcular la entrada (r0 * 8 + r8) antes de la llamada en
@ 0x080245B6. El chequeo se hace con esa entrada calculada aca aparte. r2 se pisa en 0x080245A4,
@ asi que sirve para volver.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    adds  r1, r0, #0              @ r1 = indice del eslabon
    lsls  r0, r1, #1
    adds  r0, r0, r1
    push  {r0}
    lsls  r0, r0, #3
    add   r0, r8                  @ la entrada que se va a pasar
    bl    .Lbaou
    pop   {r0}                    @ como lo deja la instruccion pisada
    adds  r3, r6, r5
    ldr   r2, =0x080245A1
    bx    r2

@ ---- el chequeo: r0 = entrada. Conserva r0-r3; usa la pila.
.Lbaou:
    push  {r0, r1, r2, r3, r4, r5, r6, r7, lr}
    ldrh  r4, [r0]
    lsls  r4, r4, #23
    lsrs  r4, r4, #24             @ r4 = id de ranura de la carta de la entrada
    adds  r0, r4, #0
    bl    .Lranura
    ldr   r0, [r0, #0x60]
    lsls  r0, r0, #26             @ bandera 5: destruida en batalla este turno
    bpl   .Lb_fin
    ldr   r2, =0x02020C20
    ldr   r5, [r2]
    lsls  r5, r5, #11
    lsrs  r5, r5, #24             @ atacante
    ldrh  r6, [r2, #2]
    lsls  r6, r6, #19
    lsrs  r6, r6, #24             @ defensor
    cmp   r4, r6
    beq   .Lb_def
    cmp   r4, r5
    bne   .Lb_fin
    adds  r5, r6, #0              @ r5 = el otro monstruo
.Lb_def:
    cmp   r5, r4
    beq   .Lb_fin
    movs  r6, #0                  @ r6 = lado
.Lb_lado:
    movs  r7, #0                  @ r7 = numero de ranura
.Lb_carta:
    lsls  r0, r6, #7
    orrs  r0, r7
    bl    .Lranura
    adds  r3, r0, #0
    ldrh  r0, [r3, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16             @ indice * 2
    beq   .Lb_sig
    ldr   r1, =0x087A8624
    ldrh  r0, [r0, r1]
    ldr   r1, =5727               @ Wicked-Breaking Flamberge - Baou
    cmp   r0, r1
    bne   .Lb_sig
    adds  r1, r3, #0
    adds  r1, #0x30
    ldrb  r0, [r1, #1]
    lsrs  r0, r0, #4
    cmp   r0, #5
    bne   .Lb_sig                 @ no esta en la zona de Magicas y Trampas
    ldrb  r0, [r1, #3]
    cmp   r0, #0x20
    beq   .Lb_sig                 @ boca abajo
    ldrb  r0, [r1, #0xc]          @ objetivo del equipo (+0x3C)
    cmp   r0, r5
    bne   .Lb_sig
    ldr   r0, [sp]                @ la entrada
    ldrb  r1, [r0, #2]
    movs  r2, #8
    orrs  r1, r2
    strb  r1, [r0, #2]            @ anulada
    b     .Lb_fin
.Lb_sig:
    adds  r7, #1
    cmp   r7, #100
    blt   .Lb_carta
    adds  r6, #1
    cmp   r6, #2
    blt   .Lb_lado
.Lb_fin:
    pop   {r0, r1, r2, r3, r4, r5, r6, r7, pc}

@ r0 = id de ranura (bit 7 = lado) -> r0 = direccion de la ranura. Usa r1 y r2.
.Lranura:
    lsrs  r2, r0, #7
    lsls  r0, r0, #25
    lsrs  r0, r0, #25
    movs  r1, #0x50
    muls  r0, r1, r0
    ldr   r1, =0x00002B08
    muls  r2, r1, r2
    adds  r0, r0, r2
    ldr   r1, =0x02022250
    adds  r0, r0, r1
    bx    lr
    .align 2
    .pool
