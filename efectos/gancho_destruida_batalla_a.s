@ Gancho en la rutina de destruccion en batalla (FUN_08068C8C, 0x08068D00), primer arbol de IDs:
@ el de la carta A del combate ([0x02020C20] bits 13-20).
@ "The ATK and DEF of a monster that destroys this monster as a result of battle is decreased by
@ 500 points": el motor lo dispara por ID para Slate Warrior (5037) y Rigorous Reaver (5044),
@ saltando a 0x08068DB4, que encola el efecto de la carta destruida con el otro monstruo en p[4]
@ (tipo de efecto 4; lo resuelve la fn_04 de Slate Warrior, 0x08042078). Electromagnetic Bagworm
@ (5040) tiene el mismo texto y no estaba en el arbol.
@
@ El gancho pisa
@     ldr r0, =0x13AD ; cmp r1, r0 ; beq 0x08068DB4 ; adds r0, #7
@ y resuelve tambien lo que seguia (cmp r1, r0 ; beq 0x08068DB4 ; b 0x08068F3E): a esta rama solo
@ llegan los IDs entre 0x13A7 y 0x147A, y ninguno mas tiene caso.
@ Entrada: r1 = ID de Konami. Las dos salidas vuelven a cargar r0 y r3.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r0, =5037               @ Slate Warrior
    cmp   r1, r0
    beq   .Lpierde
    adds  r0, #3                  @ Electromagnetic Bagworm (5040)
    cmp   r1, r0
    beq   .Lpierde
    adds  r0, #4                  @ Rigorous Reaver (5044)
    cmp   r1, r0
    beq   .Lpierde
    ldr   r0, =0x08068F3F
    bx    r0
.Lpierde:
    ldr   r0, =0x08068DB5
    bx    r0
    .align 2
    .pool
