@ Neo-Spacian Dark Panther (ID 6772, carta nueva): una vez por turno, elige 1 monstruo boca arriba
@ del rival; hasta la End Phase su nombre pasa a ser el de ese monstruo y reemplaza su efecto por
@ el del monstruo copiado.
@
@ El motor decide nombre y efectos por el ID de la carta, que sale del indice de la ranura (+0x24).
@ La copia es cambiar ese indice por el del monstruo elegido y poner la bandera 25 de +0x60:
@   - efectos/gancho_atk_cuenta.s le deja a la ranura su ATK y DEF (1000 y 500, no los del copiado),
@   - efectos/gancho_fin_control.s, en la End Phase, le devuelve el indice de Dark Panther y quita
@     la bandera.
@ Un efecto del copiado que se activa desde el menu del campo no queda disponible en el mismo
@ turno (la bandera 14 la pone el motor al entrar al campo).
@
@ Estados: 0x80 registra los monstruos boca arriba del rival + pregunta -> 0x7F ; 0x7F lista
@ (elegir 1) -> 0x7E ; 0x7E copia -> 0x64. La IA (lado 1) no lo usa.
@ Moldes: aqua_dolphin.s (lista y registro), gancho_fin_control.s (End Phase).
@ Simbolos del motor: ASK_QUESTION, DIALOGO, CLEAR_ZONE, REGISTRAR, EVENTO.

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
    bne   .Lfin0                  @ anulada
    ldrb  r0, [r4]
    movs  r1, #1
    tst   r0, r1
    bne   .Lfin0                  @ la IA no lo usa
    ldr   r0, =0x020204C6
    ldrb  r5, [r0]
    cmp   r5, #0x80
    beq   .Lentrada
    cmp   r5, #0x7f
    beq   .Llista
    cmp   r5, #0x7e
    beq   .Lcopiar
    b     .Lfin0

.Lentrada:
    bl    .Lregistrar
    cmp   r0, #0
    beq   .Lfin0                  @ ningun monstruo boca arriba del rival
    ldr   r0, =.Lm1
    ldr   r3, =ASK_QUESTION
    mov   ip, r3
    bl    .Lllamar
    movs  r0, #0x7f
    b     .Lfin

.Llista:
    bl    .Lregistrar
    ldr   r3, =DIALOGO            @ init_effect_dialogue(0, 1, 0x02019F24, 1)
    mov   ip, r3
    movs  r0, #0
    movs  r1, #1
    ldr   r2, =0x02019F24
    movs  r3, #1
    bl    .Lllamar
    ldr   r2, =0x02019F00         @ ajustes de exchange.s
    ldrb  r0, [r2, #0x1f]
    movs  r1, #0x3f
    ands  r0, r1
    strb  r0, [r2, #0x1f]
    ldr   r3, =0x02019F20
    ldrb  r0, [r3]
    movs  r1, #3
    bics  r0, r1
    strb  r0, [r3]
    ldrb  r0, [r2]
    movs  r1, #0xf0
    ands  r0, r1
    movs  r1, #2
    orrs  r0, r1
    strb  r0, [r2]
    movs  r0, #0x7e
    b     .Lfin

.Lcopiar:
    ldr   r0, =0x02019F24
    ldr   r0, [r0]
    ldr   r1, =0x0007FFFF
    ands  r0, r1
    lsrs  r6, r0, #11             @ r6 = ranura elegida
    cmp   r6, #0xff
    beq   .Lhecho
    adds  r0, r6, #0
    bl    .Lranura
    adds  r7, r0, #0              @ r7 = el monstruo elegido
    movs  r1, #0x33
    ldrb  r0, [r7, r1]
    movs  r1, #0x10
    tst   r0, r1
    beq   .Lhecho                 @ ya no esta boca arriba
    ldrh  r6, [r7, #0x24]
    lsls  r6, r6, #17
    lsrs  r6, r6, #17             @ r6 = indice del copiado (15 bits)
    ldrh  r0, [r4]
    lsls  r0, r0, #23
    lsrs  r5, r0, #24             @ r5 = ranura de esta carta
    adds  r0, r5, #0
    bl    .Lranura
    adds  r7, r0, #0              @ r7 = direccion de esta carta
    ldrh  r0, [r7, #0x24]
    lsrs  r0, r0, #15
    lsls  r0, r0, #15
    orrs  r0, r6
    strh  r0, [r7, #0x24]        @ ahora es el copiado
    movs  r0, #0x3b               @ bandera 25: copiando
    adds  r1, r5, #0
    movs  r2, #25
    ldr   r3, =EVENTO
    mov   ip, r3
    bl    .Lllamar
    movs  r0, #0x3c               @ una vez por turno: quita la bandera 14
    adds  r1, r5, #0
    movs  r2, #14
    ldr   r3, =EVENTO
    mov   ip, r3
    bl    .Lllamar
.Lhecho:
    movs  r0, #0x64
    b     .Lfin
.Lfin0:
    movs  r0, #0
.Lfin:
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

.Lllamar:
    bx    ip

.Lranura:                         @ r0 = id de ranura -> r0 = direccion; usa r1, r2
    movs  r1, #0x7f
    ands  r1, r0
    movs  r2, #0x50
    muls  r1, r2, r1
    lsrs  r0, r0, #7
    ldr   r2, =0x00002B08
    muls  r0, r2, r0
    adds  r0, r0, r1
    ldr   r2, =0x02022250
    adds  r0, r0, r2
    bx    lr

.Lregistrar:                      @ registra los monstruos boca arriba del rival -> r0 = cuantos
    push  {r4, r5, r6, r7, lr}
    movs  r0, #6
    movs  r1, #0
    ldr   r3, =CLEAR_ZONE
    mov   ip, r3
    bl    .Lllamar
    movs  r6, #0                  @ cuenta
    movs  r7, #0                  @ zona
.Lzb:
    ldr   r0, =0x02022250 + 0x5610 + 11
    ldrb  r0, [r0, r7]            @ zonas de monstruos del rival
    cmp   r0, #0xff
    beq   .Lzn
    adds  r4, r0, #0
    bl    .Lranura
    movs  r1, #0x33
    ldrb  r1, [r0, r1]
    movs  r2, #0x10
    tst   r1, r2
    beq   .Lzn                    @ boca abajo
    adds  r0, r4, #0
    ldr   r3, =REGISTRAR
    mov   ip, r3
    bl    .Lllamar
    adds  r6, #1
.Lzn:
    adds  r7, #1
    cmp   r7, #5
    blt   .Lzb
    adds  r0, r6, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

    .align 2
.Lm1:
    .asciz "Select 1 face-up monster your opponent controls."
    .align 2
    .pool
