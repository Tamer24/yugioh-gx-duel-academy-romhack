@ Gancho en FUN_080236C4 (0x080236C4): "al terminar de resolverse, esta carta va al cementerio".
@ Devuelve 1 si va al cementerio. Para las Magicas de Equipo, Continuas y de Campo, y para una
@ lista corta de Trampas escrita en el codigo (Metalmorph 0x1238 entre ellas), devuelve en cambio
@ el bit 4 de p[2]: normalmente 0, o sea que la carta queda en el campo.
@
@ Kunai with Chain (ID 4657) no esta en esa lista, asi que despues de equiparse se iba al
@ cementerio. Este gancho llama a la original y, si la carta es Kunai y se equipo a un monstruo
@ (p[8] & 0xF != 0), devuelve lo mismo que para Metalmorph. Si se activo solo para cambiar la
@ posicion del atacante sigue yendo al cementerio.
@
@ Entrada: r0 = p. Repite las 4 instrucciones que pisa el gancho y sigue en 0x080236CC.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, lr}
    adds  r4, r0, #0
    bl    .Loriginal
    ldrb  r1, [r4, #8]
    movs  r2, #0x0f
    tst   r1, r2
    beq   .Lfin                   @ sin monstruo elegido: lo que diga la original
    ldrh  r1, [r4]
    lsls  r1, r1, #0x17
    lsrs  r1, r1, #0x18           @ id de ranura de la carta
    lsrs  r3, r1, #7
    movs  r2, #0x7f
    ands  r1, r2
    movs  r2, #0x50
    muls  r1, r2, r1
    ldr   r2, =0x00002B08
    muls  r2, r3, r2
    adds  r1, r1, r2
    ldr   r2, =0x02022250
    adds  r1, r1, r2
    ldrh  r1, [r1, #0x24]
    lsls  r1, r1, #17
    lsrs  r1, r1, #16             @ indice * 2
    ldr   r2, =0x087A8624         @ indice -> ID de Konami
    ldrh  r1, [r1, r2]
    ldr   r2, =4657               @ Kunai with Chain
    cmp   r1, r2
    bne   .Lfin
    ldrb  r0, [r4, #2]
    lsls  r0, r0, #27
    lsrs  r0, r0, #31             @ bit 4 de p[2], como las cartas de la lista original
.Lfin:
    pop   {r4}
    pop   {r1}
    bx    r1
.Loriginal:
    push  {r4, r5, r6, r7, lr}
    mov   r7, sl
    mov   r6, sb
    mov   r5, r8
    ldr   r3, =0x080236CD
    bx    r3
    .align 2
    .pool
