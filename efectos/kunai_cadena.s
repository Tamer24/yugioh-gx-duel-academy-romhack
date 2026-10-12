@ Kunai with Chain (ID 4657): "Select 1 or both of these effects: Change 1 attacking monster of
@ your opponent to Defense Position. Equip this card to 1 face-up monster on your side of the
@ field to increase its ATK by 500 points."
@
@ Primer efecto. El fn_04 original lee el atacante como (lado en p[4], posicion de campo en
@ p[5]), pero el motor deja en p[4] el id de ranura del atacante (u16, bit 7 = lado), igual que
@ Sakuretsu Armor (original): con ese formato el atacante nunca se encontraba y no pasaba nada.
@ Esta version usa el id de ranura y llama como Block Attack: FUN_0801A36C(lado, id, 0, 0).
@
@ Segundo efecto. El original no lo tenia. Si la seleccion (fn_18 original, 0x08052E7C) dejo un
@ monstruo elegido (p[8] & 0xF != 0, id de ranura en p[9]), se equipa igual que Metalmorph
@ (original, 0x0803991C): con la carta boca arriba en la zona de Magicas/Trampas y el objetivo
@ boca arriba en una zona de monstruo, FUN_0801A600(lado, ranura propia, ranura objetivo).
@ El +500 ya esta en el calculador del motor (caso 0x1231 de 0x08012C94) y que la carta quede
@ en el campo lo resuelve efectos/gancho_queda_campo.s.
@ Simbolos: CAMBIAR_POSICION, EQUIPAR.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldr   r0, [r4]
    ldr   r1, =0x0007E000
    ands  r0, r1
    ldr   r1, =0x00020000         @ tipo 0x10: ataque declarado
    cmp   r0, r1
    bne   .Lequipo
    ldrb  r5, [r4, #4]            @ id de ranura del atacante
    lsrs  r0, r5, #7              @ su lado
    ldrb  r1, [r4]
    movs  r2, #1
    ands  r1, r2                  @ mi lado
    cmp   r0, r1
    beq   .Lequipo                @ es mio: no
    adds  r0, r5, #0
    bl    .Lranura
    adds  r0, #0x33
    ldrb  r0, [r0]
    movs  r1, #0x30
    ands  r0, r1
    cmp   r0, #0x10               @ cara arriba en posicion de ataque
    bne   .Lequipo
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    adds  r1, r5, #0
    movs  r2, #0
    movs  r3, #0
    ldr   r6, =CAMBIAR_POSICION
    mov   ip, r6
    bl    .Lllamar
.Lequipo:
    ldrb  r0, [r4, #8]
    movs  r1, #0x0f
    tst   r0, r1
    beq   .Lfin                   @ no se eligio monstruo
    ldrh  r5, [r4]
    lsls  r5, r5, #0x17
    lsrs  r5, r5, #0x18           @ ranura propia
    adds  r0, r5, #0
    bl    .Lranura
    bl    .Lzona_y_cara
    cmp   r0, #5                  @ zona de Magicas/Trampas, boca arriba
    bne   .Lfin
    ldrb  r6, [r4, #9]            @ monstruo elegido
    adds  r0, r6, #0
    bl    .Lranura
    bl    .Lzona_y_cara
    cmp   r0, #0                  @ zona de monstruo, boca arriba
    bne   .Lfin
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    adds  r1, r5, #0
    adds  r2, r6, #0
    ldr   r3, =EQUIPAR
    mov   ip, r3
    bl    .Lllamar
.Lfin:
    movs  r0, #0
    pop   {r4, r5, r6}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    ip

@ r0 = id de ranura (bit 7 = lado) -> r0 = direccion de la ranura. Usa r1, r2.
.Lranura:
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
    bx    lr

@ r0 = direccion de la ranura -> r0 = zona (bits 12-18 de +0x30), o 0xFF si no esta boca arriba.
.Lzona_y_cara:
    adds  r1, r0, #0
    adds  r1, #0x33
    ldrb  r1, [r1]
    movs  r2, #0x10
    tst   r1, r2
    beq   .Lno_cara
    ldr   r0, [r0, #0x30]
    lsls  r0, r0, #13
    lsrs  r0, r0, #25
    bx    lr
.Lno_cara:
    movs  r0, #0xff
    bx    lr
    .align 2
    .pool
