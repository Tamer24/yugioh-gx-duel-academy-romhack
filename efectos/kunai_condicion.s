@ Kunai with Chain (ID 4657), fn_10: se puede activar cuando el rival declara un ataque con
@ un monstruo cara arriba en posicion de ataque (primer efecto), o cuando controlo un monstruo
@ boca arriba al que equiparla (segundo efecto). Lee el atacante como id de ranura en p[4]
@ (igual que Sakuretsu Armor); ver kunai_cadena.s. La segunda rama es la del fn_10 original
@ (0x08031DD0): FUN_08010C10(lado, 1, 0) cuenta mis monstruos boca arriba.
@ Devuelve 1 si se puede, 0 si no.
@ Simbolos: CONTAR_MONSTRUOS.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, lr}
    adds  r4, r0, #0
    ldr   r0, [r4]
    ldr   r1, =0x0007E000
    ands  r0, r1
    ldr   r1, =0x00020000         @ tipo 0x10: ataque declarado
    cmp   r0, r1
    bne   .Lno
    ldrb  r3, [r4, #4]            @ id de ranura del atacante
    lsrs  r0, r3, #7              @ su lado
    ldrb  r1, [r4]
    movs  r2, #1
    ands  r1, r2                  @ mi lado
    cmp   r0, r1
    beq   .Lno
    movs  r0, #0x7f
    ands  r0, r3
    movs  r1, #0x50
    muls  r0, r1, r0
    lsrs  r2, r3, #7
    ldr   r1, =0x00002B08
    muls  r1, r2, r1
    adds  r0, r0, r1
    ldr   r1, =0x02022250
    adds  r0, r0, r1
    adds  r0, #0x33
    ldrb  r0, [r0]
    movs  r1, #0x30
    ands  r0, r1
    cmp   r0, #0x10               @ cara arriba en posicion de ataque
    bne   .Lno
    movs  r0, #1
    b     .Lfin
.Lno:
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    movs  r2, #0
    ldr   r3, =CONTAR_MONSTRUOS
    bl    .Lllamar
    lsls  r0, r0, #16             @ el resultado es s16
    asrs  r0, r0, #16
    cmp   r0, #1
    bge   .Lsi
    movs  r0, #0
    b     .Lfin
.Lsi:
    movs  r0, #1
.Lfin:
    pop   {r4}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    r3
    .align 2
    .pool
