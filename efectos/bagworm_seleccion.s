@ Electromagnetic Bagworm (ID 5040), fn_18: elige la Maquina rival cuyo control tomar.
@ La original (0x0805436C) mostraba el aviso en el paso 0, pero en los pasos siguientes solo
@ detectaba A/B y devolvia 0 sin grabar la eleccion (le falta la llamada a FUN_08051680 que si
@ tiene la fn_18 vecina 0x0805446C). Aca: paso 0 = la original (busca una Maquina, avisa y
@ avanza el paso); pasos siguientes = B cancela, A graba el objetivo bajo el cursor
@ (byte 0x02022250 + 0x5668) con FUN_08051680(p, id) y devuelve 1.
@ La rama de la IA (bit 0 de p[0] = 1) devuelve 1 sin elegir: la IA todavia no usa esta carta.
@ Cuando el efecto es el de "destruida en batalla" (tipo 4 en (p[1] >> 1) & 0xF) no hay nada
@ que elegir: devuelve 1 sin avisar, igual que la original cuando no encuentra una Maquina.
@ ORIGINAL = fn_18 original (con bit Thumb).

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldrb  r1, [r0, #1]
    lsls  r1, r1, #27
    lsrs  r1, r1, #28             @ tipo de efecto
    cmp   r1, #4
    bne   .Lvolteo
    movs  r0, #1                  @ destruida en batalla: sin seleccion
    bx    lr
.Lvolteo:
    ldr   r1, =0x020204C0         @ palabra con el contador de pasos (bits 10-17)
    ldr   r2, [r1]
    lsls  r3, r2, #14
    lsrs  r3, r3, #24
    bne   .Lsel
    ldr   r1, =ORIGINAL
    bx    r1
.Lsel:
    push  {r4, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4]
    movs  r3, #1
    tst   r0, r3
    bne   .Lia
    ldr   r0, =0x03000188         @ teclas nuevas: bit 1 = B
    ldrh  r0, [r0]
    movs  r3, #2
    tst   r0, r3
    beq   .Lnob
    ldr   r0, =0xFFFC03FF         @ B: vuelve el contador a 0
    ands  r2, r0
    str   r2, [r1]
    movs  r0, #0
    b     .Lfin
.Lnob:
    movs  r0, #0xE0
    lsls  r0, r0, #16
    ldr   r3, =0x08009095         @ FUN_08009094: A sobre un objetivo valido
    bl    .Lllamar
    cmp   r0, #0
    beq   .Lfin
    ldr   r0, =0x02022250 + 0x5668
    ldrb  r1, [r0]                @ id de ranura bajo el cursor
    adds  r0, r4, #0
    ldr   r3, =0x08051681         @ FUN_08051680(p, id): graba la eleccion
    bl    .Lllamar
    movs  r0, #1
    b     .Lfin
.Lia:
    movs  r0, #1
.Lfin:
    pop   {r4}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    r3
    .align 2
    .pool
