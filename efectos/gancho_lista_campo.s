@ Gancho en FUN_08015C78 (0x08015C78): "este monstruo tiene un efecto que se activa en el campo
@ una vez por turno". El original es una lista de IDs escrita a mano en el codigo; las cartas
@ restauradas no estan, asi que al ponerse en el campo nunca se les marca el bit 14 de
@ +0x60 y fn_10 devuelve 0 (el menu solo ofrece Detail Screen).
@
@ Este codigo reemplaza los primeros 8 bytes del original, repite las 4 instrucciones que
@ pisa (push, ldr r4, ldr r3, movs r1) y sigue en 0x08015C80. Antes revisa una lista propia
@ de IDs. Entrada: r0 = id de ranura. Salida: r0 = 1 si el ID esta en la lista.
@
@ La lista (LISTA_IDS) termina en 0. Para agregar una carta se agrega su ID de Konami.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, lr}
    movs  r1, #0x7f
    ands  r1, r0                  @ ranura
    movs  r2, #0x50
    muls  r1, r2, r1
    movs  r2, #0x80
    ands  r2, r0
    lsrs  r2, r2, #7              @ lado
    ldr   r3, =0x00002B08
    muls  r2, r3, r2
    adds  r1, r1, r2
    ldr   r3, =0x02022250
    adds  r1, r1, r3
    ldrh  r1, [r1, #0x24]
    lsls  r1, r1, #17
    lsrs  r1, r1, #16             @ indice * 2
    ldr   r2, =0x087A8624         @ indice -> ID de Konami
    ldrh  r1, [r1, r2]
    ldr   r2, =.Llista
.Lbuscar:
    ldrh  r3, [r2]
    cmp   r3, #0
    beq   .Lorig
    cmp   r3, r1
    beq   .Lsi
    adds  r2, #2
    b     .Lbuscar
.Lsi:
    movs  r0, #1
    pop   {r4}
    pop   {r1}
    bx    r1
.Lorig:                           @ lo que pisa el gancho, y a seguir en el original
    ldr   r4, =0x087A8624
    ldr   r3, =0x02022250
    movs  r1, #0x7f
    ldr   r2, =0x08015C81         @ 0x08015C80 | 1 (ands r1, r0)
    bx    r2
    .align 2
    .pool
.Llista:
    .hword 4435                   @ Goddess of Whim
    .hword 5193                   @ Lady Panther
    .hword 5202                   @ Fairy Guardian
    .hword 0
