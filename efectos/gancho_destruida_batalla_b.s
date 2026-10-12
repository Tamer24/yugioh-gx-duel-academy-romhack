@ Gancho en la rutina de destruccion en batalla (FUN_08068C8C, 0x08068FD0), segundo arbol de IDs:
@ el de la carta B del combate ([0x02020C22] bits 5-12). Es el par de
@ efectos/gancho_destruida_batalla_a.s: agrega a Electromagnetic Bagworm (5040) a la rama que ya
@ tienen Slate Warrior (5037) y Rigorous Reaver (5044), aca 0x08069138.
@
@ A 0x08068FD0 llegan los IDs entre 0x1310 y 0x13B4 (sin incluirlos). El gancho pisa
@     ldr r0, =0x13A7 ; cmp r1, r0 ; beq 0x08069034 ; adds r0, #6
@ y resuelve tambien lo que seguia (cmp r1, r0 ; bne ... ; b 0x08069138 ; b 0x0806931A).
@ Rigorous Reaver se compara antes de llegar aca.
@ Entrada: r1 = ID de Konami. Ninguna de las tres salidas usa r0 ni r3 sin cargarlos.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r0, =0x13A7             @ el caso que ya estaba en esta rama
    cmp   r1, r0
    beq   .Lotro
    adds  r0, #6                  @ Slate Warrior (5037)
    cmp   r1, r0
    beq   .Lpierde
    adds  r0, #3                  @ Electromagnetic Bagworm (5040)
    cmp   r1, r0
    beq   .Lpierde
    ldr   r0, =0x0806931B
    bx    r0
.Lotro:
    ldr   r0, =0x08069035
    bx    r0
.Lpierde:
    ldr   r0, =0x08069139
    bx    r0
    .align 2
    .pool
