@ Gancho en FUN_08012460 (0x0801273C), el calculador de ATK/DEF: casos de ATK que dependen de una
@ cuenta y que el motor resuelve por el ID de la propia carta (como Chaos Necromancer, 5827).
@
@ Hoy atiende dos cartas:
@  - Neo-Spacian Dark Panther (6772) mientras copia a otro monstruo (bandera 25 de +0x60, la pone
@    efectos/dark_panther.s): el motor le calcularia el ATK y la DEF del copiado porque su indice
@    cambio; el texto solo copia el nombre y el efecto, asi que se le dejan 1000 y 500.
@  - Neo-Spacian Flare Scarab (6773): +400 ATK por cada Magica o Trampa que controla el rival
@    (zonas 5 a 10 del campo del rival, boca arriba o boca abajo; 0xFF = vacia).
@
@ Reemplaza 8 bytes (ldr r1 / ldrh r2,[r7] / lsls r0,r2,#1 / adds r0,r0,r1) que arman la
@ direccion del ID de la carta; los repite y sigue en 0x08012744. En ese punto r7 apunta a la
@ salida ([r7] = indice de la carta, [r7+4] = ATK ya con su base), [sp+0x2c] es la ranura que se
@ calcula y [sp+0x30] la mascara pedida (bit 0 = ATK). El salto del gancho pisa r3: se guarda.
@
@ Molde: el caso de Chaos Necromancer en 0x08012934. Agregar otra carta = otro caso aca.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r3, r4, r5, r6}        @ el salto del gancho pisa r3; el resto es de trabajo
    ldr   r0, [sp, #0x2c + 16]    @ ranura de la carta
    movs  r1, #0x7f
    ands  r1, r0
    movs  r2, #0x50
    muls  r1, r2, r1
    lsrs  r0, r0, #7
    ldr   r2, =0x00002B08
    muls  r0, r2, r0
    adds  r0, r0, r1
    ldr   r2, =0x02022250
    adds  r0, r0, r2              @ direccion de la ranura
    movs  r1, #0x60
    ldr   r1, [r0, r1]            @ banderas
    lsls  r1, r1, #6              @ bit 25 al bit 31
    bpl   .Lsin_copia
    movs  r1, #0xfa
    lsls  r1, r1, #2              @ 1000
    str   r1, [r7, #4]
    movs  r1, #0xfa
    lsls  r1, r1, #1              @ 500
    str   r1, [r7, #8]
.Lsin_copia:
    ldr   r1, =0x087A8624         @ indice -> ID de Konami
    ldrh  r2, [r7]
    lsls  r0, r2, #1
    ldrh  r2, [r0, r1]            @ ID de la carta
    ldr   r0, =6773               @ Neo-Spacian Flare Scarab
    cmp   r2, r0
    bne   .Lorig
    ldr   r0, [sp, #0x30 + 16]    @ mascara pedida
    movs  r1, #1
    tst   r0, r1
    beq   .Lorig                  @ no se pidio el ATK
    ldr   r0, [sp, #0x2c + 16]    @ ranura de la carta (bit 7 = lado)
    lsrs  r0, r0, #7
    movs  r1, #1
    ands  r0, r1
    eors  r0, r1                  @ lado del rival
    movs  r1, #11
    muls  r0, r1, r0
    ldr   r1, =0x02022250 + 0x5610 + 5
    adds  r0, r0, r1              @ primera zona de Magicas y Trampas del rival
    movs  r3, #0                  @ cuenta
    movs  r4, #6                  @ 5 de Magicas y Trampas + la de campo
.Lcuenta:
    ldrb  r1, [r0]
    adds  r0, #1
    cmp   r1, #0xff
    beq   .Lsigue
    adds  r3, #1
.Lsigue:
    subs  r4, #1
    bne   .Lcuenta
    movs  r0, #0xc8
    lsls  r0, r0, #1              @ 400
    muls  r3, r0, r3
    ldr   r0, [r7, #4]
    adds  r0, r0, r3
    str   r0, [r7, #4]
.Lorig:
    pop   {r3, r4, r5, r6}
    ldr   r1, =0x087A8624         @ lo que pisa el gancho
    ldrh  r2, [r7]
    lsls  r0, r2, #1
    adds  r0, r0, r1
    ldr   r3, =0x08012745         @ 0x08012744 | 1
    bx    r3
    .align 2
    .pool
