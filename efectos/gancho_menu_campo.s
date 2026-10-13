@ Gancho en FUN_08079200 (0x08079200): "este monstruo del campo tiene un efecto que se puede
@ activar desde el menu". El original es un switch enorme por ID de carta; las cartas
@ restauradas no tienen su caso, asi que el menu del campo solo ofrece Detail Screen.
@
@ Entrada: r0 = bandera, r1 = id de ranura. Salida: r0 = 1 si el ID esta en la lista propia;
@ si no, sigue el original (0x08079208). Repite las 4 instrucciones que pisa el gancho
@ (push, mov r7,r8, push {r7}, mov r8,r0).
@ La lista termina en 0.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    mov   r7, r8
    push  {r7}
    mov   r8, r0
    movs  r2, #0x7f
    ands  r2, r1
    movs  r3, #0x50
    muls  r2, r3, r2
    movs  r3, #0x80
    ands  r3, r1
    lsrs  r3, r3, #7
    ldr   r4, =0x00002B08
    muls  r3, r4, r3
    adds  r2, r2, r3
    ldr   r3, =0x02022250
    adds  r2, r2, r3
    ldrh  r2, [r2, #0x24]
    lsls  r2, r2, #17
    lsrs  r2, r2, #16             @ indice * 2
    ldr   r3, =0x087A8624         @ indice -> ID de Konami
    ldrh  r2, [r2, r3]
    ldr   r3, =.Llista
.Lbuscar:
    ldrh  r4, [r3]
    cmp   r4, #0
    beq   .Lorig
    cmp   r4, r2
    beq   .Lsi
    adds  r3, #2
    b     .Lbuscar
.Lsi:
    movs  r0, #1
    pop   {r3}
    mov   r8, r3
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lorig:
    ldr   r3, =0x08079209         @ adds r5, r1, #0
    bx    r3
    .align 2
    .pool
.Llista:
    .hword 4435                   @ Goddess of Whim
    .hword 5193                   @ Lady Panther
    .hword 5202                   @ Fairy Guardian
    .hword 6769                   @ Neo-Spacian Air Hummingbird
    .hword 6768                   @ Neo-Spacian Aqua Dolphin
    .hword 0
